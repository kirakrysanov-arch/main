"""
main.py

Usage:
    python main.py "https://www.tori.fi/recommerce/forsale/search?...&trade_type=2" --pages 2

Scrapes the given Tori.fi search URL, runs each listing's photos through
Claude for a "hidden gem" evaluation, and writes a ranked CSV of results
(hidden_gem first, then decent_flip, then skip).
"""

import argparse
import csv
import sys

from tori_scraper import scrape_multiple_pages
from analyzer import analyze_all

VERDICT_ORDER = {"hidden_gem": 0, "decent_flip": 1, "skip": 2, "error": 3}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("search_url", help="A Tori.fi search results URL")
    parser.add_argument("--pages", type=int, default=1,
                         help="How many result pages to scrape (default 1)")
    parser.add_argument("--out", default="results.csv",
                         help="Output CSV filename (default results.csv)")
    args = parser.parse_args()

    print(f"Scraping {args.search_url} ({args.pages} page(s))...")
    listings = scrape_multiple_pages(args.search_url, max_pages=args.pages)
    print(f"Found {len(listings)} listings.")

    if not listings:
        print(
            "No listings found. Tori's page structure may not match what "
            "this scraper expects — see the SELECTORS dict in "
            "tori_scraper.py and adjust based on what you see in your "
            "browser's Inspect Element view on an actual search page."
        )
        sys.exit(1)

    print("Analyzing listings with Claude (this calls the API per listing)...")
    results = analyze_all(listings)

    results.sort(key=lambda r: VERDICT_ORDER.get(r.get("verdict"), 9))

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "verdict", "confidence", "title", "price", "location",
            "estimated_resale_eur", "reasoning", "repair_notes", "url",
        ])
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, "") for k in writer.fieldnames})

    gems = [r for r in results if r.get("verdict") == "hidden_gem"]
    print(f"\nDone. {len(gems)} potential hidden gem(s) found out of {len(results)}.")
    print(f"Full ranked results written to {args.out}")
    for r in gems:
        print(f"  ⭐ {r['title'][:60]} — {r['price']} — {r['url']}")


if __name__ == "__main__":
    main()
