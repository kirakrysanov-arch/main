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
BADGE = 390  # hintapallon halkaisija (px)
# Kuva-alue (kuva keskitetään sen alareunaan) ja tekstilohkon alareuna:
# samat kaikissa kuvissa, jotta sarja on yhtenäinen.
PHOTO_W, PHOTO_H, PHOTO_TOP = 900, 680, 240
PHOTO_AREA = 400_000  # tavoitepinta-ala (px²), jotta tuotteet näyttävät yhtä suurilta
TEXT_BOTTOM = 80


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().translate(str.maketrans("äöå", "aoa"))).strip("-")


def photo_size(path, max_w, max_h, area):
    """Skaalaa kuvan suunnilleen samaan pinta-alaan (näyttää yhtä isolta
    muodosta riippumatta), kuitenkin enintään kuva-alueen kokoiseksi."""
    if not path:
        return max_w, max_h
    with Image.open(path) as im:
        w, h = im.size
    k = min((area / (w * h)) ** 0.5, max_w / w, max_h / h)
    return round(w * k), round(h * k)


def page_html(it):
    e = html.escape
    a = lambda n: data_uri(os.path.join(HERE, "pohjat", n))
    vat = (it["price"] * ALV).quantize(Decimal("0.01"), ROUND_HALF_UP)
    img = find("kuvat", it["code"])
    pw, ph = photo_size(img, PHOTO_W, PHOTO_H, PHOTO_AREA)
    price_fs = 112 if len(money(it["price"])) <= 4 else 92
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fira+Sans+Condensed:wght@700&display=block" rel="stylesheet">
<style>
html,body{{margin:0}}
body{{width:{W}px;height:{H}px;background:{BG};overflow:hidden;font-family:'DM Sans';position:relative}}
body>div{{position:absolute}}
.pw{{left:{(W - PHOTO_W)//2}px;top:{PHOTO_TOP}px;width:{PHOTO_W}px;height:{PHOTO_H}px;display:flex;align-items:flex-end;justify-content:center}}
.pw img{{width:{pw}px;height:{ph}px}}
.badge{{left:{W - BADGE - 18}px;top:18px;width:{BADGE}px;height:{BADGE}px}}
.badge img{{width:100%;height:100%;display:block}}
.bt{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
     color:#fff;font-family:'Fira Sans Condensed';font-weight:700;transform:rotate(9deg);line-height:.92;padding-bottom:8px}}
.bt b{{font-size:{price_fs}px;letter-spacing:.5px}}
.bt i{{font-style:normal;font-size:68px;margin-top:6px}}
.txt{{left:60px;right:60px;bottom:{TEXT_BOTTOM}px;display:flex;flex-direction:column;align-items:center;text-align:center}}
.txt p{{margin:0}}
.nm{{font-weight:600;font-size:54px;line-height:1.15;color:#101828;text-wrap:balance;max-width:940px}}
.mt{{font-size:32px;line-height:1.2;color:#4a5565;margin-top:16px!important}}
.vat{{font-weight:700;font-size:50px;line-height:1.1;color:#8fb584;margin-top:14px!important}}
.cd{{font-size:30px;line-height:1.2;color:#364153;margin-top:12px!important}}
</style></head><body>
<div class="pw">{f'<img src="{data_uri(img)}">' if img else ''}</div>
<div class="badge"><img src="{a('hintapallo.png')}"><div class="bt"><b>€{money(it["price"])}</b><i>{e(it["unit"])}</i></div></div>
<div class="txt">
  <p class="nm">{e(it["name"])}</p>
  <p class="mt">{e(it["info"])}</p>
  <p class="vat">{money(vat)}€/{e(it["unit"])} sis.alv</p>
  <p class="cd">Tuotenro: {e(it["code"])}</p>
</div>
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
