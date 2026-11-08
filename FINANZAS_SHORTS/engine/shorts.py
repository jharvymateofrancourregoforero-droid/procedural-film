"""Shared engine for the five finance Shorts (1080x1920, 30 fps).

Each video folder holds narracion.mp3, words.json (word timings) and spec.py.
spec.build(E) returns the shot list and graphics, anchored to phrases of the
narration. This module renders frames with Pillow + numpy, synthesises the
music and effects, mixes them under the voice and writes:
  video_final.mp4, subtitulos.srt, miniatura.png

usage: python3 engine/shorts.py VIDEO_01_RICOS [--frames 1.5 20] [--skip-video]
"""
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS = os.path.join(ROOT, "assets", "photos")
W, H, FPS = 1080, 1920, 30
TAIL = 1.6  # seconds held after the last word

F_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
F_XB = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
F_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
F_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

# Identity: deep black, dark grey, metallic gold, white text, finance blue.
BLACK, GREY, WHITE = (8, 8, 10), (34, 35, 40), (255, 255, 255)
GOLD, GOLD_D, GOLD_L = (212, 175, 55), (150, 112, 30), (255, 226, 140)
BLUE, RED, GREEN = (64, 140, 255), (235, 72, 60), (70, 200, 120)


# ---------------------------------------------------------------- project / timing

class Project:
    def __init__(self, folder):
        self.folder = os.path.join(ROOT, folder)
        self.name = folder
        self.words = json.load(open(os.path.join(self.folder, "words.json")))["words"]
        self.voice_end = self.words[-1]["end"]
        self.END = self.voice_end + TAIL
        spec_path = os.path.join(self.folder, "spec.py")
        mod = importlib.util.spec_from_file_location("spec", spec_path)
        self.spec = importlib.util.module_from_spec(mod)
        mod.loader.exec_module(self.spec)
        out = self.spec.build(self)
        self.shots = sorted(out["shots"], key=lambda s: s[0])
        self.shots[0] = (0.0,) + tuple(self.shots[0][1:])
        self.gfx = out["gfx"]
        self.merges = out.get("merges", [])
        self.hook = out["hook"]
        self.thumb = out["thumb"]
        self.music_key = out.get("key", 0)
        self.reveal = out.get("reveal")
        self.hits = sorted(out.get("hits", []))
        self.chunks = caption_chunks(self.words, self.merges, self.END)

    @staticmethod
    def norm(s):
        s = unicodedata.normalize("NFD", s.lower())
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")
        return re.sub(r"[^a-z0-9]", "", s)

    def at(self, phrase, nth=0, end=False):
        key = [self.norm(x) for x in phrase.split()]
        found = 0
        ws = self.words
        for i in range(len(ws) - len(key) + 1):
            if all(self.norm(ws[i + k]["text"]) == key[k] for k in range(len(key))):
                if found == nth:
                    return ws[i + len(key) - 1]["end"] if end else ws[i]["start"]
                found += 1
        raise KeyError(f"{self.name}: '{phrase}' not found")

    def g(self, kind, phrase, until=None, **kw):
        t0 = self.at(phrase, kw.pop("nth", 0)) if isinstance(phrase, str) else phrase
        if until is None:
            t1 = t0 + kw.pop("dur", 2.4)
        elif isinstance(until, (int, float)):
            t1 = t0 + until
        elif until == "END":
            t1 = self.END
        else:
            t1 = self.at(until)
        return dict(kind=kind, t0=t0, t1=t1, **kw)

    def shot(self, phrase, img, mode="full", **opt):
        t = 0.0 if phrase is None else self.at(phrase) - 0.04
        return (t, img, mode, opt)

    def shot_at(self, t):
        idx = 0
        for i, s in enumerate(self.shots):
            if t >= s[0]:
                idx = i
        end = self.shots[idx + 1][0] if idx + 1 < len(self.shots) else self.END
        return idx, self.shots[idx][0], end


def caption_chunks(words, merges, END):
    toks, i = [], 0
    while i < len(words):
        for seq, rep in merges:
            n = len(seq)
            got = [Project.norm(words[i + k]["text"]) for k in range(n) if i + k < len(words)]
            if got == [Project.norm(x) for x in seq]:
                last = words[i + n - 1]["text"]
                trail = re.search(r'[.,?!:…"]*$', last).group(0)
                lead = re.match(r'^[¿¡"]*', words[i]["text"]).group(0)
                toks.append(dict(text=lead + rep + trail, start=words[i]["start"], end=words[i + n - 1]["end"]))
                i += n
                break
        else:
            toks.append(dict(text=words[i]["text"], start=words[i]["start"], end=words[i]["end"]))
            i += 1
    chunks, cur = [], []
    for j, t in enumerate(toks):
        cur.append(t)
        nxt = toks[j + 1] if j + 1 < len(toks) else None
        nchar = sum(len(x["text"]) + 1 for x in cur)
        brk = (re.search(r'[.?!:…"]$', t["text"]) or (re.search(r",$", t["text"]) and len(cur) >= 3)
               or nchar >= 26 or nxt is None or nxt["start"] - t["end"] > 0.35)
        if brk:
            chunks.append(cur)
            cur = []
    out = []
    for k, c in enumerate(chunks):
        t1 = chunks[k + 1][0]["start"] - 0.02 if k + 1 < len(chunks) else min(END, c[-1]["end"] + 0.6)
        out.append(dict(t0=c[0]["start"] - 0.03, t1=min(t1, c[-1]["end"] + 0.55), words=c))
    return out


# ---------------------------------------------------------------- drawing helpers

_fonts = {}


def font(path, size):
    if (path, size) not in _fonts:
        _fonts[(path, size)] = ImageFont.truetype(path, size)
    return _fonts[(path, size)]


def clamp01(x):
    return min(max(x, 0.0), 1.0)


