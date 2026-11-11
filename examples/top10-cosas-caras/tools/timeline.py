"""Edit decision list for "Top 10 cosas más caras que se han comprado" (El Precio del Poder, 16:9).

Cuts and graphics are anchored to phrases of the narration (ElevenLabs word timings in audio/).
The slogan block plays as the channel sting; every ranked item opens with a rank card.
"""
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1920, 1080, 30

# (block, card). card = (rank, title) shown before the block; "sting" = channel slogan over its own block.
# (block, card). card = (rank, title) shown before the block; "sting" = channel slogan over its own block.
SEGMENTS = [
    ("intro", None),
    ("slogan", "sting"),
    ("p10", ("10", "UNA PLUMA\nDE HUIA")),
    ("p09", ("9", "UNA BOTELLA\nDE VINO")),
    ("p08", ("8", "UNA\nESTAMPILLA")),
    ("p07", ("7", "UNA CÁMARA\nLEICA")),
    ("p06", ("6", "UN RELOJ\nPATEK PHILIPPE")),
    ("p05", ("5", "EL CÓDICE\nSASSOON")),
    ("p04", ("4", "UN DINOSAURIO")),
    ("p03", ("3", "EL DIAMANTE\nPINK STAR")),
    ("p02", ("2", "MERCEDES-BENZ\n300 SLR")),
    ("p01", ("1", "SALVATOR\nMUNDI")),
    ("cierre", ("", "LA LECCIÓN")),
]
CARD_LEN, END_LEN = 2.6, 18.0
STING_BG, END_BG = "gold_bars", "gallery"
END_HEAD = "¿Cuál te pareció más loco?"
END_SUB = "El dinero se gana... y el poder se aprende"


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def _load(seg):
    words = json.load(open(os.path.join(ROOT, "audio", f"words_{seg}.json")))["words"]
    return [w for w in words if not re.fullmatch(r"\[.*\]", w["text"])]


WORDS = {s: _load(s) for s, _ in SEGMENTS}
DUR = {s: WORDS[s][-1]["end"] for s, _ in SEGMENTS}

OFFSET, CARDS = {}, []
_t = 0.3
for i, (seg, card) in enumerate(SEGMENTS):
    if card == "sting":
        _t += 0.5
        OFFSET[seg] = _t
        CARDS.append(dict(kind="maintitle", t0=_t - 0.3, t1=_t + DUR[seg] + 0.6))
        _t += DUR[seg] + 0.9
        continue
    if card:
        CARDS.append(dict(kind="chapter", n=card[0], text=card[1], t0=_t + 0.25, t1=_t + 0.25 + CARD_LEN))
        _t += 0.25 + CARD_LEN + 0.2
    elif i:
        _t += 0.5
    OFFSET[seg] = _t
    _t += DUR[seg]
END_SCREEN = _t + 0.6
END = END_SCREEN + END_LEN


def at(seg, phrase, nth=0, end=False):
    ws = WORDS[seg]
    key = [_norm(x) for x in phrase.split()]
    found = 0
    for i in range(len(ws) - len(key) + 1):
        if all(_norm(ws[i + k]["text"]) == key[k] for k in range(len(key))):
            if found == nth:
                w = ws[i + len(key) - 1] if end else ws[i]
                return OFFSET[seg] + (w["end"] if end else w["start"])
            found += 1
    raise KeyError(f"{seg}: '{phrase}' not found")


SLOGAN = [("Aquí el dinero se gana...", ("slogan", "Aquí el dinero")), ("...y el poder se aprende", ("slogan", "y el poder"))]

