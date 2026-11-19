"""Valmistelee tuotekuvat ja QR-koodit rakenna.py:tä varten.

    python3 viikkotarjoukset/valmistele_kuvat.py <kuvakansio> [<qr-kansio>] [--ai 104826,...] [--kuori 145128,...]

--ai: luettelon tuotenumeroiden taustat poistetaan tekoälymallilla (rembg),
kun tuote itse on valkoinen ja tavallinen poisto syö siitä palan.
--kuori: tuotteesta pidetään kaikki sen ulkoreunan sisällä (täytetty kupera kuori),
kun vaalea pussi tai pakkaus muuten saisi reikiä.

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


def remove_bg_ai(im):
    from rembg import new_session, remove  # pip install "rembg[cpu]"
    out = remove(im.convert("RGB"), session=new_session("isnet-general-use")).convert("RGBA")
    out.putalpha(out.getchannel("A").point(lambda v: 0 if v < 12 else v))  # hajapikselit pois
    return out


def remove_bg_hull(im, white=246):
    import cv2  # pip install opencv-python-headless
    import numpy as np
    arr = np.array(im.convert("RGB"))
    fg = (arr.min(axis=2) < white).astype(np.uint8) * 255
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hull = cv2.convexHull(np.vstack([c for c in cnts if cv2.contourArea(c) > 50]))
    mask = np.zeros(fg.shape, np.uint8)
    cv2.fillPoly(mask, [hull], 255)
    m = Image.fromarray(mask).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    out = im.convert("RGBA")
    out.putalpha(m)
    return out


def main(src, qr_src=None, ai_codes=(), hull_codes=()):
    os.makedirs(os.path.join(HERE, "kuvat"), exist_ok=True)
    for name in sorted(os.listdir(src)):
        m = re.match(r"(\d{5,})", unicodedata.normalize("NFC", name))
        if not m or name.startswith("."):
            continue
        im = Image.open(os.path.join(src, name))
        if m.group(1) in hull_codes:
            im = remove_bg_hull(im)
        elif m.group(1) in ai_codes:
            im = remove_bg_ai(im)
        else:
            im = remove_white_bg(im)
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
    args = sys.argv[1:]
    opts = {}
    for flag in ("--ai", "--kuori"):
        if flag in args:
            i = args.index(flag)
            opts[flag] = tuple(args[i + 1].split(","))
            del args[i:i + 2]
    main(*args[:2], ai_codes=opts.get("--ai", ()), hull_codes=opts.get("--kuori", ()))
