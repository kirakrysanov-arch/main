"""Tekee Instagram-kuvan (1080x1350) jokaisesta tarjoukset.xlsx:n tuotteesta.

    python3 viikkotarjoukset/insta.py

Tulos: insta/vko-<viikot>/<nro>-<tuotenro>.png
"""
import html
import os
import re
import subprocess
from PIL import Image
from decimal import Decimal, ROUND_HALF_UP

from rakenna import ALV, BG, HERE, data_uri, find, money, read_sheet, week_label

W, H = 1080, 1350


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().translate(str.maketrans("äöå", "aoa"))).strip("-")


def photo_size(path, max_w, max_h):
    if not path:
        return max_w, max_h
    with Image.open(path) as im:
        w, h = im.size
    k = min(max_w / w, max_h / h)
    return round(w * k), round(h * k)


def page_html(it):
    e = html.escape
    a = lambda n: data_uri(os.path.join(HERE, "pohjat", n))
    vat = (it["price"] * ALV).quantize(Decimal("0.01"), ROUND_HALF_UP)
    img = find("kuvat", it["code"])
    pw, ph = photo_size(img, 740, 600 if it["tip"] else 660)
    tip = (f'<div class="tip"><span>Käyttövinkki</span>{e(it["tip"])}</div>' if it["tip"] else "")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fira+Sans+Condensed:wght@700&family=Just+Another+Hand&display=block" rel="stylesheet">
<style>
html,body{{margin:0}}
body{{width:{W}px;height:{H}px;background:{BG};overflow:hidden;font-family:'DM Sans';box-sizing:border-box;
     padding:60px 60px 70px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px}}
.top{{display:flex;align-items:flex-start;padding-top:90px}}
.photo{{display:block;width:{pw}px;height:{ph}px}}
.badge{{position:relative;width:260px;height:260px;flex:none;margin-left:-50px;margin-top:-90px}}
.badge img{{width:100%;height:100%;display:block}}
.bt{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
     color:#fff;font-family:'Fira Sans Condensed';font-weight:700;transform:rotate(9deg);line-height:1;padding-bottom:6px}}
.bt b{{font-size:60px;letter-spacing:1px}}
.bt i{{font-style:normal;font-size:42px;margin-top:6px}}
.txt{{display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px;max-width:960px}}
.txt p{{margin:0}}
.nm{{font-weight:500;font-size:50px;line-height:1.18;color:#101828;text-wrap:balance}}
.mt{{font-size:32px;color:#4a5565}}
.vat{{font-weight:700;font-size:36px;color:#8fb584}}
.cd{{font-size:30px;color:#364153}}
.tip{{display:flex;flex-direction:column;align-items:center;text-align:center;max-width:940px;
      font:46px/0.95 'Just Another Hand';color:#8fb584;text-wrap:balance}}
.tip span{{font-size:30px;color:#4a5565;letter-spacing:1px;margin-bottom:6px}}
</style></head><body>
<div class="top">
  {f'<img class="photo" src="{data_uri(img)}">' if img else f'<div class="photo"></div>'}
  <div class="badge"><img src="{a('hintapallo.png')}"><div class="bt"><b>€{money(it["price"])}</b><i>{e(it["unit"])}</i></div></div>
</div>
<div class="txt">
  <p class="nm">{e(it["name"])}</p>
  <p class="mt">{e(it["info"])}</p>
  <p class="vat">{money(vat)}€/{e(it["unit"])} sis.alv</p>
  <p class="cd">Tuotenro: {e(it["code"])}</p>
</div>
{tip}
</body></html>"""


def main():
    pages = read_sheet(os.path.join(HERE, "tarjoukset.xlsx"))
    items = [it for key in sorted(pages) for it in pages[key]]
    week = week_label(items)
    out_dir = os.path.join(HERE, "insta", f"vko-{week}")
    build = os.path.join(HERE, "build", "insta")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(build, exist_ok=True)
    jobs = []
    for n, it in enumerate(items, 1):
        name = f"{n:02d}-{it['code']}-{slug(it['name'])}"
        h = os.path.join(build, name + ".html")
        with open(h, "w", encoding="utf-8") as f:
            f.write(page_html(it))
        jobs += [h, os.path.join(out_dir, name + ".png")]
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(HERE, "kuvakaappaus.js"), str(W), str(H), *jobs],
                   check=True, env={**os.environ, "NODE_PATH": npm_root})
    for p in jobs[1::2]:
        print(p)


if __name__ == "__main__":
    main()
