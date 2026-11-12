"""Render "10 formas de lavar dinero" (1920x1080, 30 fps) and encode it with ffmpeg.

usage:
  python3 render.py                 full render into build/video.mp4
  python3 render.py --frames 12 95  save single frames to build/ for checking
  python3 render.py --only 0 60     render a time range
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
OUT_DIR = os.path.join(ROOT, "build")
FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FONT_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

_fonts = {}


def font(path, size):
    if (path, size) not in _fonts:
        _fonts[(path, size)] = ImageFont.truetype(path, size)
    return _fonts[(path, size)]


def clamp01(x):
    return min(max(x, 0.0), 1.0)


def ease_out_back(x, s=1.9):
    x = clamp01(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def ease(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def wobble(t, seed, freqs=(0.31, 0.67, 1.21)):
    r = np.random.RandomState(seed)
    ph = r.rand(len(freqs)) * 6.283
    return sum(math.sin(t * f * 6.283 + p) / (i + 1) for i, (f, p) in enumerate(zip(freqs, ph))) / 1.83


# ---------------------------------------------------------------- photos

_photo, _big, _bg, _card = {}, {}, {}, {}


def photo(name):
    if name not in _photo:
        _photo[name] = Image.open(os.path.join(ROOT, "photos", name + ".jpg")).convert("RGB")
    return _photo[name]


def big_photo(name):
    """Photo upscaled once to cover the frame with room to move, sharpened if it was small."""
    if name not in _big:
        im = photo(name)
        s = max(W * 1.18 / im.width, H * 1.18 / im.height)
        if s > 1:
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
        _big[name] = im
    return _big[name]


def blurred_bg(name):
    if name not in _bg:
        small = photo(name).copy()
        small.thumbnail((480, 480))
        small = small.filter(ImageFilter.GaussianBlur(7))
        _bg[name] = Image.fromarray((np.asarray(small).astype(np.float32) * 0.55).astype(np.uint8))
    return _bg[name]


def card_image(name, maxw, maxh):
    key = (name, maxw, maxh)
    if key not in _card:
        im = photo(name)
        s = min(maxw / im.width, maxh / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        b = 14
        card = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), (250, 248, 242, 255))
        card.paste(im, (b, b))
        pad = 50
        sh = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
        mask = Image.new("L", sh.size, 0)
        ImageDraw.Draw(mask).rectangle([pad, pad + 12, pad + card.width, pad + card.height + 12], fill=150)
        sh.putalpha(mask.filter(ImageFilter.GaussianBlur(20)))
        sh.alpha_composite(card, (pad, pad))
        _card[key] = sh
    return _card[key]


def affine_cover(im, zoom, pan, rot_deg, offset):
    iw, ih = im.size
    s = max(W / iw, H / ih) * zoom
    mx = max(0.0, (iw * s - W) / 2) / s
    my = max(0.0, (ih * s - H) / 2) / s
    cx, cy = iw / 2 + pan[0] * mx, ih / 2 + pan[1] * my
    th = math.radians(rot_deg)
    c, si = math.cos(th) / s, math.sin(th) / s
    ox, oy = W / 2 + offset[0], H / 2 + offset[1]
    return im.transform((W, H), Image.AFFINE, (c, si, cx - c * ox - si * oy, -si, c, cy + si * ox - c * oy),
                        resample=Image.BILINEAR)


PANS = [(-0.6, 0.0), (0.6, 0.0), (0.0, -0.5), (0.0, 0.5), (-0.5, -0.4), (0.5, 0.4)]


def paste_card(frame, card, cx, cy, scale, rot):
    c2 = card.resize((max(1, int(card.width * scale)), max(1, int(card.height * scale))), Image.BILINEAR)
    c2 = c2.rotate(rot, resample=Image.BILINEAR, expand=True)
    frame.alpha_composite(c2, (int(cx - c2.width / 2), int(cy - c2.height / 2)))


def draw_shot(t):
    idx, start, end = T.shot_at(t)
    _, name, mode, opt = T.SHOTS[idx]
    lt, dur = t - start, max(0.5, end - start)
    p = clamp01(lt / dur)
    zin = idx % 2 == 0
    z0, z1 = opt.get("z", (1.0, 1.12) if zin else (1.12, 1.0))
    zoom = (z0 + (z1 - z0) * ease(p)) * (1 + 0.06 * math.exp(-lt * 12))
    hand = (wobble(t, idx) * 6, wobble(t + 7, idx + 40) * 5)
    hrot = wobble(t + 3, idx + 90) * 0.25
    if mode == "full":
        pan0 = PANS[idx % len(PANS)]
        pan = (pan0[0] * (1 - 2 * p), pan0[1] * (1 - 2 * p))
        return affine_cover(big_photo(name), zoom, pan, hrot, hand)
    frame = affine_cover(blurred_bg(name), 1.12 + 0.08 * p, (0, 0), 0, (0, 0)).convert("RGBA")
    enter = ease_out_back(lt / 0.3)
    drift = 1 + (zoom - 1) * 0.4
    if mode == "card":
        card = card_image(name, 1180, 760)
        paste_card(frame, card, W / 2 + hand[0], 560 + (1 - enter) * 200 + hand[1],
                   (0.92 + 0.08 * enter) * drift, (-1.5 if idx % 2 else 1.5) * (1 - p * 0.5) + hrot)
    elif mode in ("left", "right"):
        card = card_image(name, 980, 760)
        sx = 560 if mode == "left" else W - 560
        dx = (-1 if mode == "left" else 1) * (1 - enter) * 420
        paste_card(frame, card, sx + dx + hand[0], 500 + hand[1], (0.94 + 0.06 * enter) * drift,
                   (2 if mode == "left" else -2) + hrot)
    elif mode == "split":
        for k, nm in enumerate((name, opt["img2"])):
            card = card_image(nm, 820, 600)
            e2 = ease_out_back((lt - 0.12 * k) / 0.3)
            sx = 500 if k == 0 else W - 500
            paste_card(frame, card, sx + hand[0], 520 + (1 - e2) * 300 + hand[1], (0.93 + 0.07 * e2) * drift,
                       (2.5 if k == 0 else -2.5) + hrot)
    return frame.convert("RGB")


# ---------------------------------------------------------------- graphics helpers

def text_img(text, size, fill, stroke=8, path=FONT_BLACK, spacing=1.0, shadow=True, align="center"):
    f = font(path, size)
    lines = text.split("\n")
    widths = [f.getbbox(l, stroke_width=stroke)[2] for l in lines]
    lh = int(size * spacing) + stroke
    w, h = max(widths) + 2 * stroke + 16, lh * len(lines) + 2 * stroke + int(size * 0.3)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = (w - widths[i]) / 2 if align == "center" else stroke
        d.text((x, stroke + i * lh), l, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    if not shadow:
        return im
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(9)).point(lambda v: v * 0.6))
    out = Image.new("RGBA", (w + 14, h + 14), (0, 0, 0, 0))
    out.alpha_composite(sh, (10, 12))
    out.alpha_composite(im, (2, 2))
    return out


def boxed(text, size, bg, fg=T.INK, pad=(30, 14), path=FONT_BLACK, radius=16):
    f = font(path, size)
    lines = text.split("\n")
    lh = int(size * 1.05)
    widths = [f.getbbox(l)[2] for l in lines]
    w, h = max(widths) + 2 * pad[0], lh * len(lines) + 2 * pad[1] + int(size * 0.1)
    im = Image.new("RGBA", (w + 22, h + 22), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 13, w + 10, h + 13], radius=radius, fill=(0, 0, 0, 130))
    d.rounded_rectangle([4, 4, w + 4, h + 4], radius=radius, fill=bg + (255,))
    for i, l in enumerate(lines):
        d.text((4 + (w - widths[i]) / 2, 4 + pad[1] + i * lh - size * 0.06), l, font=f, fill=fg)
    return im


def paste(frame, im, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.01:
        return
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1.0:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


_cache = {}


def cached(key, fn):
    if key not in _cache:
        _cache[key] = fn()
    return _cache[key]


def pop(lt, dur=0.22):
    return max(0.0, ease_out_back(lt / dur, 2.3))


def side_x(t):
    """Free side of the frame for text, given the shot on screen."""
    mode = T.SHOTS[T.shot_at(t)[0]][2]
    return {"left": 1440, "right": 480}.get(mode, W / 2)


def money(v):
    return f"{v:,}".replace(",", ".")


# ---------------------------------------------------------------- graphics

def draw_gfx(frame, t):
    for gi, g in enumerate(T.GFX):
        if not (g["t0"] <= t < g["t1"]):
            continue
        lt = t - g["t0"]
        out = clamp01((g["t1"] - t) / 0.15)
        wob = math.sin(t * 6 + gi) * 1.0
        k = g["kind"]
        if k == "big":
            im = cached(("big", gi), lambda: text_img(g["text"], g.get("size", 150), g["color"], stroke=10))
            paste(frame, im, side_x(g["t0"]), g.get("y", 430), pop(lt) * (1 + 0.025 * math.sin(lt * 8)), wob, out)
        elif k == "title":
            im = cached(("title", gi), lambda: boxed(g["text"], g.get("size", 104), g["color"], g.get("fg", T.INK)))
            paste(frame, im, W / 2, g.get("y", 430), pop(lt), -2 + wob * 0.5, out)
        elif k == "sticker":
            im = cached(("st", gi), lambda: boxed(g["text"], 58, g["color"], g.get("fg", T.INK), pad=(24, 10)))
            paste(frame, im, W / 2, 140, pop(lt, 0.18), -2.5 + wob, out)
        elif k == "side":
            def mk():
                parts = []
                for i, line in enumerate(g["lines"]):
                    first = i == 0
                    size = 118 if first and len(line) <= 3 else (84 if first else 58)
                    col = g["color"] if first else T.WHT
                    parts.append(text_img(line, size, col, stroke=8 if first else 6, path=FONT_BLACK if first else FONT_BOLD))
                w = max(p.width for p in parts)
                h = sum(p.height - 14 for p in parts) + 14
                im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                y = 0
                for p in parts:
                    im.alpha_composite(p, ((w - p.width) // 2, y))
                    y += p.height - 14
                return im
            im = cached(("side", gi), mk)
            sc = min(1.0, 820 / im.width) if side_x(g["t0"]) != W / 2 else 1.0
            paste(frame, im, side_x(g["t0"]), 470, pop(lt) * sc, wob * 0.4, out)
        elif k == "lower":
            draw_lower(frame, g, lt, out)
        elif k == "compare":
            a = cached(("ca", gi), lambda: boxed(g["a"], 60, T.WHT))
            b = cached(("cb", gi), lambda: boxed(g["b"], 60, T.YEL))
            vs = cached("vs", lambda: text_img("VS", 70, T.RED, stroke=8))
            y = 150
            sa, sb = min(1.0, 700 / a.width), min(1.0, 700 / b.width)  # long labels must not cover the VS
            paste(frame, a, 500, y, pop(lt) * sa, -2, out)
            paste(frame, vs, W / 2, y, pop(lt - 0.15), 0, out)
            paste(frame, b, W - 500, y, pop(lt - 0.25) * sb, 2, out)
        elif k == "ticker":
            dur = g["t1"] - g["t0"]
            v = int(1_250_000 * ease(lt / dur))
            im = text_img("+$" + money(v), 96, T.GRN, stroke=8)
            paste(frame, im, W / 2, 380, pop(lt), 0, out)
            lab = cached(("tick", gi), lambda: boxed("MIENTRAS DUERME", 44, T.WHT, pad=(20, 8)))
            paste(frame, lab, W / 2, 470, pop(lt - 0.1), -2, out)
        elif k == "counter":
            draw_counter(frame, g, gi, t, lt, out)
        elif k == "table":
            draw_table(frame, g, t, lt, out)
        elif k == "formula":
            draw_formula(frame, g, t, out)
        elif k == "list":
            draw_list(frame, g, gi, t, out)
        elif k == "chips":
            draw_chips(frame, g, gi, lt, out)
        elif k == "chart":
            draw_chart(frame, g, t, out)
        elif k == "note":
            im = cached(("note", gi), lambda: note_img(g["text"]))
            paste(frame, im, 40 + im.width / 2, 905, 1.0, 0, clamp01(lt / 0.3) * out)
        elif k == "badge":
            im = cached(("badge", gi), lambda: badge_img(g["n"], g["text"]))
            x = {"left": 1440, "right": 480}.get(g.get("side"), W / 2) if g.get("side") != "center" else W / 2
            if g.get("side") == "left":
                x = 480 if T.SHOTS[T.shot_at(g["t0"])[0]][2] == "right" else 1440
            paste(frame, im, x, 420 if g.get("side") == "center" else 470, pop(lt), -2 + wob * 0.5, out)
        elif k == "rule":
            draw_rule(frame, g, t, lt, out)
        elif k == "subscribe":
            draw_subscribe(frame, g, lt, out)
        elif k == "maintitle":
            draw_maintitle(frame, g, lt, out)
        elif k == "chapter":
            draw_chapter(frame, g, gi, lt, out)
        elif k == "end":
            draw_end(frame, g, lt)
        elif k == "stamp":
            pass


def draw_lower(frame, g, lt, out):
    e = ease_out_back(lt / 0.35)
    x = 90 - (1 - e) * 700
    name = cached(("ln", g["name"]), lambda: boxed(g["name"], 64, T.YEL, pad=(26, 8), radius=10))
    sub = cached(("ls", g["sub"]), lambda: boxed(g["sub"], 36, T.WHT, pad=(18, 6), path=FONT_BOLD, radius=8))
    paste(frame, name, x + name.width / 2, 780, 1, 0, out)
    paste(frame, sub, x + 20 + sub.width / 2, 862, 1, 0, clamp01((lt - 0.2) / 0.2) * out)


def draw_counter(frame, g, gi, t, lt, out):
    run = min(2.2, (g["t1"] - g["t0"]) * 0.75)
    v = int(round(g["a"] + (g["b"] - g["a"]) * ease(lt / run)))
    done = lt >= run
    x = {"left": 480, "right": 1440, "center": W / 2}[g.get("side", "center")]
    if g.get("side") in ("left", "right"):
        x = side_x(g["t0"])
    y = g.get("y", 430)
    sc = pop(lt) * (1 + (0.1 * math.exp(-(lt - run) * 10) if done else 0))
    im = text_img(g["fmt"].format(v).replace(",", "."), 120, T.GRN if g["b"] > g["a"] else T.RED, stroke=9)
    paste(frame, im, x, y, sc * min(1.0, 860 / im.width) if x != W / 2 else sc, 0, out)
    lab = cached(("clab", gi), lambda: boxed(g["label"], 48, T.WHT, pad=(20, 8)))
    paste(frame, lab, x, y + 105, pop(lt - 0.1), -2, out)


def draw_table(frame, g, t, lt, out):
    x0, y0, w = 110, 150, 760
    rows = g["rows"]
    n = 2 + len(rows)
    rh = 74
    a = clamp01(lt / 0.25) * out
    ov = Image.new("RGBA", (w, rh * n + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle([0, 0, w, rh * n + 40], radius=22, fill=(10, 10, 14, int(215 * a)))
    fb, fv = font(FONT_BOLD, 38), font(FONT_BLACK, 42)
    d.text((28, 20), g["income"], font=font(FONT_BLACK, 40), fill=T.GRN + (int(255 * a),))
    for i, (label, val, anchor) in enumerate(rows):
        ta = T.at(*anchor)
        if t < ta:
            continue
        e = clamp01((t - ta) / 0.2) * a
        y = 20 + rh * (i + 1)
        d.line([24, y - 6, w - 24, y - 6], fill=(255, 255, 255, int(40 * e)), width=2)
        d.text((28 + (1 - e) * 30, y + 8), label, font=fb, fill=(255, 255, 255, int(240 * e)))
        tw = fv.getbbox(val)[2]
        d.text((w - 28 - tw, y + 6), val, font=fv, fill=(255, 255, 255, int(255 * e)))
    tl, tv, anchor = g["total"]
    ta = T.at(*anchor)
    if t >= ta:
        e = clamp01((t - ta) / 0.2) * a
        y = 20 + rh * (len(rows) + 1)
        d.rounded_rectangle([16, y - 4, w - 16, y + 62], radius=12, fill=T.RED + (int(235 * e),))
        d.text((32, y + 6), tl, font=fv, fill=(255, 255, 255, int(255 * e)))
        tw = fv.getbbox(tv)[2]
        d.text((w - 32 - tw, y + 6), tv, font=fv, fill=(255, 255, 255, int(255 * e)))
    frame.alpha_composite(ov, (x0, y0))


def draw_formula(frame, g, t, out):
    steps = g["steps"]
    n = len(steps)
    ims = [cached(("form", label, i == n - 1), lambda: boxed(label, 46, T.YEL if i == n - 1 else T.WHT, pad=(20, 10)))
           for i, (label, _) in enumerate(steps)]
    gap = 90  # room for the arrow between boxes
    total = sum(im.width for im in ims) + gap * (n - 1)
    sc = min(1.0, 1800 / total)
    x = W / 2 - total * sc / 2
    xs = []
    for im in ims:
        xs.append(x + im.width * sc / 2)
        x += (im.width + gap) * sc
    for i, (label, anchor) in enumerate(steps):
        ta = T.at(*anchor)
        if t < ta:
            continue
        paste(frame, ims[i], xs[i], 110, pop(t - ta, 0.2) * sc, -1.5 if i % 2 else 1.5, out)
        if i:
            ar = cached("arrow", lambda: text_img("→", 64, T.YEL, stroke=6))
            ax = (xs[i - 1] + ims[i - 1].width * sc / 2 + xs[i] - ims[i].width * sc / 2) / 2
            paste(frame, ar, ax, 108, pop(t - ta) * sc, 0, out)


def draw_chips(frame, g, gi, lt, out):
    """Keywords that pop in one after another, in one or two rows at the top."""
    items = g["items"]
    col = g.get("color", T.YEL)
    ims = [cached(("chip", gi, i), lambda: boxed(txt, 50, col if col != T.RED else T.RED, T.INK if col != T.RED else T.WHT,
                                               pad=(24, 10))) for i, txt in enumerate(items)]
    rows, cur, cw = [], [], 0
    for i, im in enumerate(ims):
        if cur and cw + im.width > 1700:
            rows.append(cur)
            cur, cw = [], 0
        cur.append(i)
        cw += im.width + 10
    rows.append(cur)
    step = min(0.35, 1.6 / max(1, len(items)))
    for r, row in enumerate(rows):
        tw = sum(ims[i].width for i in row) + 10 * (len(row) - 1)
        x = W / 2 - tw / 2
        for i in row:
            paste(frame, ims[i], x + ims[i].width / 2, 120 + r * 105, pop(lt - i * step, 0.22), -1.5 if i % 2 else 1.5, out)
            x += ims[i].width + 10


def draw_list(frame, g, gi, t, out):
    items = g["items"]
    a = clamp01((t - g["t0"]) / 0.25) * out
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    step = min(150, 600 / len(items))
    ImageDraw.Draw(ov).rounded_rectangle([W / 2 - 560, 200, W / 2 + 560, 240 + step * len(items)], radius=26,
                                          fill=(10, 10, 14, int(200 * a)))
    frame.alpha_composite(ov)
    for i, (label, anchor) in enumerate(items):
        ta = T.at(*anchor)
        active = t >= ta
        if not active and i:
            col = (120, 120, 120)
        else:
            col = T.YEL if active else (120, 120, 120)
        im = cached(("li", gi, i, active), lambda: text_img(f"{i + 1}. {label}", 70, col, stroke=6, align="left"))
        sc = 1 + 0.08 * math.exp(-(t - ta) * 8) if active else 0.92
        paste(frame, im, W / 2 - 510 + im.width / 2, 200 + step * (i + 0.6), sc, 0, a)


def draw_chart(frame, g, t, out):
    """US$-style growth curve: 200.000 a month at 10% for 20 years vs what was put in."""
    x0, x1, y0, y1 = 300, 1620, 700, 230
    dur = g["t1"] - g["t0"]
    prog = ease((t - g["t0"]) / min(dur * 0.8, 9))
    a = clamp01((t - g["t0"]) / 0.3) * out
    r = 1.1 ** (1 / 12) - 1
    months = np.arange(0, 241)
    val = 200000 * ((1 + r) ** months - 1) / r
    put = 200000 * months
    top = val[-1]
    n = int(prog * 240)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle([x0 - 80, y1 - 120, x1 + 80, y0 + 70], radius=26, fill=(10, 10, 14, int(205 * a)))
    for yr in range(0, 21, 5):
        x = x0 + (x1 - x0) * yr / 20
        d.line([x, y0, x, y0 + 12], fill=(255, 255, 255, int(150 * a)), width=3)
        d.text((x - 30, y0 + 18), f"{yr} años" if yr else "0", font=font(FONT_SEMI, 26), fill=(255, 255, 255, int(200 * a)))

    def pts(arr):
        return [(x0 + (x1 - x0) * m / 240, y0 - (y0 - y1) * arr[m] / top) for m in range(0, n + 1, 2)]
    if n > 2:
        d.line(pts(put), fill=(200, 200, 200, int(230 * a)), width=8)
        d.line(pts(val), fill=(0, 0, 0, int(200 * a)), width=18)
        d.line(pts(val), fill=T.GRN + (int(255 * a),), width=12)
        ex, ey = pts(val)[-1]
        d.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=(255, 255, 255, int(255 * a)))
    d.text((x0 - 40, y1 - 100), "Valor de la inversión", font=font(FONT_BLACK, 40), fill=T.GRN + (int(255 * a),))
    d.text((x0 + 520, y1 - 100), "Lo que pusiste", font=font(FONT_BLACK, 40), fill=(210, 210, 210, int(255 * a)))
    frame.alpha_composite(ov)


def draw_rule(frame, g, t, lt, out):
    a = clamp01(lt / 0.25) * out
    parts = [(0.5, "50%", "NECESIDADES", T.BLU), (0.3, "30%", "GUSTOS", T.YEL), (0.2, "20%", "AHORRO Y DEUDAS", T.GRN)]
    x, y, w, h = 170, 330, 1500, 150
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle([x - 40, y - 150, x + w + 140, y + h + 150], radius=26, fill=(10, 10, 14, int(210 * a)))
    d.text((x, y - 120), "REGLA 50 / 30 / 20", font=font(FONT_BLACK, 64), fill=(255, 255, 255, int(255 * a)))
    cx = x
    for i, (frac, pct, label, col) in enumerate(parts):
        e = ease((lt - 0.4 - i * 0.5) / 0.4)
        if e <= 0:
            break
        ww = w * frac * e
        if ww < 30:
            break
        d.rounded_rectangle([cx, y, cx + ww - 8, y + h], radius=14, fill=col + (int(255 * a),))
        if e > 0.7:
            d.text((cx + 24, y + 22), pct, font=font(FONT_BLACK, 70), fill=T.INK + (int(255 * a),))
            d.text((cx + 6, y + h + 20), label, font=font(FONT_BLACK, 34), fill=col + (int(255 * a),))
        cx += w * frac
    frame.alpha_composite(ov)


def draw_subscribe(frame, g, lt, out):
    e = pop(lt, 0.3)
    btn = cached("subbtn", lambda: boxed("SUSCRÍBETE", 72, (230, 33, 23), T.WHT, pad=(44, 18), radius=14))
    done = cached("subdone", lambda: boxed("SUSCRITO", 72, (90, 90, 90), T.WHT, pad=(44, 18), radius=14))
    bell = cached("bell", lambda: boxed("ACTIVA LA CAMPANITA", 44, T.WHT, pad=(22, 10), path=FONT_BOLD))
    clicked = lt > 1.6
    paste(frame, done if clicked else btn, W / 2, 400, e * (0.92 if 1.6 < lt < 1.75 else 1), 0, out)
    paste(frame, bell, W / 2, 530, pop(lt - 0.5), -2, out)
    # cursor gliding in and clicking
    cx = W / 2 + 420 * (1 - ease((lt - 0.4) / 1.0)) + 140
    cy = 400 + 260 * (1 - ease((lt - 0.4) / 1.0)) + 20
    cur = cached("cursor", cursor_img)
    paste(frame, cur, cx, cy, 0.9 if 1.55 < lt < 1.75 else 1.0, 0, out * clamp01((lt - 0.3) / 0.2))


def cursor_img():
    im = Image.new("RGBA", (90, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(10, 6), (10, 92), (32, 72), (48, 108), (62, 102), (46, 68), (76, 68)]
    d.polygon(pts, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    d.line(pts + [pts[0]], fill=(0, 0, 0, 255), width=5)
    return im


def note_img(text):
    f = font(FONT_SEMI, 26)
    w = f.getbbox(text)[2] + 36
    im = Image.new("RGBA", (w, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, 48], radius=10, fill=(0, 0, 0, 165))
    d.text((18, 9), text, font=f, fill=(255, 255, 255, 235))
    return im


def badge_img(n, text):
    f = font(FONT_BLACK, 66)
    lines = text.split("\n")
    tw = max(f.getbbox(l)[2] for l in lines)
    r = 80
    w = 2 * r + 30 + tw + 40
    h = max(2 * r, len(lines) * 74 + 36) + 16
    im = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([r, 16 + 10, w + 10, h + 10], radius=24, fill=(0, 0, 0, 130))
    d.rounded_rectangle([r, 16, w, h], radius=24, fill=(255, 255, 255, 255))
    d.ellipse([0, h / 2 - r, 2 * r, h / 2 + r], fill=T.YEL + (255,), outline=T.INK + (255,), width=7)
    fn = font(FONT_BLACK, 110)
    nb = fn.getbbox(n)
    d.text((r - (nb[2] - nb[0]) / 2 - nb[0], h / 2 - (nb[3] - nb[1]) / 2 - nb[1]), n, font=fn, fill=T.INK)
    y0 = h / 2 - len(lines) * 74 / 2 + 4
    for i, l in enumerate(lines):
        d.text((2 * r + 30, y0 + i * 74), l, font=f, fill=T.INK)
    return im


def dark_cover(frame, a):
    frame.alpha_composite(Image.new("RGBA", (W, H), (8, 8, 12, int(255 * a))))


def draw_maintitle(frame, g, lt, out):
    """Channel sting for El Precio del Poder: a crown-less wordmark, gold rule and the slogan."""
    a = clamp01(lt / 0.15) * out
    bg = cached("mt_bg", lambda: Image.fromarray((np.asarray(affine_cover(blurred_bg(T.STING_BG), 1.1, (0, 0), 0, (0, 0)))
                                                  .astype(np.float32) * 0.55).astype(np.uint8)).convert("RGBA"))
    frame.alpha_composite(bg if a >= 1 else Image.blend(frame, bg, a))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    wipe = ease((lt - 0.25) / 0.6)
    d.rectangle([W / 2 - 520 * wipe, 560, W / 2 + 520 * wipe, 568], fill=T.YEL + (int(255 * out),))
    frame.alpha_composite(ov)
    t1 = cached("mt1", lambda: text_img("EL PRECIO", 150, T.WHT, stroke=10))
    t2 = cached("mt2", lambda: boxed("DEL PODER", 150, T.YEL, pad=(40, 16)))
    paste(frame, t1, W / 2, 290, pop(lt - 0.05, 0.3), 0, out)
    paste(frame, t2, W / 2, 470, pop(lt - 0.3, 0.3), -2.5, out)
    for i, (txt, anchor) in enumerate(T.SLOGAN):
        ta = T.at(*anchor) - g["t0"]
        if lt >= ta:
            im = cached(("slog", i), lambda: text_img(txt, 76, T.YEL if i else T.WHT, stroke=7))
            paste(frame, im, W / 2, 680 + i * 110, pop(lt - ta, 0.25), 0, out)


def draw_chapter(frame, g, gi, lt, out):
    a = clamp01(lt / 0.12) * out
    nxt = T.SHOTS[T.shot_at(g["t1"] + 0.05)[0]][1]
    bg = cached(("ch_bg", gi), lambda: Image.fromarray((np.asarray(affine_cover(blurred_bg(nxt), 1.1, (0, 0), 0, (0, 0)))
                                                         .astype(np.float32) * 0.7).astype(np.uint8)).convert("RGBA"))
    frame.paste(Image.blend(frame, bg, a) if a < 1 else bg.copy())
    if g["n"]:
        num = cached(("chn", gi), lambda: text_img(f"#{g['n']}", 420, T.YEL, stroke=14))
        sc = pop(lt - 0.05, 0.32) * (1 + 0.04 * lt)
        paste(frame, num, 560, 520, sc, -4, out)
        title = cached(("cht", gi), lambda: text_img(g["text"], 96, T.WHT, stroke=8, align="left"))
        sc2 = min(1.0, 900 / title.width)
        e = ease_out_back((lt - 0.3) / 0.35)
        paste(frame, title, 1050 + title.width * sc2 / 2 + (1 - e) * 300, 520, sc2, 0, out * clamp01((lt - 0.3) / 0.15))
    else:
        title = cached(("cht", gi), lambda: text_img(g["text"], 120, T.YEL, stroke=9))
        paste(frame, title, W / 2, 520, pop(lt - 0.1, 0.3), 0, out)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        wipe = ease((lt - 0.15) / 0.5)
        d.rectangle([W / 2 - 600 * wipe, 650, W / 2 + 600 * wipe, 658], fill=T.YEL + (int(255 * out),))
        frame.alpha_composite(ov)


def draw_end(frame, g, lt):
    a = clamp01(lt / 0.4)
    bg = cached("end_bg", lambda: affine_cover(blurred_bg(T.END_BG), 1.1, (0, 0), 0, (0, 0)).convert("RGBA"))
    frame.paste(Image.blend(frame, bg, a) if a < 1 else bg)
    head = cached("end_h", lambda: text_img(T.END_HEAD, 70, T.YEL, stroke=7))
    paste(frame, head, W / 2, 130, pop(lt - 0.2), 0, a)
    sub = cached("end_s", lambda: text_img(T.END_SUB, 46, T.WHT, stroke=5, path=FONT_BOLD))
    paste(frame, sub, W / 2, 215, a, 0, a)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # Spaces for YouTube end-screen elements: a video on the left, subscribe on the right.
    d.rounded_rectangle([170, 360, 170 + 896, 360 + 504], radius=18, outline=(255, 255, 255, int(220 * a)), width=6,
                        fill=(0, 0, 0, int(110 * a)))
    d.ellipse([1340, 420, 1340 + 360, 420 + 360], outline=(255, 255, 255, int(220 * a)), width=6, fill=(0, 0, 0, int(110 * a)))
    frame.alpha_composite(ov)
    nv = cached("end_v", lambda: text_img("PRÓXIMO VIDEO", 64, T.WHT, stroke=6))
    paste(frame, nv, 170 + 448, 612, a, 0, a)
    sb = cached("end_sb", lambda: boxed("SUSCRÍBETE", 44, (230, 33, 23), T.WHT, pad=(22, 10)))
    paste(frame, sb, 1520, 860, pop(lt - 0.5), 0, a)


# ---------------------------------------------------------------- captions

def draw_captions(frame, t, chunks):
    for c in chunks:
        if not (c["t0"] <= t < c["t1"]):
            continue
        lt = t - c["t0"]
        words = c["words"]
        size = 56
        f = font(FONT_BLACK, size)
        texts = [w["text"] for w in words]
        space = size * 0.26
        ws = [f.getbbox(x, stroke_width=7)[2] for x in texts]
        lines, cur, cw = [], [], 0
        for i, wd in enumerate(ws):
            if cur and cw + space + wd > 1500:
                lines.append(cur)
                cur, cw = [], 0
            cw += (space if cur else 0) + wd
            cur.append(i)
        lines.append(cur)
        lh = size * 1.12
        layer = Image.new("RGBA", (W, int(lh * len(lines) + 40)), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for li, line in enumerate(lines):
            lw = sum(ws[i] for i in line) + space * (len(line) - 1)
            x = (W - lw) / 2
            for i in line:
                said = words[i]["start"] - 0.03 <= t
                now = said and t < words[i]["end"] + 0.06
                col = T.YEL if now else T.WHT
                d.text((x, 8 + li * lh), texts[i], font=f, fill=col + (255 if said else 140,),
                       stroke_width=7, stroke_fill=(0, 0, 0, 255 if said else 140))
                x += ws[i] + space
        sc = 0.94 + 0.06 * ease_out_back(lt / 0.14, 2.0)
        paste(frame, layer, W / 2, 1000 - (lh * (len(lines) - 1)) / 2, sc)


def chapter_tag(frame, t):
    cur = None
    for c in T.CARDS:
        if c["kind"] == "chapter" and t >= c["t1"]:
            cur = c
    if cur is None or t >= T.END_SCREEN or any(c["t0"] <= t < c["t1"] for c in T.CARDS):
        return
    label = (f"#{cur['n']} · " if cur["n"] else "") + cur["text"].replace("\n", " ")
    im = cached(("tag", label), lambda: boxed(label, 26, T.WHT, pad=(14, 6), path=FONT_BOLD, radius=8))
    a = clamp01((t - cur["t1"]) / 0.4) * 0.85
    paste(frame, im, W - 40 - im.width / 2, 50, 1.0, 0, a)


# ---------------------------------------------------------------- finishing

_vig = _grain = None


def grade(arr):
    x = arr.astype(np.float32) * (1 / 255.0)
    x = x + 0.10 * (x - 0.5) * (1 - (2 * x - 1) ** 2) * 2
    lum = x.mean(axis=2, keepdims=True)
    x = lum + (x - lum) * 1.12
    x[..., 0] *= 1.025
    x[..., 2] *= 0.97
    return x


def finishing(arr, t, fi):
    global _vig, _grain
    if _vig is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
        _vig = np.clip(1 - 0.30 * r ** 2.2, 0.5, 1)[..., None].astype(np.float32)
        rs = np.random.RandomState(5)
        _grain = [np.repeat(np.repeat(rs.normal(0, 1, (H // 2, W // 2)).astype(np.float32), 2, 0), 2, 1)[..., None]
                  for _ in range(6)]
    x = arr.astype(np.float32) * _vig + _grain[fi % 6] * 5.0
    fl = 0.0
    for s in T.SHOTS:
        if s[3].get("flash") and 0 <= t - s[0] < 0.18:
            fl = max(fl, 1 - (t - s[0]) / 0.18)
    for c in T.CARDS:
        if 0 <= t - c["t0"] < 0.15:
            fl = max(fl, 1 - (t - c["t0"]) / 0.15)
    if fl:
        x = x + (255 - x) * (0.7 * fl)
    x = np.clip(x, 0, 255).astype(np.uint8)
    for h in T.HITS:
        if 0 <= t - h < 0.22:
            sft = int(9 * (1 - (t - h) / 0.22))
            if sft:
                x[..., 0] = np.roll(x[..., 0], sft, axis=1)
                x[..., 2] = np.roll(x[..., 2], -sft, axis=1)
    return x


def shake(img, t):
    amp = 0.0
    for h in T.HITS:
        if 0 <= t - h < 0.3:
            amp = max(amp, 16 * (1 - (t - h) / 0.3) ** 2)
    if amp < 0.5:
        return img
    k = 1 / 1.04
    dx, dy = math.sin(t * 91) * amp, math.cos(t * 77) * amp
    return img.transform((W, H), Image.AFFINE, (k, 0, (W - W * k) / 2 + dx, 0, k, (H - H * k) / 2 + dy), Image.BILINEAR)


def whip(img, t):
    """Motion-blur slide across every fourth cut."""
    for i, s in enumerate(T.SHOTS[1:], 1):
        if i % 4:
            continue
        d = t - s[0]
        if -0.1 <= d < 0.1:
            arr = np.asarray(img)
            k = 1 - abs(d) / 0.1
            shift = int((1 if d < 0 else -1) * 300 * k)
            acc = np.zeros(arr.shape, np.float32)
            for j in range(6):
                acc += np.roll(arr, int(shift * j / 5 * 0.9), axis=1)
            return Image.fromarray((acc / 6).astype(np.uint8))
    return img


def render_frame(fi, chunks):
    t = fi / FPS
    base = draw_shot(t)
    base = Image.fromarray(np.clip(grade(np.asarray(base)) * 255, 0, 255).astype(np.uint8))
    base = whip(shake(base, t), t)
    frame = base.convert("RGBA")
    draw_gfx(frame, t)
    if t < T.END_SCREEN:
        draw_captions(frame, t, chunks)
        chapter_tag(frame, t)
    return finishing(np.asarray(frame.convert("RGB")), t, fi)


def render_range(args):
    a, b, path = args
    chunks = T.caption_chunks()
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(render_frame(fi, chunks).tobytes())
    p.stdin.close()
    p.wait()
    return path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    if "--frames" in sys.argv:
        chunks = T.caption_chunks()
        for s in sys.argv[sys.argv.index("--frames") + 1:]:
            Image.fromarray(render_frame(int(float(s) * FPS), chunks)).save(os.path.join(OUT_DIR, f"f_{s}.jpg"), quality=88)
        return
    a, b = 0, int(round(T.END * FPS))
    if "--only" in sys.argv:
        i = sys.argv.index("--only")
        a, b = int(float(sys.argv[i + 1]) * FPS), int(float(sys.argv[i + 2]) * FPS)
    n = 4
    chunk = 900  # 30 s per job keeps every worker busy until the end
    jobs = [(s, min(b, s + chunk), os.path.join(OUT_DIR, f"part{s // chunk:03d}.mp4")) for s in range(a, b, chunk)]
    with Pool(n) as pool:
        pool.map(render_range, jobs, chunksize=1)
    parts = sorted(os.path.join(OUT_DIR, f) for f in os.listdir(OUT_DIR) if f.startswith("part") and f.endswith(".mp4"))
    lst = os.path.join(OUT_DIR, "parts.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(OUT_DIR, "video.mp4")], check=True)
    print("video ->", os.path.join(OUT_DIR, "video.mp4"))


if __name__ == "__main__":
    main()
