"""Thumbnail C: the Apex stegosaurus full-bleed, "¿44 MILLONES POR ESTO?" and a TOP 10 badge.

Real photo (CC BY-SA 4.0, DraconicDark, Wikimedia Commons). usage: python3 tools/thumbnail_c.py
"""
import os

import numpy as np
from PIL import Image, ImageFilter

import thumblib as L
from thumbnail import GRN, INK, P, RED, ROOT, WHT, YEL, card, sticker

W, H = 1280, 720


def main():
    im = Image.open(P + "apex1.jpg").convert("RGB")
    s = max(W / im.width, H / im.height) * 1.0
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x0 = int((im.width - W) * 0.42)
    y0 = int((im.height - H) * 0.75)
    im = im.crop((x0, y0, x0 + W, y0 + H))
    im = L.punch(im.convert("RGBA"), sat=1.2, con=1.18, bright=1.0)
    a = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    dark = 1 - 0.55 * np.clip(1 - yy / 260, 0, 1)[..., None] - 0.35 * np.clip((xx - 800) / 480, 0, 1)[..., None]
    a[..., :3] *= dark
    cv = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    head = L.plain_text("¿44 MILLONES POR ESTO?", 92, WHT, stroke=12)
    L.put(cv, head, 640, 84, min(1.0, 1220 / head.width), -2)
    L.put(cv, sticker("US$ 44.600.000", 64, GRN, INK, pad=(24, 12)), 330, 620, 1.0, -4)
    L.put(cv, L.gold_text("TOP 10", 76, 10), 1110, 230, 1.0, 8)
    mini = card("slr_front", 250, 170, crop=(150, 80, 1800, 1075))
    L.put(cv, mini, 1105, 430, 1.0, -6)
    L.put(cv, sticker("US$ 143 M", 34, RED, WHT, pad=(14, 6)), 1105, 535, 1.0, -6)
    L.put(cv, sticker("LO MÁS CARO DEL MUNDO", 30, YEL, INK, pad=(14, 7)), 1060, 640, 1.0, 4)
    out = os.path.join(ROOT, "exports", "miniatura_c.jpg")
    cv.convert("RGB").save(out, quality=93)
    print("thumbnail ->", out)


if __name__ == "__main__":
    main()
