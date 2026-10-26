# The Match Book: Etsy listing kit

## What to upload

| File | Where it goes on Etsy |
|---|---|
| `The-Match-Book-Tennis-Journal.pdf` | **Digital file 1**: the hyperlinked journal (131 pages, 7.5×10 in) |
| `The-Match-Book-Stats-Tracker.xlsx` | **Digital file 2**: the stats spreadsheet (works in Google Sheets, Excel and Numbers) |
| `listing-images/01-hero.jpg` | Photo 1 (thumbnail) |
| `listing-images/02-whats-inside.jpg` | Photo 2 |
| `listing-images/03-before-after.jpg` | Photo 3 |
| `listing-images/04-stats-tracker.jpg` | Photo 4 |
| `listing-images/05-who-its-for.jpg` | Photo 5 |

The spreadsheet ships with 16 sample matches so the dashboard looks alive. Its "Start Here" tab tells buyers how to clear them.

## Title (≤ 140 characters)

```
Tennis Journal Digital Planner, Tennis Stats Tracker Spreadsheet, Match Log & Opponent Scouting, GoodNotes Tennis Gift for Player Coach
```

## 13 tags (each ≤ 20 characters)

```
tennis journal
tennis planner
tennis gift
tennis stats
tennis tracker
tennis player gift
tennis coach gift
match journal
tennis log
goodnotes planner
sports journal
athlete planner
tennis mom gift
```

## Category and attributes

- **Category:** Paper & Party Supplies › Paper › Calendars & Planners
- **Type:** Digital download
- **Occasion:** Birthday · Christmas (switch to "Back to school" in August for junior players)
- **Colours:** Green · Beige

## Price

- **List price:** $34 for the journal and spreadsheet bundle
- **Launch sale:** 30% off for 2–3 weeks
- Later, sell the journal alone ($22) and the spreadsheet alone ($19) as separate listings. That gives three listings that each appear in search, and makes the bundle look like good value.

## Description

```
🎾 THE MATCH BOOK
Tennis Performance Journal + Stats Tracker

The best players don't just play more. They pay closer attention.
The Match Book is a beautiful hyperlinked tennis journal with a bonus stats spreadsheet. Use it to plan every match, review every result, scout every rival and track your game over a whole season.

━━━━━━━━━━━━━━━━━━
WHAT YOU GET
━━━━━━━━━━━━━━━━━━
1. Hyperlinked tennis journal (PDF, 131 pages)
2. Stats tracker spreadsheet (Google Sheets / Excel / Numbers)

━━━━━━━━━━━━━━━━━━
INSIDE THE JOURNAL
━━━━━━━━━━━━━━━━━━
• Player profile: plays, backhand, game style, weapons
• Season goals: outcome, performance and process goals
• Season calendar and a results log
• 30 match plans: three keys, serve and return plan, warm-up ritual, mindset word
• 30 match reviews: set scores, key stats, ratings for each part of your game, what worked and what to change
• 20 opponent scouting reports with a court diagram and head-to-head record
• 12 weekly training logs
• 20 drill cards with court diagrams
• 6 weeks of body and recovery tracking
• String and racquet log, plus a match-day kit checklist
• 6 coach-notes pages
• Lined, dotted and blank court-diagram pages

Every page is hyperlinked: tabs on the side, Before/After buttons on each match, and a home button on every page.

━━━━━━━━━━━━━━━━━━
INSIDE THE STATS TRACKER
━━━━━━━━━━━━━━━━━━
• Match log with space for 150 matches
• Automatic dashboard: win rate, 1st serve %, serve points won, break point conversion, net points won, winners vs unforced errors
• Results broken down by surface (hard, clay, grass, indoor)
• Monthly charts
• Head-to-head record against every opponent
• Season plan with countdowns to entry deadlines

━━━━━━━━━━━━━━━━━━
PERFECT FOR
━━━━━━━━━━━━━━━━━━
Junior players and tennis parents · league and club players · college hopefuls · coaches · a thoughtful gift for any tennis lover

━━━━━━━━━━━━━━━━━━
COMPATIBLE WITH
━━━━━━━━━━━━━━━━━━
Journal: GoodNotes, Notability, Noteshelf, Xodo or any PDF app on iPad, Android tablets or computers. You can also print it on US Letter or A4.
Stats tracker: Google Sheets (upload to Drive, then choose File › Save as Google Sheets), Microsoft Excel or Apple Numbers.

━━━━━━━━━━━━━━━━━━
PLEASE NOTE
━━━━━━━━━━━━━━━━━━
• This is a DIGITAL product. Nothing will be shipped.
• A tablet, stylus and apps are not included.
• For personal use only.
• Because this is a digital download, returns aren't possible. If anything isn't right, message me and I'll help.

Not affiliated with any tennis tournament, tour or governing body.
```

## Notes

- **Don't use trademarks.** Never use "Wimbledon", "US Open", "Roland-Garros", "Australian Open", "ATP", "WTA" or "USTA" in the title, tags or images.
- **Coach edition.** A $59+ edition for coaches is a good follow-up: a player roster, lesson planner and a progress page for each player.
- **Padel and pickleball.** Change the court diagram in `src/build.py` (`court()`) and some of the wording, and you have a version for padel or pickleball. Each can be its own listing.
- **When to advertise.** Tennis gift searches rise in November–December and again in spring, when the outdoor season starts.

## Rebuilding

```
cd src
python3 build.py          # journal.html
node render.js <ids...>   # PDF and page previews
python3 build_tracker.py  # spreadsheet (then recalculate it, e.g. by opening it in LibreOffice or Excel)
node render-listing.js    # listing images (needs the previews used in listing.html, plus previews/dashboard.png)
```