_EDIT = [
    # Gancho
    ("intro", "Una pluma que vale", "huia_feather", "card", {}),
    ("intro", "más que su peso", "gold_bars", "full", {}),
    ("intro", "Una botella de vino", "wine_bottles", "full", {}),
    ("intro", "más que por una casa", "cellar1", "full", {}),
    ("intro", "Y una pintura", "salvator", "card", {}),
    ("intro", "Hoy te traigo", "auction_daumier", "full", {}),
    ("intro", "con récords confirmados", "gallery", "full", {}),
    ("intro", "Y al final", "museum_man", "full", {}),
    ("intro", "porque ahí está", "cash_hands", "full", {}),
    # Slogan: shot under the sting
    ("slogan", "Muy buenas", "gold_bars", "full", {}),
    # 10 · Pluma de huia
    ("p10", "Número diez", "feather", "full", {}),
    ("p10", "Sí una sola pluma", "feather_hand", "full", {}),
    ("p10", "En mayo de dos", "huia_feather", "card", {}),
    ("p10", "se vendió en Nueva Zelanda", "huia_head", "full", {}),
    ("p10", "unos veintiocho mil", "huia_specimen", "right", {}),
    ("p10", "El huia era", "feather", "full", {"z": (1.2, 1.0)}),
    ("p10", "y se extinguió", "huia_head", "full", {"z": (1.25, 1.05)}),
    ("p10", "Por eso cada pluma", "huia_feather", "left", {}),
    ("p10", "Gramo por gramo", "gold_bars", "full", {}),
    # 9 · Romanée-Conti 1945
    ("p09", "Número nueve", "wine_bottles2", "full", {}),
    ("p09", "una botella de Romané", "vosne_village", "card", {}),
    ("p09", "se subastó en Nueva York", "wine_cellar", "full", {}),
    ("p09", "Es el vino más caro", "cellar3", "full", {}),
    ("p09", "Por qué tanto", "cellar2", "full", {}),
    ("p09", "y fue la última", "vosne_village", "full", {}),
    ("p09", "Cada botella que alguien", "wine_open", "full", {}),
    # 8 · One Cent Magenta
    ("p08", "Número ocho", "stamp", "card", {}),
    ("p08", "Un pedacito de papel", "stamp", "left", {}),
    ("p08", "Cuando salió", "coins", "full", {}),
    ("p08", "Y en dos mil veintiuno", "auction_daumier", "full", {}),
    ("p08", "La razón", "stamp", "card", {}),
    ("p08", "Y cuando algo es único", "gallery_red", "full", {}),
    # 7 · Leica 0-series nº 105
    ("p07", "Número siete", "urleica", "full", {}),
    ("p07", "Una Leica de la serie", "urleica2", "card", {}),
    ("p07", "Esta en particular", "urleica", "right", {}),
    ("p07", "perteneció a Oskar Barnack", "barnack_plaque", "card", {}),
    ("p07", "En dos mil veintidós", "auction_room", "full", {}),
    ("p07", "unos quince millones", "museum_man", "full", {}),
    ("p07", "Esperaban venderla", "urleica2", "full", {}),
    ("p07", "y terminó costando", "urleica", "card", {}),
    # 6 · Patek Philippe Grandmaster Chime
    ("p06", "Número seis", "watch_fashion", "full", {}),
    ("p06", "El Patek Philippe", "patek_hq", "card", {}),
    ("p06", "Tiene veinte funciones", "watch_clock", "full", {}),
    ("p06", "Y solo existe uno", "watch_plane", "full", {}),
    ("p06", "En dos mil diecinueve", "auction_daumier", "full", {}),
    ("p06", "Y sabes qué es", "gallery", "full", {}),
    ("p06", "Era una subasta", "museum_man", "full", {}),
    ("p06", "el dinero fue para", "dollars", "full", {}),
    # 5 · Códice Sassoon
    ("p05", "Número cinco", "codex_sassoon", "card", {}),
    ("p05", "la Biblia hebrea", "codex_sassoon", "left", {}),
    ("p05", "En dos mil veintitrés", "auction_room", "full", {}),
    ("p05", "el manuscrito más caro", "codex_sassoon", "full", {"z": (1.0, 1.25)}),
    ("p05", "Lo compró un exembajador", "gallery_red", "full", {}),
    ("p05", "y lo donó", "museum_man", "full", {}),
    # 4 · Stegosaurus "Apex"
    ("p04", "Número cuatro", "apex1", "full", {}),
    ("p04", "Un esqueleto de estegosaurio", "apex2", "card", {}),
    ("p04", "al que llamaron Apex", "apex1", "full", {"z": (1.15, 1.0)}),
    ("p04", "Lo encontraron", "apex3", "card", {}),
    ("p04", "La casa de subastas", "apex2", "full", {}),
    ("p04", "pero en julio", "cash_hands", "full", {}),
    ("p04", "el multimillonario Ken", "dollars", "full", {}),
    ("p04", "Es el fósil más caro", "apex1", "full", {}),
    # 3 · Pink Star
    ("p03", "Número tres", "diamond_rose", "full", {}),
    ("p03", "El Pink Star", "pink_ring", "full", {}),
    ("p03", "En bruto pesaba", "diamond_gems", "full", {}),
    ("p03", "y tardaron dos años", "diamond_ring", "full", {}),
    ("p03", "En dos mil diecisiete", "hk_night", "full", {}),
    ("p03", "la joya más cara", "pink_ring", "full", {"z": (1.2, 1.0)}),
    ("p03", "Su comprador", "hk_day", "full", {}),
    # 2 · Mercedes-Benz 300 SLR Uhlenhaut Coupé
    ("p02", "Número dos", "car_red", "full", {}),
    ("p02", "Es un Mercedes-Benz", "slr_front", "full", {}),
    ("p02", "de mil novecientos cincuenta", "slr_side", "full", {}),
    ("p02", "Solo se fabricaron dos", "slr_gullwing", "full", {}),
    ("p02", "En mayo de dos", "slr_profile", "full", {}),
    ("p02", "unos ciento cuarenta", "mercedes_wheel", "full", {}),
    ("p02", "Superó el récord", "slr_doors", "full", {}),
    ("p02", "Es el carro más caro", "slr_museum", "full", {}),
    # 1 · Salvator Mundi
    ("p01", "Y el número uno", "gallery", "full", {}),
    ("p01", "El Salvator Mundi", "salvator", "card", {}),
    ("p01", "Una pintura de Jesús", "salvator_face", "full", {}),
    ("p01", "En noviembre de dos", "auction_daumier", "full", {}),
    ("p01", "por cuatrocientos cincuenta", "museum_man", "full", {}),
    ("p01", "Es la obra de arte", "salvator", "full", {"z": (1.0, 1.2)}),
    ("p01", "Lo más raro", "gallery_red", "full", {}),
    ("p01", "Desde ese día", "salvator_face", "full", {"z": (1.2, 1.0)}),
    # Cierre
    ("cierre", "Y qué tienen", "museum_man", "full", {}),
    ("cierre", "Uno son escasas", "stamp", "card", {}),
    ("cierre", "Dos tienen una historia", "urleica", "card", {}),
    ("cierre", "Y tres hubo alguien", "auction_daumier", "full", {}),
    ("cierre", "Porque al final", "salvator_face", "full", {}),
    ("cierre", "Y esa misma regla", "cash_hands", "full", {}),
    ("cierre", "Lo escaso vale más", "gold_bars", "full", {}),
    ("cierre", "Por eso la habilidad", "dollars", "full", {}),
    ("cierre", "Ahora dime", "apex1", "full", {}),
    ("cierre", "Suscríbete y activa", "coins", "full", {}),
    ("cierre", "Esto fue El Precio", "gold_bars", "full", {}),
]
# The first photo of every block enters with the block's first word.
_first = {}
for seg, ph, img, mode, opt in _EDIT:
    _first.setdefault(seg, ph)
