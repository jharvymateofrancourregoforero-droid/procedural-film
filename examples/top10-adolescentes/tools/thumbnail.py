"""YouTube thumbnail: cut-out teen (OpenCV GrabCut, no AI) over a monochrome pile of bills, big "TOP 10"."""
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "photos") + "/"
W, H = 1280, 720
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
BI = "/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf"


def cutout(name, rect):
    img = cv2.imread(P + name + ".jpg")
    h, w = img.shape[:2]
    m = np.zeros((h, w), np.uint8)
    bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(img, m, rect, bg, fg, 8, cv2.GC_INIT_WITH_RECT)
    m = np.where((m == 1) | (m == 3), 255, 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    m = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    m = cv2.GaussianBlur(cv2.erode(m, np.ones((3, 3), np.uint8)), (5, 5), 0)
    return Image.fromarray(np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), m]))


def main():
    bg = Image.open(P + "bills.jpg").convert("RGB")
    s = max(W / bg.width, H / bg.height) * 1.1
    bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(1.5))
    a = np.asarray(bg).astype(np.float32)
    g = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = (g[..., None] * 0.75 + a * 0.25) * 0.5
    xx = np.linspace(0, 1, W)[None, :, None]
    a *= 0.55 + 0.45 * np.clip(xx / 0.5, 0, 1)
    canvas = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

    person = cutout("teen_boy", (180, 20, 560, 620))
    sc = 1.25
    person = person.resize((int(person.width * sc), int(person.height * sc)), Image.LANCZOS)
    px, py = -170, -20
    halo = Image.new("RGBA", person.size, (0, 0, 0, 0))
    halo.putalpha(person.getchannel("A").filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.9)))
    canvas.alpha_composite(halo, (px + 12, py + 10))
    canvas.alpha_composite(person, (px, py))

    d = ImageDraw.Draw(canvas)

    def text(cx, y, s, path, size, fill, stroke=10, maxw=620):
        f = ImageFont.truetype(path, size)
        while f.getbbox(s, stroke_width=stroke)[2] > maxw:
            size -= 4
            f = ImageFont.truetype(path, size)
        w = f.getbbox(s, stroke_width=stroke)[2]
        d.text((cx - w / 2 + 7, y + 9), s, font=f, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(0, 0, 0))
        d.text((cx - w / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))

    cx = 945
    text(cx, 30, "TOP 10", BLACK, 190, (255, 214, 10), stroke=12)
    text(cx, 255, "FORMAS DE GANAR", BLACK, 80, (255, 255, 255))
    text(cx, 355, "DINERO", BLACK, 130, (255, 255, 255))
    f = ImageFont.truetype(BLACK, 66)
    label = "SIENDO ADOLESCENTE"
    w = f.getbbox(label)[2]
    box = Image.new("RGBA", (w + 70, 120), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle([6, 10, w + 60, 108], radius=16, fill=(255, 59, 48))
    bd.text((32, 18), label, font=f, fill=(255, 255, 255))
    box = box.rotate(-3, expand=True, resample=Image.BICUBIC)
    sc2 = min(1.0, 640 / box.width)
    box = box.resize((int(box.width * sc2), int(box.height * sc2)), Image.LANCZOS)
    canvas.alpha_composite(box, (int(cx - box.width / 2), 530))
    canvas.convert("RGB").save(os.path.join(ROOT, "exports", "miniatura.jpg"), quality=93)


if __name__ == "__main__":
    main()
