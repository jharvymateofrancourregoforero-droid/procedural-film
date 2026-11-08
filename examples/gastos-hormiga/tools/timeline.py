"""Edit decision list for "Gastos hormiga".

Every time below comes from the ElevenLabs word timings in audio/words.json,
so cuts, captions, graphics and sound effects land on the spoken words.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
END = 65.4  # voice ends at 63.84, then the end card holds

# Shots: (start, photo, mode, options). A shot runs until the next one starts.
#   full: the photo fills the frame with a slow push and handheld drift
#   card: the photo sits on a tilted white-bordered card over its own blurred copy
SHOTS = [
    (0.00, "latte_art", "full", dict(z=(1.05, 1.18), pan=(0.0, -0.2))),
    (2.56, "hundred", "full", dict(z=(1.25, 1.05), pan=(0.3, -0.3), whip=True)),
    (5.40, "iced_girl", "full", dict(z=(1.0, 1.12), pan=(0.0, 0.2))),
    (7.04, "ant_leaf", "full", dict(z=(1.1, 1.3), pan=(-0.2, 0.0), flash=True)),
    (8.40, "ant1", "card", dict(rot=(-3, -1), z=(1.0, 1.08))),
    (9.36, "safari_ants", "card", dict(rot=(2.5, 1), z=(1.05, 1.15))),
    (10.45, "card_pay", "full", dict(z=(1.15, 1.0), pan=(0.4, -0.4), whip=True)),
    (12.52, "barista", "card", dict(rot=(-2, 0), z=(1.0, 1.1))),
    (13.60, "barista_latte", "full", dict(z=(1.0, 1.15), pan=(0.0, -0.3))),
    (15.25, "calc2", "card", dict(rot=(2, 0.5), z=(1.0, 1.1))),
    (17.90, "delivery", "full", dict(z=(1.0, 1.12), pan=(-0.5, 0.5), whip=True)),
    (19.58, "bamba", "full", dict(z=(1.15, 1.3), pan=(0.0, 0.0))),
    (20.90, "netflix_stream", "full", dict(z=(1.0, 1.1), pan=(-0.6, -0.2), whip=True)),
    (22.78, "mall_girl", "full", dict(z=(1.0, 1.1), pan=(0.0, 0.3))),
    (24.70, "woman_phone2", "full", dict(z=(1.1, 1.0), pan=(0.0, -0.2))),
    (26.68, "piggy_hand", "full", dict(z=(1.0, 1.2), pan=(0.2, 0.0), flash=True)),
    (28.05, "strap", "full", dict(z=(1.0, 1.15), pan=(0.4, -0.4))),
    (30.05, "money_coins", "card", dict(rot=(-2.5, -1), z=(1.0, 1.06))),
    (32.75, "piggy_cc0", "full", dict(z=(1.0, 1.2), pan=(0.0, 0.0), flash=True)),
    (36.45, "coins_euro", "full", dict(z=(1.0, 1.1), pan=(0.0, -0.3), whip=True)),
    (38.70, "hourglass", "card", dict(rot=(-2, -0.5), z=(1.0, 1.1))),
    (41.42, "woman_phone", "full", dict(z=(1.0, 1.12), pan=(0.0, -0.2))),
    (44.78, "apps", "card", dict(rot=(2, 0.5), z=(1.0, 1.1), whip=True)),
    (47.45, "remote", "card", dict(rot=(-2, -3), z=(1.0, 1.08))),
    (49.95, "journal", "card", dict(rot=(1.5, 0), z=(1.0, 1.1), whip=True)),
    (53.65, "notebook2", "card", dict(rot=(-2, -1), z=(1.05, 1.15))),
    (55.05, "friends1", "card", dict(rot=(2, 1), z=(1.0, 1.08))),
    (56.93, "cash2", "card", dict(rot=(-1.5, 0), z=(1.0, 1.12))),
    (59.50, "friends3", "card", dict(rot=(2, 0.5), z=(1.0, 1.08), flash=True)),
    (62.50, "coffee_cup", "card", dict(rot=(-2, -1), z=(1.0, 1.06))),
]

YEL, GRN, RED, WHT, INK = (255, 214, 10), (43, 217, 107), (255, 59, 48), (255, 255, 255), (12, 12, 12)

# Graphics. y is the vertical centre in pixels.
GFX = [
    dict(kind="sticker", t0=0.05, t1=2.56, text="¿CUÁNTO TE CUESTA\nTU CAFÉ?", color=YEL, y=340, rot=-3),
    dict(kind="big", t0=3.78, t1=5.40, text="+US$10.000", color=YEL, y=760, size=140),
    dict(kind="title", t0=7.06, t1=8.40, text="GASTOS\nHORMIGA", color=YEL, y=760, size=170, rot=-4),
    dict(kind="sticker", t0=8.50, t1=10.45, text="PEQUEÑITOS", color=WHT, y=330, rot=-3),
    dict(kind="sticker", t0=9.40, t1=10.45, text="INVISIBLES", color=YEL, y=440, rot=3),
    dict(kind="big", t0=14.24, t1=15.25, text="US$2 / día", color=WHT, y=520, size=140),
    dict(kind="counter", t0=15.45, t1=17.05, hold=17.90, a=0, b=730, fmt="US${:,}", label="AL AÑO", color=YEL, y=290, size=150),
    dict(kind="sticker", t0=18.25, t1=19.58, text="+ DOMICILIO", color=YEL, y=420, rot=-4),
    dict(kind="sticker", t0=19.70, t1=20.90, text="+ SNACK", color=YEL, y=420, rot=3),
    dict(kind="sticker", t0=21.15, t1=22.78, text="+ SUSCRIPCIÓN", color=YEL, y=420, rot=-3),
    dict(kind="sticker", t0=23.00, t1=26.68, text="OJO", color=RED, y=380, rot=-6, fg=WHT),
    dict(kind="title", t0=26.75, t1=28.05, text="AHORA VIENE\nLO BUENO", color=GRN, y=760, size=120, rot=-3),
    dict(kind="chart", t0=30.15, t1=32.70, y=300),
    dict(kind="sticker", t0=31.30, t1=32.75, text="+8% ANUAL", color=GRN, y=1215, rot=-3),
    dict(kind="counter", t0=33.00, t1=35.50, hold=36.45, a=0, b=10575, fmt="US${:,}", label="EN 10 AÑOS", color=GRN, y=700, size=176),
    dict(kind="note", t0=30.05, t1=36.45, text="Ejemplo: US$730 al año, 8% anual compuesto, 10 años.\nRendimiento no garantizado. No es asesoría financiera."),
    dict(kind="title", t0=37.60, t1=38.70, text="3 TRUCOS", color=YEL, y=760, size=190, rot=-3),
    dict(kind="badge", t0=38.75, t1=41.42, n="1", text="REGLA DE\nLAS 24 HORAS", y=300),
    dict(kind="sticker", t0=43.75, t1=44.78, text="ESPERA 1 DÍA", color=YEL, y=420, rot=-3),
    dict(kind="badge", t0=44.85, t1=47.45, n="2", text="REVISA TUS\nSUSCRIPCIONES", y=300),
    dict(kind="stamp", t0=48.84, t1=49.95, text="CANCELADA", color=RED, y=800, rot=-12),
    dict(kind="badge", t0=50.00, t1=53.65, n="3", text="ANOTA CADA\nGASTO 7 DÍAS", y=300),
    dict(kind="sticker", t0=57.70, t1=59.50, text="TU PLATA\nTRABAJA", color=GRN, y=330, rot=-3),
    dict(kind="title", t0=59.60, t1=62.50, text="MÁNDASELO A\nESE AMIGO", color=YEL, y=300, size=110, rot=-3),
    dict(kind="end", t0=63.90, t1=END, text="¿Cuánto gastas\ntú en café?", sub="Te leo en los comentarios"),
]

# Camera hits: short shake + chromatic split.
HITS = [3.80, 7.08, 17.05, 26.68, 32.77, 35.50, 37.60, 48.84, 59.52]

# Spoken numbers shown as figures in the captions.
MERGES = [
    (["diez", "mil", "dólares?"], "US$10.000?"),
    (["dos", "dólares"], "US$2"),
    (["setecientos", "treinta", "dólares"], "US$730"),
    (["ocho", "por", "ciento..."], "8%..."),
    (["diez", "años"], "10 años"),
    (["diez", "mil", "quinientos", "dólares!"], "US$10.500!"),
    (["veinticuatro", "horas."], "24 horas."),
]


def load_words():
    words = json.load(open(os.path.join(ROOT, "audio", "words.json")))["words"]
    words = [w for w in words if not re.fullmatch(r"\[.*\]", w["text"])]
    out, i = [], 0
    while i < len(words):
        for seq, rep in MERGES:
            got = [words[i + k]["text"].lower().strip('¡¿"') for k in range(len(seq)) if i + k < len(words)]
            if got == [s.lower() for s in seq]:
                lead = "¡" if words[i]["text"].startswith("¡") else ""
                out.append(dict(text=lead + rep, start=words[i]["start"], end=words[i + len(seq) - 1]["end"]))
                i += len(seq)
                break
        else:
            out.append(dict(text=words[i]["text"], start=words[i]["start"], end=words[i]["end"]))
            i += 1
    return out


def caption_chunks():
    toks = load_words()
    chunks, cur = [], []
    for j, t in enumerate(toks):
        cur.append(t)
        nxt = toks[j + 1] if j + 1 < len(toks) else None
        # Up to three words, or four when the fourth closes the phrase.
        closes_next = nxt is not None and re.search(r'[.,?!:…"]$', nxt["text"]) and len(cur) == 3
        brk = (re.search(r'[.,?!:…"]$', t["text"]) or (len(cur) >= 3 and not closes_next) or len(cur) >= 4
               or nxt is None or nxt["start"] - t["end"] > 0.3)
        if brk:
            chunks.append(cur)
            cur = []
    out = []
    for k, c in enumerate(chunks):
        t0 = c[0]["start"] - 0.04
        t1 = chunks[k + 1][0]["start"] - 0.04 if k + 1 < len(chunks) else c[-1]["end"] + 0.4
        out.append(dict(t0=t0, t1=min(t1, c[-1]["end"] + 0.6), words=c))
    return out


def shot_at(t):
    idx = 0
    for i, s in enumerate(SHOTS):
        if t >= s[0]:
            idx = i
    start = SHOTS[idx][0]
    end = SHOTS[idx + 1][0] if idx + 1 < len(SHOTS) else END
    return idx, start, end
