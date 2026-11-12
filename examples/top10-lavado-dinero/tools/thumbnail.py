"""YouTube thumbnail for "10 formas de lavar dinero": dirty cash, a red EXPUESTO stamp and two real case cards.

Real photos only (StockSnap CC0, Wikimedia Commons). usage: python3 tools/thumbnail.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import thumblib as L

ROOT, P, BLACK = L.ROOT, L.P, L.BLACK
W, H = 1280, 720
YEL, RED, GRN, WHT, INK = (255, 214, 10), (230, 33, 23), (43, 217, 107), (255, 255, 255), (12, 12, 12)


def cover(name, w, h, crop=None):
    im = Image.open(P + name + ".jpg").convert("RGB")
    if crop:
        im = im.crop(crop)
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x0, y0 = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))


def card(name, w, h, crop=None, border=10):
    im = L.punch(cover(name, w, h, crop).convert("RGBA"), sat=1.2, con=1.12, bright=1.05)
    c = Image.new("RGBA", (w + 2 * border, h + 2 * border), (250, 248, 242, 255))
    c.alpha_composite(im, (border, border))
    return L.outline(c, width=1, color=(250, 248, 242))


def sticker(text, size, bg, fg, pad=(22, 10)):
    f = ImageFont.truetype(BLACK, size)
    b = f.getbbox(text)
    im = Image.new("RGBA", (b[2] + 2 * pad[0], b[3] - b[1] + 2 * pad[1] + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=14, fill=bg + (255,))
    d.text((pad[0], pad[1] - b[1] + 2), text, font=f, fill=fg)
    return L.outline(im, width=5, color=INK)


def stamp(text, size):
    """Rubber-stamp look: red outlined box with rough edges."""
    f = ImageFont.truetype(BLACK, size)
    b = f.getbbox(text)
    w, h = b[2] + 60, b[3] - b[1] + 50
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, w - 7, h - 7], radius=12, fill=(245, 240, 230, 235), outline=RED + (255,), width=10)
    d.text((30, 25 - b[1]), text, font=f, fill=RED + (255,))
    a = np.asarray(im).copy()
    rng = np.random.RandomState(3)
    holes = (rng.rand(h, w) < 0.06) & (a[..., 0] > 200) & (a[..., 1] < 80)
    a[..., 3] = np.where(holes, (a[..., 3] * 0.35).astype(np.uint8), a[..., 3])
    return Image.fromarray(a)


def main():
    bg = cover("money_cash", W, H).filter(ImageFilter.GaussianBlur(3))
    a = np.asarray(bg).astype(np.float32)
    lum = a.mean(axis=2, keepdims=True)
    a = lum + (a - lum) * 0.55  # desaturated, dirty money
    yy, xx = np.mgrid[0:H, 0:W]
    a = a * (0.38 + 0.25 * np.exp(-(((xx - 640) / 520) ** 2 + ((yy - 330) / 300) ** 2)))[..., None]
    a = a + np.array([30, 6, 0], np.float32) * np.clip(1 - yy / H, 0, 1)[..., None]
    cv = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

    L.put(cv, card("hsbc_mexico", 270, 330), 170, 470, 1.0, 6)
    L.put(cv, sticker("US$ 1.920 M DE MULTA", 28, RED, WHT, pad=(12, 7)), 190, 660, 1.0, 4)
    L.put(cv, card("bitcoin_coin", 270, 330), 1110, 470, 1.0, -6)
    L.put(cv, sticker("US$ 3.600 M INCAUTADOS", 28, GRN, INK, pad=(12, 7)), 1090, 660, 1.0, -4)

    t1 = L.plain_text("10 FORMAS DE", 84, WHT, stroke=11)
    t2 = L.gold_text("LAVAR DINERO", 132, 14)
    L.put(cv, t1, 640, 120, 1.0, -2)
    L.put(cv, t2, 640, 250, min(1.0, 900 / t2.width), -2)
    L.put(cv, stamp("Y CÓMO LOS ATRAPARON", 64), 640, 470, min(1.0, 760 / stamp("Y CÓMO LOS ATRAPARON", 64).width), -7)
    out = os.path.join(ROOT, "exports", "miniatura.jpg")
    cv.convert("RGB").save(out, quality=93)
    print("thumbnail ->", out)


if __name__ == "__main__":
    main()
