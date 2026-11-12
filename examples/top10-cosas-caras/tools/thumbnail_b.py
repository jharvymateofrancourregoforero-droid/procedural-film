"""Thumbnail B: the Salvator Mundi story, "45 LIBRAS" (1958) vs "450 MILLONES" (2017) with a rising arrow.

Real photos only (public-domain painting). usage: python3 tools/thumbnail_b.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import thumblib as L
from thumbnail import BLACK, GRN, INK, P, RED, ROOT, WHT, YEL, card, sticker

W, H = 1280, 720


def split_bg():
    """Cold grey on the left (1958), hot gold on the right (2017)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    left = np.array([40, 44, 52], np.float32)
    right = np.array([120, 80, 8], np.float32)
    t = np.clip((xx - 420) / 500, 0, 1)[..., None]
    base = left * (1 - t) + right * t
    glow = np.exp(-(((xx - 900) / 380) ** 2 + ((yy - 380) / 260) ** 2))[..., None] * np.array([150, 110, 20], np.float32)
    vig = 1 - 0.45 * np.clip(np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) - 0.5, 0, 1)[..., None]
    return Image.fromarray(np.clip((base + glow) * vig, 0, 255).astype(np.uint8)).convert("RGBA")


def arrow(w, h, color):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(0, h * 0.78), (w * 0.62, h * 0.30), (w * 0.55, h * 0.18), (w, 0), (w * 0.86, h * 0.42), (w * 0.76, h * 0.34),
           (w * 0.10, h)]
    d.polygon(pts, fill=color + (255,))
    return L.outline(im, width=6, color=INK)


def main():
    cv = split_bg()
    old = card("salvator", 250, 330, crop=(0, 60, 1280, 1760))
    old = Image.fromarray(np.asarray(old.convert("LA").convert("RGBA")))  # 1958: black and white, small
    L.put(cv, old, 230, 420, 1.0, -6)
    paint = card("salvator", 370, 490, crop=(0, 60, 1280, 1760), border=16, frame=(214, 168, 60))
    L.put(cv, paint, 930, 400, 1.0, 3)
    L.put(cv, arrow(330, 230, GRN), 560, 380, 1.0, 0)
    L.put(cv, sticker("1958: 45 LIBRAS", 40, WHT, INK), 230, 625, 1.0, -4)
    L.put(cv, sticker("US$ 450 MILLONES", 58, GRN, INK, pad=(22, 10)), 930, 655, 1.0, -3)
    head = L.plain_text("LA MISMA PINTURA", 92, YEL, stroke=12)
    L.put(cv, head, 640, 82, min(1.0, 1180 / head.width), -2)
    out = os.path.join(ROOT, "exports", "miniatura_b.jpg")
    cv.convert("RGB").save(out, quality=93)
    print("thumbnail ->", out)


if __name__ == "__main__":
    main()
