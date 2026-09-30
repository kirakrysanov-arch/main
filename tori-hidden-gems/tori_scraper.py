"""
tori_scraper.py

Scrapes Tori.fi search result pages for listings (title, price, location,
url, image urls). Built defensively since Tori's exact HTML/JSON structure
can change and wasn't verifiable from a live test environment.

Strategy, in order of preference:
1. Look for an embedded JSON state blob (many modern sites, including
   Schibsted-family marketplaces like Tori, ship listing data as JSON
   inside a <script> tag rather than pure HTML). We try a few common
   patterns (__NEXT_DATA__, application/ld+json, window.__INITIAL_STATE__).
2. Fall back to CSS-selector scraping of listing cards. Selectors are
   isolated in SELECTORS below so you can fix them in one place if Tori's
   markup doesn't match (open a listing page, right-click > Inspect, and
   compare against these selectors).

Usage:
    from tori_scraper import scrape_search_page
    listings = scrape_search_page("https://www.tori.fi/recommerce/forsale/search?...")
"""

import json
import re
import time
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup

HEADERS = {
    # A normal browser user-agent. Being a well-behaved scraper: identify
    # as a real browser but don't spoof anything deceptive beyond that.
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "fi-FI,fi;q=0.9,en;q=0.8",
}

# Be polite: minimum seconds between requests to Tori's servers.
MIN_DELAY_SECONDS = 2.0

# --- CSS fallback selectors -------------------------------------------------
# Adjust these if the JSON-extraction strategy fails and fallback parsing
# returns nothing useful. Use your browser's "Inspect Element" on a real
# Tori search results page to find the right selectors.
SELECTORS = {
    "card": "div[data-testid='ads__list-item']",
    "title": "h2, h3, [data-testid='ads__list-item__title']",
    "price": "[data-testid='ads__list-item__price']",
    "location": "[data-testid='ads__list-item__subtitle']",
    "link": "a",
    "image": "img",
}


@dataclass
class Listing:
    title: str
    price: str
    location: str
    url: str
    image_urls: list = field(default_factory=list)
    listing_id: str = ""


def _extract_json_blobs(html: str):
    """Try to find embedded JSON state in the page. Returns list of dicts."""
    blobs = []

    # Pattern 1: Next.js-style __NEXT_DATA__
    m = re.search(
        r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL
    )
    if m:
        try:
            blobs.append(json.loads(m.group(1)))
        except json.JSONDecodeError:
            pass

    # Pattern 2: window.__INITIAL_STATE__ = {...};
    m = re.search(
        r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\});", html, re.DOTALL
    )
    if m:
        try:
            blobs.append(json.loads(m.group(1)))
        except json.JSONDecodeError:
            pass

    # Pattern 3: application/ld+json (structured data, often per-item, less
    # useful for search result pages but worth trying).
    for m in re.finditer(
        r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
        html,
        re.DOTALL,
    ):
        try:
            blobs.append(json.loads(m.group(1)))
        except json.JSONDecodeError:
            pass

    return blobs


def _walk_json_for_listings(obj, found):
    """
    Recursively walk a JSON blob looking for dict entries that look like
    listing records (have something like a title/subject + price + image).
    This is deliberately loose since we don't know Tori's exact schema.
    """
    if isinstance(obj, dict):
        keys = {k.lower() for k in obj.keys()}
        looks_like_listing = (
            any(k in keys for k in ("heading", "title", "subject"))
            and any(k in keys for k in ("price", "priceinfo"))
        )
        if looks_like_listing:
            found.append(obj)
        for v in obj.values():
            _walk_json_for_listings(v, found)
    elif isinstance(obj, list):
        for item in obj:
            _walk_json_for_listings(item, found)


def _listing_from_json_record(record: dict) -> Listing:
    def first_present(*keys):
        for k in keys:
            if k in record and record[k]:
                return record[k]
        return ""

    title = first_present("heading", "title", "subject")
    price = first_present("price", "priceInfo")
    if isinstance(price, dict):
        price = price.get("amount") or price.get("formatted") or ""
    location = first_present("location", "region", "municipality")
    if isinstance(location, dict):
        location = location.get("name", "")
    url = first_present("canonicalUrl", "url", "link")
    listing_id = str(first_present("id", "adId", "listingId"))

    images = []
    img_field = first_present("images", "image", "thumbnail")
    if isinstance(img_field, list):
        for im in img_field:
            if isinstance(im, dict):
                images.append(im.get("url") or im.get("src", ""))
            elif isinstance(im, str):
                images.append(im)
    elif isinstance(img_field, str):
        images.append(img_field)

    return Listing(
        title=str(title),
        price=str(price),
        location=str(location),
        url=str(url),
        image_urls=[i for i in images if i],
        listing_id=listing_id,
    )


def _fallback_css_scrape(html: str, base_url: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(SELECTORS["card"])
    listings = []
    for card in cards:
        title_el = card.select_one(SELECTORS["title"])
        price_el = card.select_one(SELECTORS["price"])
        loc_el = card.select_one(SELECTORS["location"])
        link_el = card.select_one(SELECTORS["link"])
        img_el = card.select_one(SELECTORS["image"])

        url = link_el["href"] if link_el and link_el.has_attr("href") else ""
        if url and url.startswith("/"):
            url = "https://www.tori.fi" + url

        img_url = ""
        if img_el:
            img_url = img_el.get("src") or img_el.get("data-src", "")

        listings.append(
            Listing(
                title=title_el.get_text(strip=True) if title_el else "",
                price=price_el.get_text(strip=True) if price_el else "",
                location=loc_el.get_text(strip=True) if loc_el else "",
                url=url,
                image_urls=[img_url] if img_url else [],
            )
        )
    return listings


def scrape_search_page(url: str) -> list:
    """
    Fetch one Tori.fi search results page and return a list of Listing
    objects. Tries JSON-blob extraction first, falls back to CSS scraping.
    """
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    html = resp.text

    listings = []

    blobs = _extract_json_blobs(html)
    records = []
    for blob in blobs:
        _walk_json_for_listings(blob, records)

    if records:
        listings = [_listing_from_json_record(r) for r in records]
        listings = [l for l in listings if l.title and l.url]

    if not listings:
        listings = _fallback_css_scrape(html, url)

    return listings


def scrape_multiple_pages(base_url: str, max_pages: int = 3) -> list:
    """
    Scrape several pages of a search query. Assumes pagination via a
    `?page=N` query param — adjust if Tori uses a different scheme
    (check the URL bar when you click "next page" on a real search).
    """
    all_listings = []
    for page in range(1, max_pages + 1):
        sep = "&" if "?" in base_url else "?"
        page_url = f"{base_url}{sep}page={page}" if page > 1 else base_url
        try:
            listings = scrape_search_page(page_url)
        except requests.RequestException as e:
            print(f"  [warn] failed to fetch page {page}: {e}")
            break
        if not listings:
            break
        all_listings.extend(listings)
        time.sleep(MIN_DELAY_SECONDS)
    return all_listings
