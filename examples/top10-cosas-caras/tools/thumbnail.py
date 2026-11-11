"""YouTube thumbnail for "Top 10 cosas más caras": three real record items as photo cards with price stickers.

Real photos (Wikimedia Commons / StockSnap); no AI. usage: python3 tools/thumbnail.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import thumblib as L

ROOT, P, BLACK = L.ROOT, L.P, L.BLACK
W, H = 1280, 720
YEL, RED, GRN, WHT, INK = (255, 214, 10), (230, 33, 23), (43, 217, 107), (255, 255, 255), (12, 12, 12)


def background():
    bg = Image.open(P + "gold_bars.jpg").convert("RGB")
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1), Image.LANCZOS).crop((0, 0, W, H))
    bg = bg.filter(ImageFilter.GaussianBlur(9))
    a = np.asarray(bg).astype(np.float32) * 0.42
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((xx - W / 2) / 520) ** 2 + ((yy - 470) / 300) ** 2))[..., None]
    a = a + glow * np.array([120, 85, 10], np.float32)
    vig = 1 - 0.5 * np.clip(np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) - 0.45, 0, 1)[..., None]
    return Image.fromarray(np.clip(a * vig, 0, 255).astype(np.uint8)).convert("RGBA")


def card(name, w, h, crop=None, border=10, frame=(250, 248, 242)):
    im = Image.open(P + name + ".jpg").convert("RGB")
    if crop:
        im = im.crop(crop)
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x0, y0 = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((x0, y0, x0 + w, y0 + h))
    im = L.punch(im.convert("RGBA"), sat=1.25, con=1.12, bright=1.06)
    c = Image.new("RGBA", (w + 2 * border, h + 2 * border), frame + (255,))
    c.alpha_composite(im, (border, border))
    return L.outline(c, width=1, color=frame)


def sticker(text, size, bg, fg, pad=(22, 10)):
    f = ImageFont.truetype(BLACK, size)
    b = f.getbbox(text)
    im = Image.new("RGBA", (b[2] + 2 * pad[0], b[3] - b[1] + 2 * pad[1] + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=14, fill=bg + (255,))
    d.text((pad[0], pad[1] - b[1] + 2), text, font=f, fill=fg)
    return L.outline(im, width=5, color=INK)


def main():
    cv = background()
    # left: the Apex stegosaurus, right: the 300 SLR, centre (biggest): Salvator Mundi
    dino = card("apex1", 400, 330, crop=(150, 60, 1500, 1200))
    car = card("slr_front", 420, 300, crop=(150, 80, 1800, 1075))
    paint = card("salvator", 330, 440, crop=(0, 60, 1280, 1760), border=14, frame=(214, 168, 60))
    L.put(cv, dino, 230, 470, 1.0, 7)
    L.put(cv, car, 1050, 470, 1.0, -7)
    L.put(cv, paint, 640, 440, 1.0, 0)
    L.put(cv, sticker("US$ 44,6 M", 46, RED, WHT), 235, 650, 1.0, 4)
    L.put(cv, sticker("US$ 143 M", 46, RED, WHT), 1045, 650, 1.0, -4)
    L.put(cv, sticker("US$ 450 M", 74, GRN, INK, pad=(26, 12)), 640, 640, 1.0, -3)
    head = L.plain_text("¿QUIÉN PAGA ESTO?", 96, WHT, stroke=12)
    L.put(cv, head, 640, 92, min(1.0, 1200 / head.width), -2)
    t10 = L.gold_text("TOP 10", 70, 9)
    L.put(cv, t10, 140, 205, 1.0, -8)
    sub = sticker("LO MÁS CARO DEL MUNDO", 30, YEL, INK, pad=(14, 7))
    L.put(cv, sub, 1045, 212, 1.0, 5)
    out = os.path.join(ROOT, "exports", "miniatura.jpg")
    cv.convert("RGB").save(out, quality=93)
    print("thumbnail ->", out)


if __name__ == "__main__":
    main()
