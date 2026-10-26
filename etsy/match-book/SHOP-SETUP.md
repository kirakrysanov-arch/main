# The Match Book: shop setup and launch

## What's in this folder

| Folder | Contents |
|---|---|
| `listings/club/` | Club Edition: green, cream and gold |
| `listings/retro/` | Retro Club Edition: 1970s racquet-club style |
| `listings/rally/` | Rally Edition: black, white and ball yellow |
| `extra-styles/` | Clay Court journal, kept for a later listing (it has no listing images yet) |
| `style-options.jpg` | All four styles side by side |
| `src/` | The generators that build every file (see "Rebuilding" below) |

Each listing folder contains:

- `upload/`: the three files buyers download
- `images/`: seven listing images and a 12-second video
- `LISTING.md`: title, tags, description, alt text and settings, ready to paste into Etsy

## Launch checklist

1. **Create a shop section** called **Tennis Journals** (Shop Manager › Listings › Sections).
2. **Create the three listings** with the copy and files in each `LISTING.md`. Publish all three on the same day so they support each other in search.
3. **Set the message to buyers for digital orders** (below). Etsy shows it with every download.
4. **Add the shop FAQs** (below).
5. **Run a launch sale** of 30% off all three for 2–3 weeks (Marketing › Sales and discounts).
6. **Turn on Etsy Ads** at $1–3 a day for the three listings.
7. **Test a download yourself.** Open each journal in GoodNotes and tap a few tabs and Before/After buttons. Open each spreadsheet in Google Sheets.
8. **Check your stats after 30 days.** Compare views, favourites and sales. Move ad money to the best performer, and refresh the thumbnail of the weakest.

## Message to buyers (digital orders)

```
Thank you so much for your order! 🎾

Your files are ready to download from Etsy › You › Purchases. Start with READ-ME-FIRST.pdf, which shows how to open the journal in GoodNotes, Notability or other apps, and the stats tracker in Google Sheets or Excel.

If anything doesn't download or open properly, just send me a message and I'll sort it out quickly.

Have a great season, and if you enjoy The Match Book, a review would mean the world to my small shop.
```

## Shop FAQs

**Is this a physical product?**
No. It's an instant digital download. Nothing is shipped.

**Which apps does the journal work with?**
GoodNotes, Notability, Noteshelf, Xodo, Samsung Notes and any app that opens PDFs. It also prints well on US Letter or A4.

**Do I need Excel for the stats tracker?**
No. It also works free in Google Sheets, and in Apple Numbers.

**Can I use it for more than one season?**
Yes. Re-import the original PDF whenever you want a fresh journal, or duplicate pages inside your app.

**Is it dated?**
No. It's fully undated, so you can start at any point in the season.

**Can I share it with my team?**
The files are licensed for one player. Coaches and clubs can message me about a team licence.

**The links aren't working. What should I do?**
Import the PDF as a new document rather than inserting pages into an existing notebook. In GoodNotes, switch to read-only mode (the pen icon) to follow links.

## Pricing plan

| When | What |
|---|---|
| Launch | $34 bundle, 30% off for 2–3 weeks |
| After 10–20 sales | Remove the sale. Add the journal alone ($22) and the stats tracker alone ($19) as separate listings |
| November–December | Run a gift sale. Add "gift for tennis player" wording to the first line of each description |
| Later | A coach edition ($59+), and Clay Court and grass versions as a "choose your surface" set |

## Rules to keep listings safe

- **Trademarks:** never use "Wimbledon", "US Open", "Roland-Garros", "Australian Open", "ATP", "WTA" or "USTA" in titles, tags, images or descriptions.
- **Mockups:** keep the generic tablet and laptop mockups. Don't add brand logos (Apple, GoodNotes) to images.
- **Fonts:** all fonts are from Google Fonts and licensed for commercial use (SIL Open Font License).

## Rebuilding

From `src/`:

```
python3 build.py <club|retro|rally|clay>        # journal HTML
THEME=<style> node render.js <page ids...>       # journal PDF and page previews
                                                  # (for clay, add OUT=extra-styles/The-Match-Book-Tennis-Journal-Clay.pdf)
python3 build.py <style> guide                    # Read Me First HTML
SRC=guide-<style>.html OUT=listings/<style>/upload/READ-ME-FIRST.pdf THEME=<style> node render.js guide-1 guide-2
python3 build_tracker.py <club|retro|rally>       # stats spreadsheet (then recalculate in LibreOffice or Excel)
python3 build_listing.py <style> && node render-listing.js <style>   # listing images
sh make_video.sh <style>                          # listing video
```

The listing images need these previews in `src/previews/<style>/`: cover, profile, season, results, matches, m01-pre, m01-post, scout-01, train-1, drills-1, body-1, gear, coach-1, note-5, and dashboard.png. dashboard.png is a picture of the spreadsheet's Dashboard tab.