def ease(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def back(x, s=1.6):
    x = clamp01(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def gold_fill(size_wh):
    """Vertical metallic gold gradient with a soft highlight band."""
    w, h = size_wh
    y = np.linspace(0, 1, h)[:, None]
    stops = np.array([[255, 236, 170], [226, 186, 72], [170, 128, 34], [232, 196, 96], [255, 230, 150]], np.float32)
    pos = np.array([0.0, 0.35, 0.55, 0.78, 1.0])
    rgb = np.stack([np.interp(y[:, 0], pos, stops[:, c]) for c in range(3)], 1)
    arr = np.repeat(rgb[:, None, :], w, 1)
    return Image.fromarray(arr.astype(np.uint8))


def text_img(text, size, style="white", path=F_BLACK, stroke=0, spacing=1.04, shadow=True, track=0):
    """Multi-line centred text. style: white | gold | blue | red | green | grey."""
    f = font(path, size)
    lines = text.split("\n")

    def line_w(l):
        if not track:
            return f.getbbox(l)[2]
        return int(sum(f.getlength(ch) for ch in l) + track * max(0, len(l) - 1)) + 4
    widths = [line_w(l) for l in lines]
    lh = int(size * spacing)
    pad = 24
    w, h = max(widths) + 2 * pad, lh * (len(lines) - 1) + int(size * 1.22) + 2 * pad
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    for i, l in enumerate(lines):
        x = (w - widths[i]) / 2
        if track:
            for ch in l:
                d.text((x, pad + i * lh), ch, font=f, fill=255)
                x += f.getlength(ch) + track
        else:
            d.text((x, pad + i * lh), l, font=f, fill=255)
    if style == "gold":
        fill = gold_fill((w, h)).convert("RGBA")
    else:
        col = {"white": WHITE, "blue": BLUE, "red": RED, "green": GREEN, "grey": (190, 190, 196), "black": BLACK}[style]
        fill = Image.new("RGBA", (w, h), col + (255,))
    fill.putalpha(mask)
    out = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sh.putalpha(mask.filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.85)))
        out.alpha_composite(sh, (12, 16))
        sh2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sh2.putalpha(mask.filter(ImageFilter.MaxFilter(5)).point(lambda v: int(v * 0.55)))
        out.alpha_composite(sh2, (10, 10))
    out.alpha_composite(fill, (10, 10))
    return out


def panel(w, h, radius=26, alpha=200, border=True):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=(12, 12, 14, alpha))
    if border:
        d.rounded_rectangle([1, 1, w - 2, h - 2], radius=radius, outline=GOLD + (200,), width=3)
    return im


