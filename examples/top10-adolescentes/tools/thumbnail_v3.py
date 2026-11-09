"""Before / after YouTube thumbnail (v3): sad kid in grey with $0 vs happy kid in colour with bills.

Real CC0 photos; cut-outs with OpenCV GrabCut (no AI). usage: python3 tools/thumbnail_v3.py
"""
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import thumbnail_v2 as V2

ROOT = V2.ROOT
P = V2.P
W, H = 1280, 720
BLACK = V2.BLACK


def cutout_filled(name, rect):
    """GrabCut cut-out with interior holes filled."""
    c = V2.cutout(name, rect, iters=10)
    a = np.asarray(c).copy()
    m = (a[..., 3] > 127).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(m)
    cv2.drawContours(filled, cnts, -1, 255, -1)
    a[..., 3] = cv2.GaussianBlur(filled, (5, 5), 0)
    im = Image.fromarray(a)
    return im.crop(im.getchannel("A").getbbox())


def grey(im, dark=0.85):
    a = np.asarray(im).astype(np.float32)
    lum = a[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)
    rgb = np.repeat(lum[..., None], 3, -1) * dark
    rgb = (rgb - 128) * 1.15 + 128
    return Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), a[..., 3:]], -1).astype(np.uint8))


def label(text, bg, fg, size=58, rot=0):
    f = ImageFont.truetype(BLACK, size)
    w = f.getbbox(text)[2]
    im = Image.new("RGBA", (w + 70, int(size * 1.6) + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    h = int(size * 1.6)
    d.rounded_rectangle([8, 12, w + 64, h + 12], radius=14, fill=(0, 0, 0, 150))
    d.rounded_rectangle([2, 4, w + 58, h + 4], radius=14, fill=bg, outline=(0, 0, 0), width=5)
    d.text((30, 4 + size * 0.22), text, font=f, fill=fg)
    return im.rotate(rot, expand=True, resample=Image.BICUBIC) if rot else im


def main():
    # left half: cold grey; right half: gold burst; split by a slanted white bar
    canvas = V2.burst_bg()
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    split = 610 + (H / 2 - yy) * 0.18  # slanted divider
    left = xx < split
    a = np.asarray(canvas).astype(np.float32)
    cold = np.array([38, 44, 56], np.float32) * (1 - 0.35 * np.clip(np.abs(xx - 300) / 500, 0, 1))[..., None]
    a[..., :3] = np.where(left[..., None], cold, a[..., :3])
    canvas = Image.fromarray(a.astype(np.uint8))
    # brighter burst centred on the right
    burst = V2.burst_bg().transform((W, H), Image.AFFINE, (1, 0, -620, 0, 1, 0), Image.BILINEAR)
    b = np.asarray(burst).astype(np.float32)
    a = np.asarray(canvas).astype(np.float32)
    a = np.where(left[..., None], a, b)
    canvas = Image.fromarray(a.astype(np.uint8))

    # flying bills on the right
    cash = V2.punch(V2.cutout("cash_hand", (230, 60, 520, 470)), sat=1.25)
    cash = cash.crop(cash.getchannel("A").getbbox())
    for x, y, s, r in ((1180, 150, 0.5, -20), (1170, 600, 0.45, 15), (760, 110, 0.38, 30)):
        V2.put(canvas, V2.outline(cash, 6), x, y, s, r)

    # BEFORE: sad kid, grey
    sad = cutout_filled("kid_sad", (10, 235, 780, 1200))
    V2.put(canvas, V2.outline(grey(sad), 9, (200, 200, 205)), 300, 455, 0.62)

    # AFTER: happy kid, vivid
    happy = cutout_filled("kid_happy", (140, 90, 340, 550))
    V2.put(canvas, V2.outline(V2.punch(happy, sat=1.3, con=1.12, bright=1.0), 10), 960, 430, 1.25)

    # divider bar
    d = ImageDraw.Draw(canvas)
    x_top, x_bot = 610 + (H / 2) * 0.18, 610 - (H / 2) * 0.18
    d.polygon([(x_top - 9, 0), (x_top + 9, 0), (x_bot + 9, H), (x_bot - 9, H)], fill=(255, 255, 255))

    # labels and money tags
    V2.put(canvas, label("ANTES", (230, 40, 40), (255, 255, 255), 60, 3), 170, 70)
    V2.put(canvas, label("DESPUÉS", (40, 200, 90), (255, 255, 255), 60, -3), 1090, 70)
    V2.put(canvas, V2.plain_text("$0", 150, (255, 70, 60), 12), 120, 520, 1.0, 8)
    V2.put(canvas, V2.gold_text("$$$", 150, 12), 1150, 470, 1.0, -8)

    # bottom headline across both halves
    band = Image.new("RGBA", (W, 150), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle([0, 18, W, 150], fill=(0, 0, 0, 205))
    canvas.alpha_composite(band, (0, H - 150))
    top10 = V2.gold_text("TOP 10", 120, 10)
    V2.put(canvas, top10, 250, H - 70, 1.0, -2)
    V2.put(canvas, V2.plain_text("FORMAS DE GANAR DINERO", 62, (255, 255, 255), 8), 800, H - 92, 0.95)
    V2.put(canvas, V2.plain_text("SIENDO ADOLESCENTE", 46, (255, 214, 10), 7), 800, H - 38, 0.95)

    canvas.convert("RGB").save(os.path.join(ROOT, "exports", "miniatura.jpg"), quality=94)


if __name__ == "__main__":
    main()
