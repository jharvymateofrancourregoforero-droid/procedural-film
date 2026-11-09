"""Phone-payment thumbnail (v5): a teen celebrating next to a giant phone with a "payment received" notification.

Real CC0 photos (cut-outs with OpenCV GrabCut, no AI); the phone and notification are drawn.
usage: python3 tools/thumbnail_v5.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import thumbnail_v2 as V2
import thumbnail_v4 as V4

ROOT, BLACK = V2.ROOT, V2.BLACK
BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
W, H = 1280, 720


def cut_cheer():
    """GrabCut seeded with the bright sky as background and the orange jacket as foreground."""
    import cv2
    img = cv2.imread(V2.P + "cheer.jpg")
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = np.full((h, w), cv2.GC_BGD, np.uint8)
    m[10:640, 300:740] = cv2.GC_PR_FGD
    sky = ((hsv[..., 2] > 185) & (hsv[..., 1] < 40)).astype(np.uint8)
    sky = cv2.erode(sky, np.ones((7, 7), np.uint8))
    sky[200:310, 430:590] = 0  # keep the beanie
    m[sky > 0] = cv2.GC_BGD
    orange = ((hsv[..., 0] > 8) & (hsv[..., 0] < 28) & (hsv[..., 1] > 150) & (hsv[..., 2] > 120)).astype(np.uint8)
    m[(orange > 0) & (m != cv2.GC_BGD)] = cv2.GC_FGD
    m[230:330, 470:560] = cv2.GC_FGD  # face
    bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(img, m, None, bg, fg, 10, cv2.GC_INIT_WITH_MASK)
    mm = np.where((m == 1) | (m == 3), 255, 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(mm)
    mm = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
    mm = cv2.morphologyEx(mm, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    cnts, _ = cv2.findContours(mm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(mm)
    cv2.drawContours(filled, cnts, -1, 255, -1)
    alpha = cv2.GaussianBlur(cv2.erode(filled, np.ones((3, 3), np.uint8)), (5, 5), 0)
    im = Image.fromarray(np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), alpha]))
    return im.crop(im.getchannel("A").getbbox())


def background():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = 560, 330
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / 950
    ang = np.arctan2(yy - cy, xx - cx)
    rays = (np.sin(ang * 16) > 0).astype(np.float32)
    inner = np.array([255, 236, 60], np.float32)
    outer = np.array([20, 170, 90], np.float32)
    t = np.clip(r, 0, 1)[..., None] ** 0.9
    base = inner * (1 - t) + outer * t
    base *= 1 - 0.10 * rays[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")


def emoji(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    s = size / im.height
    return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)


def phone():
    pw, ph = 380, 760
    im = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([14, 20, pw + 14, ph + 20], radius=54, fill=(0, 0, 0, 120))
    d.rounded_rectangle([0, 0, pw, ph], radius=54, fill=(18, 18, 22), outline=(70, 70, 80), width=6)
    # screen: deep gradient
    sx0, sy0, sx1, sy1 = 18, 18, pw - 18, ph - 18
    sw, sh = sx1 - sx0, sy1 - sy0
    y = np.linspace(0, 1, sh)[:, None]
    grad = np.array([30, 40, 90], np.float32) * (1 - y) + np.array([70, 20, 110], np.float32) * y
    scr = Image.fromarray(np.repeat(grad[:, None, :], sw, 1).astype(np.uint8)).convert("RGBA")
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, sh - 1], radius=40, fill=255)
    im.paste(scr, (sx0, sy0), mask)
    d.rounded_rectangle([pw / 2 - 60, 30, pw / 2 + 60, 58], radius=14, fill=(10, 10, 12))  # notch
    f = ImageFont.truetype(BOLD, 64)
    d.text((pw / 2 - f.getbbox("9:41")[2] / 2, 120), "9:41", font=f, fill=(255, 255, 255, 230))
    # notification card
    cx0, cy0, cx1, cy1 = 34, 250, pw - 34, 440
    d.rounded_rectangle([cx0 + 4, cy0 + 8, cx1 + 4, cy1 + 8], radius=26, fill=(0, 0, 0, 110))
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=26, fill=(250, 250, 252))
    d.ellipse([cx0 + 20, cy0 + 22, cx0 + 92, cy0 + 94], fill=(30, 185, 90))
    fd = ImageFont.truetype(BLACK, 50)
    d.text((cx0 + 56 - fd.getbbox("$")[2] / 2, cy0 + 26), "$", font=fd, fill=(255, 255, 255))
    d.text((cx0 + 106, cy0 + 30), "¡Pago recibido!", font=ImageFont.truetype(BLACK, 26), fill=(20, 20, 24))
    d.text((cx0 + 108, cy0 + 66), "ahora", font=ImageFont.truetype(BOLD, 22), fill=(120, 120, 130))
    d.text((cx0 + 22, cy0 + 112), "+ $ $ $", font=ImageFont.truetype(BLACK, 52), fill=(30, 170, 80))
    im.alpha_composite(emoji("💰", 54), (int(cx1 - 80), int(cy0 + 112)))
    return im


def main():
    canvas = background()

    # phone, tilted, with bills bursting out of the screen
    cash = V2.punch(V2.cutout("cash_hand", (230, 60, 520, 470)), sat=1.25)
    cash = cash.crop(cash.getchannel("A").getbbox())
    for x, y, s, r in ((90, 600, 0.42, -15),):
        V2.put(canvas, V2.outline(cash, 6), x, y, s, r)
    V2.put(canvas, phone(), 285, 395, 0.92, 8)
    for x, y, s, r in ((470, 560, 0.4, -40), (420, 70, 0.4, 20)):
        V2.put(canvas, V2.outline(cash, 6), x, y, s, r)

    # the teen celebrating
    teen = cut_cheer()
    teen = teen.crop((0, 0, teen.width, int(teen.height * 0.8)))
    teen = V2.punch(teen, sat=1.25, con=1.12, bright=1.0).filter(ImageFilter.UnsharpMask(2, 80, 2))
    V2.put(canvas, V4.glow(V2.outline(teen, 10), (255, 255, 200), 24, 0.7), 735, 430, 1.25)

    # sparkle emojis
    for ch, x, y, s in (("✨", 560, 120, 70), ("🤑", 930, 140, 90), ("💸", 520, 640, 80)):
        V2.put(canvas, emoji(ch, s), x, y)

    # headline column on the right
    cx = 1105
    t10 = V2.gold_text("TOP 10", 120, 11)
    V2.put(canvas, t10, cx, 255, min(1.0, 330 / t10.width), -4)
    for i, (txt, size) in enumerate((("FORMAS DE", 54), ("GANAR", 82), ("DINERO", 82))):
        im = V2.plain_text(txt, size, (255, 255, 255), 9)
        V2.put(canvas, im, cx, 360 + i * 88, min(1.0, 320 / im.width), -4)
    f = ImageFont.truetype(BLACK, 40)
    lab = "ADOLESCENTE"
    w = f.getbbox(lab)[2]
    b = Image.new("RGBA", (w + 60, 86), (0, 0, 0, 0))
    bd = ImageDraw.Draw(b)
    bd.rounded_rectangle([6, 10, w + 56, 82], radius=14, fill=(0, 0, 0, 150))
    bd.rounded_rectangle([0, 2, w + 50, 74], radius=14, fill=(230, 35, 45), outline=(0, 0, 0), width=4)
    bd.text((25, 12), lab, font=f, fill=(255, 255, 255))
    V2.put(canvas, b, cx, 640, min(1.0, 330 / b.width), -4)

    canvas.convert("RGB").save(os.path.join(ROOT, "exports", "miniatura.jpg"), quality=94)


if __name__ == "__main__":
    main()
