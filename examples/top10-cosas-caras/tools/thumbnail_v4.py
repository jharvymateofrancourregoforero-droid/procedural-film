"""Split "rich vs broke" thumbnail (v4), in the style of a wavy-split shower thumbnail.

Left: happy kid under a shower of gold on purple bricks. Right: sad kid under grey rain on blue bricks.
Real CC0 photos; cut-outs with OpenCV GrabCut (no AI). usage: python3 tools/thumbnail_v4.py
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import thumbnail_v2 as V2

ROOT, P, BLACK = V2.ROOT, V2.P, V2.BLACK
W, H = 1280, 720
rng = np.random.RandomState(7)


def grabcut(name, rect, bg_boxes=()):
    img = cv2.imread(P + name + ".jpg")
    h, w = img.shape[:2]
    m = np.zeros((h, w), np.uint8)
    x, y, rw, rh = rect
    m[y:y + rh, x:x + rw] = cv2.GC_PR_FGD
    for bx0, by0, bx1, by1 in bg_boxes:
        m[by0:by1, bx0:bx1] = cv2.GC_BGD
    bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(img, m, None, bg, fg, 10, cv2.GC_INIT_WITH_MASK)
    mm = np.where((m == 1) | (m == 3), 255, 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(mm)
    mm = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
    mm = cv2.morphologyEx(mm, cv2.MORPH_CLOSE, np.ones((13, 13), np.uint8))
    cnts, _ = cv2.findContours(mm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(mm)
    cv2.drawContours(filled, cnts, -1, 255, -1)
    alpha = cv2.GaussianBlur(cv2.erode(filled, np.ones((3, 3), np.uint8)), (5, 5), 0)
    im = Image.fromarray(np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), alpha]))
    return im.crop(im.getchannel("A").getbbox())


def bricks(color, mortar, w, h, bw=110, bh=48):
    im = Image.new("RGB", (w, h), mortar)
    d = ImageDraw.Draw(im)
    for r in range(h // bh + 1):
        off = (r % 2) * bw // 2
        for c in range(-1, w // bw + 2):
            x0, y0 = c * bw - off + 3, r * bh + 3
            jit = rng.randint(-14, 14)
            col = tuple(int(np.clip(v + jit, 0, 255)) for v in color)
            d.rectangle([x0, y0, x0 + bw - 6, y0 + bh - 6], fill=col)
    # soft light from above
    a = np.asarray(im).astype(np.float32)
    yy = np.linspace(0, 1, h)[:, None, None]
    xx = np.linspace(0, 1, w)[None, :, None]
    light = 1.15 - 0.45 * yy - 0.25 * np.abs(xx - 0.5)
    return Image.fromarray(np.clip(a * light, 0, 255).astype(np.uint8)).convert("RGBA")


def tint(im, color, amount, sat=1.0, bright=1.0):
    a = np.asarray(im).astype(np.float32)
    rgb = a[..., :3] / 255
    lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    rgb = lum[..., None] + (rgb - lum[..., None]) * sat
    rgb = rgb * (1 - amount) + np.array(color, np.float32) / 255 * lum[..., None] * 1.25 * amount
    rgb = np.clip(rgb * bright, 0, 1)
    return Image.fromarray(np.concatenate([rgb * 255, a[..., 3:]], -1).astype(np.uint8))


def glow(im, color, radius=28, strength=0.9):
    pad = radius * 2
    a = im.getchannel("A")
    big = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0)
    big.paste(a, (pad, pad))
    g = big.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(v * strength))
    out = Image.new("RGBA", big.size, color + (0,))
    out.putalpha(g)
    out.alpha_composite(im, (pad, pad))
    return out


def shower(canvas, x0, x1, color, n, gold=False):
    """Falling drops (streaks) and, for gold, sparkles."""
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(-40, H)
        L = rng.uniform(14, 40)
        wdt = rng.randint(2, 5)
        a = rng.randint(120, 230)
        d.line([x, y, x - L * 0.12, y + L], fill=color + (a,), width=wdt)
        if gold and rng.rand() < 0.35:
            r = rng.uniform(2, 6)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 245, 190, 255))
    canvas.alpha_composite(ov.filter(ImageFilter.GaussianBlur(0.6)))
    if gold:
        sp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(sp)
        for _ in range(28):
            x, y = rng.uniform(x0 + 20, x1 - 20), rng.uniform(20, H - 40)
            s = rng.uniform(8, 20)
            for ang in (0, 90):
                dx, dy = math.cos(math.radians(ang)) * s, math.sin(math.radians(ang)) * s
                sd.line([x - dx, y - dy, x + dx, y + dy], fill=(255, 255, 230, 240), width=3)
        canvas.alpha_composite(sp.filter(ImageFilter.GaussianBlur(0.8)))


def wavy_mask(xc=640, amp=26, waves=2.2):
    """True on the left side of a wavy vertical divider."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    edge = xc + amp * np.sin(yy / H * 2 * math.pi * waves) + (H / 2 - yy) * 0.08
    return xx < edge, edge


def coin(r):
    """A drawn gold coin (front-facing or tilted), with rim and highlight."""
    sz = int(r * 2 + 8)
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = sz / 2
    d.ellipse([c - r + 3, c - r + 5, c + r + 3, c + r + 5], fill=(80, 50, 0, 120))
    d.ellipse([c - r, c - r, c + r, c + r], fill=(196, 140, 20, 255))
    d.ellipse([c - r * 0.82, c - r * 0.82, c + r * 0.82, c + r * 0.82], fill=(255, 205, 50, 255), outline=(170, 115, 10, 255), width=max(2, int(r * 0.08)))
    f = ImageFont.truetype(BLACK, int(r * 1.05))
    tw = f.getbbox("$")
    d.text((c - (tw[2] - tw[0]) / 2 - tw[0], c - (tw[3] - tw[1]) / 2 - tw[1]), "$", font=f, fill=(190, 130, 15, 255))
    d.ellipse([c - r * 0.55, c - r * 0.75, c - r * 0.05, c - r * 0.45], fill=(255, 250, 210, 170))
    return im


