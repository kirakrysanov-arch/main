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
ALV = Decimal("1.135")  # oletus: elintarvikkeiden alv 13,5 %


def alv_kerroin(formula):
    """Lukee alv-kertoimen taulukon E-sarakkeen kaavasta (esim. "=D17*1.255",
    muut kuin elintarvikkeet 25,5 %); ilman kaavaa käytetään oletusta."""
    m = re.search(r"\*\s*([0-9]+[.,][0-9]+)", str(formula or ""))
    return Decimal(m.group(1).replace(",", ".")) if m else ALV
BG = "#e8f5e3"
COLS = [166, 397, 629]  # sarakkeiden keskikohdat (pt)

# Kuvakohtainen kallistus tuotenumeron mukaan (asteina, negatiivinen = vastapäivään).
# Koko ja paikka lasketaan automaattisesti (sovita_kuva).
SAADOT = {
    "145141": {"scale": 0.86, "dx": -22, "dy": 8, "rotate": -15},  # Miyata pankojauho, kallistus vastapäivään
}

# Asettelu kummallekin pohjalle (pt, sivun yläreunasta).
LAYOUTS = {
    "perus": {  # pohja ilman käyttövinkkejä
        "template": "pohjat/pohja-perus.pdf",
        "kuva": (210, 182, 19500),  # kuva-alueen leveys, korkeus ja tavoitepinta-ala (pt)
        "covers": [(20, 250, 773, 590), (20, 622, 773, 958)],
        "rows": [
            {"img": (268, 478), "badge": 264, "text": 488},
            {"img": (640, 850), "badge": 635, "text": 859},
        ],
    },
    "vinkit": {  # pohja, jossa käyttövinkit ja QR-koodit
        "template": "pohjat/pohja-vinkit.pdf",
        "kuva": (196, 138, 13500),
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
            "price": Decimal(str(row[3])), "alv": alv_kerroin(row[4]), "unit": str(row[5]).strip(),
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


def aariviiva(path, paksuus=0.05):
    """Lisää tuotekuvan ympärille valkoisen ääriviivan (tarramainen tyyli).
    Paksuus suhteessa kuvan pidempään sivuun; tulos tallennetaan build/aariviiva/."""
    if not path:
        return path
    from PIL import Image, ImageFilter
    out_dir = os.path.join(HERE, "build", "aariviiva")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, os.path.splitext(os.path.basename(path))[0] + ".png")
    with Image.open(path) as im:
        im = im.convert("RGBA")
    r = max(9, round(max(im.size) * paksuus))
    pad = r + 2
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big.paste(im, (pad, pad))
    a = big.getchannel("A").point(lambda v: 255 if v > 40 else 0)
    # pyöreä laajennus: sumenna ja kynnystä, jolloin kulmat pyöristyvät
    halo = a.filter(ImageFilter.GaussianBlur(r * 0.6)).point(lambda v: 255 if v > 18 else 0)
    halo = halo.filter(ImageFilter.GaussianBlur(0.8))
    base = Image.new("RGBA", big.size, (255, 255, 255, 0))
    base.putalpha(halo)
    base.alpha_composite(big)
    base.crop(base.getbbox()).save(out)
    return out


# Tuotelohkon välit (pt), samat joka sarakkeessa: vinkki -> hintapallo ja kuva -> tekstit.
# Kuva-alueen koko on asettelukohtainen (LAYOUTS[..]["kuva"]).
KUVA_RAKO = 10              # kuva-alueen ja tuotenimen väli
PALLO_NOUSU = 22            # kuinka paljon hintapallo nousee kuva-alueen yläpuolelle
VINKKI_RAKO = 4             # käyttövinkin ja hintapallon väli


def kierretty(path, code, deg):
    from PIL import Image
    out_dir = os.path.join(HERE, "build", "kierto")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{code}.png")
    with Image.open(path) as im:
        im = im.convert("RGBA").rotate(-deg, resample=Image.BICUBIC, expand=True)
        im.crop(im.getbbox()).save(out)
    return out


def sovita_kuva(path, max_w, max_h, area):
    """Kuvan koko (pt): suunnilleen sama pinta-ala kaikille tuotteille, jotta
    leveät tai isot tuotteet eivät näytä muita kookkaammilta; enintään kuva-alue."""
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    k = min((area / (iw * ih)) ** 0.5, max_w / iw, max_h / ih)
    return iw * k, ih * k


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
    # ensimmäisen alkupäivän ja viimeisen loppupäivän viikot, jotta vuodenvaihde
    # menee oikein (esim. 30.11.-17.1. -> "49-2", ei "2-49")
    starts = [it["from"] for it in items if isinstance(it["from"], (dt.date, dt.datetime))]
    ends = [it["to"] for it in items if isinstance(it["to"], (dt.date, dt.datetime))]
    if not starts and not ends:
        return None
    first = min(starts or ends).isocalendar()[1]
    last = max(ends or starts).isocalendar()[1]
    return f"{first}-{last}" if first != last else str(first)


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
    # alatunnisteen hintarivi: hinta sis. alv näytetään vihreällä
    out.append('<div class="cover" style="left:554pt;top:1030pt;width:206pt;height:16pt"></div>')
    out.append('<div class="foot" style="left:556.5pt;top:1034pt">Hinnat täysin myyntierin, vihreä hinta sis. alv.</div>')

    for i, it in enumerate(items[:6]):
        r, c = divmod(i, 3)
        row, cx = L["rows"][r], COLS[c]
        T = row["text"]
        KW, KH, KA = L["kuva"]
        box_top = T - KUVA_RAKO - KH            # kuva-alueen yläreuna
        badge_top = box_top - PALLO_NOUSU       # hintapallo kuva-alueen oikeaan yläkulmaan
        if "tip" in row:
            qr = find_qr(it["tip"])
            qr_html = (f'<img src="{data_uri(qr)}">' if qr else '<span>QR</span>')
            # käyttövinkki ankkuroidaan alareunastaan juuri hintapallon yläpuolelle
            out.append(f'<div class="vinkki" style="left:{cx-115}pt;top:{badge_top - VINKKI_RAKO}pt">'
                       f'<div class="vh"><span class="kv">Käyttövinkki</span>'
                       f'<span class="qr{"" if qr else " ph"}">{qr_html}</span></div>'
                       f'<div class="tip">{e(it["tip"])}</div></div>')
        img = find("kuvat", it["code"])
        rot = SAADOT.get(it["code"], {}).get("rotate", 0)
        img = aariviiva(kierretty(img, it["code"], -rot) if img and rot else img)
        if img:
            # kuvat keskitetään kuva-alueeseen ja skaalataan suunnilleen samaan pinta-alaan
            # ja asetetaan samalle perusviivalle tuotenimen yläpuolelle
            w, h = sovita_kuva(img, KW, KH, KA)
            out.append(f'<div class="ph-img" style="left:{cx - w / 2:.1f}pt;top:{box_top + KH - h:.1f}pt;'
                       f'width:{w:.1f}pt;height:{h:.1f}pt"><img src="{data_uri(img)}"></div>')
        else:
            out.append(f'<div class="ph-img ph" style="left:{cx-80}pt;top:{box_top}pt;width:160pt;height:{KH}pt">'
                       f'<span>TUOTEKUVA<br>{e(it["code"])}</span></div>')
        bx = cx + 14
        out.append(f'<div class="badge" style="left:{bx}pt;top:{badge_top}pt">'
                   f'<img src="{badge}"><div class="bt"><b>€{money(it["price"])}</b>'
                   f'<i>{e(it["unit"])}</i></div></div>')
        vat = (it["price"] * it["alv"]).quantize(Decimal("0.01"), ROUND_HALF_UP)
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
.foot{{font:400 9pt/9pt 'DM Sans';color:#364153;white-space:nowrap}}
.vinkki{{width:230pt;transform:translateY(-100%);display:flex;flex-direction:column;align-items:center;gap:3pt}}
.vh{{display:flex;align-items:center;gap:10pt}}
.kv{{font:16pt/1 'Just Another Hand';color:#4a5565}}
.qr{{display:block;width:42pt;height:42pt;background:#fff}}
.qr img{{width:100%;height:100%;display:block;image-rendering:pixelated}}
.tip{{width:220pt;text-align:center;margin:0 auto;font:22pt/0.95 'Just Another Hand';color:#8fb584;text-wrap:balance}}
.ph{{border:1.2pt dashed #8fb584;border-radius:6pt;display:flex;align-items:center;justify-content:center;
     text-align:center;font:600 9pt/1.4 'DM Sans';color:#8fb584;letter-spacing:.05em;box-sizing:border-box}}
.ph-img img{{width:100%;height:100%;display:block}}
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