SHOTS = sorted([((OFFSET[seg] - 0.05) if ph == _first[seg] else (at(seg, ph) - 0.05), img, mode, opt)
                for seg, ph, img, mode, opt in _EDIT], key=lambda s: s[0])
SHOTS[0] = (0.0,) + SHOTS[0][1:]

YEL, GRN, RED, WHT, INK, BLU = (255, 214, 10), (43, 217, 107), (255, 69, 58), (255, 255, 255), (12, 12, 12), (90, 170, 255)


def g(kind, seg, phrase, until=None, until_end=False, **kw):
    t0 = at(seg, phrase)
    if until is None:
        t1 = t0 + kw.pop("dur", 2.5)
    elif isinstance(until, (int, float)):
        t1 = t0 + until
    else:
        t1 = at(until[0], until[1], end=until_end)
    return dict(kind=kind, t0=t0, t1=t1, **kw)


def price(seg, phrase, until, b, fmt, label, **kw):
    return g("counter", seg, phrase, until, a=0, b=b, fmt=fmt, label=label, **kw)


GFX = [
    g("sticker", "intro", "más que su peso", 2.4, text="VALE MÁS QUE EL ORO", color=YEL),
    g("sticker", "intro", "más que por una casa", 2.4, text="MÁS CARA QUE UNA CASA", color=YEL),
    price("intro", "cuatrocientos cincuenta millones", ("intro", "Hoy te traigo"), 450_000_000, "US$ {:,}", "UNA SOLA PINTURA"),
    g("title", "intro", "las diez cosas más caras", 2.6, text="TOP 10 COMPRAS MÁS CARAS", color=YEL, size=90),
    g("sticker", "intro", "con récords confirmados", 2.2, text="RÉCORDS CONFIRMADOS", color=GRN),
    g("sticker", "intro", "porque ahí está", 3.0, text="AL FINAL: LA LECCIÓN DE DINERO", color=YEL),

    g("big", "p10", "Sí una sola pluma", 1.8, text="UNA SOLA PLUMA", color=YEL, size=120),
    price("p10", "cuarenta y seis mil", ("p10", "El huia era"), 46_521, "NZ$ {:,}", "≈ US$ 28.400 · MAYO 2024", side="left"),
    g("chips", "p10", "El huia era", ("p10", "Por eso cada pluma"), items=["AVE SAGRADA MAORÍ", "EXTINTA DESDE ~1907"]),
    g("big", "p10", "Gramo por gramo", 2.8, text="MÁS QUE EL ORO", color=YEL),
    g("note", "p10", "En mayo de dos", 5.0, text="Subasta Webb's, Auckland (Nueva Zelanda), mayo de 2024: NZ$ 46.521 con comisión."),

    g("lower", "p09", "una botella de Romané", 3.4, name="ROMANÉE-CONTI 1945", sub="BORGOÑA · FRANCIA"),
    price("p09", "ochocientos doce mil", ("p09", "Es el vino más caro"), 812_500, "US$ {:,}", "1 BOTELLA · MARZO 2026"),
    g("title", "p09", "Es el vino más caro", 2.6, text="EL VINO MÁS CARO DE LA HISTORIA", color=YEL, size=84),
    g("big", "p09", "unas seiscientas botellas", 2.4, text="~600 BOTELLAS", color=YEL),
    g("sticker", "p09", "deja una menos", 2.6, text="CADA VEZ QUEDAN MENOS", color=RED, fg=WHT),

    g("lower", "p08", "Un pedacito de papel", 3.4, name="ONE CENT MAGENTA", sub="GUAYANA BRITÁNICA · 1856"),
    g("big", "p08", "costaba un centavo", 2.2, text="1 CENTAVO", color=YEL),
    price("p08", "ocho millones trescientos", ("p08", "La razón"), 8_300_000, "US$ {:,}", "SOTHEBY'S · 2021"),
    g("title", "p08", "Es la única", 2.4, text="ÚNICA EN EL MUNDO", color=YEL),
    g("sticker", "p08", "el precio lo pone", 2.6, text="EL PRECIO LO PONE QUIEN LO DESEA", color=GRN),

    g("lower", "p07", "perteneció a Oskar Barnack", 3.6, name="OSKAR BARNACK", sub="CREADOR DE LA LEICA"),
    price("p07", "catorce millones", ("p07", "Esperaban venderla"), 14_400_000, "€ {:,}", "VIENA · 2022 · ≈ US$ 15 M"),
    g("compare", "p07", "Esperaban venderla", 3.6, a="ESPERABAN: € 3 M", b="PAGARON: € 14,4 M"),

    g("chips", "p06", "Tiene veinte funciones", ("p06", "Y solo existe uno"), items=["20 FUNCIONES", "5 FORMAS DE SONAR"]),
    g("big", "p06", "Y solo existe uno", 2.2, text="SOLO 1 EN ACERO", color=YEL, size=120),
    price("p06", "treinta y un millones", ("p06", "Y sabes qué es"), 31_000_000, "US$ {:,}", "GINEBRA · 2019"),
    g("sticker", "p06", "Era una subasta benéfica", 3.6, text="SUBASTA BENÉFICA: INVESTIGACIÓN DE DUCHENNE", color=GRN),
    g("note", "p06", "El Patek Philippe", 3.6, text="Imágenes de referencia de la marca Patek Philippe (Ginebra)."),

    g("side", "p05", "la Biblia hebrea", ("p05", "En dos mil veintitrés"), lines=["~1.100", "AÑOS DE", "ANTIGÜEDAD"], color=YEL),
    price("p05", "treinta y ocho millones", ("p05", "el manuscrito más caro"), 38_100_000, "US$ {:,}", "SOTHEBY'S · NUEVA YORK · 2023"),
    g("title", "p05", "el manuscrito más caro", 2.6, text="EL MANUSCRITO MÁS CARO", color=YEL),
    g("sticker", "p05", "y lo donó", 3.0, text="DONADO A UN MUSEO EN TEL AVIV", color=GRN),

    g("big", "p04", "ciento cincuenta millones", 2.4, text="150 MILLONES DE AÑOS", color=YEL, size=110),
    g("title", "p04", "al que llamaron Apex", 2.2, text="APEX", color=YEL, size=140),
    g("compare", "p04", "La casa de subastas", ("p04", "pero en julio"), a="ESPERABAN: US$ 6 M", b="PAGARON: US$ 44,6 M"),
    price("p04", "cuarenta y cuatro millones", ("p04", "Es el fósil más caro"), 44_600_000, "US$ {:,}", "SOTHEBY'S · JULIO 2024"),
    g("title", "p04", "Es el fósil más caro", 2.6, text="EL FÓSIL MÁS CARO DE LA HISTORIA", color=YEL, size=84),

    g("formula", "p03", "En bruto pesaba", ("p03", "En dos mil diecisiete"),
      steps=[("132 QUILATES EN BRUTO", ("p03", "En bruto pesaba")), ("2 AÑOS DE CORTE", ("p03", "y tardaron dos años")),
             ("59,6 QUILATES", ("p03", "y pulirlo"))]),
    price("p03", "setenta y un millones", ("p03", "la joya más cara"), 71_200_000, "US$ {:,}", "HONG KONG · 2017"),
    g("title", "p03", "la joya más cara", 2.6, text="LA JOYA MÁS CARA DE LA HISTORIA", color=YEL, size=84),
    g("note", "p03", "El Pink Star", 5.0, text="Fotos de referencia: diamantes rosados, no el Pink Star original."),

    g("sticker", "p02", "Y no no es", 2.4, text="NO ES UN FERRARI", color=RED, fg=WHT),
    g("lower", "p02", "Es un Mercedes-Benz", 3.6, name="300 SLR UHLENHAUT COUPÉ", sub="MERCEDES-BENZ · 1955"),
    g("big", "p02", "Solo se fabricaron dos", 2.2, text="SOLO 2", color=YEL),
    price("p02", "ciento treinta y cinco", ("p02", "Superó el récord"), 135_000_000, "€ {:,}", "≈ US$ 143 M · MAYO 2022"),
    g("sticker", "p02", "Superó el récord", 3.2, text="+90 MILLONES SOBRE EL RÉCORD ANTERIOR", color=GRN),
    g("title", "p02", "Es el carro más caro", 2.6, text="EL CARRO MÁS CARO DE LA HISTORIA", color=YEL, size=84),

    g("lower", "p01", "El Salvator Mundi", 3.6, name="LEONARDO DA VINCI (ATRIBUIDO)", sub="SALVATOR MUNDI · c. 1500"),
    g("big", "p01", "sesenta y cinco centímetros", 2.2, text="65 CM", color=YEL),
    price("p01", "cuatrocientos cincuenta millones", ("p01", "Es la obra de arte"), 450_300_000, "US$ {:,}", "CHRISTIE'S · NUEVA YORK · 2017"),
    g("title", "p01", "Es la obra de arte", 2.8, text="LA OBRA DE ARTE MÁS CARA", color=YEL),
    g("sticker", "p01", "Lo más raro", 3.4, text="CASI NADIE LA HA VUELTO A VER", color=RED, fg=WHT),

    g("list", "cierre", "Uno son escasas", ("cierre", "Porque al final"),
      items=[("ESCASEZ", ("cierre", "Uno son escasas")), ("UNA HISTORIA ÚNICA", ("cierre", "Dos tienen una historia")),
             ("ALGUIEN QUE LO DESEA", ("cierre", "Y tres hubo alguien"))]),
    g("title", "cierre", "Porque al final", ("cierre", "Y esa misma regla"), text="EL PRECIO LO PONE QUIEN LO DESEA", color=YEL, size=80),
    g("big", "cierre", "Lo escaso vale más", 2.6, text="LO ESCASO VALE MÁS", color=GRN, size=120),
    g("sticker", "cierre", "Por eso la habilidad", 4.6, text="TU HABILIDAD MÁS ESCASA = TU MEJOR SUELDO", color=YEL),
    g("title", "cierre", "te comprarías un dinosaurio", 3.0, text="¿TE COMPRARÍAS UN DINOSAURIO?", color=YEL, size=88),
    g("subscribe", "cierre", "Suscríbete y activa", ("cierre", "Esto fue El Precio")),
    g("title", "cierre", "Esto fue El Precio", ("cierre", "Nos vemos", True), text="EL PRECIO DEL PODER", color=YEL),
]
# graphics whose end is a phrase in the past: give them a length
for x in GFX:
    if x["t1"] <= x["t0"] + 0.3:
        x["t1"] = x["t0"] + 4.5
