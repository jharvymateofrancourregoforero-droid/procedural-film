"""YouTube thumbnails in the style of a cut-out person over a monochrome money background.

The person is cut out with OpenCV GrabCut (classic graph-cut segmentation, no neural network).
usage: python3 tools/thumbnail.py
"""
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'photos') + '/'
W, H = 1280, 720
BLACK = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
BI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'

def cutout(name, rect, iters=8):
    img = cv2.imread(P + name + '.jpg'); h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8); bg = np.zeros((1, 65)); fg = np.zeros((1, 65))
    cv2.grabCut(img, mask, rect, bg, fg, iters, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    m = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    m = cv2.erode(m, np.ones((3, 3), np.uint8))
    m = cv2.GaussianBlur(m, (5, 5), 0)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(np.dstack([rgb, m]))

def mono(im, keep=0.18, contrast=1.25, bright=1.0):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    g = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = g[..., None] * (1 - keep) + a * keep
    a = (a - 128) * contrast + 128
    return np.clip(a * bright, 0, 255)

def build(line1, line2, label, out, l2size=150):
    # background: pile of dollar bills, near-monochrome, darker on the left and at the edges
    bgimg = Image.open(P + 'savings_bills.jpg').convert('RGB')
    s = max(W / bgimg.width, H / bgimg.height) * 1.15
    bgimg = bgimg.resize((int(bgimg.width * s), int(bgimg.height * s)), Image.LANCZOS)
    bgimg = bgimg.crop((bgimg.width - W, 0, bgimg.width, H)).filter(ImageFilter.GaussianBlur(1.2))
    a = mono(bgimg, keep=0.22, contrast=1.15, bright=0.62)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = np.clip(1 - 0.55 * (((xx - W * 0.62) / (W * 0.7)) ** 2 + ((yy - H * 0.55) / (H * 0.8)) ** 2), 0.25, 1)
    a = a * vig[..., None]
    a *= (0.45 + 0.55 * np.clip(xx / (W * 0.45), 0, 1))[..., None]  # dark band behind the person
    canvas = Image.fromarray(a.astype(np.uint8)).convert('RGBA')

    # person: cut out, near-monochrome, big on the left, cropped at the chest
    person = cutout('biz_stress', (225, 25, 728, 610))
    al = np.asarray(person).copy(); al[520:, :, 3] = 0; person = Image.fromarray(al)  # drop the desk
    sc = 1.4
    person = person.resize((int(person.width * sc), int(person.height * sc)), Image.LANCZOS)
    rgb = mono(person, keep=0.3, contrast=1.3, bright=1.05)
    person = Image.fromarray(np.dstack([rgb.astype(np.uint8), np.asarray(person)[..., 3]]))
    px, py = -470, -12
    # dark halo so the figure pops off the background
    alpha = person.getchannel('A')
    halo = Image.new('RGBA', person.size, (0, 0, 0, 0))
    halo.putalpha(alpha.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.85)))
    canvas.alpha_composite(halo, (px + 14, py + 10))
    canvas.alpha_composite(person, (px, py))

    d = ImageDraw.Draw(canvas)
    def text(cx, y, s, path, size, fill, stroke=9, maxw=600):
        f = ImageFont.truetype(path, size)
        while f.getbbox(s, stroke_width=stroke)[2] > maxw:
            size -= 4; f = ImageFont.truetype(path, size)
        w = f.getbbox(s, stroke_width=stroke)[2]
        # hard drop shadow, then the stroked text
        d.text((cx - w / 2 + 7, y + 9), s, font=f, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(0, 0, 0))
        d.text((cx - w / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
        return f.getbbox(s, stroke_width=stroke)[3]
    cx = 940
    h1 = text(cx, 40, line1, BLACK, 118, (255, 255, 255))
    text(cx, 40 + h1 + 4, line2, BLACK, l2size, (255, 214, 10))
    f = ImageFont.truetype(BI, 44)
    w = f.getbbox(label)[2]
    d.text((290 - w / 2 + 3, 625 + 4), label, font=f, fill=(0, 0, 0), stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((290 - w / 2, 625), label, font=f, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0, 0, 0))
    canvas.convert('RGB').save(out, quality=93)

O = os.path.join(ROOT, 'exports') + '/'
build('EL SECRETO', 'DE LOS RICOS', 'Trabaja 12 horas al día', O + 'miniatura_a.jpg')
build('TRABAJAR MÁS', 'NO TE HACE RICO', 'Trabaja 12 horas al día', O + 'miniatura_b.jpg')
build('ASÍ PIENSAN', 'LOS RICOS', 'Trabaja 12 horas al día', O + 'miniatura_c.jpg')
print('ok')
