"""Valmistelee tuotekuvat ja QR-koodit rakenna.py:tä varten.

    python3 viikkotarjoukset/valmistele_kuvat.py <kuvakansio> [<qr-kansio>]

Tuotekuvat: tiedostonimen alussa oleva tuotenumero (esim. "137653_lohi.png")
ratkaisee tuotteen. Valkoinen tausta poistetaan reunoilta alkaen, joten kuva
istuu vihreälle pohjalle kuten alkuperäisissä PDF:issä. Tulos: kuvat/<tuotenro>.png

QR-koodit kopioidaan sellaisenaan kansioon qr/ (PNG-muodossa); rakenna.py
yhdistää ne käyttövinkkeihin tiedostonimen ensimmäisen sanan perusteella.
"""
import os
import re
import sys
import unicodedata
from collections import deque

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))


def remove_white_bg(im, tol=24):
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    near_white = lambda p: p[3] < 16 or min(p[:3]) >= 255 - tol
    bg = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.extend(((x, 0), (x, h - 1)))
    for y in range(h):
        q.extend(((0, y), (w - 1, y)))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if bg[i] or not near_white(px[x, y]):
            continue
        bg[i] = 1
        if x > 0: q.append((x - 1, y))
        if x < w - 1: q.append((x + 1, y))
        if y > 0: q.append((x, y - 1))
        if y < h - 1: q.append((x, y + 1))
    mask = Image.frombytes("L", (w, h), bytes(0 if b else 255 for b in bg))
    mask = Image.composite(mask, Image.new("L", (w, h), 0), im.getchannel("A"))
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    im.putalpha(mask)
    return im


def main(src, qr_src=None):
    os.makedirs(os.path.join(HERE, "kuvat"), exist_ok=True)
    for name in sorted(os.listdir(src)):
        m = re.match(r"(\d{5,})", unicodedata.normalize("NFC", name))
        if not m or name.startswith("."):
            continue
        im = remove_white_bg(Image.open(os.path.join(src, name)))
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
        im.thumbnail((900, 900), Image.LANCZOS)
        out = os.path.join(HERE, "kuvat", f"{m.group(1)}.png")
        im.save(out, optimize=True)
        print(out, im.size)
    if qr_src:
        os.makedirs(os.path.join(HERE, "qr"), exist_ok=True)
        for name in sorted(os.listdir(qr_src)):
            if name.startswith(".") or not name.lower().endswith((".gif", ".png", ".jpg", ".jpeg")):
                continue
            stem = unicodedata.normalize("NFC", os.path.splitext(name)[0])
            out = os.path.join(HERE, "qr", f"{stem}.png")
            src_im = Image.open(os.path.join(qr_src, name)).convert("RGBA")
            qr = Image.new("RGB", src_im.size, "white")
            qr.paste(src_im, mask=src_im.getchannel("A"))
            # terävä suurennos, jotta moduulit pysyvät painossa teräväreunaisina
            qr.resize((qr.width * 6, qr.height * 6), Image.NEAREST).save(out)
            print(out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
