"""Edit decision list for "10 formas de lavar dinero (y cómo los atraparon)" (El Precio del Poder, 16:9).

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
    ("basico", None),
    ("slogan", "sting"),
    ("p10", ("10", "EL PITUFEO")),
    ("p09", ("9", "NEGOCIOS\nDE FACHADA")),
    ("p08", ("8", "LOS CASINOS")),
    ("p07", ("7", "CASAS\nDE LUJO")),
    ("p06", ("6", "EL ARTE")),
    ("p05", ("5", "MERCADO NEGRO\nDEL PESO")),
    ("p04", ("4", "EMPRESAS\nFANTASMA")),
    ("p03", ("3", "CRIPTOMONEDAS")),
    ("p02", ("2", "BANCOS QUE MIRAN\nPARA OTRO LADO")),
    ("p01", ("1", "1MDB: EL ROBO\nDE UN PAÍS")),
    ("cierre", ("", "LA LECCIÓN")),
]
CARD_LEN, END_LEN = 2.6, 18.0
STING_BG, END_BG = "money_cash", "bills"
END_HEAD = "¿Qué caso te pareció más increíble?"
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
    ("intro", "En dos mil doce", "hsbc_mexico", "full", {}),
    ("intro", "aceptó pagar casi", "money_cash", "full", {}),
    ("intro", "Por sus ventanillas", "bank_building", "full", {}),
    ("intro", "en cajas hechas", "bills", "full", {}),
    ("intro", "Eso es lavar dinero", "cash_flow", "full", {}),
    ("intro", "Hoy te traigo", "fbi_hq", "full", {}),
    ("intro", "Ojo esto no es", "doj", "full", {}),
    ("intro", "Al final vas", "money_pyramid", "full", {}),
    # Lo básico
    ("basico", "Antes de arrancar", "stocks_graph", "full", {}),
    ("basico", "Uno la colocación", "bills", "full", {"z": (1.2, 1.0)}),
    ("basico", "Dos la estratificación", "code_screen", "full", {}),
    ("basico", "Y tres la integración", "apartment", "full", {}),
    ("basico", "Y del otro lado", "bogota", "full", {}),
    ("basico", "En Colombia existe", "documents", "full", {}),
    ("basico", "que recibe los reportes", "bank_building", "full", {}),
    ("basico", "Y en el mundo", "money_cash2", "full", {}),
    ("basico", "Con eso claro", "coins", "full", {}),
    # Slogan
    ("slogan", "Muy buenas", "money_cash", "full", {}),
    # 10 · Pitufeo
    ("p10", "Número diez", "cash_hands2", "full", {}),
    ("p10", "en vez de mover", "bills", "full", {}),
    ("p10", "En Estados Unidos los bancos", "bank_building", "full", {}),
    ("p10", "Y partir la plata", "money_cash", "full", {}),
    ("p10", "Le pasó a Dennis", "doj", "full", {}),
    ("p10", "Sacó cerca de", "money_cash2", "full", {}),
    ("p10", "para comprar el silencio", "documents2", "full", {}),
    ("p10", "El banco notó", "stocks_graph", "full", {}),
    ("p10", "el FBI investigó", "fbi_hq", "full", {}),
    ("p10", "La lección", "cash_flow", "full", {}),
    # 9 · Negocios de fachada
    ("p09", "Número nueve", "restaurant_bar", "full", {}),
    ("p09", "Un restaurante", "restaurant_kitchen", "full", {}),
    ("p09", "que funciona de verdad", "restaurant_food", "full", {}),
    ("p09", "Así la plata sucia", "money_cash", "full", {}),
    ("p09", "Y un dato curioso", "capone", "card", {}),
    ("p09", "La expresión se popularizó", "watergate", "full", {}),
    ("p09", "Y a Capone", "capone", "full", {"z": (1.2, 1.0)}),
    ("p09", "Y cómo los atrapan", "documents", "full", {}),
    ("p09", "un local pequeño", "restaurant_bar", "full", {"z": (1.2, 1.0)}),
    ("p09", "Las autoridades comparan", "stocks_graph", "full", {}),
    # 8 · Casinos
    ("p08", "Número ocho", "poker_chips", "full", {}),
    ("p08", "La idea es entrar", "cards", "full", {}),
    ("p08", "cambiarlo por fichas", "poker", "full", {}),
    ("p08", "En la provincia canadiense", "vancouver", "full", {}),
    ("p08", "los casinos recibieron", "river_rock", "full", {}),
    ("p08", "Doscientos setenta y nueve", "bills", "full", {}),
    ("p08", "Llegaba gente con", "dice", "full", {}),
    ("p08", "El escándalo terminó", "documents2", "full", {}),
    ("p08", "que en dos mil veintidós", "vancouver", "full", {"z": (1.2, 1.0)}),
    ("p08", "La lección", "poker_chips", "full", {"z": (1.2, 1.0)}),
    # 7 · Casas de lujo
    ("p07", "Número siete", "apartment", "full", {}),
    ("p07", "Una propiedad puede", "dining_room", "full", {}),
    ("p07", "Y si se paga", "documents", "full", {}),
    ("p07", "Por eso ciudades", "miami", "full", {}),
    ("p07", "o Nueva York", "miami2", "full", {}),
    ("p07", "En dos mil dieciséis el Tesoro", "documents2", "full", {}),
    ("p07", "se identificara a la persona", "doj", "full", {}),
    ("p07", "Y la plata de uno", "apartment2", "full", {}),
    ("p07", "en un apartamento de lujo", "dining_room", "full", {"z": (1.2, 1.0)}),
    ("p07", "De ese caso", "petronas_night", "full", {}),
    ("p07", "La lección", "miami", "full", {"z": (1.2, 1.0)}),
    # 6 · Arte
    ("p06", "Número seis", "gallery", "full", {}),
    ("p06", "Una pintura puede valer", "gallery_red", "full", {}),
    ("p06", "Edemar Cid Ferreira", "sao_paulo", "full", {}),
    ("p06", "El banco quebró", "documents2", "full", {}),
    ("p06", "pero él había comprado", "museum_man", "full", {}),
    ("p06", "Una de ellas", "auction_daumier", "full", {}),
    ("p06", "Sabes con qué valor", "port", "full", {}),
    ("p06", "Cien dólares", "money_cash2", "full", {"z": (1.25, 1.0)}),
    ("p06", "Las autoridades lo encontraron", "containers", "full", {}),
    ("p06", "La lección", "gallery", "full", {"z": (1.2, 1.0)}),
    # 5 · Mercado negro del peso
    ("p05", "Número cinco", "bogota", "full", {}),
    ("p05", "Así funcionaba", "money_cash", "full", {}),
    ("p05", "pero necesitaban pesos", "cash_flow", "full", {}),
    ("p05", "Al mismo tiempo", "port", "full", {}),
    ("p05", "Un intermediario", "briefcase", "full", {}),
    ("p05", "y usaba esos dólares", "containers", "full", {}),
    ("p05", "El dinero casi no", "port_night", "full", {}),
    ("p05", "A veces además", "documents", "full", {}),
    ("p05", "Las autoridades de Estados", "doj", "full", {}),
    ("p05", "La lección", "containers2", "full", {}),
    # 4 · Empresas fantasma
    ("p04", "Número cuatro", "panama", "full", {}),
    ("p04", "Son empresas que existen", "documents", "full", {}),
    ("p04", "Sirven para esconder", "briefcase", "full", {}),
    ("p04", "En dos mil dieciséis estallaron", "mossack_sign", "card", {}),
    ("p04", "más de once millones", "documents2", "full", {}),
    ("p04", "con más de doscientas", "panama2", "full", {}),
    ("p04", "Ojo tener una empresa", "panama", "full", {"z": (1.2, 1.0)}),
    ("p04", "Pero la filtración", "mossack_sign", "full", {}),
    ("p04", "La lección", "documents", "full", {"z": (1.2, 1.0)}),
    # 3 · Criptomonedas
    ("p03", "Número tres", "bitcoin_casascius", "full", {}),
    ("p03", "Mucha gente cree", "code_screen", "full", {}),
    ("p03", "En dos mil dieciséis un hacker", "keyboard", "full", {}),
    ("p03", "Él y su esposa", "stocks_graph", "full", {}),
    ("p03", "Pero en la blockchain", "bitcoin_hand", "full", {}),
    ("p03", "En dos mil veintidós", "doj", "full", {}),
    ("p03", "y recuperaron unos", "bitcoin_coin", "card", {}),
    ("p03", "la incautación más grande", "fbi_hq", "full", {}),
    ("p03", "Él recibió cinco", "documents2", "full", {}),
    ("p03", "La lección", "bitcoin_casascius", "full", {"z": (1.2, 1.0)}),
    # 2 · Bancos
    ("p02", "Número dos", "hsbc_tower", "full", {}),
    ("p02", "Entre dos mil seis", "hsbc_mexico", "full", {}),
    ("p02", "movieron al menos", "bills", "full", {}),
    ("p02", "Llegaban a depositar", "bank_building", "full", {}),
    ("p02", "En dos mil doce el banco", "doj", "full", {}),
    ("p02", "Y la historia se repitió", "td_bank", "full", {}),
    ("p02", "aceptó pagar unos tres", "money_pyramid", "full", {}),
    ("p02", "por dejar que redes", "money_cash2", "full", {}),
    ("p02", "La lección", "hsbc_tower", "full", {"z": (1.2, 1.0)}),
    # 1 · 1MDB
    ("p01", "Y el número uno", "petronas_night", "full", {}),
    ("p01", "1MDB era un fondo", "petronas", "full", {}),
    ("p01", "Entre dos mil nueve", "money_pyramid", "full", {}),
    ("p01", "El cerebro según", "briefcase", "full", {}),
    ("p01", "La plata pasó", "bank_building", "full", {}),
    ("p01", "y terminó en un yate", "equanimity", "full", {}),
    ("p01", "en cuadros de Monet", "gallery", "full", {}),
    ("p01", "en mansiones", "apartment2", "full", {}),
    ("p01", "y según la justicia", "doj", "full", {}),
    ("p01", "El ex primer ministro", "najib", "card", {}),
    ("p01", "Y Jho Low", "documents", "full", {}),
    ("p01", "La lección", "petronas_night", "full", {"z": (1.2, 1.0)}),
    # Cierre
    ("cierre", "Y qué tienen", "stocks_graph", "full", {}),
    ("cierre", "Retiros con patrones", "bills", "full", {}),
    ("cierre", "El lavado de dinero puede", "doj", "full", {}),
    ("cierre", "Y aquí va la parte", "money_cash", "full", {}),
    ("cierre", "nunca prestes tu cuenta", "bank_building", "full", {}),
    ("cierre", "Así es como reclutan", "documents", "full", {}),
    ("cierre", "Ahora dime", "cash_flow", "full", {}),
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
    g("sticker", "intro", "aceptó pagar casi", 2.6, text="CASI US$ 2.000 MILLONES DE MULTA", color=YEL),
    g("sticker", "intro", "en cajas hechas", 3.0, text="CAJAS A LA MEDIDA DE LA VENTANILLA", color=RED, fg=WHT),
    g("title", "intro", "Eso es lavar dinero", 3.4, text="LAVAR = HACER QUE LO ILEGAL PAREZCA LEGAL", color=YEL, size=74),
    g("title", "intro", "Hoy te traigo", 2.8, text="10 CASOS REALES", color=YEL),
    g("sticker", "intro", "y cómo los atraparon", 2.2, text="Y CÓMO LOS ATRAPARON", color=GRN),
    g("note", "intro", "Ojo esto no es", 6.0, text="Video educativo e informativo. Casos públicos; las fuentes están en la descripción."),
    g("sticker", "intro", "Al final vas", 3.6, text="AL FINAL: CÓMO PROTEGERTE", color=GRN),

    g("title", "basico", "Antes de arrancar", 2.4, text="LO BÁSICO", color=YEL),
    g("formula", "basico", "Uno la colocación", ("basico", "Y del otro lado"),
      steps=[("COLOCACIÓN", ("basico", "Uno la colocación")), ("ESTRATIFICACIÓN", ("basico", "Dos la estratificación")),
             ("INTEGRACIÓN", ("basico", "Y tres la integración"))]),
    g("lower", "basico", "En Colombia existe", 4.0, name="UIAF", sub="UNIDAD DE INFORMACIÓN Y ANÁLISIS FINANCIERO"),
    g("sticker", "basico", "operaciones sospechosas", 2.8, text="REPORTES DE OPERACIONES SOSPECHOSAS", color=YEL),
    g("big", "basico", "el GAFI pone", 2.0, text="GAFI", color=YEL),
    g("sticker", "basico", "más de doscientos países", 2.4, text="+200 PAÍSES Y TERRITORIOS", color=GRN),

    g("big", "p10", "de más de diez mil", 2.4, text="+US$ 10.000 = REPORTE", color=YEL, size=110),
    g("sticker", "p10", "ya es un delito", 2.8, text="PARTIR LA PLATA A PROPÓSITO = DELITO", color=RED, fg=WHT),
    g("lower", "p10", "Le pasó a Dennis", 4.0, name="DENNIS HASTERT", sub="EXPRESIDENTE DE LA CÁMARA DE REPRESENTANTES (EE. UU.)"),
    g("chips", "p10", "Sacó cerca de", ("p10", "El banco notó"), items=["~US$ 950.000", "+100 RETIROS PEQUEÑOS"]),
    g("big", "p10", "lo condenaron", 2.4, text="15 MESES DE PRISIÓN", color=RED, size=110),
    g("title", "p10", "los bancos no ven", ("p10", "Ven patrones", True), text="LOS BANCOS VEN PATRONES", color=YEL),

    g("chips", "p09", "Un restaurante", ("p09", "que funciona de verdad"), items=["RESTAURANTES", "LAVADEROS", "TIENDAS"]),
    g("sticker", "p09", "reporta muchas más", 2.6, text="VENTAS INFLADAS", color=RED, fg=WHT),
    g("title", "p09", "pero es un mito", 2.0, text="MITO", color=RED, fg=WHT, size=130),
    g("lower", "p09", "La expresión se popularizó", 4.0, name="WATERGATE · 1973", sub="AHÍ SE POPULARIZÓ LA EXPRESIÓN"),
    g("sticker", "p09", "sino por no pagar", 2.8, text="CAPONE CAYÓ POR IMPUESTOS (1931)", color=YEL),
    g("chips", "p09", "Con números que no", ("p09", "Las autoridades comparan"), items=["VENTAS ENORMES", "SIN CLIENTES", "SIN INVENTARIO"]),
    g("title", "p09", "con lo que de verdad", 2.6, text="LOS NÚMEROS TIENEN QUE CUADRAR", color=YEL, size=84),

    g("formula", "p08", "La idea es entrar", ("p08", "En la provincia canadiense"),
      steps=[("EFECTIVO", ("p08", "La idea es entrar")), ("FICHAS", ("p08", "cambiarlo por fichas")), ("¿GANANCIA?", ("p08", "y salir con algo"))]),
    price("p08", "trescientos setenta y seis", ("p08", "Doscientos setenta y nueve"), 376_000_000, "C$ {:,}", "EFECTIVO SOSPECHOSO · 2012–2015"),
    g("sticker", "p08", "Doscientos setenta y nueve", 3.4, text="C$ 279 M EN BILLETES DE 20", color=YEL),
    g("lower", "p08", "la Comisión Cullen", 4.0, name="COMISIÓN CULLEN · 2022", sub="INVESTIGACIÓN PÚBLICA EN CANADÁ"),
    g("title", "p08", "el efectivo en masa", 2.8, text="EL EFECTIVO DEJA HUELLA", color=YEL),

    g("sticker", "p07", "Y si se paga", 3.4, text="DE CONTADO + A NOMBRE DE UNA EMPRESA", color=RED, fg=WHT),
    g("chips", "p07", "Por eso ciudades", ("p07", "En dos mil dieciséis el Tesoro"), items=["MIAMI", "NUEVA YORK"]),
    g("lower", "p07", "En dos mil dieciséis el Tesoro", 4.6, name="EE. UU. · 2016", sub="HAY QUE IDENTIFICAR AL DUEÑO REAL"),
    g("sticker", "p07", "terminó confiscando", 2.6, text="CONFISCADO", color=RED, fg=WHT),
    g("title", "p07", "detrás de cada empresa", 3.4, text="DETRÁS DE CADA EMPRESA HAY UNA PERSONA", color=YEL, size=74),

    g("lower", "p06", "Edemar Cid Ferreira", 4.0, name="EDEMAR CID FERREIRA", sub="DUEÑO DEL BANCO SANTOS (BRASIL)"),
    g("sticker", "p06", "El banco quebró", 3.0, text="QUIEBRA: +US$ 1.000 M EN DEUDAS", color=RED, fg=WHT),
    g("note", "p06", "Una de ellas", 5.0, text="Basquiat, \"Hannibal\": la obra no se muestra por derechos de autor."),
    g("compare", "p06", "Sabes con qué valor", ("p06", "Las autoridades lo encontraron"), a="VALOR: ~US$ 8 M", b="DECLARADO: US$ 100"),
    g("big", "p06", "Cien dólares", 2.4, text="US$ 100", color=RED, size=200),
    g("title", "p06", "un precio absurdo", 3.0, text="UN PRECIO ABSURDO ES UNA ALARMA", color=YEL, size=84),

    g("chips", "p05", "Así funcionaba", ("p05", "Al mismo tiempo"), items=["CARTEL: DÓLARES EN EE. UU.", "QUIERE PESOS"], color=RED),
    g("chips", "p05", "Al mismo tiempo", ("p05", "Un intermediario"), items=["IMPORTADOR: TIENE PESOS", "QUIERE DÓLARES"]),
    g("formula", "p05", "Un intermediario", ("p05", "El dinero casi no"),
      steps=[("CAMBISTA", ("p05", "Un intermediario")), ("PESOS AL CARTEL", ("p05", "le pagaba pesos")),
             ("DÓLARES AL IMPORTADOR", ("p05", "y usaba esos dólares"))]),
    g("sticker", "p05", "inflaban o rebajaban", 3.0, text="FACTURAS INFLADAS O REBAJADAS", color=RED, fg=WHT),
    g("title", "p05", "el comercio también", 2.6, text="EL COMERCIO TAMBIÉN SE AUDITA", color=YEL, size=84),

    g("chips", "p04", "pero no tienen oficinas", ("p04", "Sirven para esconder"), items=["SIN OFICINAS", "SIN EMPLEADOS", "SIN ACTIVIDAD"]),
    g("lower", "p04", "En dos mil dieciséis estallaron", 4.0, name="PAPELES DE PANAMÁ · 2016", sub="FILTRACIÓN DEL BUFETE MOSSACK FONSECA"),
    price("p04", "más de once millones", ("p04", "con más de doscientas"), 11_500_000, "{:,} DOCUMENTOS", "LA MAYOR FILTRACIÓN DE SU ÉPOCA"),
    g("big", "p04", "doscientas catorce mil", 2.6, text="+214.000 EMPRESAS", color=YEL, size=120),
    g("sticker", "p04", "Ojo tener una empresa", 3.4, text="TENER UNA EMPRESA AFUERA NO ES ILEGAL", color=GRN),
    g("sticker", "p04", "y el bufete terminó", 2.6, text="MOSSACK FONSECA CERRÓ EN 2018", color=RED, fg=WHT),
    g("title", "p04", "los secretos financieros", 2.6, text="LOS SECRETOS NO SON ETERNOS", color=YEL, size=88),

    g("sticker", "p03", "imposibles de rastrear", 2.4, text="¿IMPOSIBLES DE RASTREAR? FALSO", color=RED, fg=WHT),
    g("big", "p03", "ciento diecinueve mil", 2.8, text="119.754 BTC", color=YEL),
    g("lower", "p03", "del exchange Bitfinex", 3.4, name="BITFINEX · 2016", sub="EL HACKEO"),
    g("sticker", "p03", "Pero en la blockchain", 3.4, text="LA BLOCKCHAIN ES PÚBLICA Y NO OLVIDA", color=GRN),
    price("p03", "unos tres mil seiscientos", ("p03", "Él recibió cinco"), 3_600_000_000, "US$ {:,}", "~94.000 BTC RECUPERADOS (2022)"),
    g("chips", "p03", "Él recibió cinco", ("p03", "La lección"), items=["ÉL: 5 AÑOS", "ELLA: 18 MESES"], color=RED),
    g("title", "p03", "en cripto el rastro", 2.6, text="EL RASTRO ES PERMANENTE", color=YEL),

    g("chips", "p02", "el cartel de Sinaloa", ("p02", "movieron al menos"), items=["CARTEL DE SINALOA", "CARTEL DEL NORTE DEL VALLE"], color=RED),
    price("p02", "ochocientos ochenta y un", ("p02", "Llegaban a depositar"), 881_000_000, "US$ {:,}", "LAVADOS VÍA HSBC · 2006–2010"),
    g("sticker", "p02", "Llegaban a depositar", 3.2, text="CAJAS A LA MEDIDA DE LAS VENTANILLAS", color=YEL),
    g("compare", "p02", "Y la historia se repitió", ("p02", "La lección"), a="HSBC 2012: US$ 1.920 M", b="TD BANK 2024: ~US$ 3.000 M"),
    g("title", "p02", "hasta los bancos", 2.8, text="HASTA LOS GRANDES PAGAN CARO", color=YEL, size=88),

    g("lower", "p01", "1MDB era un fondo", 4.0, name="1MDB", sub="FONDO DEL GOBIERNO DE MALASIA"),
    price("p01", "cuatro mil quinientos", ("p01", "El cerebro según"), 4_500_000_000, "US$ {:,}", "DESVIADOS ENTRE 2009 Y 2015"),
    g("lower", "p01", "fue un financista", 3.6, name="JHO LOW", sub="EL CEREBRO, SEGÚN LAS AUTORIDADES"),
    g("chips", "p01", "y terminó en un yate", ("p01", "y según la justicia"), items=["YATE ~US$ 250 M", "MONET Y VAN GOGH", "MANSIONES"]),
    g("sticker", "p01", "hasta ayudó a financiar", 3.4, text="Y HASTA \"EL LOBO DE WALL STREET\"", color=YEL),
    g("lower", "p01", "Najib Razak", 3.6, name="NAJIB RAZAK", sub="EX PRIMER MINISTRO · CONDENADO"),
    g("title", "p01", "sigue prófugo", 2.4, text="JHO LOW SIGUE PRÓFUGO", color=RED, fg=WHT),
    g("big", "p01", "Pero no para siempre", 2.4, text="PERO NO PARA SIEMPRE", color=YEL, size=110),

    g("list", "cierre", "Retiros con patrones", ("cierre", "El lavado de dinero puede"),
      items=[("PATRONES RAROS", ("cierre", "Retiros con patrones")), ("VENTAS QUE NO CUADRAN", ("cierre", "ventas que no cuadran")),
             ("PRECIOS ABSURDOS", ("cierre", "precios absurdos")), ("DOCUMENTOS FILTRADOS", ("cierre", "documentos filtrados")),
             ("LA BLOCKCHAIN", ("cierre", "una blockchain"))]),
    g("chips", "cierre", "con multas", ("cierre", "Y aquí va la parte"), items=["MULTAS", "CÁRCEL", "BIENES CONFISCADOS"], color=RED),
    g("title", "cierre", "nunca prestes tu cuenta", 2.6, text="NUNCA PRESTES TU CUENTA", color=RED, fg=WHT),
    g("chips", "cierre", "tu Nequi", ("cierre", "Así es como reclutan"), items=["CUENTA BANCARIA", "NEQUI", "DAVIPLATA"]),
    g("sticker", "cierre", "Así es como reclutan", 3.6, text="ASÍ RECLUTAN A LAS \"MULAS\" DE DINERO", color=YEL),
    g("title", "cierre", "cuál de estos casos", 3.0, text="¿CUÁL TE PARECIÓ MÁS INCREÍBLE?", color=YEL, size=84),
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


_CH = {"10": "El pitufeo", "9": "Negocios de fachada", "8": "Los casinos", "7": "Casas de lujo", "6": "El arte",
       "5": "Mercado negro del peso", "4": "Empresas fantasma", "3": "Criptomonedas", "2": "Bancos que miran para otro lado",
       "1": "1MDB: el robo de un país"}
CHAPTERS = [(0.0, "Introducción")] + [(c["t0"], f"#{c['n']} " + _CH[c["n"]] if c["n"] else c["text"].replace("\n", " ").capitalize())
                                      for c in CARDS if c["kind"] == "chapter"]

if __name__ == "__main__":
    print("END %.1f s = %d:%02d" % (END, END // 60, END % 60), "shots", len(SHOTS), "gfx", len(GFX))
    for c in CHAPTERS:
        print("%d:%02d %s" % (c[0] // 60, c[0] % 60, c[1]))
    durs = [(SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END_SCREEN) - SHOTS[i][0] for i in range(len(SHOTS))]
    print("long", [(round(SHOTS[i][0], 1), SHOTS[i][1], round(d, 1)) for i, d in enumerate(durs) if d > 7])
    print("short", [(round(SHOTS[i][0], 1), SHOTS[i][1], round(d, 2)) for i, d in enumerate(durs) if d < 0.8])
