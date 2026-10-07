"""Rakentaa viikkotarjous-PDF:t taulukosta tarjoukset.xlsx.

Alkuperäiset PDF:t (pohjat/) säilyvät pohjana: otsikko, logot ja alatunniste
jäävät ennalleen, ja tuotealueet peitetään ja piirretään uudelleen.

    python3 viikkotarjoukset/rakenna.py

Tuotekuvat: kuvat/<tuotenro>.png|jpg  (puuttuva kuva -> paikkamerkki)
QR-koodit:  qr/<nimi>.png, jonka ensimmäinen sana vastaa käyttövinkin
            ensimmäistä sanaa, esim. qr/Lohiwallenberg.png (puuttuva QR -> paikkamerkki)
"""
import base64
import datetime as dt
import html
import os
import re
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP
from io import BytesIO

import openpyxl
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
ALV = Decimal("1.135")
BG = "#e8f5e3"
COLS = [166, 397, 629]  # sarakkeiden keskikohdat (pt)

# Kuvakohtaiset säädöt tuotenumeron mukaan: koko (scale) ja siirto (dx, dy, pt),
# esim. jotta hintapallo ei peitä tuotetta.
SAADOT = {
    "137653": {"scale": 0.86, "dx": -18, "dy": 28},  # Hätälä lohimurekemassa
    "131717": {"scale": 0.9, "dx": -14, "dy": 40},   # Atria tryffelikassler
    "128394": {"scale": 0.88, "dx": -16, "dy": 30},  # Eesti Pagar porkkanakakku
    "103821": {"scale": 0.78, "dx": -12, "dy": 10},            # Sauvon maustekurkkukuutio
}

# Asettelu kummallekin pohjalle (pt, sivun yläreunasta).
LAYOUTS = {
    "perus": {  # pohja ilman käyttövinkkejä
        "template": "pohjat/pohja-perus.pdf",
        "covers": [(20, 250, 773, 590), (20, 622, 773, 958)],
        "rows": [
            {"img": (268, 478), "badge": 264, "text": 488},
            {"img": (640, 850), "badge": 635, "text": 859},
        ],
    },
    "vinkit": {  # pohja, jossa käyttövinkit ja QR-koodit
        "template": "pohjat/pohja-vinkit.pdf",
        "covers": [(20, 205, 773, 585), (20, 602, 773, 982)],
        "rows": [
            {"tip": 212, "img": (318, 476), "badge": 312, "text": 486},
            {"tip": 608, "img": (716, 872), "badge": 708, "text": 883},
        ],
    },
}


def money(d):
    return f"{d:.2f}".replace(".", ",")


def read_sheet(path):
    ws = openpyxl.load_workbook(path, data_only=False).active
    pages, cur = {}, None
    for row in ws.iter_rows(values_only=True):
        a = row[0]
        if isinstance(a, str) and a.lower().startswith("page"):
            cur = pages.setdefault(a.strip(), [])
            continue
        if cur is None or not isinstance(row[3], (int, float)) or not row[6]:
            continue
        cur.append({
            "from": row[1], "to": row[2],
            "price": Decimal(str(row[3])), "unit": str(row[5]).strip(),
            "name": str(row[6]).strip(), "info": str(row[7] or "").strip(),
            "code": str(int(row[8])) if isinstance(row[8], (int, float)) else str(row[8] or ""),
            "tip": str(row[10]).strip() if len(row) > 10 and row[10] else "",
        })
    return pages


def data_uri(path):
    ext = os.path.splitext(path)[1].lower().lstrip(".").replace("jpg", "jpeg")
    with open(path, "rb") as f:
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()


def find(folder, stem):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(HERE, folder, f"{stem}{ext}")
        if os.path.exists(p):
            return p
    return None