GFX += CARDS
GFX.append(dict(kind="end", t0=END_SCREEN, t1=END))

HITS = sorted({round(x["t0"], 3) for x in GFX if x["kind"] in ("title", "big")})


def caption_chunks():
    toks = []
    for seg, card in SEGMENTS:
        if card == "sting":
            continue  # the slogan is on screen as the sting
        for w in WORDS[seg]:
            toks.append(dict(text=w["text"], start=OFFSET[seg] + w["start"], end=OFFSET[seg] + w["end"]))
    chunks, cur = [], []
    for j, t in enumerate(toks):
        cur.append(t)
        nxt = toks[j + 1] if j + 1 < len(toks) else None
        brk = (re.search(r'[.?!:…"]$', t["text"]) or (re.search(r",$", t["text"]) and len(cur) >= 3) or len(cur) >= 6
               or nxt is None or nxt["start"] - t["end"] > 0.35)
        if brk:
            chunks.append(cur)
            cur = []
    out = []
    for k, c in enumerate(chunks):
        t1 = chunks[k + 1][0]["start"] - 0.03 if k + 1 < len(chunks) else c[-1]["end"] + 0.4
        out.append(dict(t0=c[0]["start"] - 0.03, t1=min(t1, c[-1]["end"] + 0.5), words=c))
    return out


