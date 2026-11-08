"""Render the video frames of "Gastos hormiga" and encode them with ffmpeg.

usage: python3 render.py [--preview] [--only START END]
Frames are drawn with Pillow + numpy from the real photos in photos/.
Four workers each encode a slice; the slices are joined losslessly at the end.
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import timeline as T

W, H, FPS = T.W, T.H, T.FPS
ROOT = T.ROOT
FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
OUT_DIR = os.path.join(ROOT, "build")

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def ease_out_back(x, s=1.9):
    x = min(max(x, 0.0), 1.0) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def ease_in_out(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def smooth_noise(t, seed, freqs=(0.37, 0.71, 1.33)):
    """Slow handheld-camera wobble in [-1, 1]."""
    r = np.random.RandomState(seed)
    ph = r.rand(len(freqs)) * 6.28
    return sum(math.sin(t * f * 6.283 + p) / (i + 1) for i, (f, p) in enumerate(zip(freqs, ph))) / 1.83


# ---------- photo layers ----------

_img_cache = {}


def photo(name):
    if name not in _img_cache:
        im = Image.open(os.path.join(ROOT, "photos", name + ".jpg")).convert("RGB")
        _img_cache[name] = im
    return _img_cache[name]


def grade(arr):
    """Punchy warm grade: S-curve contrast, a touch of warmth and saturation."""
    x = arr.astype(np.float32) / 255.0
    x = x + 0.12 * (x - 0.5) * (1 - (2 * x - 1) ** 2) * 2  # gentle S-curve
    lum = x.mean(axis=2, keepdims=True)
    x = lum + (x - lum) * 1.15
    x[..., 0] *= 1.03
    x[..., 2] *= 0.96
    return np.clip(x * 255, 0, 255).astype(np.uint8)


def affine_cover(im, zoom, pan, rot_deg, offset):
    """Cover-fit im into W x H, zoomed, panned (in units of the spare margin), rotated."""
    iw, ih = im.size
    s = max(W / iw, H / ih) * zoom
    # spare margin at this scale, in source pixels
    mx = max(0.0, (iw * s - W) / 2) / s
    my = max(0.0, (ih * s - H) / 2) / s
    cx = iw / 2 + pan[0] * mx
    cy = ih / 2 + pan[1] * my
    th = math.radians(rot_deg)
    c, si = math.cos(th) / s, math.sin(th) / s
    ox, oy = W / 2 + offset[0], H / 2 + offset[1]
    # input = R(-th)/s * (out - o) + center
    a, b = c, si
    d, e = -si, c
    return im.transform((W, H), Image.AFFINE, (a, b, cx - a * ox - b * oy, d, e, cy - d * ox - e * oy),
                        resample=Image.BILINEAR)


_bg_cache = {}


def blurred_bg(name):
    if name not in _bg_cache:
        im = photo(name)
        small = im.copy()
        small.thumbnail((360, 360))
        small = small.filter(ImageFilter.GaussianBlur(5))
        arr = np.asarray(small).astype(np.float32) * 0.62
        _bg_cache[name] = Image.fromarray(arr.astype(np.uint8))
    return _bg_cache[name]


_card_cache = {}


def card_image(name):
    """Photo with a white print border, plus a soft shadow, as RGBA."""
    if name not in _card_cache:
        im = photo(name)
        maxw, maxh = 900, 1020
        s = min(maxw / im.width, maxh / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        b = 18
        card = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), (250, 248, 242, 255))
        card.paste(im, (b, b))
        pad = 60
        sh = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
        mask = Image.new("L", sh.size, 0)
        ImageDraw.Draw(mask).rectangle([pad, pad + 14, pad + card.width, pad + card.height + 14], fill=150)
        mask = mask.filter(ImageFilter.GaussianBlur(22))
        sh.putalpha(mask)
        sh.alpha_composite(card, (pad, pad))
        _card_cache[name] = sh
    return _card_cache[name]


def draw_shot(t):
    idx, start, end = T.shot_at(t)
    _, name, mode, opt = T.SHOTS[idx]
    lt, dur = t - start, end - start
    p = lt / dur
    z0, z1 = opt.get("z", (1.0, 1.1))
    zoom = z0 + (z1 - z0) * ease_in_out(p)
    zoom *= 1 + 0.10 * math.exp(-lt * 14)  # punch-in on every cut
    hand = (smooth_noise(t, idx) * 7, smooth_noise(t + 9, idx + 50) * 9)
    hrot = smooth_noise(t + 3, idx + 99) * 0.35
    if mode == "full":
        pan0, pan1 = opt.get("pan", (0, 0)), (0, 0)
        pan = (pan0[0] * (1 - p) + pan1[0] * p, pan0[1] * (1 - p) + pan1[1] * p)
        frame = affine_cover(photo(name), zoom, pan, hrot, hand)
    else:
        frame = affine_cover(blurred_bg(name), 1.15 + 0.1 * p, (0, 0), 0, (0, 0))
        card = card_image(name)
        r0, r1 = opt.get("rot", (-2, 0))
        rot = r0 + (r1 - r0) * ease_in_out(p) + hrot
        enter = ease_out_back(lt / 0.28)
        cz = (0.92 + 0.08 * enter) * (1 + (zoom - 1) * 0.35)
        c2 = card.resize((max(1, int(card.width * cz)), max(1, int(card.height * cz))), Image.BILINEAR)
        c2 = c2.rotate(rot, resample=Image.BILINEAR, expand=True)
        cy = 820 + (1 - enter) * 260 + hand[1]
        cx = W / 2 + hand[0]
        frame = frame.convert("RGBA")
        frame.alpha_composite(c2, (int(cx - c2.width / 2), int(cy - c2.height / 2)))
        frame = frame.convert("RGB")
    return frame


# ---------- text and graphics ----------

def text_block(text, size, fill, stroke=10, stroke_fill=(0, 0, 0), path=FONT_BLACK, spacing=0.92, shadow=True):
    """Render multi-line centred text into a tight RGBA image."""
    f = font(path, size)
    lines = text.split("\n")
    widths = [f.getbbox(l, stroke_width=stroke)[2] for l in lines]
    lh = int(size * spacing) + stroke
    w = max(widths) + 2 * stroke + 20
    h = lh * len(lines) + 2 * stroke + int(size * 0.3)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = (w - widths[i]) / 2
        d.text((x, stroke + i * lh), l, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sh.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 0.6))
        base = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
        base.alpha_composite(sh, (12, 14))
        base.alpha_composite(im, (4, 4))
        im = base
    return im


def boxed(text, size, bg, fg, pad=(34, 18), path=FONT_BLACK):
    f = font(path, size)
    lines = text.split("\n")
    lh = int(size * 1.02)
    widths = [f.getbbox(l)[2] for l in lines]
    w = max(widths) + 2 * pad[0]
    h = lh * len(lines) + 2 * pad[1] + int(size * 0.12)
    im = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 14, w + 10, h + 14], radius=18, fill=(0, 0, 0, 140))
    d.rounded_rectangle([4, 4, w + 4, h + 4], radius=18, fill=bg + (255,))
    for i, l in enumerate(lines):
        d.text((4 + (w - widths[i]) / 2, 4 + pad[1] + i * lh - size * 0.06), l, font=f, fill=fg)
    return im


def paste_center(frame, im, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy()
        im.putalpha(a)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


_tcache = {}


def cached(key, fn):
    if key not in _tcache:
        _tcache[key] = fn()
    return _tcache[key]


def pop_scale(lt, dur=0.22):
    return max(0.0, ease_out_back(lt / dur, 2.4))


def draw_gfx(frame, t):
    for gi, g in enumerate(T.GFX):
        t1 = g.get("hold", g["t1"])
        if not (g["t0"] <= t < t1):
            continue
        lt = t - g["t0"]
        out = max(0.0, min(1.0, (t1 - t) / 0.12))  # quick fade on exit
        k = g["kind"]
        wob = math.sin(t * 7 + gi) * 1.2
        if k == "big":
            im = cached(("big", gi), lambda: text_block(g["text"], g["size"], g["color"], stroke=12))
            paste_center(frame, im, W / 2, g["y"], pop_scale(lt) * (1 + 0.03 * math.sin(lt * 9)), wob, out)
        elif k == "title":
            im = cached(("title", gi), lambda: boxed(g["text"], g["size"], g["color"], T.INK))
            paste_center(frame, im, W / 2, g["y"], pop_scale(lt), g.get("rot", 0) + wob * 0.5, out)
        elif k == "sticker":
            im = cached(("st", gi), lambda: boxed(g["text"], 76, g["color"], g.get("fg", T.INK), pad=(26, 12)))
            paste_center(frame, im, W / 2, g["y"], pop_scale(lt, 0.18), g.get("rot", 0) + wob, out)
        elif k == "stamp":
            def mk():
                f = font(FONT_BLACK, 150)
                w = f.getbbox(g["text"])[2] + 80
                im = Image.new("RGBA", (w, 230), (0, 0, 0, 0))
                d = ImageDraw.Draw(im)
                d.rounded_rectangle([8, 8, w - 8, 222], radius=20, outline=g["color"] + (255,), width=14)
                d.text((40, 30), g["text"], font=f, fill=g["color"] + (255,))
                return im
            im = cached(("stamp", gi), mk)
            sc = 1 + 1.4 * math.exp(-lt * 22)
            paste_center(frame, im, W / 2, g["y"], sc * 0.95, g["rot"], min(1.0, lt / 0.05) * out)
        elif k == "counter":
            prog = ease_in_out((t - g["t0"]) / (g["t1"] - g["t0"]))
            val = int(round(g["a"] + (g["b"] - g["a"]) * prog))
            txt = g["fmt"].format(val).replace(",", ".")
            done = t >= g["t1"]
            sc = pop_scale(lt) * (1 + (0.12 * math.exp(-(t - g["t1"]) * 10) if done else 0))
            im = text_block(txt, g["size"], g["color"], stroke=12)
            paste_center(frame, im, W / 2, g["y"], sc, 0, out)
            lab = cached(("lab", gi), lambda: boxed(g["label"], 64, T.WHT, T.INK, pad=(22, 10)))
            paste_center(frame, lab, W / 2, g["y"] + g["size"] * 0.82, pop_scale(lt - 0.1), -2, out)
        elif k == "chart":
            prog = ease_in_out((t - g["t0"]) / (g["t1"] - g["t0"]))
            draw_chart(frame, prog, g["y"], out)
        elif k == "note":
            im = cached(("note", gi), lambda: note_img(g["text"]))
            paste_center(frame, im, W / 2, 1640, 1.0, 0, min(1.0, lt / 0.2) * out)
        elif k == "badge":
            im = cached(("badge", gi), lambda: badge_img(g["n"], g["text"]))
            paste_center(frame, im, W / 2, g["y"], pop_scale(lt), -2 + wob * 0.6, out)
        elif k == "end":
            a = min(1.0, lt / 0.25)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, int(150 * a)))
            frame.alpha_composite(ov)
            im = cached(("end", gi), lambda: text_block(g["text"], 120, T.YEL, stroke=10))
            paste_center(frame, im, W / 2, 820, pop_scale(lt), -2, a)
            sub = cached(("endsub", gi), lambda: boxed(g["sub"], 56, T.WHT, T.INK, pad=(24, 10), path=FONT_BOLD))
            paste_center(frame, sub, W / 2, 1060, pop_scale(lt - 0.15), 2, a)


def note_img(text):
    f = font(FONT_BOLD, 34)
    lines = text.split("\n")
    w = max(f.getbbox(l)[2] for l in lines) + 44
    h = 46 * len(lines) + 22
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, h], radius=14, fill=(0, 0, 0, 165))
    for i, l in enumerate(lines):
        d.text((22, 10 + i * 46), l, font=f, fill=(255, 255, 255, 235))
    return im


def badge_img(n, text):
    f = font(FONT_BLACK, 74)
    lines = text.split("\n")
    tw = max(f.getbbox(l)[2] for l in lines)
    r = 86
    w = 2 * r + 36 + tw + 50
    h = max(2 * r, len(lines) * 80 + 40) + 20
    im = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([r, 18 + 10, w + 10, h + 10], radius=26, fill=(0, 0, 0, 130))
    d.rounded_rectangle([r, 18, w, h], radius=26, fill=(255, 255, 255, 255))
    d.ellipse([4, h / 2 - r + 9, 4 + 2 * r, h / 2 + r + 9], fill=(0, 0, 0, 130))
    d.ellipse([0, h / 2 - r, 2 * r, h / 2 + r], fill=T.YEL + (255,), outline=T.INK + (255,), width=8)
    fn = font(FONT_BLACK, 120)
    nb = fn.getbbox(n)
    d.text((r - (nb[2] - nb[0]) / 2 - nb[0], h / 2 - (nb[3] - nb[1]) / 2 - nb[1]), n, font=fn, fill=T.INK)
    y0 = h / 2 - len(lines) * 80 / 2 + 6
    for i, l in enumerate(lines):
        d.text((2 * r + 36, y0 + i * 80), l, font=f, fill=T.INK)
    return im


def draw_chart(frame, prog, y, alpha):
    """Growth curve of US$730 a year at 8%, drawn left to right."""
    x0, x1, h = 120, 960, 260
    vals = [730 * ((1.08 ** (k + 1) - 1) / 0.08) for k in range(10)]
    top = vals[-1]
    pts = [(x0 + (x1 - x0) * k / 9, y + h / 2 - h * v / top) for k, v in enumerate(vals)]
    n = prog * 9
    vis = [pts[k] for k in range(int(n) + 1)]
    if int(n) < 9:
        a, b = pts[int(n)], pts[int(n) + 1]
        f = n - int(n)
        vis.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle([x0 - 50, y - h / 2 - 60, x1 + 50, y + h / 2 + 40], radius=24, fill=(0, 0, 0, int(160 * alpha)))
    for k in range(10):
        bx = x0 + (x1 - x0) * k / 9
        d.line([bx, y + h / 2, bx, y + h / 2 + 10], fill=(255, 255, 255, int(120 * alpha)), width=3)
    if len(vis) > 1:
        d.line(vis, fill=(0, 0, 0, int(200 * alpha)), width=22, joint="curve")
        d.line(vis, fill=T.GRN + (int(255 * alpha),), width=14, joint="curve")
    ex, ey = vis[-1]
    d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=(255, 255, 255, int(255 * alpha)))
    frame.alpha_composite(ov)


def draw_captions(frame, t, chunks):
    for c in chunks:
        if not (c["t0"] <= t < c["t1"]):
            continue
        lt = t - c["t0"]
        words = c["words"]
        size = 84
        f = font(FONT_BLACK, size)
        texts = [w["text"].upper() for w in words]
        space = size * 0.28
        ws = [f.getbbox(x, stroke_width=10)[2] for x in texts]
        # wrap into lines no wider than 940 px
        lines, cur, cw = [], [], 0
        for i, wd in enumerate(ws):
            if cur and cw + space + wd > 940:
                lines.append(cur)
                cur, cw = [], 0
            cw += (space if cur else 0) + wd
            cur.append(i)
        lines.append(cur)
        lh = size * 1.08
        layer = Image.new("RGBA", (W, int(lh * len(lines) + 60)), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for li, line in enumerate(lines):
            lw = sum(ws[i] for i in line) + space * (len(line) - 1)
            x = (W - lw) / 2
            for i in line:
                active = words[i]["start"] - 0.03 <= t
                speaking = words[i]["start"] - 0.03 <= t < words[i]["end"] + 0.08
                col = T.YEL if speaking else (T.WHT if active else (235, 235, 235))
                if "US$" in texts[i] or "%" in texts[i]:
                    col = T.GRN if active else col
                d.text((x, 10 + li * lh), texts[i], font=f, fill=col + (255 if active else 150,),
                       stroke_width=10, stroke_fill=(0, 0, 0, 255 if active else 150))
                x += ws[i] + space
        sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        sh.putalpha(layer.getchannel("A").filter(ImageFilter.GaussianBlur(8)).point(lambda v: v * 0.55))
        sc = 0.86 + 0.14 * ease_out_back(lt / 0.16, 2.0)
        cy = 1400
        paste_center(frame, sh, W / 2 + 4, cy + 8, sc)
        paste_center(frame, layer, W / 2, cy, sc)


# ---------- finishing ----------

_vig = None
_grain = None


def finishing(arr, t, fi):
    global _vig, _grain
    if _vig is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
        _vig = np.clip(1 - 0.38 * r ** 2.2, 0.45, 1)[..., None].astype(np.float32)
        rs = np.random.RandomState(7)
        _grain = [rs.normal(0, 1, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
    x = arr.astype(np.float32) * _vig
    g = _grain[fi % 6]
    g = np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None]
    x += g * 6.5
    # flashes on marked cuts and hits
    fl = 0.0
    for s in T.SHOTS:
        if s[3].get("flash") and 0 <= t - s[0] < 0.2:
            fl = max(fl, 1 - (t - s[0]) / 0.2)
    if fl:
        x = x + (255 - x) * (0.75 * fl)
    x = np.clip(x, 0, 255).astype(np.uint8)
    # chromatic split + shake on hits
    for h in T.HITS:
        if 0 <= t - h < 0.25:
            k = 1 - (t - h) / 0.25
            sft = int(10 * k)
            if sft:
                x[..., 0] = np.roll(x[..., 0], sft, axis=1)
                x[..., 2] = np.roll(x[..., 2], -sft, axis=1)
    return x


def whip(arr, t):
    """Horizontal motion-blur slide across cuts marked whip."""
    for i, s in enumerate(T.SHOTS):
        if not s[3].get("whip"):
            continue
        d = t - s[0]
        if -0.1 <= d < 0.1:
            k = 1 - abs(d) / 0.1
            shift = int((1 if d < 0 else -1) * 260 * k)
            taps = 6
            acc = np.zeros_like(arr, dtype=np.float32)
            for j in range(taps):
                acc += np.roll(arr, int(shift * (j / (taps - 1)) * 0.9), axis=1)
            return (acc / taps).astype(np.uint8)
    return arr


def camera_shake(img, t):
    amp = 0.0
    for h in T.HITS:
        if 0 <= t - h < 0.35:
            amp = max(amp, 22 * (1 - (t - h) / 0.35) ** 2)
    if amp < 0.5:
        return img
    dx = math.sin(t * 91) * amp
    dy = math.cos(t * 77) * amp
    k = 1 / 1.06  # zoom in a little so the shaken frame never shows its edges
    return img.transform((W, H), Image.AFFINE, (k, 0, (W - W * k) / 2 + dx, 0, k, (H - H * k) / 2 + dy),
                         Image.BILINEAR)


def progress_bar(frame, t):
    d = ImageDraw.Draw(frame)
    d.rectangle([0, 0, W, 10], fill=(0, 0, 0, 90))
    d.rectangle([0, 0, int(W * min(1, t / T.END)), 10], fill=T.YEL + (255,))


def render_frame(fi, chunks):
    t = fi / FPS
    base = draw_shot(t)
    base = Image.fromarray(grade(np.asarray(base)))
    base = camera_shake(base, t)
    base = Image.fromarray(whip(np.asarray(base), t))  # blur the photo only, keep text sharp
    frame = base.convert("RGBA")
    draw_gfx(frame, t)
    draw_captions(frame, t, chunks)
    progress_bar(frame, t)
    return finishing(np.asarray(frame.convert("RGB")), t, fi)


def render_range(args):
    a, b, path = args
    chunks = T.caption_chunks()
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(render_frame(fi, chunks).tobytes())
    p.stdin.close()
    p.wait()
    return path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total = int(round(T.END * FPS))
    a, b = 0, total
    if "--only" in sys.argv:
        i = sys.argv.index("--only")
        a, b = int(float(sys.argv[i + 1]) * FPS), int(float(sys.argv[i + 2]) * FPS)
    if "--frames" in sys.argv:
        chunks = T.caption_chunks()
        for s in sys.argv[sys.argv.index("--frames") + 1:]:
            Image.fromarray(render_frame(int(float(s) * FPS), chunks)).save(os.path.join(OUT_DIR, f"frame_{s}.jpg"), quality=90)
        return
    n = 4
    step = math.ceil((b - a) / n)
    jobs = [(a + k * step, min(b, a + (k + 1) * step), os.path.join(OUT_DIR, f"part{k}.mp4")) for k in range(n)]
    with Pool(n) as pool:
        parts = pool.map(render_range, jobs)
    lst = os.path.join(OUT_DIR, "parts.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(OUT_DIR, "video.mp4")], check=True)
    print("video ->", os.path.join(OUT_DIR, "video.mp4"))


if __name__ == "__main__":
    main()