def find_qr(tip):
    folder = os.path.join(HERE, "qr")
    word = re.split(r"[\s,]+", tip.strip().lower())[0] if tip.strip() else ""
    if not word or not os.path.isdir(folder):
        return None
    for name in sorted(os.listdir(folder)):
        stem = re.split(r"[\s,._-]+", name.lower())[0]
        if word.startswith(stem) or stem.startswith(word):
            return os.path.join(folder, name)
    return None


def week_label(items):
    weeks = sorted({d.isocalendar()[1] for it in items for d in (it["from"], it["to"])
                    if isinstance(d, (dt.date, dt.datetime))})
    if not weeks:
        return None
    return f"{weeks[0]}-{weeks[-1]}" if len(weeks) > 1 else str(weeks[0])


def overlay_html(layout, items, week):
    L = LAYOUTS[layout]
    badge = data_uri(os.path.join(HERE, "pohjat/hintapallo.png"))
    e = html.escape
    out = []
    for (x0, y0, x1, y1) in L["covers"]:
        out.append(f'<div class="cover" style="left:{x0}pt;top:{y0}pt;width:{x1-x0}pt;height:{y1-y0}pt"></div>')
    # viikkonumero
    out.append('<div class="cover" style="left:560pt;top:38pt;width:200pt;height:44pt"></div>')
    out.append(f'<div class="week">Hinnat voimassa vko {e(week)}</div>')

    for i, it in enumerate(items[:6]):
        r, c = divmod(i, 3)
        row, cx = L["rows"][r], COLS[c]
        if "tip" in row:
            t = row["tip"]
            qr = find_qr(it["tip"])
            qr_html = (f'<img src="{data_uri(qr)}">' if qr else '<span>QR</span>')
            out.append(f'<div class="kv" style="left:{cx-63}pt;top:{t+8}pt">Käyttövinkki</div>')
            out.append(f'<div class="qr{"" if qr else " ph"}" style="left:{cx+19}pt;top:{t}pt">{qr_html}</div>')
            out.append(f'<div class="tip" style="left:{cx-110}pt;top:{t+44}pt">{e(it["tip"])}</div>')
        y0, y1 = row["img"]
        img = find("kuvat", it["code"])
        if img:
            a = SAADOT.get(it["code"], {})
            tf = f'translate({a.get("dx", 0)}pt,{a.get("dy", 0)}pt) scale({a.get("scale", 1)})'
            out.append(f'<div class="ph-img" style="left:{cx-100}pt;top:{y0}pt;height:{y1-y0}pt">'
                       f'<img src="{data_uri(img)}" style="transform:{tf}"></div>')
        else:
            out.append(f'<div class="ph-img ph" style="left:{cx-80}pt;top:{y0+20}pt;width:160pt;height:{y1-y0-30}pt">'
                       f'<span>TUOTEKUVA<br>{e(it["code"])}</span></div>')
        bx = cx + 5
        out.append(f'<div class="badge" style="left:{bx}pt;top:{row["badge"]}pt">'
                   f'<img src="{badge}"><div class="bt"><b>€{money(it["price"])}</b>'
                   f'<i>{e(it["unit"])}</i></div></div>')
        vat = (it["price"] * ALV).quantize(Decimal("0.01"), ROUND_HALF_UP)
        out.append(
            f'<div class="txt" style="left:{cx-115}pt;top:{row["text"]}pt">'
            f'<p class="nm">{e(it["name"])}</p><p class="mt">{e(it["info"])}</p>'
            f'<p class="vat">{money(vat)}€/{e(it["unit"])} sis.alv</p>'
            f'<p class="cd">Tuotenro: {e(it["code"])}</p></div>')

    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fira+Sans+Condensed:wght@700&family=Just+Another+Hand&display=block" rel="stylesheet">
