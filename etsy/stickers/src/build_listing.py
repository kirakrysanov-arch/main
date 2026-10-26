"""Builds the Etsy listing-image slides for the sticker pack (listing.html). Run: python3 build_listing.py"""
import json
from pathlib import Path

from PIL import Image

here = Path(__file__).parent
stickers = json.loads((here / "stickers.json").read_text())
CAT = {s["id"]: s["cat"] for s in stickers}
JOURNAL = (here / ".." / ".." / "match-book" / "src" / "previews" / "retro" / "m01-pre.png").resolve()
FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,800;1,9..144,400"
         "&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap")


def img(sid, h, style=""):
    return f'<img src="{(here / "png" / CAT[sid] / f"{sid}.png").as_uri()}" style="height:{h}px;{style}">'


def placed(sid, h, x, y, rot=0):
    return img(sid, h, f"position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg)")


def grid(ids, k):
    """Stickers at k times their natural size, so wide labels and round badges keep their proportions."""
    out = ""
    for sid in ids:
        w, h = Image.open(here / "png" / CAT[sid] / f"{sid}.png").size
        out += img(sid, round(h / 4 * k))
    return out


ids = [s["id"] for s in stickers]
icons = [s for s in ids if CAT[s] == "icons"]
words = [s for s in ids if CAT[s] == "words"]
helpers = [s for s in ids if CAT[s] in ("planner", "quotes")]

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
.slide { width: 1600px; height: 1200px; position: relative; overflow: hidden; font-family: 'Barlow Semi Condensed', sans-serif; }
.light { background: #F6EDD9; color: #1B2B4B; }
.navy { background: #1B2B4B; color: #F6EDD9; }
.green { background: #1F6B3B; color: #F6EDD9; }
.awning::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 110px;
  background: repeating-linear-gradient(90deg, #1F6B3B 0 60px, #F6EDD9 60px 120px); }
.awning::after { content: ""; position: absolute; top: 110px; left: 0; right: 0; height: 30px;
  background: radial-gradient(circle at 30px 0, #1F6B3B 29px, transparent 30px) 0 0 / 120px 30px repeat-x; }
.k { font-size: 17px; letter-spacing: 7px; text-transform: uppercase; font-weight: 700; color: #C2412D; }
.navy .k, .green .k { color: #D7F04A; }
h1, h2 { font-family: 'Fraunces', serif; font-weight: 800; letter-spacing: -2px; line-height: 1.02; }
h1 { font-size: 110px; } h2 { font-size: 72px; }
h1 em, h2 em { font-weight: 400; font-style: italic; color: #C2412D; letter-spacing: -1px; }
.navy h2 em, .green h2 em { color: #D7F04A; }
.rule { height: 9px; width: 140px; margin: 30px 0; background: linear-gradient(to bottom, #1F6B3B 0 3px, transparent 3px 6px, #C2412D 6px 9px); }
.badges { display: flex; gap: 14px; flex-wrap: wrap; }
.badges span { border: 2px solid #1B2B4B; padding: 14px 22px; font-size: 17px; letter-spacing: 3px; text-transform: uppercase; font-weight: 700; }
.wall { position: absolute; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; align-content: center; gap: 10px 16px; }
.head { position: absolute; top: 80px; left: 0; right: 0; text-align: center; }
.dev { position: absolute; border-radius: 28px; background: #14213A; padding: 22px; box-shadow: 0 40px 80px rgba(0,0,0,.35); }
.dev img { display: block; width: 100%; border-radius: 6px; }
.files { display: grid; grid-template-columns: repeat(3, 1fr); gap: 34px; position: absolute; left: 110px; right: 110px; top: 380px; }
.files div { border: 2px solid #1B2B4B; padding: 56px 34px; text-align: center; background: #FBF6EA; }
.files .ic { width: 96px; height: 96px; margin: 0 auto 24px; border: 3px solid #C2412D; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-weight: 700; font-size: 21px; letter-spacing: 2px; color: #C2412D; }
.files b { display: block; font-family: 'Fraunces', serif; font-size: 34px; margin-bottom: 10px; }
.files span { font-size: 20px; line-height: 1.5; }
.strip { position: absolute; left: 0; right: 0; bottom: 110px; text-align: center; font-size: 20px; letter-spacing: 3px; text-transform: uppercase; font-weight: 700; color: #1F6B3B; }
"""

SLIDES = f"""
<section class="slide light awning" id="s1">
  <div style="position:absolute;left:100px;top:250px;width:640px">
    <div class="k">Digital stickers · GoodNotes &amp; print</div>
    <h1 style="margin-top:24px">Tennis <em>Planner</em> Stickers</h1>
    <div class="rule"></div>
    <div class="badges"><span>69 stickers</span><span>Transparent PNG</span><span>Printable</span></div>
  </div>
  {placed("icon-ball", 190, 830, 200, -8)}{placed("word-match-day", 92, 1090, 230, 4)}{placed("icon-racquet", 230, 1350, 190, 14)}
  {placed("word-ace", 175, 820, 430, -6)}{placed("icon-trophy", 190, 1030, 380, 0)}{placed("word-win", 150, 1250, 450, 8)}
  {placed("planner-scorecard", 150, 900, 640, -3)}{placed("word-game-face", 95, 1250, 660, -5)}
  {placed("quote-one-point-at-a-time", 140, 820, 860, 4)}{placed("icon-crossed-racquets", 200, 1120, 820, -6)}{placed("word-love-all", 85, 1330, 900, 6)}
</section>

<section class="slide light" id="s2">
  <div class="head"><div class="k">Everything in the pack</div><h2 style="margin-top:14px">All <em>69</em> stickers</h2></div>
  <div class="wall" style="left:60px;right:60px;top:250px;bottom:50px">{grid(icons, .62)}{grid(words, .62)}{grid(helpers, .55)}</div>
</section>

<section class="slide navy" id="s3">
  <div class="head"><div class="k">21 illustrations</div><h2 style="margin-top:14px">Tennis <em>icons</em></h2></div>
  <div class="wall" style="left:120px;right:120px;top:260px;bottom:80px;gap:16px 34px">{grid(icons, 1.0)}</div>
</section>

<section class="slide light" id="s4">
  <div class="head"><div class="k">31 word stickers</div><h2 style="margin-top:14px">Words &amp; <em>match moments</em></h2></div>
  <div class="wall" style="left:80px;right:80px;top:250px;bottom:60px;gap:14px 20px">{grid(words, 1.05)}</div>
</section>

<section class="slide green" id="s5">
  <div class="head"><div class="k">16 planner stickers</div><h2 style="margin-top:14px">Helpers &amp; <em>pep talks</em></h2></div>
  <div class="wall" style="left:90px;right:90px;top:260px;bottom:70px;gap:20px 26px">{grid(helpers, .95)}</div>
</section>

<section class="slide light awning" id="s6">
  <div style="position:absolute;left:100px;top:260px;width:560px">
    <div class="k">See them in use</div>
    <h2 style="margin-top:20px">Make every page <em>match day</em></h2>
    <div class="rule"></div>
    <p style="font-family:'Fraunces',serif;font-size:30px;line-height:1.45">Drop them into any digital planner or journal. They pair perfectly with The Match Book tennis journal.</p>
  </div>
  <div class="dev" style="width:660px;left:820px;top:150px;transform:rotate(2deg)"><img src="{JOURNAL.as_uri()}"></div>
  {placed("word-match-day", 82, 1120, 250, -4)}{placed("icon-ball", 130, 1360, 330, 10)}{placed("word-ace", 130, 1230, 700, 8)}
  {placed("planner-court-time", 70, 960, 560, -2)}{placed("quote-one-point-at-a-time", 110, 920, 860, -4)}{placed("word-lets-go", 80, 1220, 940, 3)}
</section>

<section class="slide light" id="s7">
  <div class="head" style="top:120px"><div class="k">Instant download</div><h2 style="margin-top:16px">What you <em>receive</em></h2></div>
  <div class="files">
    <div><div class="ic">PNG</div><b>69 Stickers</b><span>Transparent PNG files<br>in four folders</span></div>
    <div><div class="ic">PDF</div><b>Printable Sheets</b><span>Six pages to print<br>on sticker paper</span></div>
    <div><div class="ic">PDF</div><b>Read Me First</b><span>How to use them in<br>every app</span></div>
  </div>
  <div class="strip">GoodNotes · Notability · Noteshelf · Samsung Notes · Canva · Print</div>
</section>
"""

(here / "listing.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
                                   f'<style>{CSS}</style></head><body>{SLIDES}</body></html>')
print("listing.html")
