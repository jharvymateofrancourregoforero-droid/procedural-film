"""Music bed, sound effects and final mix for "Top 10 formas de ganar dinero siendo adolescente".

The beat (drums, bass, electric-piano chords) and every effect are synthesised
here with numpy, so the soundtrack uses no samples and no generative AI.
The voice is the ElevenLabs narration, one file per block in audio/.
"""
import os
import subprocess
import wave

import numpy as np
from scipy.signal import butter, sosfilt

import timeline as T

SR = 44100
BPM = 96
BEAT = 60 / BPM
STEP = BEAT / 4
LEN = T.END + 0.6
N = int(LEN * SR)
rng = np.random.RandomState(11)


def env_exp(n, k):
    return np.exp(-np.arange(n) / SR * k)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def add(buf, sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= buf.shape[0] or i + len(sig) <= 0:
        return
    j = min(buf.shape[0], i + len(sig))
    s = sig[: j - i] * gain
    buf[i:j, 0] += s * (1 - max(0, pan))
    buf[i:j, 1] += s * (1 + min(0, pan))


# ---------- instruments ----------

def kick():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 48 + 95 * np.exp(-t * 38)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env_exp(n, 7.5)
    s[:120] += rng.randn(120) * np.linspace(0.6, 0, 120)
    return np.tanh(s * 1.6)


def snare():
    n = int(0.3 * SR)
    nz = bp(rng.randn(n), 1200, 7000) * env_exp(n, 17)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 185 * t) * env_exp(n, 30)
    clap = np.zeros(n)
    for o in (0, 0.011, 0.023):
        k = int(o * SR)
        m = int(0.02 * SR)
        clap[k:k + m] += bp(rng.randn(m), 900, 3500) * np.linspace(1, 0, m)
    return 0.8 * nz + 0.5 * body + 0.5 * clap


def hat(open_=False):
    n = int((0.28 if open_ else 0.06) * SR)
    return hp(rng.randn(n), 7000) * env_exp(n, 11 if open_ else 70) * 0.5


def shaker():
    n = int(0.07 * SR)
    e = np.minimum(1, np.arange(n) / (0.012 * SR)) * env_exp(n, 45)
    return bp(rng.randn(n), 4000, 9000) * e * 0.35


def bass_note(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) + 0.12 * np.sin(2 * np.pi * 3 * freq * t)
    e = np.minimum(1, t / 0.006) * np.exp(-t * 3.2)
    e[-200:] *= np.linspace(1, 0, 200)
    return np.tanh(s * e * 1.3) * 0.8