def shot_at(t):
    idx = 0
    for i, s in enumerate(SHOTS):
        if t >= s[0]:
            idx = i
    end = SHOTS[idx + 1][0] if idx + 1 < len(SHOTS) else END
    return idx, SHOTS[idx][0], end


_CH = {"10": "Pluma de huia", "9": "Romanée-Conti 1945", "8": "Estampilla One Cent Magenta", "7": "Cámara Leica nº 105",
       "6": "Patek Philippe Grandmaster Chime", "5": "Códice Sassoon", "4": "Dinosaurio Apex", "3": "Diamante Pink Star",
       "2": "Mercedes-Benz 300 SLR", "1": "Salvator Mundi", "": "La lección de dinero"}
CHAPTERS = [(0.0, "Introducción")] + [(c["t0"], (f"#{c['n']} " if c["n"] else "") + _CH[c["n"]]) for c in CARDS if c["kind"] == "chapter"]

if __name__ == "__main__":
    print("END %.1f s = %d:%02d" % (END, END // 60, END % 60), "shots", len(SHOTS), "gfx", len(GFX))
    for c in CHAPTERS:
        print("%d:%02d %s" % (c[0] // 60, c[0] % 60, c[1]))
    durs = [(SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END_SCREEN) - SHOTS[i][0] for i in range(len(SHOTS))]
    print("long", [(round(SHOTS[i][0], 1), SHOTS[i][1], round(d, 1)) for i, d in enumerate(durs) if d > 7])
    print("short", [(round(SHOTS[i][0], 1), SHOTS[i][1], round(d, 2)) for i, d in enumerate(durs) if d < 0.8])