def soft_glow(canvas, cx, cy, rx, ry, color, strength):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2))
    a = np.asarray(canvas).astype(np.float32)
    a[..., :3] = a[..., :3] * (1 - strength * g[..., None]) + np.array(color, np.float32) * strength * g[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def bokeh(canvas, x0, x1, color, n, rmin, rmax, alpha):
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y, r = rng.uniform(x0, x1), rng.uniform(0, H), rng.uniform(rmin, rmax)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (int(rng.uniform(0.4, 1) * alpha),))
    canvas.alpha_composite(ov.filter(ImageFilter.GaussianBlur(3)))


def vignette(canvas, amount=0.45):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    v = np.clip(1 - amount * r ** 2.2, 0.3, 1)
    a = np.asarray(canvas).astype(np.float32)
    a[..., :3] *= v[..., None]
    return Image.fromarray(a.astype(np.uint8))


def main():
    left_mask, edge = wavy_mask(amp=22, waves=1.6)
    purple = bricks((140, 60, 200), (80, 30, 120), W, H)
    blue = bricks((40, 140, 205), (18, 85, 140), W, H)
    a = np.where(left_mask[..., None], np.asarray(purple), np.asarray(blue))
    canvas = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    # warm golden light behind the rich kid, cold dim light behind the sad one
    canvas = soft_glow(canvas, 300, 330, 330, 300, (255, 200, 60), 0.75)
    canvas = soft_glow(canvas, 980, 380, 380, 340, (10, 30, 60), 0.35)
    canvas = vignette(canvas, 0.5)
    bokeh(canvas, 0, 600, (255, 220, 120), 40, 4, 16, 170)
    bokeh(canvas, 690, W, (200, 230, 255), 18, 3, 9, 90)

    # RICH: happy kid, big, gold rim light
    happy = grabcut("kid_happy", (140, 90, 340, 550))
    happy = happy.crop((0, 0, happy.width, int(happy.height * 0.78)))  # head and torso
    happy = V2.punch(happy, sat=1.2, con=1.12, bright=0.9)
    happy = happy.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    rich = glow(V2.outline(happy, 9, (255, 240, 170)), (255, 200, 40), 26, 0.85)
    V2.put(canvas, rich, 315, 440, 1.95)

    # falling gold coins around (not over) the rich kid's face
    for x, y, r, rot in ((80, 90, 30, 0), (560, 330, 22, -15), (70, 560, 34, 10), (210, 40, 18, 0), (40, 330, 20, 0), (590, 470, 16, 0)):
        c = coin(r)
        c = c.resize((c.width, int(c.height * rng.uniform(0.55, 1.0))), Image.LANCZOS)
        V2.put(canvas, c, x, y, 1.0, rot)

    # BROKE: sad kid, cool and desaturated, big
    sad = grabcut("kid_sad", (20, 240, 760, 1200), bg_boxes=((0, 0, 290, 800), (790, 0, 960, 1440)))
    sad = tint(sad, (130, 165, 210), 0.3, sat=0.5, bright=0.95)
    V2.put(canvas, V2.outline(sad, 8, (230, 238, 248)), 985, 460, 0.7)

    # a few tears-like light drops on the sad side (subtle)
    bokeh(canvas, 700, W, (180, 210, 240), 12, 2, 5, 120)

    # wavy white divider with a soft shadow
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    ys = range(0, H + 8, 8)
    pts_l = [(edge[min(y, H - 1), 0] - 11, y) for y in ys]
    pts_r = [(edge[min(y, H - 1), 0] + 11, y) for y in reversed(ys)]
    od.polygon(pts_l + pts_r, fill=(255, 255, 255, 255))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(ov.getchannel("A").filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * 0.6)))
    canvas.alpha_composite(sh, (8, 0))
    canvas.alpha_composite(ov)

    # the story: who watched the video and who didn't
    def chip(text, bg, rot):
        f = ImageFont.truetype(BLACK, 46)
        w = f.getbbox(text)[2]
        im = Image.new("RGBA", (w + 64, 96), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([8, 12, w + 60, 92], radius=14, fill=(0, 0, 0, 150))
        d.rounded_rectangle([2, 4, w + 54, 84], radius=14, fill=bg, outline=(0, 0, 0), width=5)
        d.text((28, 14), text, font=f, fill=(255, 255, 255))
        return im.rotate(rot, expand=True, resample=Image.BICUBIC)

    V2.put(canvas, chip("VIO ESTE VIDEO", (30, 175, 75), 4), 455, 545)
    V2.put(canvas, V2.gold_text("$$$", 110, 10), 470, 650, 1.0, -6)
    V2.put(canvas, chip("NO LO VIO", (220, 35, 40), -4), 1110, 545)
    V2.put(canvas, V2.plain_text("$0", 110, (255, 255, 255), 10), 1170, 650, 1.0, 6)

    # title across the divider: what the video is about
    t10 = V2.gold_text("TOP 10", 132, 12)
    V2.put(canvas, t10, 640, 92, min(1.0, 470 / t10.width), -2)
    sub = V2.plain_text("FORMAS DE GANAR DINERO", 44, (255, 255, 255), 7)
    V2.put(canvas, sub, 640, 192, min(1.0, 560 / sub.width), -2)

    canvas.convert("RGB").save(os.path.join(ROOT, "exports", "miniatura.jpg"), quality=94)


if __name__ == "__main__":
    main()