def epiano(freqs, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        f = f * (1 + rng.randn() * 0.0015)
        tone = np.sin(2 * np.pi * f * t) * 0.7 + np.sin(2 * np.pi * 2 * f * t) * 0.18 * np.exp(-t * 6)
        tone += np.sin(2 * np.pi * 7 * f * t) * 0.04 * np.exp(-t * 25)  # tine
        out += tone
    e = np.minimum(1, t / 0.004) * np.exp(-t * 2.2) * (1 + 0.12 * np.sin(2 * np.pi * 5 * t))
    e[-300:] *= np.linspace(1, 0, 300)
    return out * e / len(freqs)


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


# One progression per chapter, cycling; each is four bars.
PROGS = [
    ([[57, 60, 64, 67, 71], [53, 57, 60, 64], [48, 55, 59, 64], [55, 59, 62, 64]], [45, 41, 36, 43]),  # Am9 F C G6
    ([[50, 53, 57, 60, 64], [55, 59, 62, 65], [48, 52, 55, 59], [45, 52, 55, 60]], [38, 43, 36, 45]),  # Dm9 G7 Cmaj7 Am7
    ([[52, 55, 59, 62], [48, 52, 55, 59], [53, 57, 60, 64], [55, 59, 62, 66]], [40, 36, 41, 43]),      # Em7 Cmaj7 Fmaj7 G
    ([[53, 57, 60, 64], [55, 59, 62, 65], [52, 55, 59, 62], [57, 60, 64, 67]], [41, 43, 40, 45]),      # Fmaj7 G7 Em7 Am7
]
BASS_PAT = [(0, 3), (3, 1), (6, 2), (10, 2), (12, 1), (14, 2)]
CHORD_HITS = [(0, 3), (6, 2), (10, 4)]
SOFT_SEGS = {"reglas"}  # sober chapters: no hats, softer drums


def chapter_index(t):
    k = 0
    for i, c in enumerate([c for c in T.CARDS if c["kind"] == "chapter"]):
        if t >= c["t0"]:
            k = i + 1
    return k


def segment_at(t):
    cur = T.SEGMENTS[0][0]
    for seg, _ in T.SEGMENTS:
        if t >= T.OFFSET[seg] - 0.5:
            cur = seg
    return cur


def section(t):
    for c in T.CARDS:
        if c["kind"] == "chapter" and c["t0"] - 0.6 <= t < c["t1"]:
            return "card"
    if t >= T.END_SCREEN:
        return "end"
    return "soft" if segment_at(t) in SOFT_SEGS else "full"


def music():
    buf = np.zeros((N, 2))
    K, S = kick(), snare()
    steps = int(LEN / STEP)
    for st in range(steps):
        t = st * STEP
        sec = section(t)
        bar, s16 = divmod(st, 16)
        chords, roots = PROGS[chapter_index(t) % len(PROGS)]
        chord = bar % 4
        hum = rng.randn() * 0.004
        vel = 0.85 + rng.rand() * 0.15
        tt = t + (STEP * 0.12 if s16 % 2 else 0) + hum
        if sec in ("full", "soft", "end"):
            if s16 in (0, 7, 10) or (s16 == 15 and bar % 2):
                add(buf, K, tt, (0.9 if sec != "soft" else 0.7) * vel)
            if s16 in (4, 12):
                add(buf, S, tt, (0.5 if sec != "soft" else 0.32) * vel, 0.05)
            if sec != "soft":
                if s16 % 2 == 0:
                    add(buf, hat(s16 % 8 == 6), tt, (0.45 if s16 % 4 == 2 else 0.28) * vel, -0.25)
                add(buf, shaker(), tt, 0.4 * vel * (1.0 if s16 % 4 == 2 else 0.6), 0.3)
            for ps, ln in BASS_PAT:
                if s16 == ps:
                    m = roots[chord] + (12 if ps in (6, 14) else 0)
                    add(buf, bass_note(midi(m), ln * STEP * 0.95), tt, 0.5 * vel)
        if sec in ("full", "soft", "card", "end"):
            for ps, ln in CHORD_HITS:
                if s16 == ps:
                    g = 0.5 if sec != "card" else 0.35
                    add(buf, epiano([midi(x) for x in chords[chord]], ln * STEP + 0.3), tt, g * vel, 0.15 if ps else -0.15)
    # every chapter card: the beat drops out under a muffled pad, then a hit
    for c in [c for c in T.CARDS if c["kind"] == "chapter"]:
        a, b = int((c["t0"] - 0.6) * SR), int(c["t1"] * SR)
        seg = buf[a:b].copy()
        buf[a:b] = np.stack([lp(seg[:, ch], 700) for ch in range(2)], 1)
        add(buf, K, c["t0"], 1.0)
        add(buf, K, c["t1"], 0.9)
    tail = int((T.END - 1.5) * SR)
    buf[tail:] *= np.linspace(1, 0, N - tail)[:, None]
    return buf


def whoosh(dur=0.32, up=True):
    n = int(dur * SR)
    x = rng.randn(n)
    out = np.zeros(n)
    blk = 512
    for i in range(0, n, blk):
        p = i / n
        fc = 400 + (5000 if up else 3000) * (p if up else 1 - p)
        out[i:i + blk] = bp(x[i:i + blk], fc * 0.7, min(fc * 1.4, 18000), 1)
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5 * 1.6


def pop():
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 220
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 40) * 0.7


def boom():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t * 18)) / SR) * env_exp(n, 4)
    s += lp(rng.randn(n), 900) * env_exp(n, 10) * 0.6
    return np.tanh(s * 1.8) * 0.9


