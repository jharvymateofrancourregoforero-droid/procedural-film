"""Music bed, sound effects and final mix for "Gastos hormiga".

The beat (drums, bass, electric-piano chords) and every effect are synthesised
here with numpy, so the soundtrack uses no samples and no generative AI.
The voice is the ElevenLabs narration in audio/voz.mp3.
"""
import os
import subprocess
import wave

import numpy as np
from scipy.signal import butter, sosfilt

import timeline as T

SR = 44100
BPM = 100
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


# Am9 | Fmaj7 | Cmaj7 | G6  (one bar each)
CHORDS = [[57, 60, 64, 67, 71], [53, 57, 60, 64], [48, 55, 59, 64], [55, 59, 62, 64]]
ROOTS = [45, 41, 36, 43]
BASS_PAT = [(0, 3), (3, 1), (6, 2), (10, 2), (12, 1), (14, 2)]  # (16th step, length)
CHORD_HITS = [(0, 3), (6, 2), (10, 4)]


def section(t):
    """Arrangement driven by the narration."""
    if 26.68 <= t < 32.70:
        return "break"
    if 36.40 <= t < 38.70:
        return "stop"
    if 55.0 <= t < 59.5:
        return "soft"
    if t >= 63.9:
        return "end"
    return "full"


def music():
    buf = np.zeros((N, 2))
    K, S = kick(), snare()
    steps = int(LEN / STEP)
    for st in range(steps):
        t = st * STEP
        sec = section(t)
        bar, s16 = divmod(st, 16)
        chord = bar % 4
        hum = rng.randn() * 0.004
        vel = 0.85 + rng.rand() * 0.15
        swing = STEP * 0.12 if s16 % 2 else 0
        tt = t + swing + hum
        if sec in ("full", "soft"):
            if s16 in (0, 7, 10) or (s16 == 15 and bar % 2):
                add(buf, K, tt, 0.95 * vel)
            if s16 in (4, 12):
                add(buf, S, tt, 0.55 * vel, 0.05)
            if sec == "full":
                if s16 % 2 == 0:
                    add(buf, hat(s16 % 8 == 6), tt, (0.5 if s16 % 4 == 2 else 0.32) * vel, -0.25)
                add(buf, shaker(), tt, 0.5 * vel * (1.0 if s16 % 4 == 2 else 0.6), 0.3)
        if sec == "break" and t >= 30.0:  # snare roll building to the reveal
            rate = 4 if t < 31.2 else (2 if t < 32.1 else 1)
            if s16 % rate == 0:
                add(buf, S, tt, 0.15 + 0.4 * (t - 30.0) / 2.7, 0.0)
        if sec == "stop" and s16 == 0 and t < 37.6:
            add(buf, K, tt, 0.9)
        if sec in ("full", "soft", "break"):
            for ps, ln in BASS_PAT:
                if s16 == ps and sec != "break":
                    m = ROOTS[chord] + (12 if ps in (6, 14) else 0)
                    add(buf, bass_note(midi(m), ln * STEP * 0.95), tt, 0.55 * vel)
            for ps, ln in CHORD_HITS:
                if s16 == ps:
                    sig = epiano([midi(x) for x in CHORDS[chord]], ln * STEP + 0.25)
                    g = 0.55 if sec != "break" else 0.4
                    add(buf, sig, tt, g * vel, 0.15 if ps else -0.15)
    # filter sweep in the break: muffled pad opening up into the reveal
    a, b = int(26.68 * SR), int(32.75 * SR)
    seg = buf[a:b].copy()
    lo = np.stack([lp(seg[:, c], 600) for c in range(2)], 1)
    mix = np.linspace(1, 0.2, b - a)[:, None]
    buf[a:b] = lo * mix + seg * (1 - mix)
    # final hit and tail
    add(buf, K, 63.9, 1.0)
    add(buf, epiano([midi(x) for x in CHORDS[0]], 1.6), 63.9, 0.7)
    buf[int((T.END + 0.2) * SR):] *= 0
    return buf


# ---------- effects ----------

