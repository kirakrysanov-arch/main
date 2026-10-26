"""Builds the printable sticker sheets (HTML) from the exported PNGs.
Run after render_stickers.js: python3 build_sheets.py <png_dir>"""
import json
import sys
from pathlib import Path

from PIL import Image

here = Path(__file__).parent
png = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else here / "png"
stickers = json.loads((here / "stickers.json").read_text())
FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,800;1,9..144,400"
         "&family=Barlow+Semi+Condensed:wght@600;700&display=swap")

by_cat = {c: [s["id"] for s in stickers if s["cat"] == c] for c in ("icons", "words", "planner", "quotes")}
words = by_cat["words"]
# Pages: (title, italic part, sticker ids, size on the page relative to the rendered sticker)
PAGES = [
    ("Tennis", "icons", by_cat["icons"][:12], 1.0),
    ("More", "icons", by_cat["icons"][12:], 1.0),
    ("Session", "labels", words[:14], 1.05),
    ("Match", "moments", words[14:], 0.84),
    ("Planner", "helpers", by_cat["planner"], 0.95),
    ("Little", "pep talks", by_cat["quotes"], 0.98),
]

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Barlow Semi Condensed', sans-serif; color: #1B2B4B; }
.page { position: relative; overflow: hidden; display: flex; flex-direction: column; break-after: page; }
.page:last-child { break-after: auto; }
.awning { height: 34px; flex: none; background: repeating-linear-gradient(90deg, #1F6B3B 0 26px, transparent 26px 52px); position: relative; }
.awning::after { content: ""; position: absolute; left: 0; right: 0; top: 34px; height: 13px;
  background: radial-gradient(circle at 13px 0, #1F6B3B 12.5px, transparent 13px) 0 0 / 52px 13px repeat-x; }
.head { padding: 26px 40px 0; }
.k { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #C2412D; font-weight: 700; }
h1 { font-family: 'Fraunces', serif; font-weight: 800; font-size: 34px; letter-spacing: -1px; margin-top: 4px; }
h1 em { font-weight: 400; color: #C2412D; }
.grid { flex: 1; display: flex; flex-wrap: wrap; align-content: center; justify-content: center; align-items: center; gap: 14px 18px; padding: 10px 34px 30px; }
.grid img { display: block; }
.foot { text-align: center; font-size: 9px; letter-spacing: 3px; text-transform: uppercase; color: #1F6B3B; font-weight: 700; padding-bottom: 18px; }
"""


def size(sid):
    cat = next(s["cat"] for s in stickers if s["id"] == sid)
    w, h = Image.open(png / cat / f"{sid}.png").size
    return cat, w / 4, h / 4  # the PNGs were rendered at 4x


def build():
    pages = []
    for title, em, ids, scale in PAGES:
        imgs = ""
        for sid in ids:
            cat, iw, ih = size(sid)
            imgs += f'<img src="{(png / cat / f"{sid}.png").as_uri()}" style="width:{iw * scale:.0f}px;height:{ih * scale:.0f}px">'
        pages.append(f'<section class="page" style="width:816px;height:1056px;background:#FFFFFF"><div class="awning"></div>'
                     f'<div class="head"><div class="k">Printable sticker sheet · cut around the white edge</div>'
                     f'<h1>{title} <em>{em}</em></h1></div>'
                     f'<div class="grid">{imgs}</div><div class="foot">Tennis planner stickers · personal use</div></section>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
            f'<style>@page {{ size: 8.5in 11in; margin: 0; }}{CSS}</style></head><body>{"".join(pages)}</body></html>')


(here / "print-sheets.html").write_text(build())
print("print-sheets.html")
