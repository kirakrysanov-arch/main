"""Tekee Instagram-kuvan (1080x1350) jokaisesta tarjoukset.xlsx:n tuotteesta.

    python3 viikkotarjoukset/insta.py

Tulos: insta/vko-<viikot>/<nro>-<tuotenro>.png
"""
import html
import os
import re
import subprocess
from decimal import Decimal, ROUND_HALF_UP

from rakenna import ALV, BG, HERE, data_uri, find, money, read_sheet, week_label

W, H = 1080, 1350


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().translate(str.maketrans("äöå", "aoa"))).strip("-")


def page_html(it, week):
    e = html.escape
    a = lambda n: data_uri(os.path.join(HERE, "pohjat", n))
    vat = (it["price"] * ALV).quantize(Decimal("0.01"), ROUND_HALF_UP)
    img = find("kuvat", it["code"])
    tip = (f'<div class="tip"><span>Käyttövinkki</span>{e(it["tip"])}</div>' if it["tip"] else "")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fira+Sans+Condensed:wght@700&family=Just+Another+Hand&display=block" rel="stylesheet">
<style>
html,body{{margin:0}}
body{{width:{W}px;height:{H}px;background:{BG};position:relative;overflow:hidden;font-family:'DM Sans'}}
body>*{{position:absolute}}
.vk{{left:34px;top:22px;width:350px}}
.ot{{right:44px;top:34px;width:400px}}
.week{{right:58px;top:160px;font:48px/1 'Just Another Hand';color:#364153;white-space:nowrap}}
.photo{{left:80px;top:262px;width:690px;height:590px;display:flex;align-items:center;justify-content:center}}
.photo img{{width:100%;height:100%;object-fit:contain}}
.badge{{left:762px;top:236px;width:270px;height:270px}}
.badge img{{width:100%;height:100%;display:block}}
.bt{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
     color:#fff;font-family:'Fira Sans Condensed';font-weight:700;transform:rotate(9deg);line-height:1;padding-bottom:6px}}
.bt b{{font-size:62px;letter-spacing:1px}}
.bt i{{font-style:normal;font-size:44px;margin-top:6px}}
.txt{{left:60px;right:60px;top:872px;height:{"300" if tip else "400"}px;display:flex;flex-direction:column;
      align-items:center;justify-content:center;text-align:center;gap:14px}}
.txt p{{margin:0}}
.nm{{font-weight:500;font-size:50px;line-height:1.18;color:#101828;text-wrap:balance}}
.mt{{font-size:32px;color:#4a5565}}
.vat{{font-weight:700;font-size:36px;color:#8fb584}}
.cd{{font-size:30px;color:#364153}}
.tip{{left:70px;right:70px;top:1176px;height:110px;display:flex;flex-direction:column;align-items:center;justify-content:center;
      text-align:center;font:46px/0.95 'Just Another Hand';color:#8fb584;text-wrap:balance}}
.tip span{{font-size:30px;color:#4a5565;letter-spacing:1px;margin-bottom:6px}}
.bar{{left:0;bottom:0;width:{W}px}}
</style></head><body>
<img class="vk" src="{a('insta/viikoittaiset.png')}">
<img class="ot" src="{a('insta/otsikko.png')}">
<div class="week">Hinnat voimassa vko {e(week)}</div>
<div class="photo">{f'<img src="{data_uri(img)}">' if img else ''}</div>
<div class="badge"><img src="{a('hintapallo.png')}"><div class="bt"><b>€{money(it["price"])}</b><i>{e(it["unit"])}</i></div></div>
<div class="txt">
  <p class="nm">{e(it["name"])}</p>
  <p class="mt">{e(it["info"])}</p>
  <p class="vat">{money(vat)}€/{e(it["unit"])} sis.alv</p>
  <p class="cd">Tuotenro: {e(it["code"])}</p>
</div>
{tip}
<img class="bar" src="{a('insta/alapalkki.png')}">
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
            f.write(page_html(it, week))
        jobs += [h, os.path.join(out_dir, name + ".png")]
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(HERE, "kuvakaappaus.js"), str(W), str(H), *jobs],
                   check=True, env={**os.environ, "NODE_PATH": npm_root})
    for p in jobs[1::2]:
        print(p)


if __name__ == "__main__":
    main()
