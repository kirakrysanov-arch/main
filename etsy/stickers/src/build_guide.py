"""Builds the one-page Read Me First guide for the sticker pack (guide.html). Run: python3 build_guide.py"""
from pathlib import Path

here = Path(__file__).parent
png = here / "png"
FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,800;1,9..144,400"
         "&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap")
deco = "".join(f'<img src="{(png / c / f"{s}.png").as_uri()}" style="height:{h}px">'
               for c, s, h in [("icons", "icon-ball", 74), ("words", "word-match-day", 50), ("icons", "icon-racquet", 78),
                               ("words", "word-ace", 74), ("icons", "icon-trophy", 74)])
steps = [
    ("GoodNotes", "Unzip the PNG pack in the Files app. In GoodNotes, open the Stickers tool and import the PNG files "
                  "to make your own sticker collection, or use the Image tool to add any sticker to a page."),
    ("Notability", "Tap the + button, choose an image from Files or Photos, and pick a sticker. "
                   "Drag the corners to resize it."),
    ("Other apps", "Noteshelf, Samsung Notes, Xodo, Canva and most planner apps let you insert an image. "
                   "The transparent background means each sticker sits neatly on any page."),
    ("Printing", "Print the sheets at 100% (actual size) on full-page sticker paper, then cut around the white edge. "
                 "For print-then-cut machines, upload the individual PNG files."),
]
html = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>
@page {{ size: 8.5in 11in; margin: 0; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Barlow Semi Condensed', sans-serif; color: #1B2B4B; }}
.page {{ width: 816px; height: 1056px; background: #FBF6EA; padding: 0 56px 40px; display: flex; flex-direction: column; overflow: hidden; }}
.awning {{ height: 46px; margin: 0 -56px 30px; background: repeating-linear-gradient(90deg, #1F6B3B 0 34px, #FBF6EA 34px 68px); position: relative; }}
.awning::after {{ content: ""; position: absolute; left: 0; right: 0; top: 46px; height: 17px;
  background: radial-gradient(circle at 17px 0, #1F6B3B 16.5px, transparent 17px) 0 0 / 68px 17px repeat-x; }}
.k {{ font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #C2412D; font-weight: 700; }}
h1 {{ font-family: 'Fraunces', serif; font-weight: 800; font-size: 40px; letter-spacing: -1px; margin: 6px 0 4px; }}
h1 em {{ font-weight: 400; color: #C2412D; }}
.rule {{ height: 6px; margin: 12px 0 16px; background: linear-gradient(to bottom, #1F6B3B 0 2px, transparent 2px 4px, #C2412D 4px 6px); }}
.lead {{ font-family: 'Fraunces', serif; font-style: italic; font-size: 19px; line-height: 1.45; color: #1F6B3B; margin-bottom: 16px; }}
.box {{ border: 1.5px solid #1B2B4B; padding: 14px 16px; margin-bottom: 14px; }}
.lbl {{ font-size: 10px; letter-spacing: 2.5px; text-transform: uppercase; font-weight: 700; color: #C2412D; display: block; margin-bottom: 8px; }}
.box p {{ font-size: 14.5px; line-height: 1.6; }}
.steps {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }}
.steps div {{ border: 1.5px solid #1B2B4B; padding: 14px; }}
.steps h4 {{ font-family: 'Fraunces', serif; font-weight: 800; font-size: 17px; margin-bottom: 6px; }}
.steps h4 em {{ color: #C2412D; font-weight: 400; margin-right: 6px; }}
.steps p {{ font-size: 13.5px; line-height: 1.45; }}
.deco {{ display: flex; justify-content: center; align-items: center; gap: 22px; margin: auto 0 10px; }}
.foot {{ text-align: center; font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #1F6B3B; font-weight: 700; }}
</style></head><body><section class="page"><div class="awning"></div>
<div class="k">Read me first</div><h1>Thank <em>you</em></h1><div class="rule"></div>
<p class="lead">Thank you for choosing these tennis planner stickers. They're made to bring a little match-day energy to every page.</p>
<div class="box"><span class="lbl">What's included</span><p>
<b>Tennis-Stickers-PNG.zip</b> — 69 stickers as transparent PNG files, in four folders: icons, words, planner and quotes<br>
<b>Printable Sheets</b> — a 6-page PDF to print on sticker paper<br><b>This guide</b> — how to use them</p></div>
<div class="steps">{"".join(f'<div><h4><em>{n}.</em>{h}</h4><p>{d}</p></div>' for n, (h, d) in zip("i ii iii iv".split(), steps))}</div>
<div class="steps" style="margin-bottom:0">
<div><h4>Need help?</h4><p>Send me a message on Etsy and I'll reply as soon as I can. If you enjoy the stickers, a review helps a small studio more than you know.</p></div>
<div><h4>Terms of use</h4><p>For personal use only. Please don't share or resell the stickers, or use them in products for sale.</p></div></div>
<div class="deco">{deco}</div><div class="foot">Every point tells you something</div></section></body></html>"""
(here / "guide.html").write_text(html)
print("guide.html")
