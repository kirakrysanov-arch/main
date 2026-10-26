# The Gilded Year: Etsy listing kit

## What to upload

| File | Where it goes on Etsy |
|---|---|
| `The-Gilded-Year-Planner.pdf` | **Digital files** (the product buyers download) |
| `listing-images/01-hero.jpg` | Photo 1 (thumbnail) |
| `listing-images/02-whats-inside.jpg` | Photo 2 |
| `listing-images/03-hyperlinked.jpg` | Photo 3 |
| `listing-images/04-digital-and-print.jpg` | Photo 4 |
| `listing-images/05-features.jpg` | Photo 5 |

Images are 3200×2400 (4:3), which is Etsy's recommended ratio. The PDF is 7.5×10 in (iPad ratio), 133 pages, with 3,000+ internal hyperlinks.

## Title (135 of 140 characters)

```
Luxury Digital Planner Undated, Black Gold Hyperlinked iPad Planner, GoodNotes Notability Planner, Printable Life Planner, Budget Habit
```

## 13 tags (each ≤ 20 characters)

```
luxury planner
digital planner
goodnotes planner
undated planner
hyperlinked planner
ipad planner
black gold planner
notability planner
printable planner
aesthetic planner
budget planner
life planner
gift for her
```

## Category and attributes

- **Category:** Paper & Party Supplies › Paper › Calendars & Planners
- **Type:** Digital download
- **Occasion:** New Year (also use for "Birthday" or "Christmas" in Q4 promos)
- **Primary colour:** Black · **Secondary colour:** Gold

## Price

- **List price:** $24.00
- **Launch sale:** 40% off for the first 2–3 weeks (shows as $14.40), to build early reviews and sales velocity
- Luxury hyperlinked planners in this style usually sell for $12–$35 on Etsy. $24 with frequent sales is a strong position for a new shop.

## Description

```
✦ THE GILDED YEAR ✦
Undated Luxury Digital Planner, Black & Gold

Your year deserves the same care you give to everything you love. The Gilded Year is a fully hyperlinked, undated planner in noir and champagne gold. It turns every plan into a quiet luxury.

Begin on any day, in any month, of any year.

━━━━━━━━━━━━━━━━━━
✦ WHAT'S INSIDE: 133 PAGES
━━━━━━━━━━━━━━━━━━
• Elegant cover with a "This year belongs to" line
• Welcome and how-to-use guide
• Hyperlinked index
• Year at a Glance (12 undated mini calendars)
• Vision board: wealth, wellness, love, career, home, travel
• Annual goals by quarter, plus habits to build and release
• 12 undated monthly calendars with focus, priorities and important dates
• 60 weekly spreads (5 for every month) with top three, to-do, self-care, gratitude and notes
• 12 monthly review pages
• 14 daily ritual pages with an hourly schedule from 6am to 9pm, water and mood trackers
• 12 habit trackers (16 habits × 31 days)
• Monthly budget, expense log and savings tracker
• Self-care menu
• Weekly meal planner with grocery list
• 10 note pages: lined, dotted and grid

━━━━━━━━━━━━━━━━━━
✦ FULLY HYPERLINKED
━━━━━━━━━━━━━━━━━━
• Side tabs on every page jump to any month or section
• Each month links to its weeks, habit tracker and review
• Arrows move you from week to week
• The gold diamond on every page takes you back to the index

━━━━━━━━━━━━━━━━━━
✦ COMPATIBLE WITH
━━━━━━━━━━━━━━━━━━
GoodNotes · Notability · Noteshelf · Xodo · ZoomNotes · Samsung Notes · any PDF annotation app on iPad, Android tablets or computers.

You can also print at home on US Letter or A4 (choose "fit to page"). Heavy ivory card stock gives the most luxurious finish.

━━━━━━━━━━━━━━━━━━
✦ HOW IT WORKS
━━━━━━━━━━━━━━━━━━
1. Purchase and download the PDF from your Etsy Purchases page
2. Open it in your note-taking app (import it as a new notebook)
3. Start planning. Duplicate any page whenever you need more

━━━━━━━━━━━━━━━━━━
✦ PLEASE NOTE
━━━━━━━━━━━━━━━━━━
• This is a DIGITAL product. No physical item will be shipped.
• A tablet, stylus and annotation app are needed for digital use. They are not included.
• Colours may vary slightly between screens and printers.
• For personal use only. Please don't resell or share the file.
• Because this is a digital download, returns aren't possible. If you have any problem, message me and I'll make it right.

Thank you for supporting a small studio ✦
```

## Shop tips

- **Ship a free bonus.** A second PDF gives buyers more value and earns better reviews. Good options are a GoodNotes sticker sheet or a set of dated 2027 calendar pages.
- **Make variants.** Rebuilding in other colours takes minutes because the palette is set by the variables in `src/planner.css` (`--noir`, `--foil`, `--paper`). Ivory + rose gold, emerald + gold and navy + champagne all work. Each variant can be its own listing, which gives your shop more places to be found in search.
- **Bundle later.** A "Gilded Collection" bundle (planner, budget-only planner and wedding planner) can be priced around $39.
- **Timing.** Planner searches peak from late October to January. List now, and run Etsy Ads at about $1–3 a day through the New Year.

## Rebuilding the files

```
cd src
python3 build.py              # writes planner.html
node render.js <page ids...>  # writes the PDF and PNG previews of those pages
node render-listing.js        # writes listing images (needs previews: cover index year vision goals
                              # jan jan-w1 review-jan daily-1 habits-jan budget savings selfcare meals daily)
```
