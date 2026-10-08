"""Kokoaa viikon materiaalipaketin (zip) valmiista PDF-sivuista ja IG-kuvista.

    python3 viikkotarjoukset/rakenna.py
    python3 viikkotarjoukset/insta.py
    python3 viikkotarjoukset/paketti.py

Paketin sisältö:
  Viikkotarjoukset-vko-XX-YY.pdf        sivut 1 ja 2 yhtenä PDF:nä
  PDF/      sivut erillisinä PDF:inä
  PNG/      sivut erillisinä korkealaatuisina PNG-kuvina (300 dpi)
  Instagram/sivut/     sivut Instagram-kokoon (1080x1350)
  Instagram/tuotteet/  tuotekohtaiset Instagram-kuvat
"""
import glob
import os
import re
import shutil
import subprocess
import zipfile

from PIL import Image
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_DPI = 300
IG_W, IG_H = 1080, 1350


def render_png(pdf, out_stem, dpi):
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", pdf, out_stem], check=True)
    return out_stem + ".png"


def page_to_ig(src_png, out):
    """Sovittaa sivun 4:5-kuvaan korkeuden mukaan ja jatkaa sivun reunoja
    sivuttain, jotta tausta ja alapalkki jatkuvat saumattomasti."""
    page = Image.open(src_png).convert("RGB")
    w = round(page.width * IG_H / page.height)
    page = page.resize((w, IG_H), Image.LANCZOS)
    canvas = Image.new("RGB", (IG_W, IG_H))
    left = (IG_W - w) // 2
    # sivun uloimmat pikselisarakkeet ovat reunan pehmennyksen takia hieman
    # eriväriset, joten reunaa jatketaan muutaman pikselin sisempää
    e = 4
    right = IG_W - left - w
    canvas.paste(page.crop((e, 0, e + 1, IG_H)).resize((left + e, IG_H)), (0, 0))
    canvas.paste(page.crop((w - e - 1, 0, w - e, IG_H)).resize((right + e, IG_H)), (left + w - e, 0))
    canvas.paste(page.crop((e, 0, w - e, IG_H)), (left + e, 0))
    canvas.save(out, optimize=True)


def main():
    pages = sorted(glob.glob(os.path.join(HERE, "Viikkotarjoukset-vko-*-sivu-[0-9].pdf")))
    weeks = sorted({re.search(r"vko-([\d-]+)-sivu", p).group(1) for p in pages})[-1]
    pages = [p for p in pages if f"vko-{weeks}-" in p]
    name = f"Viikkotarjoukset-vko-{weeks}"
    root = os.path.join(HERE, "build", name)
    shutil.rmtree(root, ignore_errors=True)
    for d in ("PDF", "PNG", "Instagram/sivut", "Instagram/tuotteet"):
        os.makedirs(os.path.join(root, d))

    merged = PdfWriter()
    for p in pages:
        merged.add_page(PdfReader(p).pages[0])
        shutil.copy(p, os.path.join(root, "PDF"))
    merged.compress_identical_objects()
    with open(os.path.join(root, f"{name}.pdf"), "wb") as f:
        merged.write(f)

    for p in pages:
        stem = os.path.splitext(os.path.basename(p))[0]
        png = render_png(p, os.path.join(root, "PNG", stem), PNG_DPI)
        page_to_ig(png, os.path.join(root, "Instagram", "sivut", f"{stem}-instagram.png"))

    for img in sorted(glob.glob(os.path.join(HERE, "insta", f"vko-{weeks}", "*.png"))):
        shutil.copy(img, os.path.join(root, "Instagram", "tuotteet"))

    zip_path = os.path.join(HERE, "build", f"{name}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, _, files in os.walk(root):
            for fn in sorted(files):
                full = os.path.join(dirpath, fn)
                z.write(full, os.path.relpath(full, os.path.dirname(root)))
    print(zip_path)


if __name__ == "__main__":
    main()