def chip(text, size=50, fg=BLACK, bg=GOLD, path=F_BLACK, pad=(28, 12)):
    f = font(path, size)
    tw = f.getbbox(text)[2]
    w, h = tw + 2 * pad[0], int(size * 1.2) + 2 * pad[1]
    im = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 12, w + 8, h + 12], radius=h // 2, fill=(0, 0, 0, 120))
    d.rounded_rectangle([4, 4, w + 4, h + 4], radius=h // 2, fill=bg + (255,))
    d.text((4 + pad[0], 4 + pad[1] - size * 0.04), text, font=f, fill=fg)
    return im


def paste(frame, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
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


def money(v, cur="$", dec=0):
    s = f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return cur + s


# ---------------------------------------------------------------- photos and shots

_photo, _big, _blur = {}, {}, {}


def photo(name):
    if name not in _photo:
        _photo[name] = Image.open(os.path.join(PHOTOS, name + ".jpg")).convert("RGB")
    return _photo[name]


def big(name):
    """Upscaled once so it covers the frame with room to move; sharpened when it was small."""
    if name not in _big:
        im = photo(name)
        s = max(W * 1.16 / im.width, H * 1.16 / im.height)
        if s > 1:
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
        _big[name] = im
    return _big[name]


def blurred(name):
    if name not in _blur:
        sm = photo(name).copy()
        sm.thumbnail((360, 360))
        _blur[name] = Image.fromarray((np.asarray(sm.filter(ImageFilter.GaussianBlur(8))).astype(np.float32) * 0.45).astype(np.uint8))
    return _blur[name]


def cover(im, zoom, pan, box=(W, H), offset=(0, 0)):
    bw, bh = box
    iw, ih = im.size
    s = max(bw / iw, bh / ih) * zoom
    mx, my = max(0.0, (iw * s - bw) / 2) / s, max(0.0, (ih * s - bh) / 2) / s
    cx, cy = iw / 2 + pan[0] * mx, ih / 2 + pan[1] * my
    a = 1 / s
    ox, oy = bw / 2 + offset[0], bh / 2 + offset[1]
    return im.transform((bw, bh), Image.AFFINE, (a, 0, cx - a * ox, 0, a, cy - a * oy), resample=Image.BILINEAR)


MOVES = [((1.0, 1.10), (0, 0.25), (0, -0.25)), ((1.10, 1.0), (0, -0.2), (0, 0.2)), ((1.04, 1.12), (-0.4, 0), (0.4, 0)),
         ((1.12, 1.03), (0.4, 0.1), (-0.3, -0.1)), ((1.0, 1.08), (0, -0.3), (0, 0.3))]


def drift(t, seed):
    r = np.random.RandomState(seed)
    ph = r.rand(2) * 6.283
    return math.sin(t * 0.43 * 6.283 + ph[0]) * 4, math.sin(t * 0.31 * 6.283 + ph[1]) * 5


def render_shot(P, idx, t):
    start, name, mode, opt = P.shots[idx]
    end = P.shots[idx + 1][0] if idx + 1 < len(P.shots) else P.END
    p = clamp01((t - start) / max(0.6, end - start))
    (z0, z1), pa, pb = opt.get("move", MOVES[idx % len(MOVES)])
    zoom = z0 + (z1 - z0) * ease(p)
    pan = (pa[0] + (pb[0] - pa[0]) * ease(p), pa[1] + (pb[1] - pa[1]) * ease(p))
    off = drift(t, idx)
    if mode == "black":
        return Image.new("RGB", (W, H), BLACK)
    if mode == "full":
        return cover(big(name), zoom, pan, offset=off)
    if mode == "split":
        frame = Image.new("RGB", (W, H), BLACK)
        hh = H // 2 - 4
        top = cover(big(name), zoom, pan, box=(W, hh), offset=off)
        bot = cover(big(opt["img2"]), 2.1 - zoom, (-pan[0], -pan[1]), box=(W, hh), offset=(-off[0], -off[1]))
        frame.paste(top, (0, 0))
        frame.paste(bot, (0, H - hh))
        d = ImageDraw.Draw(frame)
        d.rectangle([0, hh, W, H - hh], fill=GOLD)
        return frame
    # card: framed landscape photo over its own blurred copy
    frame = cover(blurred(name), 1.15 + 0.08 * p, (0, 0)).convert("RGBA")
    im = photo(name)
    maxw, maxh = 940, opt.get("maxh", 900)
    s = min(maxw / im.width, maxh / im.height) * (0.97 + 0.05 * ease(p))
    cw, ch = int(im.width * s), int(im.height * s)
    card = im.resize((cw, ch), Image.BILINEAR).convert("RGBA")
    bordered = Image.new("RGBA", (cw + 8, ch + 8), GOLD + (255,))
    bordered.alpha_composite(card, (4, 4))
    shadow = Image.new("RGBA", (cw + 120, ch + 120), (0, 0, 0, 0))
    m = Image.new("L", shadow.size, 0)
    ImageDraw.Draw(m).rectangle([60, 70, 60 + cw + 8, 70 + ch + 8], fill=200)
    shadow.putalpha(m.filter(ImageFilter.GaussianBlur(28)))
    cy = opt.get("cy", 900)
    frame.alpha_composite(shadow, (int(W / 2 - shadow.width / 2 + off[0]), int(cy - shadow.height / 2 + off[1])))
    frame.alpha_composite(bordered, (int(W / 2 - bordered.width / 2 + off[0]), int(cy - bordered.height / 2 + off[1])))
    return frame.convert("RGB")


def grade(img):
    """Cinematic look: slight desaturation, contrast, cool shadows and warm highlights."""
    x = np.asarray(img).astype(np.float32) / 255.0
    lum = x @ np.array([0.299, 0.587, 0.114], np.float32)
    x = lum[..., None] + (x - lum[..., None]) * 0.78
    x = np.clip((x - 0.5) * 1.16 + 0.5, 0, 1)
    sh = (1 - lum)[..., None] ** 2
    hi = lum[..., None] ** 2
    x = x + sh * np.array([-0.025, 0.0, 0.03], np.float32) + hi * np.array([0.04, 0.02, -0.03], np.float32)
    return np.clip(x * 0.93, 0, 1)


def draw_base(P, t):
    idx, start, end = P.shot_at(t)
    frame = render_shot(P, idx, t)
    # natural cross-dissolve into each shot
    xf = 0.22
    if idx > 0 and t - start < xf:
        prev = render_shot(P, idx - 1, t)
        frame = Image.blend(prev, frame, ease((t - start) / xf))
    return frame


# ---------------------------------------------------------------- graphics

_cache = {}


def cached(key, fn):
    if key not in _cache:
        _cache[key] = fn()
    return _cache[key]


def pop(lt, d=0.28):
    return max(0.0, back(lt / d))


def fade_io(lt, total, fin=0.2, fout=0.18):
    return clamp01(lt / fin) * clamp01((total - lt) / fout)


def draw_gfx(P, frame, t):
    for gi, g in enumerate(P.gfx):
        if not (g["t0"] <= t < g["t1"]):
            continue
        lt, total = t - g["t0"], g["t1"] - g["t0"]
        a = fade_io(lt, total)
        k = g["kind"]
        fn = GFX_DRAW.get(k)
        if fn:
            fn(P, frame, g, gi, t, lt, total, a)


def gx_big(P, frame, g, gi, t, lt, total, a):
    im = cached(("big", P.name, gi), lambda: text_img(g["text"], g.get("size", 150), g.get("style", "gold"),
                                                    track=g.get("track", 0)))
    sc = (0.9 + 0.1 * ease_out(lt / 0.35)) * (1 + 0.02 * lt / max(total, 1))
    sc *= min(1.0, 980 / im.width)
    paste(frame, im, W / 2, g.get("y", 760), sc, a)


def gx_label(P, frame, g, gi, t, lt, total, a):
    im = cached(("lab", P.name, gi), lambda: text_img(g["text"], g.get("size", 64), g.get("style", "white"), path=F_XB))
    paste(frame, im, W / 2, g.get("y", 900), min(1.0, 980 / im.width), a)


def gx_chip(P, frame, g, gi, t, lt, total, a):
    im = cached(("chip", P.name, gi), lambda: chip(g["text"], g.get("size", 52), fg=g.get("fg", BLACK), bg=g.get("bg", GOLD)))
    paste(frame, im, g.get("x", W / 2), g.get("y", 420), pop(lt), a)


def gx_counter(P, frame, g, gi, t, lt, total, a):
    run = g.get("run", min(1.6, total * 0.7))
    v = g["a"] + (g["b"] - g["a"]) * ease_out(lt / run)
    txt = money(v, g.get("cur", "$"), g.get("dec", 0))
    im = text_img(txt, g.get("size", 150), g.get("style", "gold"))
    done = lt >= run
    sc = (1 + (0.08 * math.exp(-(lt - run) * 9) if done else 0)) * min(1.0, 990 / im.width)
    paste(frame, im, W / 2, g.get("y", 760), sc, a)
    if g.get("label"):
        lab = cached(("clab", P.name, gi), lambda: text_img(g["label"], 52, "white", path=F_XB))
        paste(frame, lab, W / 2, g.get("y", 760) + g.get("size", 150) * 0.78, 1.0, a)


def gx_note(P, frame, g, gi, t, lt, total, a):
    def mk():
        f = font(F_SEMI, 30)
        lines = g["text"].split("\n")
        w = max(f.getbbox(l)[2] for l in lines) + 40
        h = 42 * len(lines) + 24
        im = panel(w, h, radius=14, alpha=170, border=False)
        d = ImageDraw.Draw(im)
        for i, l in enumerate(lines):
            d.text((20, 12 + 42 * i), l, font=f, fill=(230, 230, 230, 255))
        return im
    im = cached(("note", P.name, gi), mk)
    paste(frame, im, W / 2, g.get("y", 1700), 1.0, a)


def gx_price(P, frame, g, gi, t, lt, total, a):
    """Price tag that ticks from one value to another, with a % badge."""
    x, y = W / 2, g.get("y", 700)
    pnl = cached(("pp", P.name, gi), lambda: panel(860, 360))
    paste(frame, pnl, x, y, 0.95 + 0.05 * ease_out(lt / 0.3), a)
    lab = cached(("plab", P.name, gi), lambda: text_img(g["label"], 46, "grey", path=F_XB, shadow=False))
    paste(frame, lab, x, y - 120, 1.0, a)
    ts = g["t_change"] - g["t0"]
    v = g["a"] if lt < ts else g["a"] + (g["b"] - g["a"]) * ease_out((lt - ts) / 0.9)
    im = text_img(money(v), 140, "gold" if lt < ts else "white", shadow=False)
    paste(frame, im, x, y + 20, 1.0, a)
    if lt >= ts:
        badge = cached(("pb", P.name, gi), lambda: chip(g["badge"], 54, fg=WHITE, bg=RED))
        paste(frame, badge, x + 300, y - 170, pop(lt - ts), a)


def gx_bar(P, frame, g, gi, t, lt, total, a):
    """Purchasing-power bar that drops from 100 % to a lower share."""
    x0, y, w, h = 120, g.get("y", 760), 840, 90
    pnl = cached(("bp", P.name, gi), lambda: panel(940, 330))
    paste(frame, pnl, W / 2, y + 20, 1.0, a)
    lab = cached(("bl", P.name, gi), lambda: text_img(g["label"], 48, "white", path=F_XB, shadow=False))
    paste(frame, lab, W / 2, y - 80, 1.0, a)
    frac = 1 - (1 - g["to"]) * ease((lt - 0.5) / 1.2)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=18, fill=(50, 50, 56, int(255 * a)))
    d.rounded_rectangle([x0, y, x0 + max(36, int(w * frac)), y + h], radius=18, fill=GOLD + (int(255 * a),))
    frame.alpha_composite(ov)
    pct = text_img(f"{frac * 100:.0f} %", 72, "white", shadow=False)
    paste(frame, pct, W / 2, y + h + 70, 1.0, a)


def gx_steps(P, frame, g, gi, t, lt, total, a):
    """Stacked numbered values that appear one by one (e.g. 100 → 110 → 121 → 133)."""
    items = g["items"]
    y0 = g.get("y", 520)
    for i, (txt, anchor) in enumerate(items):
        ta = P.at(anchor) if isinstance(anchor, str) else anchor
        if t < ta:
            continue
        e = ease_out((t - ta) / 0.3)
        active = i == max(j for j, (_, an) in enumerate(items) if t >= (P.at(an) if isinstance(an, str) else an))
        im = cached(("st", P.name, gi, i, active), lambda: text_img(txt, 110 if active else 84, "gold" if active else "grey"))
        paste(frame, im, W / 2, y0 + i * 150 + (1 - e) * 40, 1.0, a * e)


def gx_chart(P, frame, g, gi, t, lt, total, a):
    """Growth curve drawn left to right; values from g['fn'](x) over x in [0, 1]."""
    x0, x1 = 120, 960
    yb, yt = g.get("y", 1080), g.get("y", 1080) - 520
    prog = ease(lt / g.get("draw", min(total * 0.8, 3.5)))
    pnl = cached(("cp", P.name, gi), lambda: panel(940, 640))
    paste(frame, pnl, W / 2, (yb + yt) / 2 + 10, 1.0, a)
    n = 120
    xs = np.linspace(0, 1, n + 1)
    vals = np.array([g["fn"](x) for x in xs])
    lo, hi = g.get("lo", vals.min()), vals.max()
    pts = [(x0 + (x1 - x0) * x, yb - (yb - yt) * (v - lo) / (hi - lo)) for x, v in zip(xs, vals)]
    m = max(2, int(prog * n))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for k in range(1, 4):
        yy = yb - (yb - yt) * k / 4
        d.line([x0, yy, x1, yy], fill=(255, 255, 255, int(28 * a)), width=2)
    poly = pts[: m + 1] + [(pts[m][0], yb), (x0, yb)]
    d.polygon(poly, fill=g.get("color", GOLD) + (int(55 * a),))
    d.line(pts[: m + 1], fill=g.get("color", GOLD) + (int(255 * a),), width=10, joint="curve")
    ex, ey = pts[m]
    d.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=(255, 255, 255, int(255 * a)))
    frame.alpha_composite(ov)
    if g.get("xlabels"):
        for xl, txt in g["xlabels"]:
            im = cached(("cx", P.name, gi, txt), lambda: text_img(txt, 32, "grey", path=F_SEMI, shadow=False))
            paste(frame, im, x0 + (x1 - x0) * xl, yb + 40, 1.0, a)


