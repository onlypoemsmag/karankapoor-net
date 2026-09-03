#!/usr/bin/env python3
"""Generate the site's responsive images from archive/ originals.

Reads archive/photos.json (the ground-truth manifest) and the header images,
emits WebP at 2000/1200/700px wide (long edge) plus a JPEG fallback per photo
into assets/photos/, and the portrait/artwork/logos into assets/img/.
Writes assets/photos/manifest.json used by tools/build_photos.py.
"""
import json, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "archive", "photos")
OUT = os.path.join(ROOT, "assets", "photos")
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

SIZES = [2000, 1200, 700]

def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def resize(im, target):
    w, h = im.size
    k = min(1.0, target / max(w, h))
    return im if k == 1.0 else im.resize((round(w * k), round(h * k)), Image.LANCZOS)

def emit(src_path, base, sizes=SIZES, jpeg_fallback=True):
    im = Image.open(src_path).convert("RGB")
    out = {}
    for s in sizes:
        r = resize(im, s)
        p = f"{base}-{s}.webp"
        r.save(p, "WEBP", quality=80, method=6)
        out[s] = {"file": os.path.relpath(p, ROOT), "w": r.size[0], "h": r.size[1]}
    if jpeg_fallback:
        r = resize(im, 1200)
        p = f"{base}-1200.jpg"
        r.save(p, "JPEG", quality=84, optimize=True, progressive=True)
        out["jpg"] = {"file": os.path.relpath(p, ROOT), "w": r.size[0], "h": r.size[1]}
    return out

def main():
    manifest = json.load(open(os.path.join(ROOT, "archive", "photos.json")))
    site = []
    for e in manifest:
        slug = slugify(e["title"])
        files = emit(os.path.join(SRC, e["filename"]), os.path.join(OUT, slug))
        site.append({"slug": slug, "title": e["title"], "files": files})
        print(slug)
    json.dump(site, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)

    emit(os.path.join(ROOT, "archive", "artwork", "Home portrait (IMG_6009).jpg"),
         os.path.join(IMG, "unused-squarespace-portrait"), sizes=[1200], jpeg_fallback=False)
    # the cover portrait comes from the photographer's HEIC-derived JPEG kept in mocks
    emit(os.path.join(ROOT, "mocks", "img", "portrait-full.jpg"),
         os.path.join(IMG, "portrait"), sizes=[1600, 800], jpeg_fallback=True)
    emit(os.path.join(ROOT, "mocks", "img", "chalhoub.jpg"),
         os.path.join(IMG, "chalhoub"), sizes=[1200, 700], jpeg_fallback=True)
    print("done")

if __name__ == "__main__":
    main()
