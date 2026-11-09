"""Eye-catching YouTube thumbnail (v2): burst background, outlined cut-out, flying real bills, gold TOP 10, #1 mystery box.

Cut-outs use OpenCV GrabCut (classic segmentation, no AI). usage: python3 tools/thumbnail_v2.py
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "photos") + "/"
W, H = 1280, 720
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"


def cutout(name, rect, iters=8):
    img = cv2.imread(P + name + ".jpg")
    h, w = img.shape[:2]
    m = np.zeros((h, w), np.uint8)
    bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(img, m, rect, bg, fg, iters, cv2.GC_INIT_WITH_RECT)
    m = np.where((m == 1) | (m == 3), 255, 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    m = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    m = cv2.GaussianBlur(cv2.erode(m, np.ones((3, 3), np.uint8)), (5, 5), 0)
    return Image.fromarray(np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), m]))


def punch(im, sat=1.35, con=1.15, bright=1.05):
    """Thumbnail-style colour: more saturation and contrast."""
    a = np.asarray(im).astype(np.float32)
    rgb, alpha = a[..., :3] / 255, a[..., 3:]
    lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    rgb = lum[..., None] + (rgb - lum[..., None]) * sat
    rgb = np.clip(((rgb - 0.5) * con + 0.5) * bright, 0, 1)
    return Image.fromarray(np.concatenate([rgb * 255, alpha], -1).astype(np.uint8))


def outline(im, width=10, color=(255, 255, 255)):
    """Thick sticker-style outline plus a soft drop shadow behind a cut-out."""
    pad = width * 3
    a = im.getchannel("A")
    big = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0)
    big.paste(a, (pad, pad))
    ring = big.filter(ImageFilter.MaxFilter(2 * width + 1))
    out = Image.new("RGBA", big.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0))
    sh.putalpha(ring.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.75)))
    out.alpha_composite(sh, (10, 14))
    stroke = Image.new("RGBA", big.size, color + (255,))
    stroke.putalpha(ring)
    out.alpha_composite(stroke)
    out.alpha_composite(im, (pad, pad))
    return out


def burst_bg():
    """Radial rays from yellow-orange centre to deep red edges."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = 330, 360
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / 900
    ang = np.arctan2(yy - cy, xx - cx)
    rays = (np.sin(ang * 14) > 0).astype(np.float32)
    inner = np.array([255, 196, 0], np.float32)
    outer = np.array([200, 20, 30], np.float32)
    t = np.clip(r, 0, 1)[..., None] ** 0.8
    base = inner * (1 - t) + outer * t
    base = base * (1 - 0.13 * rays[..., None])
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")


def gold_text(text, size, stroke=12):
    f = ImageFont.truetype(BLACK, size)
    l, tp, r, b = f.getbbox(text)
    w, h = r + 2 * stroke + 20, b + 2 * stroke + 20
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((stroke + 10, stroke + 10), text, font=f, fill=255)
    y = np.linspace(0, 1, h)[:, None]
    stops = np.array([[255, 248, 180], [255, 214, 10], [235, 150, 0], [255, 214, 10]], np.float32)
    pos = [0, 0.4, 0.75, 1]
    grad = np.stack([np.interp(y[:, 0], pos, stops[:, c]) for c in range(3)], 1)
    fill = Image.fromarray(np.repeat(grad[:, None, :], w, 1).astype(np.uint8)).convert("RGBA")
    fill.putalpha(mask)
    st = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    st.putalpha(mask.filter(ImageFilter.MaxFilter(2 * stroke + 1)))
    out = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh.putalpha(st.getchannel("A").filter(ImageFilter.GaussianBlur(8)))
    out.alpha_composite(sh, (12, 14))
    out.alpha_composite(st, (0, 0))
    out.alpha_composite(fill, (0, 0))
    return out


def plain_text(text, size, fill, stroke=9):
    f = ImageFont.truetype(BLACK, size)
    l, tp, r, b = f.getbbox(text, stroke_width=stroke)
    im = Image.new("RGBA", (r + 20, b + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((10 + 6, 10 + 8), text, font=f, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(0, 0, 0))
    d.text((10, 10), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return im


def put(canvas, im, cx, cy, scale=1.0, rot=0.0):
    if scale != 1:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def main():
    canvas = burst_bg()

    # flying real bills (cut from the "cash in hands" photo) behind the person
    cash = punch(cutout("cash_hand", (230, 60, 520, 470)), sat=1.2)
    cash = cash.crop(cash.getchannel("A").getbbox())
    for x, y, s, r in ((120, 120, 0.55, 25), (60, 610, 0.45, -10)):
        put(canvas, outline(cash, 6), x, y, s, r)

    # the teen, big, outlined like a sticker
    teen = punch(cutout("teen_boy", (180, 20, 560, 620)), sat=1.25, con=1.12, bright=0.94)
    teen = teen.crop(teen.getchannel("A").getbbox())
    put(canvas, outline(teen, 11), 345, 410, 1.28)

    # headline on the right
    cx = 930
    put(canvas, gold_text("TOP 10", 200, 14), cx, 125, min(1.0, 640 / gold_text("TOP 10", 200, 14).width), -3)
    put(canvas, plain_text("FORMAS DE GANAR", 64, (255, 255, 255)), cx, 268, min(1.0, 600 / plain_text("FORMAS DE GANAR", 64, (255, 255, 255)).width))
    put(canvas, plain_text("DINERO", 130, (255, 255, 255), 11), cx, 365, 1.0, 0)

    # badge
    f = ImageFont.truetype(BLACK, 52)
    lab = "SIENDO ADOLESCENTE"
    w = f.getbbox(lab)[2]
    badge = Image.new("RGBA", (w + 70, 104), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.rounded_rectangle([8, 12, w + 64, 100], radius=16, fill=(0, 0, 0, 160))
    bd.rounded_rectangle([2, 4, w + 58, 92], radius=16, fill=(20, 20, 24), outline=(255, 214, 10), width=5)
    bd.text((30, 14), lab, font=f, fill=(255, 214, 10))
    put(canvas, badge, cx, 480, min(1.0, 620 / badge.width), 2)

    # mystery box: "#1 = ???" with a red arrow pointing at it
    box = Image.new("RGBA", (340, 150), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle([10, 14, 334, 146], radius=20, fill=(0, 0, 0, 150))
    bd.rounded_rectangle([0, 0, 324, 132], radius=20, fill=(255, 255, 255), outline=(0, 0, 0), width=6)
    fb = ImageFont.truetype(BLACK, 92)
    bd.text((24, 8), "#1 ???", font=fb, fill=(220, 20, 30))
    put(canvas, box, 1085, 620, 1.0, -4)
    ar = Image.new("RGBA", (220, 120), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ar)
    pts = [(10, 48), (140, 48), (140, 10), (210, 60), (140, 110), (140, 72), (10, 72)]
    ad.polygon([(x + 4, y + 6) for x, y in pts], fill=(0, 0, 0, 150))
    ad.polygon(pts, fill=(235, 30, 40), outline=(255, 255, 255))
    ad.line(pts + [pts[0]], fill=(255, 255, 255), width=6)
    put(canvas, ar, 815, 640, 0.9, -12)

    canvas.convert("RGB").save(os.path.join(ROOT, "exports", "miniatura.jpg"), quality=94)


if __name__ == "__main__":
    main()