def gx_compare(P, frame, g, gi, t, lt, total, a):
    """Two options, e.g. GASTAR vs INVERTIR, laid on the split screen."""
    top = cached(("cpa", P.name, gi), lambda: text_img(g["a"], 120, g.get("sa", "white"), track=4))
    bot = cached(("cpb", P.name, gi), lambda: text_img(g["b"], 120, g.get("sb", "gold"), track=4))
    paste(frame, top, W / 2, g.get("ya", 520), pop(lt), a)
    paste(frame, bot, W / 2, g.get("yb", 1340), pop(lt - 0.15), a)
    if g.get("vs", True):
        vs = cached("vs", lambda: chip("VS", 58, fg=BLACK, bg=GOLD))
        paste(frame, vs, W / 2, H / 2, pop(lt - 0.3), a)


def gx_clock(P, frame, g, gi, t, lt, total, a):
    """24-hour clock whose hand sweeps a full turn, with a gold arc."""
    cx, cy, r = W / 2, g.get("y", 760), 260
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.ellipse([cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30], fill=(10, 10, 12, int(215 * a)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD + (int(255 * a),), width=8)
    for k in range(24):
        ang = math.radians(k * 15 - 90)
        r1 = r - (38 if k % 6 == 0 else 20)
        d.line([cx + r1 * math.cos(ang), cy + r1 * math.sin(ang), cx + (r - 6) * math.cos(ang), cy + (r - 6) * math.sin(ang)],
               fill=(255, 255, 255, int(220 * a)), width=6 if k % 6 == 0 else 3)
    sweep = 360 * ease(lt / g.get("sweep", 2.2))
    if sweep > 1:
        d.arc([cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30], -90, -90 + sweep, fill=GOLD + (int(170 * a),), width=26)
    ang = math.radians(sweep - 90)
    d.line([cx, cy, cx + (r - 70) * math.cos(ang), cy + (r - 70) * math.sin(ang)], fill=(255, 255, 255, int(255 * a)), width=12)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=GOLD + (int(255 * a),))
    frame.alpha_composite(ov)
    lab = cached(("clk", P.name, gi), lambda: text_img(g.get("text", "24 HORAS"), 110, "gold"))
    paste(frame, lab, W / 2, cy + r + 130, pop(lt - 0.3), a)


