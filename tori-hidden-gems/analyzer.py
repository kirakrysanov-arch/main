"""
analyzer.py

Downloads a listing's image(s) and asks the Claude API to evaluate it as
a furniture-flipping opportunity: is this a "hidden gem" (undervalued,
good design/wood/craftsmanship, worth the repair effort) or an ordinary
flip at best?

Requires an ANTHROPIC_API_KEY environment variable (get one at
https://console.anthropic.com).
"""

import base64
import json
import os
import time

import requests
from anthropic import Anthropic

MODEL = "claude-sonnet-5"  # swap for a different model if you prefer

SYSTEM_PROMPT = """You are helping a furniture flipper in Finland evaluate \
free/cheap secondhand furniture listings scraped from Tori.fi. For each \
listing (title + price + one or more photos), assess:

1. Likely material/construction (solid wood vs veneer vs laminate/flatpack)
2. Any recognizable design style, era, or maker (Scandinavian mid-century, \
   Asko, Artek, English brown furniture, IKEA, etc.)
3. Visible condition/damage from the photo
4. Whether this looks like a genuine "hidden gem" (real design/material \
   value relative to asking price) vs an ordinary flip vs not worth it

Respond ONLY with a JSON object, no other text, in this exact shape:
{
  "verdict": "hidden_gem" | "decent_flip" | "skip",
  "confidence": "low" | "medium" | "high",
  "reasoning": "2-3 sentences explaining the call",
  "estimated_resale_eur": "e.g. 50-150",
  "repair_notes": "1 sentence on what it would need"
}
"""


def _image_to_base64(url: str) -> tuple:
    """Download an image and return (base64_data, media_type)."""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type", "image/jpeg")
    if "image" not in content_type:
        content_type = "image/jpeg"
    return base64.b64encode(resp.content).decode("utf-8"), content_type


def analyze_listing(client: Anthropic, listing) -> dict:
    """
    listing: a tori_scraper.Listing object.
    Returns a dict with the parsed verdict, or an error dict if something
    went wrong (missing images, API error, bad JSON back, etc.).
    """
    if not listing.image_urls:
        return {"verdict": "skip", "confidence": "low",
                "reasoning": "No image available to analyze.",
                "estimated_resale_eur": "", "repair_notes": ""}

    content = [
        {
            "type": "text",
            "text": f"Title: {listing.title}\nPrice: {listing.price}\n"
                    f"Location: {listing.location}",
        }
    ]

    # Use up to the first 2 images to keep API cost/latency reasonable.
    for img_url in listing.image_urls[:2]:
        try:
            b64, media_type = _image_to_base64(img_url)
        except requests.RequestException:
            continue
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": b64,
            },
        })

    if len(content) == 1:
        return {"verdict": "skip", "confidence": "low",
                "reasoning": "Could not download any images.",
                "estimated_resale_eur": "", "repair_notes": ""}

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": content}],
        )
        text = "".join(
            block.text for block in response.content if block.type == "text"
        )
        # Strip markdown code fences if the model added them anyway.
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(text)
    except (json.JSONDecodeError, Exception) as e:
        return {"verdict": "error", "confidence": "low",
                "reasoning": f"Analysis failed: {e}",
                "estimated_resale_eur": "", "repair_notes": ""}


def analyze_all(listings: list, delay_seconds: float = 1.0) -> list:
    """Run analyze_listing over every listing, returning enriched dicts."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set the ANTHROPIC_API_KEY environment variable before running "
            "(get one at https://console.anthropic.com)."
        )
    client = Anthropic(api_key=api_key)

    results = []
    for i, listing in enumerate(listings, 1):
        print(f"  Analyzing {i}/{len(listings)}: {listing.title[:60]}")
        verdict = analyze_listing(client, listing)
        results.append({
            "title": listing.title,
            "price": listing.price,
            "location": listing.location,
            "url": listing.url,
            **verdict,
        })
        time.sleep(delay_seconds)
    return results
