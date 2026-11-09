"""Edit decision list for "Top 10 formas de ganar dinero siendo adolescente" (El Precio del Poder, 16:9).

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
SEGMENTS = [
    ("intro", None),
    ("slogan", "sting"),
    ("p10", ("10", "LAVAR CARROS\nY MOTOS")),
    ("p09", ("9", "PASEAR Y CUIDAR\nMASCOTAS")),
    ("p08", ("8", "VENDER POSTRES\nY SNACKS")),
    ("p07", ("7", "DAR CLASES\nO TUTORÍAS")),
    ("p06", ("6", "EL TÉCNICO\nDEL BARRIO")),
    ("p05", ("5", "VENDER Y\nREVENDER")),
    ("p04", ("4", "HECHO A MANO")),
    ("p03", ("3", "EDITAR VIDEOS\nY DISEÑAR")),
    ("p02", ("2", "REDES PARA\nNEGOCIOS")),
    ("p01", ("1", "CREAR TU PROPIO\nCONTENIDO")),
    ("reglas", ("", "5 REGLAS\nDE ORO")),
    ("cierre", None),
]
CARD_LEN, END_LEN = 2.6, 18.0
STING_BG, END_BG = "coins2", "friends_sunset"
END_HEAD = "¿Cuál vas a probar primero?"
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
    ("intro", "Tienes entre trece", "teen_boy", "full", {}),
    ("intro", "y quieres tener", "cash_hand", "full", {}),
    ("intro", "sin tener que pedirle", "teens_phones", "full", {}),
    ("intro", "Hoy te traigo", "friends_sunset", "full", {}),
    ("intro", "Vamos de la más sencilla", "skate_feet", "full", {}),
    ("intro", "Y quédate hasta", "teen_girl", "full", {}),
    ("intro", "Pero antes", "student_think", "full", {}),
    ("intro", "con permiso y acompañamiento", "elderly_care", "full", {}),
    # Slogan: shot under the sting
    ("slogan", "Muy buenas", "coins2", "full", {}),
    # 10 · Lavar carros y motos
    ("p10", "Suena básico", "car_vintage", "full", {}),
    ("p10", "Mucha gente del barrio", "neighborhood", "full", {}),
    ("p10", "y prefiere pagarle", "car_red", "full", {}),
    ("p10", "Solo necesitas un balde", "bucket_red", "card", {}),
    ("p10", "jabón para carros", "water_splash", "card", {}),
    ("p10", "y muchas ganas", "moto_red", "full", {}),
    ("p10", "Empieza con los vecinos", "house_blue", "full", {}),
    ("p10", "haz un trabajo impecable", "car_window", "full", {}),
    ("p10", "Un buen tip", "moto_parked", "left", {}),
    ("p10", "Así tienes clientes", "car_bmw", "full", {}),
    ("p10", "y no tienes que salir", "moto_street", "full", {}),
    # 9 · Mascotas
    ("p09", "Hay dueños que trabajan", "dog_walk", "full", {}),
    ("p09", "y sus perros", "dog_happy", "full", {}),
    ("p09", "Otros se van de viaje", "cat_gray", "full", {}),
    ("p09", "Si amas los animales", "puppy", "full", {}),
    ("p09", "Empieza con las mascotas", "dog_pug", "full", {}),
    ("p09", "y mándales fotos", "phone_hand", "right", {}),
    ("p09", "Eso sí", "dog_sign", "full", {}),
    ("p09", "y nunca vayas solo", "dog_walk2", "full", {}),
    ("p09", "no tienen con quién", "cat_cute", "card", {}),
    # 8 · Postres
    ("p08", "Brownies", "brownies", "full", {}),
    ("p08", "galletas", "cookies", "full", {}),
    ("p08", "lo que mejor te quede", "baking_hands", "full", {}),
    ("p08", "Puedes vender en tu cuadra", "bake_shop", "full", {}),
    ("p08", "o por pedido", "phone_sell", "right", {}),
    ("p08", "La clave está", "muffins", "full", {}),
    ("p08", "anota cuánto te cuesta", "cookies_cand", "left", {}),
    ("p08", "Muchos venden un montón", "cupcakes2", "full", {}),
    ("p08", "Y si quieres vender", "student_walk", "full", {}),
    ("p08", "pide permiso primero", "cake_slice", "full", {}),
    # 7 · Tutorías
    ("p07", "Si eres bueno", "homework_kid", "full", {}),
    ("p07", "hay niños más pequeños", "homework_girl", "full", {}),
    ("p07", "y papás dispuestos", "study_group", "full", {}),
    ("p07", "Y tienes una ventaja", "books_open", "full", {}),
    ("p07", "y sabes explicarlos", "laptop_kid", "full", {}),
    ("p07", "Empieza con los hermanos", "homeschool", "full", {}),
    ("p07", "Si lo haces bien", "student_desk", "full", {}),
    # 6 · Técnico del barrio
    ("p06", "Para ti es normal", "phone_coffee", "full", {}),
    ("p06", "Para muchos adultos", "grandma_phone", "full", {}),
    ("p06", "Puedes cobrar", "elderly_phone", "full", {}),
    ("p06", "o por ayudarles", "grandpa", "full", {}),
    ("p06", "Aquí la confianza", "elderly_cafe", "full", {}),
    ("p06", "y si hay pagos", "safety", "card", {}),
    ("p06", "que la persona siempre", "bank_calc", "full", {}),
    # 5 · Vender y revender
    ("p05", "Revisa tu cuarto", "hangers", "full", {}),
    ("p05", "videojuegos", "clothes_rack", "full", {}),
    ("p05", "Tómale buenas fotos", "camera_photo", "full", {}),
    ("p05", "y publícalo", "phone_social", "right", {}),
    ("p05", "Cuando le cojas el ritmo", "thrift_girl", "full", {}),
    ("p05", "lavarla", "clothes_shop", "full", {}),
    ("p05", "Eso se llama", "woman_vintage", "full", {}),
    # 4 · Hecho a mano
    ("p04", "Pulseras", "bracelet", "full", {}),
    ("p04", "velas", "candle_jar", "full", {}),
    ("p04", "Lo hecho a mano", "handmade", "full", {}),
    ("p04", "Y si lo personalizas", "sewing", "full", {}),
    ("p04", "Las fechas especiales", "candles", "full", {}),
    ("p04", "Prepárate con tiempo", "craft_blue", "full", {}),
    ("p04", "y muestra tus productos", "bracelet2", "full", {}),
    ("p04", "llaveros", "earrings", "full", {}),
    ("p04", "stickers", "stickers", "full", {}),
    # 3 · Edición y diseño
    ("p03", "Hoy todos los negocios", "barber", "full", {}),
    ("p03", "la panadería", "bakery_front", "full", {}),
    ("p03", "el gimnasio", "gym", "full", {}),
    ("p03", "Y tú puedes hacerlo", "iphone_cam", "full", {}),
    ("p03", "Empieza armando", "design_mock", "full", {}),
    ("p03", "Luego ofrécele", "bakery_man", "full", {}),
    ("p03", "Si les gusta", "photographer", "full", {}),
    ("p03", "Y cada trabajo", "swatches", "full", {}),
    ("p03", "es una habilidad", "code", "full", {}),
    # 2 · Redes de negocios
    ("p02", "Muchos dueños de negocio", "barber2", "full", {}),
    ("p02", "pero no tienen tiempo", "insta_phone", "full", {}),
    ("p02", "Puedes ofrecer un plan", "social_media", "full", {}),
    ("p02", "y mostrarles cuánta gente", "insta_hand", "left", {}),
    ("p02", "Esto ya no es", "office_work", "full", {}),
    ("p02", "Eso sí todo acuerdo", "student_write", "full", {}),
    ("p02", "y por escrito", "bills", "full", {}),
    # 1 · Contenido propio
    ("p01", "Un canal de YouTube", "youtube_phone", "full", {}),
    ("p01", "videojuegos", "videocam", "full", {}),
    ("p01", "Por qué es el número uno", "content_creator", "full", {}),
    ("p01", "Un video que haces hoy", "vlog_tiles", "full", {}),
    ("p01", "Pero ojo", "student_lap", "full", {}),
    ("p01", "Y plataformas como YouTube", "camera_girl", "full", {}),
    ("p01", "así que la cuenta de cobro", "grandpa", "card", {}),
    ("p01", "Lo bueno es que", "blog_tiles", "full", {}),
    ("p01", "hablar en cámara", "skate_sunset", "full", {}),
    ("p01", "te sirve para cualquier cosa", "teen_girl", "full", {}),
    # Reglas de oro
    ("reglas", "Uno todo con permiso", "elderly_care", "full", {}),
    ("reglas", "En Colombia por ejemplo", "homework_girl", "full", {}),
    ("reglas", "autorización del inspector", "study_group", "full", {}),
    ("reglas", "Dos tu seguridad", "mask_tiles", "full", {}),
    ("reglas", "y no compartas", "phone_hand", "full", {}),
    ("reglas", "Tres el colegio", "student_desk", "full", {}),
    ("reglas", "Cuatro ahorra", "pig_calc", "full", {}),
    ("reglas", "Y cinco huye", "burn_money", "full", {}),
    ("reglas", "solo te van a quitar", "cash_hand", "full", {}),
    # Cierre
    ("cierre", "Ahora dime tú", "teens_phones", "full", {}),
    ("cierre", "Y si ya ganas", "friends_group", "full", {}),
    ("cierre", "Si este video te sirvió", "phone_hand", "full", {}),
    ("cierre", "Esto fue El Precio", "coins", "full", {}),
]
# The first photo of every block enters with the block's first word (e.g. "Número siete").
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


GFX = [
    g("big", "intro", "Tienes entre trece", 2.2, text="13 A 17 AÑOS", color=YEL),
    g("title", "intro", "diez formas reales", 2.4, text="10 FORMAS REALES", color=YEL),
    g("sticker", "intro", "Y quédate hasta", 2.6, text="EL #1 PUEDE CAMBIAR TU FUTURO", color=YEL),
    g("title", "intro", "una regla que no se negocia", ("intro", "con permiso y acompañamiento"), text="REGLA #0", color=RED, fg=WHT),
    g("side", "intro", "con permiso y acompañamiento", 3.6, lines=["CON PERMISO", "DE UN ADULTO"], color=YEL),

    g("list", "p10", "Solo necesitas un balde", ("p10", "Empieza con los vecinos"),
      items=[("BALDE", ("p10", "Solo necesitas un balde")), ("JABÓN PARA CARROS", ("p10", "jabón para carros")),
             ("TOALLAS DE MICROFIBRA", ("p10", "toallas de microfibra")), ("MUCHAS GANAS", ("p10", "y muchas ganas"))]),
    g("sticker", "p10", "pídeles que te recomienden", 2.4, text="EL BOCA A BOCA VENDE", color=YEL),
    g("side", "p10", "Un buen tip", ("p10", "Así tienes clientes"), lines=["PLAN FIJO", "1 LAVADO", "POR SEMANA"], color=GRN),
    g("title", "p10", "clientes que vuelven", 2.4, text="CLIENTES QUE VUELVEN", color=GRN),

    g("side", "p09", "y mándales fotos", ("p09", "Eso sí"), lines=["MANDA FOTOS", "= CONFIANZA"], color=GRN),
    g("sticker", "p09", "acepta solo animales", 3.4, text="SOLO ANIMALES QUE PUEDAS CONTROLAR", color=RED, fg=WHT),

    g("side", "p08", "o por pedido", ("p08", "La clave está"), lines=["PEDIDOS", "POR WHATSAPP"], color=GRN),
    g("formula", "p08", "anota cuánto te cuesta", ("p08", "Muchos venden un montón"),
      steps=[("COSTO", ("p08", "anota cuánto te cuesta")), ("POR PORCIÓN", ("p08", "calcula cuánto te sale")),
             ("PRECIO CON GANANCIA", ("p08", "y ponle un precio"))]),
    g("big", "p08", "y ganan casi nada", 2.2, text="SIN CUENTAS = SIN GANANCIA", color=RED, size=110),
    g("sticker", "p08", "pide permiso primero", 2.2, text="PIDE PERMISO EN EL COLEGIO", color=YEL),

    g("chips", "p07", "Si eres bueno", ("p07", "hay niños más pequeños"), items=["MATEMÁTICAS", "INGLÉS", "CUALQUIER MATERIA"]),
    g("title", "p07", "Y tienes una ventaja", 2.6, text="TU VENTAJA: LO VISTE HACE POCO", color=YEL, size=84),
    g("sticker", "p07", "siempre con un adulto", 2.4, text="SIEMPRE CON UN ADULTO ENTERADO", color=YEL),

    g("chips", "p06", "Para ti es normal", ("p06", "Para muchos adultos"), items=["CONFIGURAR EL CELULAR", "WHATSAPP", "VIDEOLLAMADAS", "PASAR FOTOS"]),
    g("big", "p06", "eso es otro mundo", 1.8, text="OTRO MUNDO", color=YEL),
    g("list", "p06", "Aquí la confianza", ("p06", "Aquí la confianza", True), dur=0,
      items=[("NUNCA PIDAS CONTRASEÑAS", ("p06", "nunca pidas")), ("PAGOS: LA PERSONA PRESENTE", ("p06", "y si hay pagos"))]),

    g("chips", "p05", "ropa que ya no", ("p05", "Todo eso puede ser dinero"), items=["ROPA", "VIDEOJUEGOS", "LIBROS", "ACCESORIOS"]),
    g("big", "p05", "Todo eso puede ser dinero", 2.0, text="= DINERO", color=GRN),
    g("side", "p05", "Tómale buenas fotos", ("p05", "y publícalo"), lines=["FOTOS CON", "LUZ NATURAL"], color=YEL),
    g("side", "p05", "y publícalo", ("p05", "Cuando le cojas el ritmo"), lines=["CON AYUDA", "DE UN ADULTO"], color=YEL),
    g("formula", "p05", "comprar ropa de segunda", ("p05", "Eso se llama"),
      steps=[("COMPRA", ("p05", "comprar ropa de segunda")), ("LAVA", ("p05", "lavarla")), ("PRESENTA", ("p05", "presentarla bien")),
             ("VENDE", ("p05", "y venderla"))]),
    g("title", "p05", "Eso se llama", 2.6, text="AGREGAR VALOR", color=GRN),

    g("chips", "p04", "Pulseras", ("p04", "Lo hecho a mano"), items=["PULSERAS", "ARETES", "LLAVEROS", "VELAS", "STICKERS"]),
    g("big", "p04", "es único", 1.8, text="ÚNICO", color=YEL),
    g("sticker", "p04", "la gente paga más", 2.2, text="PERSONALIZADO = MÁS VALOR", color=GRN),
    g("chips", "p04", "Las fechas especiales", ("p04", "Prepárate con tiempo"), items=["AMOR Y AMISTAD", "NAVIDAD", "DÍA DE LA MADRE"]),

    g("chips", "p03", "Hoy todos los negocios", ("p03", "Y tú puedes hacerlo"), items=["PELUQUERÍA", "PANADERÍA", "GIMNASIO"]),
    g("side", "p03", "Y tú puedes hacerlo", ("p03", "Empieza armando"), lines=["CAPCUT", "CANVA", "GRATIS"], color=YEL),
    g("formula", "p03", "Empieza armando", ("p03", "Y cada trabajo"),
      steps=[("PORTAFOLIO", ("p03", "Empieza armando")), ("VIDEO DE PRUEBA", ("p03", "Luego ofrécele")),
             ("PRIMER CLIENTE", ("p03", "ya tienes tu primer cliente"))]),
    g("title", "p03", "Y cada trabajo", 2.6, text="HABILIDAD = VALOR", color=GRN),

    g("chips", "p02", "Puedes ofrecer un plan", ("p02", "Esto ya no es"), items=["FOTOS", "PUBLICACIONES", "MENSAJES", "RESULTADOS"]),
    g("big", "p02", "es un servicio", 2.4, text="PAGO MENSUAL", color=GRN),
    g("sticker", "p02", "Eso sí todo acuerdo", 2.8, text="ACUERDOS CON UN ADULTO Y POR ESCRITO", color=YEL),

    g("chips", "p01", "Un canal de YouTube", ("p01", "Por qué es el número uno"), items=["YOUTUBE", "TIKTOK", "BLOG", "PÓDCAST"]),
    g("title", "p01", "mientras duermes", 2.4, text="TRABAJA MIENTRAS DUERMES", color=GRN),
    g("big", "p01", "no da plata rápido", 2.2, text="NO ES RÁPIDO", color=RED),
    g("side", "p01", "Y plataformas como YouTube", ("p01", "así que la cuenta de cobro"), lines=["PAGOS", "DESDE 18 AÑOS"], color=RED),
    g("sticker", "p01", "así que la cuenta de cobro", 3.4, text="LA CUENTA DE COBRO LA MANEJA UN ADULTO", color=YEL),
    g("chips", "p01", "grabar", ("p01", "te sirve para cualquier cosa"), items=["GRABAR", "EDITAR", "HABLAR EN CÁMARA", "VENDER UNA IDEA"]),

    g("list", "reglas", "Uno todo con permiso", ("reglas", "Y cinco huye", True), dur=0,
      items=[("CON PERMISO DE UN ADULTO", ("reglas", "Uno todo con permiso")), ("TU SEGURIDAD PRIMERO", ("reglas", "Dos tu seguridad")),
             ("EL COLEGIO NO SE NEGOCIA", ("reglas", "Tres el colegio")), ("AHORRA UNA PARTE", ("reglas", "Cuatro ahorra")),
             ("HUYE DEL DINERO FÁCIL", ("reglas", "Y cinco huye"))]),
    g("note", "reglas", "En Colombia por ejemplo", 7.5,
      text="Colombia: edad mínima de trabajo 15 años; de 15 a 17 se requiere autorización del inspector de trabajo (Ley 1098, art. 35)."),
    g("chips", "reglas", "Apuestas", ("reglas", "Apuestas", True), dur=0, items=["APUESTAS", "PIRÁMIDES", "GURÚS"], color=RED),

    g("title", "cierre", "cuál de estas diez", 3.0, text="¿CUÁL VAS A PROBAR?", color=YEL),
    g("subscribe", "cierre", "Si este video te sirvió", ("cierre", "Esto fue El Precio")),
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


CHAPTERS = [(0.0, "Introducción")] + [(c["t0"], (f"#{c['n']} " if c["n"] else "") + c["text"].replace("\n", " ").capitalize())
                                      for c in CARDS if c["kind"] == "chapter"]

if __name__ == "__main__":
    print("END %.1f s = %d:%02d" % (END, END // 60, END % 60), "shots", len(SHOTS), "gfx", len(GFX))
    for c in CHAPTERS:
        print("%d:%02d %s" % (c[0] // 60, c[0] % 60, c[1]))
    durs = [(SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END_SCREEN) - SHOTS[i][0] for i in range(len(SHOTS))]
    print("long", [(round(SHOTS[i][0], 1), SHOTS[i][1], round(d, 1)) for i, d in enumerate(durs) if d > 7])
    print("short", [(round(SHOTS[i][0], 1), SHOTS[i][1], round(d, 2)) for i, d in enumerate(durs) if d < 0.8])