def gx_split_price(P, frame, g, gi, t, lt, total, a):
    """Total price versus the same price split into instalments."""
    y = g.get("y", 760)
    pnl = cached(("sp", P.name, gi), lambda: panel(920, 560))
    paste(frame, pnl, W / 2, y + 40, 1.0, a)
    l1 = cached(("sp1", P.name, gi), lambda: text_img("PRECIO TOTAL", 44, "grey", path=F_XB, shadow=False))
    paste(frame, l1, W / 2, y - 170, 1.0, a)
    tot = cached(("sp2", P.name, gi), lambda: text_img(g["total"], 120, "white", shadow=False))
    paste(frame, tot, W / 2, y - 70, 1.0, a)
    ts = P.at(g["at_split"]) - g["t0"] if isinstance(g["at_split"], str) else g["at_split"]
    if lt >= ts:
        e = ease_out((lt - ts) / 0.4)
        eq = cached(("sp3", P.name, gi), lambda: text_img("=", 70, "grey", shadow=False))
        paste(frame, eq, W / 2, y + 40, e, a)
        cu = cached(("sp4", P.name, gi), lambda: text_img(g["split"], 96, "gold", shadow=False))
        paste(frame, cu, W / 2, y + 150, 0.9 + 0.1 * e, a * e)
        if g.get("foot"):
            ft = cached(("sp5", P.name, gi), lambda: text_img(g["foot"], 36, "grey", path=F_SEMI, shadow=False))
            paste(frame, ft, W / 2, y + 250, 1.0, a * e)


def gx_list(P, frame, g, gi, t, lt, total, a):
    """Numbered decisions that light up as they are spoken."""
    items = g["items"]
    y0 = g.get("y", 470)
    pnl = cached(("lp", P.name, gi), lambda: panel(940, 130 * len(items) + 70))
    paste(frame, pnl, W / 2, y0 + 65 * (len(items) - 1) + 0, 1.0, a)
    for i, (txt, anchor) in enumerate(items):
        ta = P.at(anchor)
        on = t >= ta
        im = cached(("li", P.name, gi, i, on), lambda: text_img(f"{i + 1}  {txt}", 58, "gold" if on else "grey",
                                                                path=F_BLACK if on else F_XB, shadow=False))
        fit = min(1.0, 820 / im.width)
        sc = (1 + 0.06 * math.exp(-(t - ta) * 8) if on else 1.0) * fit
        paste(frame, im, 140 + im.width * fit / 2, y0 + i * 130, sc, a if on else a * 0.55)


def gx_question(P, frame, g, gi, t, lt, total, a):
    """Closing call to comment: a question and two answer buttons."""
    q = cached(("q", P.name, gi), lambda: text_img(g["text"], g.get("size", 70), "white", path=F_BLACK))
    paste(frame, q, W / 2, g.get("y", 560), min(1.0, 980 / q.width) * (0.95 + 0.05 * ease_out(lt / 0.3)), a)
    opts = g.get("options", [])
    for i, o in enumerate(opts):
        b = cached(("qo", P.name, gi, i), lambda: chip(o, g.get("osize", 64), fg=BLACK if i == 0 else WHITE, bg=GOLD if i == 0 else GREY, pad=(40, 18)))
        x = W / 2 + (i - (len(opts) - 1) / 2) * 470
        paste(frame, b, x, g.get("y", 560) + 260, pop(lt - 0.25 - 0.12 * i), a)
    if g.get("sub"):
        s = cached(("qs", P.name, gi), lambda: text_img(g["sub"], 44, "gold", path=F_XB))
        paste(frame, s, W / 2, g.get("y", 560) + (420 if opts else 220), a, a)


