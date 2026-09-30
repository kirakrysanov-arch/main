# Tori Hidden Gems Scanner

Scrapes a Tori.fi search results page and uses the Claude API (vision) to
flag listings that look like genuine "hidden gem" furniture finds versus
ordinary flips or skips — the same kind of evaluation Claude's been doing
manually on your screenshots, just automated across many listings at once.

## ⚠️ Before you run this

- **This was built without being able to test live against Tori.fi** (the
  build environment couldn't reach the site directly). It's written
  defensively with two extraction strategies, but if it returns zero
  listings on your first run, see "Troubleshooting" below — you'll likely
  need to adjust the CSS selectors in `tori_scraper.py` to match Tori's
  actual current markup.
- **Respect Tori's terms of service and servers.** This script adds a
  2-second delay between page requests and is meant for light personal
  use (scanning a search you'd browse anyway), not high-frequency
  polling or scraping their whole site. Check Tori's robots.txt and terms
  before relying on this regularly.
- **API costs money.** Each listing analyzed = one Claude API call with
  images attached. Vision calls cost more than text-only. Test on a
  small `--pages 1` run first to see typical cost/listing before
  scaling up.

## Setup

```bash
cd tori-hidden-gems
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"   # get one at console.anthropic.com
```

## Usage

1. Go to Tori.fi in your browser, set up the search you want (e.g.
   "Annetaan" furniture in Uusimaa, or "under €30" tables), and copy the
   URL from your address bar.
2. Run:

```bash
python main.py "https://www.tori.fi/recommerce/forsale/search?...&trade_type=2" --pages 2
```

3. Check `results.csv` — sorted with `hidden_gem` verdicts first, then
   `decent_flip`, then `skip`. Each row includes Claude's reasoning,
   an estimated resale range, and a direct link back to the listing.

## Troubleshooting

**"No listings found"**: Tori's page structure doesn't match what the
scraper expects. Open a real Tori search results page in your browser,
right-click a listing → Inspect Element, and:

- If you see a `<script id="__NEXT_DATA__">` or similar embedded JSON
  blob in the page source (Ctrl+U to view source), the JSON extraction
  path should work automatically — if it's not finding listings, the
  field names inside that JSON may differ from what `_listing_from_json_record()`
  in `tori_scraper.py` expects. Print `blobs` to inspect the actual shape
  and adjust the key names there.
- If there's no such script tag, you're on the CSS fallback path — update
  the `SELECTORS` dict at the top of `tori_scraper.py` to match the
  actual class names / data-testid attributes you see for listing cards,
  titles, prices, and images.

**Images not downloading**: Tori may serve images from a CDN that
requires a Referer header or blocks direct requests. If `analyzer.py`
reports failed image downloads, add a `Referer` header matching the
listing URL to the `requests.get()` call in `_image_to_base64()`.

**Rate limiting / blocked requests**: increase `MIN_DELAY_SECONDS` in
`tori_scraper.py`, and consider adding retry logic with backoff if you
see repeated failures.

## Extending this

- **Scheduling**: wrap `main.py` in a cron job to run daily and email/
  Slack you the new hidden gems.
- **Dedup**: track `listing_id` across runs (e.g. in a small SQLite file)
  so you don't re-analyze (and re-pay for) listings you've already seen.
- **Better prompting**: `SYSTEM_PROMPT` in `analyzer.py` is a starting
  point — feed it a few examples of pieces you've actually flipped
  (like the ones from your chat history) to calibrate its judgment
  closer to your own taste and margin targets.