def whoosh(dur=0.32, up=True):
    n = int(dur * SR)
    x = rng.randn(n)
    out = np.zeros(n)
    blk = 512
    for i in range(0, n, blk):
        p = i / n
        fc = 400 + (5000 if up else 3000) * (p if up else 1 - p)
        out[i:i + blk] = bp(x[i:i + blk], fc * 0.7, min(fc * 1.4, 18000), 1)
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5
    return out * e * 1.6


def pop():
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 220
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 40) * 0.7


def boom():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t * 18)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 4)
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
    s[:m] += bp(rng.randn(m), 2000, 9000) * np.linspace(1, 0, m) * 0.8  # drawer clack
    m2 = int(0.12 * SR)
    s[:m2] += np.sin(2 * np.pi * 90 * t[:m2]) * np.exp(-t[:m2] * 30) * 0.8
    return s * 0.6


def tick():
    n = int(0.02 * SR)
    return bp(rng.randn(n), 2500, 8000) * env_exp(n, 250) * 0.5


def shutter():
    s = np.zeros(int(0.12 * SR))
    for o, g in ((0, 1.0), (0.055, 0.7)):
        k = int(o * SR)
        m = int(0.018 * SR)
        s[k:k + m] += bp(rng.randn(m), 1500, 9000) * np.linspace(1, 0, m) * g
    return s * 0.8


def riser(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 200 * (8 ** (t / dur))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    nz = hp(rng.randn(n), 3000) * 0.3
    return (tone + nz) * (t / dur) ** 2


def thud():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-t * 40)) / SR) * env_exp(n, 12)
    s[:300] += rng.randn(300) * np.linspace(0.8, 0, 300)
    return s


def effects():
    buf = np.zeros((N, 2))
    for s in T.SHOTS[1:]:
        t0, mode, opt = s[0], s[2], s[3]
        if opt.get("whip"):
            add(buf, whoosh(0.3), t0 - 0.16, 0.45, 0.0)
        elif mode == "card":
            add(buf, shutter(), t0, 0.35, 0.2)
        else:
            add(buf, whoosh(0.18, up=False), t0 - 0.05, 0.18)
    for g in T.GFX:
        if g["kind"] in ("sticker", "title", "badge", "big"):
            add(buf, pop(), g["t0"], 0.35, 0.1)
        if g["kind"] == "counter":
            t = g["t0"]
            while t < g["t1"]:
                add(buf, tick(), t, 0.25)
                p = (t - g["t0"]) / (g["t1"] - g["t0"])
                t += 0.03 + 0.09 * p
            add(buf, kaching(), g["t1"], 0.55)
        if g["kind"] == "stamp":
            add(buf, thud(), g["t0"], 0.7)
    for h in (3.80, 7.08, 32.77, 37.60):
        add(buf, boom(), h, 0.55)
    add(buf, riser(2.7), 30.05, 0.35)
    add(buf, riser(1.2), 25.5, 0.2)
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
    m = m / np.abs(m).max() * 0.9
    fx = effects()
    fx = fx / max(1e-9, np.abs(fx).max()) * 0.9
    write_wav(os.path.join(out, "music.wav"), m)
    write_wav(os.path.join(out, "sfx.wav"), fx)
    voice = os.path.join(T.ROOT, "audio", "voz.mp3")
    # Voice up front; music ducks under it (sidechain); effects on top. Then loudness to -14 LUFS.
    flt = (
        "[0:a]aresample=44100,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
        "equalizer=f=3500:t=q:w=1:g=2.5,volume=1.0,asplit=2[v][vsc];"
        "[1:a]volume=0.42[m];"
        "[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=250[md];"
        "[2:a]volume=0.55[fx];"
        "[v][md][fx]amix=inputs=3:normalize=0:duration=longest,"
        "loudnorm=I=-14:TP=-1.0:LRA=9[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", os.path.join(out, "music.wav"),
                    "-i", os.path.join(out, "sfx.wav"), "-filter_complex", flt, "-map", "[out]",
                    "-ar", "48000", "-t", str(T.END), os.path.join(out, "mix.wav")], check=True)
    print("mix ->", os.path.join(out, "mix.wav"))


if __name__ == "__main__":
    main()