def gx_coins(P, frame, g, gi, t, lt, total, a):
    """Stacks of gold coins that grow in steps (drawn, not photographed)."""
    stacks = g["stacks"]
    base_y = g.get("y", 1180)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    n = len(stacks)
    for i, (count, anchor) in enumerate(stacks):
        ta = P.at(anchor) if isinstance(anchor, str) else g["t0"] + anchor
        if t < ta:
            continue
        shown = min(count, int((t - ta) / 0.05) + 1)
        cx = W / 2 + (i - (n - 1) / 2) * 200
        for c in range(shown):
            y = base_y - c * 22
            d.ellipse([cx - 70, y - 20, cx + 70, y + 20], fill=GOLD_D + (int(255 * a),))
            d.ellipse([cx - 70, y - 28, cx + 70, y + 12], fill=GOLD + (int(255 * a),), outline=GOLD_L + (int(255 * a),), width=3)
    frame.alpha_composite(ov)


def gx_vignette_dark(P, frame, g, gi, t, lt, total, a):
    frame.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(g.get("amount", 150) * a))))


GFX_DRAW = dict(big=gx_big, label=gx_label, chip=gx_chip, counter=gx_counter, note=gx_note, price=gx_price, bar=gx_bar,
                steps=gx_steps, chart=gx_chart, compare=gx_compare, clock=gx_clock, split_price=gx_split_price,
                list=gx_list, question=gx_question, coins=gx_coins, dark=gx_vignette_dark)


# ---------------------------------------------------------------- captions, hook, finishing

def draw_captions(P, frame, t):
    for c in P.chunks:
        if not (c["t0"] <= t < c["t1"]):
            continue
        words = c["words"]
        size = 64
        f = font(F_BLACK, size)
        texts = [w["text"] for w in words]
        space = size * 0.27
        ws = [f.getbbox(x)[2] for x in texts]
        lines, cur, cw = [], [], 0
        for i, wd in enumerate(ws):
            if cur and cw + space + wd > 860:
                lines.append(cur)
                cur, cw = [], 0
            cw += (space if cur else 0) + wd
            cur.append(i)
        lines.append(cur)
        lines = lines[:2]
        lh = size * 1.18
        layer = Image.new("RGBA", (W, int(lh * len(lines) + 40)), (0, 0, 0, 0))
        mask_d = ImageDraw.Draw(layer)
        for li, line in enumerate(lines):
            lw = sum(ws[i] for i in line) + space * (len(line) - 1)
            x = (W - lw) / 2
            for i in line:
                said = words[i]["start"] - 0.03 <= t
                now = said and t < words[i]["end"] + 0.06
                col = GOLD_L if now else WHITE
                mask_d.text((x, 10 + li * lh), texts[i], font=f, fill=col + (255 if said else 120,),
                            stroke_width=6, stroke_fill=(0, 0, 0, 255 if said else 120))
                x += ws[i] + space
        lt = t - c["t0"]
        sc = 0.96 + 0.04 * ease_out(lt / 0.12)
        paste(frame, layer, W / 2, 1450, sc)


def draw_hook(P, frame, t):
    """Big title over the first seconds: the visual hook."""
    if t > 3.2:
        return
    a = clamp01((3.2 - t) / 0.3)
    l1, l2 = P.hook
    im1 = cached(("h1", P.name), lambda: text_img(l1, 76, "white", track=3))
    im2 = cached(("h2", P.name), lambda: text_img(l2, 112, "gold", track=2))
    paste(frame, im1, W / 2, 330, min(1.0, 980 / im1.width) * (0.94 + 0.06 * ease_out(t / 0.4)), a * clamp01(t / 0.15))
    paste(frame, im2, W / 2, 450, min(1.0, 990 / im2.width) * (0.94 + 0.06 * ease_out((t - 0.15) / 0.4)),
          a * clamp01((t - 0.15) / 0.15))


_vig = _grain = None