def kaching():
    n = int(1.1 * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for f, a, k in ((2093, 0.5, 4), (2637, 0.4, 5), (3136, 0.35, 6), (4186, 0.2, 8)):
        d = int(0.07 * SR) if f > 2500 else 0
        s[d:] += a * np.sin(2 * np.pi * f * t[: n - d]) * np.exp(-t[: n - d] * k)
    m = int(0.05 * SR)
    s[:m] += bp(rng.randn(m), 2000, 9000) * np.linspace(1, 0, m) * 0.8
    return s * 0.6


def tick():
    n = int(0.02 * SR)
    return bp(rng.randn(n), 2500, 8000) * env_exp(n, 250) * 0.5


def shutter():
    s = np.zeros(int(0.12 * SR))
    for o, g in ((0, 1.0), (0.055, 0.7)):
        k, m = int(o * SR), int(0.018 * SR)
        s[k:k + m] += bp(rng.randn(m), 1500, 9000) * np.linspace(1, 0, m) * g
    return s * 0.8


def riser(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * np.cumsum(200 * (8 ** (t / dur))) / SR) * 0.25
    return (tone + hp(rng.randn(n), 3000) * 0.3) * (t / dur) ** 2


def click():
    n = int(0.03 * SR)
    return bp(rng.randn(n), 1000, 6000) * env_exp(n, 160) * 0.9


def effects():
    buf = np.zeros((N, 2))
    for i, s in enumerate(T.SHOTS[1:], 1):
        t0, mode = s[0], s[2]
        if i % 4 == 0:
            add(buf, whoosh(0.3), t0 - 0.16, 0.4)
        elif mode != "full":
            add(buf, shutter(), t0, 0.3, 0.2)
        else:
            add(buf, whoosh(0.16, up=False), t0 - 0.04, 0.12)
    for g in T.GFX:
        k = g["kind"]
        if k in ("sticker", "title", "badge", "big", "side", "compare", "lower", "chips", "list", "formula"):
            add(buf, pop(), g["t0"], 0.3, 0.1)
        if k == "counter":
            run = min(2.2, (g["t1"] - g["t0"]) * 0.75)
            t = g["t0"]
            while t < g["t0"] + run:
                add(buf, tick(), t, 0.22)
                t += 0.03 + 0.09 * (t - g["t0"]) / run
            add(buf, kaching(), g["t0"] + run, 0.5)
        if k == "table":
            for _, _, anchor in g["rows"] + [g["total"]]:
                add(buf, pop(), T.at(*anchor), 0.25)
        if k == "subscribe":
            add(buf, click(), g["t0"] + 1.6, 0.6)
        if k in ("chapter", "maintitle"):
            add(buf, riser(1.2), g["t0"] - 1.2, 0.3)
            add(buf, boom(), g["t0"], 0.5)
            add(buf, whoosh(0.4), g["t1"] - 0.2, 0.35)
    for h in T.HITS:
        add(buf, boom(), h, 0.25)
    return buf


def voice():
    buf = np.zeros((N, 2))
    for seg, _ in T.SEGMENTS:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(T.ROOT, "audio", seg + ".mp3"),
                              "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
        add(buf, x, T.OFFSET[seg], 1.0)
    return buf


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def main():
    out = os.path.join(T.ROOT, "build")
    os.makedirs(out, exist_ok=True)
    m = music()
    write_wav(os.path.join(out, "music.wav"), m / np.abs(m).max() * 0.9)
    fx = effects()
    write_wav(os.path.join(out, "sfx.wav"), fx / max(1e-9, np.abs(fx).max()) * 0.9)
    v = voice()
    write_wav(os.path.join(out, "voice.wav"), v / np.abs(v).max() * 0.95)
    # Voice up front, music ducked under it, effects on top, then -14 LUFS for YouTube.
    flt = (
        "[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
        "equalizer=f=3500:t=q:w=1:g=2,asplit=2[v][vsc];"
        "[1:a]volume=0.30[m];"
        "[m][vsc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300[md];"
        "[2:a]volume=0.45[fx];"
        "[v][md][fx]amix=inputs=3:normalize=0:duration=longest,"
        "loudnorm=I=-14:TP=-1.0:LRA=9[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(out, "voice.wav"), "-i", os.path.join(out, "music.wav"),
                    "-i", os.path.join(out, "sfx.wav"), "-filter_complex", flt, "-map", "[out]",
                    "-ar", "48000", "-t", str(T.END), os.path.join(out, "mix.wav")], check=True)
    print("mix ->", os.path.join(out, "mix.wav"))


if __name__ == "__main__":
    main()