<style>
@page{{size:793.699pt 1122.52pt;margin:0}}
html,body{{margin:0;background:transparent}}
body{{position:relative;width:793.699pt;height:1122.52pt;overflow:hidden}}
body>div{{position:absolute}}
.cover{{background:{BG}}}
.week{{right:47.5pt;top:41pt;font:29pt/1 'Just Another Hand';color:#364153;white-space:nowrap}}
.kv{{font:16pt/1 'Just Another Hand';color:#4a5565;width:76pt;text-align:center}}
.qr{{width:42pt;height:42pt;background:#fff}}
.qr img{{width:100%;height:100%;display:block;image-rendering:pixelated}}
.tip{{width:220pt;text-align:center;font:22pt/0.95 'Just Another Hand';color:#8fb584;text-wrap:balance}}
.ph{{border:1.2pt dashed #8fb584;border-radius:6pt;display:flex;align-items:center;justify-content:center;
     text-align:center;font:600 9pt/1.4 'DM Sans';color:#8fb584;letter-spacing:.05em;box-sizing:border-box}}
.ph-img:not(.ph){{width:200pt;display:flex;align-items:center;justify-content:center}}
.ph-img img{{max-width:100%;max-height:100%;object-fit:contain}}
.badge{{width:101pt;height:101pt}}
.badge img{{width:100%;height:100%;display:block}}
.bt{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
     color:#fff;font-family:'Fira Sans Condensed';font-weight:700;transform:rotate(9deg);line-height:1;padding-bottom:2pt}}
.bt b{{font-size:22.5pt;letter-spacing:.3pt}}
.bt i{{font-style:normal;font-size:16pt;margin-top:2pt}}
.txt{{width:230pt;text-align:center;font-family:'DM Sans'}}
.txt p{{margin:0}}
.nm{{font-weight:500;font-size:13pt;line-height:18pt;color:#101828;height:36pt;display:flex;align-items:flex-end;justify-content:center;text-wrap:balance}}
.mt{{font-size:11pt;line-height:11pt;color:#4a5565;margin-top:6pt!important}}
.vat{{font-weight:700;font-size:11pt;line-height:11pt;color:#8fb584;margin-top:8pt!important}}
.cd{{font-size:11pt;line-height:11pt;color:#364153;margin-top:8pt!important}}
</style></head><body>
{chr(10).join(out)}
</body></html>"""


def render(html_path, pdf_path):
    subprocess.run(["node", os.path.join(HERE, "tulosta.js"), html_path, pdf_path], check=True,
                   env={**os.environ, "NODE_PATH": subprocess.run(
                       ["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()})


def merge(template, overlay, out):
    base = PdfReader(os.path.join(HERE, template)).pages[0]
    base.merge_page(PdfReader(overlay).pages[0])
    w = PdfWriter()
    w.add_page(base)
    w.compress_identical_objects()
    with open(out, "wb") as f:
        w.write(f)


def main():
    pages = read_sheet(os.path.join(HERE, "tarjoukset.xlsx"))
    week = week_label([it for items in pages.values() for it in items])
    build = os.path.join(HERE, "build")
    os.makedirs(build, exist_ok=True)
    # Taulukon Page 1 sisältää käyttövinkit -> vinkkipohja, Page 2 -> peruspohja.
    plan = [("Page 1", "vinkit", 1), ("Page 2", "perus", 2)]
    for key, layout, n in plan:
        items = pages.get(key, [])
        if not items:
            print(f"{key}: ei tuotteita, ohitetaan")
            continue
        h = os.path.join(build, f"sivu-{n}.html")
        with open(h, "w", encoding="utf-8") as f:
            f.write(overlay_html(layout, items, week))
        ov = os.path.join(build, f"sivu-{n}-overlay.pdf")
        render(h, ov)
        out = os.path.join(HERE, f"Viikkotarjoukset-vko-{week}-sivu-{n}.pdf")
        merge(LAYOUTS[layout]["template"], ov, out)
        missing = [it["code"] for it in items[:6] if not find("kuvat", it["code"])]
        print(f"{out}  (puuttuvat kuvat: {', '.join(missing) or '-'})")


if __name__ == "__main__":
    sys.exit(main())