def finish(P, arr, t, fi):
    global _vig, _grain
    if _vig is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
        _vig = np.clip(1 - 0.45 * r ** 2.4, 0.35, 1)[..., None].astype(np.float32)
        rs = np.random.RandomState(9)
        _grain = [np.repeat(np.repeat(rs.normal(0, 1, (H // 2, W // 2)).astype(np.float32), 2, 0), 2, 1)[..., None] for _ in range(5)]
    x = arr * 255.0 * _vig + _grain[fi % 5] * 3.5
    # soft dip at the reveal
    if P.reveal is not None and 0 <= t - P.reveal < 0.35:
        k = 1 - (t - P.reveal) / 0.35
        x = x + (255 - x) * 0.35 * k
    return np.clip(x, 0, 255).astype(np.uint8)


def camera_punch(P, img, t):
    amp = 0.0
    for h in P.hits:
        if 0 <= t - h < 0.5:
            amp = max(amp, 0.045 * (1 - (t - h) / 0.5) ** 2)
    if amp <= 0.002:
        return img
    k = 1 / (1 + amp)
    return img.transform((W, H), Image.AFFINE, (k, 0, (W - W * k) / 2, 0, k, (H - H * k) / 2), Image.BILINEAR)


def render_frame(P, fi):
    t = fi / FPS
    base = camera_punch(P, draw_base(P, t), t)
    frame = Image.fromarray((grade(base) * 255).astype(np.uint8)).convert("RGBA")
    # darken the caption area and top for legibility
    frame.alpha_composite(cached("grad", gradient_overlay))
    draw_gfx(P, frame, t)
    draw_hook(P, frame, t)
    if t < P.voice_end + 0.6:
        draw_captions(P, frame, t)
    arr = np.asarray(frame.convert("RGB")).astype(np.float32) / 255.0
    return finish(P, arr, t, fi)


def gradient_overlay():
    y = np.linspace(0, 1, H)
    a = np.clip((y - 0.62) / 0.3, 0, 1) ** 1.4 * 170 + np.clip((0.16 - y) / 0.16, 0, 1) * 110
    im = np.zeros((H, W, 4), np.uint8)
    im[..., 3] = a[:, None].astype(np.uint8)
    return Image.fromarray(im, "RGBA")


# ---------------------------------------------------------------- audio

SR = 44100


def _bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)


def _lp(x, f, o=2):
    return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)


def _hp(x, f, o=2):
    return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)


def _add(buf, sig, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i < 0:
        sig, i = sig[-i:], 0
    j = min(len(buf), i + len(sig))
    if j <= i:
        return
    buf[i:j, 0] += sig[: j - i] * g * (1 - max(0, pan))
    buf[i:j, 1] += sig[: j - i] * g * (1 + min(0, pan))


def _midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def music(P, rng):
    """Cinematic documentary bed: pads, a piano ostinato, a sub pulse and a soft clock tick."""
    n = int((P.END + 1) * SR)
    buf = np.zeros((n, 2))
    bpm = 84
    beat = 60 / bpm
    bar = beat * 4
    key = 45 + P.music_key  # A minor family
    prog = [[0, 3, 7, 10], [-4, 0, 3, 7], [-7, -3, 0, 5], [-5, -1, 2, 7]]  # i7 VI III VII-ish voicings
    nbars = int(P.END / bar) + 2
    t_all = np.arange(int(bar * SR)) / SR
    for b in range(nbars):
        ch = prog[b % 4]
        t0 = b * bar
        # pad: detuned saws, slow attack, filtered
        pad = np.zeros_like(t_all)
        for iv in ch:
            for det in (-0.12, 0.12):
                f = _midi(key + 12 + iv) * (1 + det / 100)
                pad += 2 * ((t_all * f) % 1) - 1
        env = np.minimum(1, t_all / 0.9) * np.minimum(1, (bar - t_all) / 0.4)
        pad = _lp(pad * env, 1400) * 0.05
        _add(buf, pad, t0, 1.0, -0.2)
        _add(buf, pad, t0 + 0.012, 0.8, 0.25)
        # piano ostinato on eighths
        for e in range(8):
            note = key + 24 + ch[[0, 2, 1, 3, 2, 1, 3, 2][e]]
            nn = int(1.2 * SR)
            tt = np.arange(nn) / SR
            f = _midi(note)
            tone = (np.sin(2 * np.pi * f * tt) * 0.6 + np.sin(2 * np.pi * 2 * f * tt) * 0.2 * np.exp(-tt * 5)
                    + np.sin(2 * np.pi * 3 * f * tt) * 0.06 * np.exp(-tt * 9)) * np.exp(-tt * 3.2)
            vel = 0.75 + 0.25 * rng.rand()
            _add(buf, tone * 0.06 * vel, t0 + e * beat / 2 + rng.randn() * 0.004, 1.0, 0.3 if e % 2 else -0.3)
        # sub pulse on beats 1 and 3 after the hook
        if t0 > 2.5:
            for bb in (0, 2):
                nn = int(0.5 * SR)
                tt = np.arange(nn) / SR
                sub = np.sin(2 * np.pi * np.cumsum(45 + 40 * np.exp(-tt * 30)) / SR) * np.exp(-tt * 6)
                _add(buf, sub * 0.22, t0 + bb * beat)
            # clock tick on sixteenths, very quiet
            for s in range(16):
                nn = int(0.03 * SR)
                tick = _hp(rng.randn(nn), 6000) * np.exp(-np.arange(nn) / SR * 180)
                _add(buf, tick * (0.03 if s % 4 else 0.05), t0 + s * beat / 4, 1.0, 0.4)
    # swell into the reveal
    if P.reveal is not None:
        a, b = int((P.reveal - 2.0) * SR), int(P.reveal * SR)
        buf[a:b] *= np.linspace(1, 1.25, b - a)[:, None]
    fade = int(1.2 * SR)
    end = int(P.END * SR)
    buf[end - fade:end] *= np.linspace(1, 0, fade)[:, None]
    buf[end:] = 0
    return buf


def sfx(P, rng):
    n = int((P.END + 1) * SR)
    buf = np.zeros((n, 2))

    def whoosh(d=0.35):
        nn = int(d * SR)
        x = rng.randn(nn)
        out = np.zeros(nn)
        for i in range(0, nn, 512):
            fc = 300 + 3500 * (i / nn)
            out[i:i + 512] = _bp(x[i:i + 512], fc * 0.7, fc * 1.4, 1)
        return out * np.sin(np.pi * np.linspace(0, 1, nn)) ** 1.6

    def hit():
        nn = int(1.4 * SR)
        tt = np.arange(nn) / SR
        s = np.sin(2 * np.pi * np.cumsum(36 + 60 * np.exp(-tt * 14)) / SR) * np.exp(-tt * 2.8)
        s += _lp(rng.randn(nn), 700) * np.exp(-tt * 7) * 0.4
        return np.tanh(s * 1.5)

    def tick():
        nn = int(0.02 * SR)
        return _bp(rng.randn(nn), 2500, 8000) * np.exp(-np.arange(nn) / SR * 260)

    def chime():
        nn = int(1.2 * SR)
        tt = np.arange(nn) / SR
        return sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * k) for f, a, k in ((1568, .5, 3), (2349, .3, 4), (3136, .2, 6)))

    def riser(d):
        nn = int(d * SR)
        tt = np.arange(nn) / SR
        return (_hp(rng.randn(nn), 2500) * 0.6 + np.sin(2 * np.pi * np.cumsum(150 * 6 ** (tt / d)) / SR) * 0.3) * (tt / d) ** 2

    for s in P.shots[1:]:
        _add(buf, whoosh(0.3), s[0] - 0.15, 0.10)
    for g in P.gfx:
        if g["kind"] in ("big", "chip", "compare", "price", "bar", "clock", "split_price", "question"):
            _add(buf, whoosh(0.25), g["t0"] - 0.08, 0.14)
        if g["kind"] == "counter":
            run = g.get("run", min(1.6, (g["t1"] - g["t0"]) * 0.7))
            tt = g["t0"]
            while tt < g["t0"] + run:
                _add(buf, tick(), tt, 0.12)
                tt += 0.035 + 0.08 * (tt - g["t0"]) / run
            _add(buf, chime(), g["t0"] + run, 0.18)
        if g["kind"] == "steps":
            for _, an in g["items"]:
                _add(buf, chime(), P.at(an) if isinstance(an, str) else an, 0.12)
        if g["kind"] == "clock":
            for k in range(12):
                _add(buf, tick(), g["t0"] + k * 0.18, 0.2)
    for h in P.hits:
        _add(buf, hit(), h, 0.35)
    if P.reveal is not None:
        _add(buf, riser(1.8), P.reveal - 1.8, 0.16)
        _add(buf, hit(), P.reveal, 0.5)
    return buf


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def build_audio(P, build):
    rng = np.random.RandomState(abs(hash(P.name)) % 2 ** 31)
    m = music(P, rng)
    fx = sfx(P, rng)
    write_wav(os.path.join(build, "music.wav"), m / np.abs(m).max() * 0.9)
    write_wav(os.path.join(build, "sfx.wav"), fx / max(1e-9, np.abs(fx).max()) * 0.9)
    flt = ("[0:a]aresample=44100,highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=90,"
           "equalizer=f=3000:t=q:w=1:g=1.5,apad=pad_dur=3,asplit=2[v][vsc];"
           "[1:a]volume=0.22[m];[m][vsc]sidechaincompress=threshold=0.025:ratio=6:attack=15:release=320[md];"
           "[2:a]volume=0.5[fx];[v][md][fx]amix=inputs=3:normalize=0:duration=longest,"
           "loudnorm=I=-14:TP=-1.0:LRA=8[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(P.folder, "narracion.mp3"),
                    "-i", os.path.join(build, "music.wav"), "-i", os.path.join(build, "sfx.wav"),
                    "-filter_complex", flt, "-map", "[out]", "-ar", "48000", "-t", f"{P.END:.3f}",
                    os.path.join(build, "mix.wav")], check=True)


# ---------------------------------------------------------------- SRT and thumbnail

def write_srt(P):
    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    out = []
    for i, c in enumerate(P.chunks, 1):
        nxt = P.chunks[i]["t0"] if i < len(P.chunks) else None
        t1 = min(c["t1"], nxt - 0.001) if nxt is not None else c["t1"]
        words = [w["text"] for w in c["words"]]
        text = " ".join(words)
        if len(text) > 32:  # two lines at most, split near the middle
            best = min(range(1, len(words)), key=lambda k: abs(len(" ".join(words[:k])) - len(text) / 2))
            text = " ".join(words[:best]) + "\n" + " ".join(words[best:])
        out.append(f"{i}\n{ts(max(0, c['t0']))} --> {ts(t1)}\n{text}\n")
    open(os.path.join(P.folder, "subtitulos.srt"), "w").write("\n".join(out))


def write_thumbnail(P):
    th = P.thumb
    img = cover(big(th["img"]), 1.05, th.get("pan", (0, 0)))
    arr = grade(img)
    frame = Image.fromarray((arr * 255).astype(np.uint8)).convert("RGBA")
    frame.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    frame.alpha_composite(gradient_overlay())
    y = np.linspace(0, 1, H)
    band = np.zeros((H, W, 4), np.uint8)
    band[..., 3] = (np.clip(1 - np.abs(y - th.get("y", 0.30)) / 0.22, 0, 1) ** 1.2 * 190)[:, None].astype(np.uint8)
    frame.alpha_composite(Image.fromarray(band, "RGBA"))
    l1, l2 = th["lines"]
    im1 = text_img(l1, 120, "white", track=3)
    im2 = text_img(l2, 150, "gold", track=2)
    cy = int(H * th.get("y", 0.30))
    paste(frame, im1, W / 2, cy - 90, min(1.0, 1000 / im1.width))
    paste(frame, im2, W / 2, cy + 70, min(1.0, 1010 / im2.width))
    d = ImageDraw.Draw(frame)
    d.rectangle([W / 2 - 160, cy + 200, W / 2 + 160, cy + 208], fill=GOLD)
    frame.convert("RGB").save(os.path.join(P.folder, "miniatura.png"))


# ---------------------------------------------------------------- main

_P = None


def _init(folder):
    global _P
    _P = Project(folder)


def _render_range(args):
    a, b, path = args
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "15", "-pix_fmt", "yuv420p", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(render_frame(_P, fi).tobytes())
    p.stdin.close()
    p.wait()
    return path


def main():
    folder = sys.argv[1]
    P = Project(folder)
    build = os.path.join(ROOT, "build", folder)
    os.makedirs(build, exist_ok=True)
    if "--frames" in sys.argv:
        for s in sys.argv[sys.argv.index("--frames") + 1:]:
            Image.fromarray(render_frame(P, int(float(s) * FPS))).save(os.path.join(build, f"f_{s}.jpg"), quality=88)
        return
    write_srt(P)
    write_thumbnail(P)
    build_audio(P, build)
    if "--skip-video" in sys.argv:
        return
    total = int(round(P.END * FPS))
    step = 240
    jobs = [(s, min(total, s + step), os.path.join(build, f"part{s // step:03d}.mp4")) for s in range(0, total, step)]
    with Pool(4, initializer=_init, initargs=(folder,)) as pool:
        parts = pool.map(_render_range, jobs, chunksize=1)
    lst = os.path.join(build, "parts.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", os.path.join(build, "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-maxrate", "9M",
                    "-bufsize", "18M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", os.path.join(P.folder, "video_final.mp4")], check=True)
    print(folder, "->", os.path.join(P.folder, "video_final.mp4"), f"{P.END:.2f}s")


if __name__ == "__main__":
    main()
