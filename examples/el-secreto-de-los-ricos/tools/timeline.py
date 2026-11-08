"""Edit decision list for "El secreto de los ricos" (YouTube, 16:9).

Every cut and graphic is anchored to a phrase of the narration, so timings
come from the ElevenLabs word timestamps in audio/words_<segment>.json.
To add a narration block later, add it to SEGMENTS and anchor shots to it.
"""
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1920, 1080, 30

# Narration blocks in playback order. card = chapter card shown before the block.
SEGMENTS = [
    ("escena0", None),
    ("escena1", ("1", "ANDRÉS Y CAMILA")),
    ("andres_mes", None),
    ("escena2", ("2", "LA TRAMPA DE\nVENDER TU TIEMPO")),
    ("palancas", ("3", "LAS 3 PALANCAS\nDE LA RIQUEZA")),
    ("escena3", ("4", "INGRESOS VS.\nPATRIMONIO")),
    ("escena4", ("5", "EL PODER\nDE LOS ACTIVOS")),
    ("trampas", ("6", "LAS TRAMPAS DEL\nDINERO FÁCIL")),
    ("escena5", ("7", "CUATRO\nDECISIONES")),
    ("plan30", ("8", "TU PLAN\nDE 30 DÍAS")),
    ("escena6", ("", "PARA\nTERMINAR")),
]
TITLE_LEN, CARD_LEN, END_LEN = 4.2, 3.2, 20.0


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def _load(seg):
    words = json.load(open(os.path.join(ROOT, "audio", f"words_{seg}.json")))["words"]
    return [w for w in words if not re.fullmatch(r"\[.*\]", w["text"])]


WORDS = {s: _load(s) for s, _ in SEGMENTS}
DUR = {s: WORDS[s][-1]["end"] for s, _ in SEGMENTS}

# Global layout: where each block starts, and where cards sit.
OFFSET, CARDS = {}, []
_t = 0.4
for i, (seg, card) in enumerate(SEGMENTS):
    if i == 1:
        CARDS.append(dict(kind="maintitle", t0=_t + 0.4, t1=_t + 0.4 + TITLE_LEN))
        _t += 0.4 + TITLE_LEN
    if card:
        CARDS.append(dict(kind="chapter", n=card[0], text=card[1], t0=_t + 0.3, t1=_t + 0.3 + CARD_LEN))
        _t += 0.3 + CARD_LEN + 0.3
    elif i:
        _t += 0.5
    OFFSET[seg] = _t
    _t += DUR[seg]
END_SCREEN = _t + 0.6
END = END_SCREEN + END_LEN


def at(seg, phrase, nth=0, end=False):
    """Global time of a phrase in a narration block (start of its first word)."""
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


# ---------------------------------------------------------------- shots
# (segment, phrase, photo, mode, options). Modes: full, card, left, right, split.
_EDIT = [
    # Gancho
    ("escena0", "Si trabajar duro", "traffic", "full", {}),
    ("escena0", "las personas más ricas", "luxcar_in", "card", {}),
    ("escena0", "las que más horas", "alarm_blue", "full", {}),
    ("escena0", "Y no lo son", "chess_fall", "full", {}),
    ("escena0", "Piénsalo", "worker_hat", "full", {}),
    ("escena0", "carga ladrillos", "bricks_tools", "left", {}),
    ("escena0", "trabaja más duro", "biz_laugh", "full", {}),
    ("escena0", "Entonces qué está pasando", "think_wall", "full", {}),
    ("escena0", "En este video", "cash_hands", "full", {}),
    ("escena0", "y construir riqueza", "bricks", "full", {}),
    ("escena0", "Y al final", "calendar_jan", "right", {}),
    ("escena0", "ganes lo que ganes", "cash_fan", "full", {}),
    ("escena0", "Quédate", "chess_pawn", "full", {}),
    # 1. Andrés y Camila
    ("escena1", "Te presento a Andrés", "andres", "full", {}),
    ("escena1", "Se levanta", "alarm_dark", "full", {}),
    ("escena1", "Dos horas de bus", "tm_night", "full", {}),
    ("escena1", "Diez horas de trabajo", "andres2", "full", {}),
    ("escena1", "Llega a la casa", "sofa_tired", "full", {}),
    ("escena1", "y al día siguiente", "alarm_vintage", "full", {"flash": True}),
    ("escena1", "Y te presento a Camila", "camila", "full", {}),
    ("escena1", "Camila trabaja menos", "camila2", "right", {}),
    ("escena1", "Pero tiene algo", "wallst_book", "full", {}),
    ("escena1", "dinero que sigue entrando", "sleep_woman", "full", {}),
    ("escena1", "Los dos necesitan", "andres", "split", {"img2": "camila"}),
    ("escena1", "La diferencia no es", "chess_game", "full", {}),
    ("escena1", "La diferencia es cómo", "money_machine", "full", {}),
    ("escena1", "y qué hacen con él", "cash_hand", "full", {}),
    # 1b. El mes de Andrés
    ("andres_mes", "Vamos a ponerle", "calc_acc", "full", {}),
    ("andres_mes", "Andrés gana", "andres2", "left", {}),
    ("andres_mes", "Parece suficiente", "calendar_desk", "full", {}),
    ("andres_mes", "Setecientos mil se van", "apartment", "right", {}),
    ("andres_mes", "Seiscientos mil en mercado", "fruit_market", "right", {}),
    ("andres_mes", "Ciento cincuenta mil en transporte", "tm_station", "right", {}),
    ("andres_mes", "Doscientos mil en servicios", "woman_phone", "right", {}),
    ("andres_mes", "Doscientos cincuenta mil en la cuota", "card_hand", "right", {}),
    ("andres_mes", "Y ciento cincuenta mil en salidas", "motos", "right", {}),
    ("andres_mes", "Total", "calc_hand", "right", {}),
    ("andres_mes", "Andrés no está ahorrando", "biz_stress", "full", {}),
    ("andres_mes", "Y esa diferencia", "card_hand2", "full", {}),
    ("andres_mes", "Mes a mes", "rain_window", "full", {}),
    ("andres_mes", "Y Andrés trabaja más", "andres2", "full", {}),
    ("andres_mes", "Robert Kiyosaki", "library", "full", {}),
    ("andres_mes", "la carrera de la rata", "runner", "full", {"flash": True}),
    ("andres_mes", "Corres todos los días", "track", "full", {}),
    ("andres_mes", "porque todo lo que entra", "cash_fan", "full", {}),
    ("andres_mes", "Y ojo Andrés no es", "andres", "full", {}),
    ("andres_mes", "Andrés simplemente nunca", "think_dark", "full", {}),
    ("andres_mes", "Y eso es exactamente", "road_forest", "full", {}),
    # 2. La trampa de vender tu tiempo
    ("escena2", "Desde niños", "kid_homework", "full", {}),
    ("escena2", "estudia", "student_book", "card", {}),
    ("escena2", "consigue un buen empleo", "handshake", "card", {}),
    ("escena2", "trabaja duro", "worker_belt", "card", {}),
    ("escena2", "y tendrás una vida estable", "family", "full", {}),
    ("escena2", "Y ojo ese camino", "office_women", "full", {}),
    ("escena2", "Un empleo te da", "office_man", "full", {}),
    ("escena2", "El problema es otro", "night_person", "full", {}),
    ("escena2", "Si tu único ingreso", "watches", "full", {}),
    ("escena2", "tu dinero tiene un techo", "clock_vintage", "full", {}),
    ("escena2", "Y ese techo se llama", "clock_wall", "full", {"flash": True}),
    ("escena2", "Hagamos la cuenta", "calc_acc", "left", {}),
    ("escena2", "y trabajas unas", "calendar_desk", "left", {}),
    ("escena2", "tu hora vale", "calc_hand", "left", {}),
    ("escena2", "Quieres ganar el doble", "chess_pawn", "full", {}),
    ("escena2", "trabajar el doble de horas", "alarm_dark", "left", {}),
    ("escena2", "conseguir que te paguen", "code", "left", {}),
    ("escena2", "o crear dinero", "seedlings", "left", {}),
    ("escena2", "La primera tiene un límite", "sofa_tired", "full", {}),
    ("escena2", "La segunda se logra", "book_read", "full", {}),
    ("escena2", "Y la tercera", "mountain", "full", {"flash": True}),
    # 3. Las 3 palancas
    ("palancas", "Pero cómo se crea", "think_wall", "full", {}),
    ("palancas", "La respuesta tiene un nombre", "chess_dark", "full", {}),
    ("palancas", "Apalancarte es usar", "brain", "full", {}),
    ("palancas", "Y existen tres palancas", "bulb", "full", {}),
    ("palancas", "La primera el trabajo", "team2", "full", {}),
    ("palancas", "Piensa en la dueña", "bakery", "full", {}),
    ("palancas", "Si ella sola hace el pan", "baker", "card", {}),
    ("palancas", "Pero si contrata", "bread_shop", "full", {}),
    ("palancas", "el negocio produce", "bread_basket", "full", {}),
    ("palancas", "La segunda el capital", "coins", "full", {}),
    ("palancas", "Un ahorro bien invertido", "bolsa_sp", "full", {}),
    ("palancas", "Y la tercera la más poderosa", "video_cam", "full", {"flash": True}),
    ("palancas", "Un video un libro", "videographer", "split", {"img2": "mic"}),
    ("palancas", "Los haces una vez", "keyboard", "full", {}),
    ("palancas", "y se pueden vender", "rocket_trail", "full", {}),
    ("palancas", "Mira este ejemplo", "students", "full", {}),
    ("palancas", "Una profesora de matemáticas", "kid_writing", "right", {}),
    ("palancas", "Si quiere ganar más", "alarm_pink", "right", {}),
    ("palancas", "Pero si graba un curso", "podcast", "right", {}),
    ("palancas", "cien estudiantes", "laptop_study", "right", {}),
    ("palancas", "por un trabajo que hizo", "rocket", "full", {}),
    ("palancas", "Ahora no te voy a mentir", "biz_think", "full", {}),
    ("palancas", "El apalancamiento no es", "stairs", "full", {}),
    ("palancas", "Es trabajo que una vez hecho", "seedlings2", "full", {}),
    ("palancas", "Esa es la gran diferencia", "andres", "split", {"img2": "camila2"}),
    ("palancas", "Camila construye cosas", "camila", "full", {}),
    # 4. Ingresos vs patrimonio
    ("escena3", "Ahora una verdad incómoda", "think_dark", "full", {}),
    ("escena3", "ganar mucho no es", "skyline", "full", {}),
    ("escena3", "Imagina a alguien que gana quince", "biz_coffee", "left", {}),
    ("escena3", "Carro nuevo", "luxcar_in2", "full", {}),
    ("escena3", "ropa de marca", "shopping", "full", {}),
    ("escena3", "viajes cada tres meses", "airplane", "full", {}),
    ("escena3", "Pero gasta todo", "card_shop", "full", {}),
    ("escena3", "y un poquito más", "card_hand2", "full", {}),
    ("escena3", "Si mañana pierde", "biz_stress", "full", {}),
    ("escena3", "Quizá ninguno", "rain_building", "full", {}),
    ("escena3", "Ahora imagina a alguien que gana tres", "tienda", "left", {}),
    ("escena3", "no tiene deudas caras", "notebook_calc", "left", {}),
    ("escena3", "y cada mes guarda", "piggy_calc", "left", {}),
    ("escena3", "Quién crees", "biz_coffee", "split", {"img2": "tienda"}),
    ("escena3", "Para entenderlo", "library", "full", {}),
    ("escena3", "Ingresos el dinero", "cash_hand", "right", {}),
    ("escena3", "Gastos el dinero", "shopping2", "right", {}),
    ("escena3", "Y patrimonio", "keys", "right", {}),
    ("escena3", "La riqueza no se mide", "seedlings", "full", {}),
    ("escena3", "Se mide por lo que se queda", "garden", "full", {}),
    # 5. El poder de los activos
    ("escena4", "Entonces qué hace diferente", "camila2", "full", {}),
    ("escena4", "Que compra y construye", "bricks", "full", {"flash": True}),
    ("escena4", "Un activo es algo", "savings_bills", "full", {}),
    ("escena4", "Un negocio bien administrado", "cafe_cacao", "left", {}),
    ("escena4", "Un apartamento que se arrienda", "apartment2", "left", {}),
    ("escena4", "Una inversión que da", "bolsa_sp", "left", {}),
    ("escena4", "Un libro un curso", "mic_guitar", "left", {}),
    ("escena4", "Y sí también una habilidad", "students", "full", {}),
    ("escena4", "Aprender inglés", "code2", "split", {"img2": "sales"}),
    ("escena4", "puede multiplicar", "calc_hand", "full", {}),
    ("escena4", "Ahora la parte", "biz_think", "full", {}),
    ("escena4", "todos los activos tienen riesgo", "stock_red", "full", {"flash": True}),
    ("escena4", "Un negocio puede quebrar", "rain_building", "full", {}),
    ("escena4", "un apartamento se puede quedar", "old_building", "full", {}),
    ("escena4", "una inversión puede bajar", "stock_red2", "full", {}),
    ("escena4", "Por eso la idea no es apostar", "dice", "full", {}),
    ("escena4", "La idea es aprender", "plant_pot", "right", {}),
    ("escena4", "Y lo más poderoso", "clock_vintage", "full", {}),
    ("escena4", "Si inviertes doscientos", "coins", "card", {}),
    ("escena4", "habrías puesto", "savings_bills", "card", {}),
    ("escena4", "pero podrías terminar", "cash_hands", "full", {"flash": True}),
    ("escena4", "No por trabajar más horas", "garden", "full", {}),
    # 6. Trampas
    ("trampas", "Y ya que hablamos", "wrong_way", "full", {}),
    ("trampas", "Cada cierto tiempo", "burn_money", "full", {}),
    ("trampas", "Y la historia de Colombia", "night_street", "full", {}),
    ("trampas", "miles de personas", "bus_people", "full", {}),
    ("trampas", "Prometían rendimientos", "dice", "full", {}),
    ("trampas", "Aprende estas cuatro", "road_closed", "full", {"flash": True}),
    ("trampas", "Uno te garantizan", "stop_sign", "left", {}),
    ("trampas", "En las inversiones reales", "stock_red2", "left", {}),
    ("trampas", "Dos te presionan", "alarm_pink", "left", {}),
    ("trampas", "Tres ganas dinero", "team", "left", {}),
    ("trampas", "Y cuatro nadie", "think_wall", "left", {}),
    ("trampas", "Antes de entregar", "handshake2", "full", {}),
    ("trampas", "Y hay otra trampa", "card_hand", "full", {}),
    ("trampas", "Los préstamos gota a gota", "motos", "full", {}),
    ("trampas", "los avances de tarjeta", "card_shop", "full", {}),
    ("trampas", "Cada peso que pagas", "cash_fan", "full", {}),
    ("trampas", "y empieza a trabajar", "money_machine", "full", {}),
    # 7. Cuatro decisiones
    ("escena5", "Muy bien", "andres", "full", {}),
    ("escena5", "Con cuatro decisiones", "checklist", "full", {"flash": True}),
    ("escena5", "Uno conoce tus números", "bank_calc", "right", {}),
    ("escena5", "Durante un mes", "writing", "right", {}),
    ("escena5", "No puedes mejorar", "calc_hand", "right", {}),
    ("escena5", "Dos invierte en tu", "laptop_study", "right", {}),
    ("escena5", "Es el activo que nadie", "book_read", "right", {}),
    ("escena5", "y el que más rápido", "code2", "right", {}),
    ("escena5", "Tres la que más gente", "luxcar_in", "full", {"flash": True}),
    ("escena5", "Si te aumentan", "cash_hands", "left", {}),
    ("escena5", "deja que al menos", "piggy_calc", "left", {}),
    ("escena5", "Así tu estilo de vida", "seedlings2", "full", {}),
    ("escena5", "Y cuatro construye", "umbrella", "full", {"flash": True}),
    ("escena5", "Después estudia", "wallst_book", "full", {}),
    ("escena5", "y con el riesgo", "chess_dark", "full", {}),
    ("escena5", "Y si tienes dudas", "handshake2", "full", {}),
    ("escena5", "No se trata de renunciar", "office_man", "full", {}),
    ("escena5", "ni de buscar dinero fácil", "burn_money", "full", {}),
    ("escena5", "Se trata de usar", "cash_hand", "full", {}),
    ("escena5", "como la herramienta", "freedom", "full", {}),
    # 8. Plan de 30 días
    ("plan30", "Y para que esto", "todo", "full", {}),
    ("plan30", "Semana uno", "pen_paper", "right", {}),
    ("plan30", "Puede ser en una libreta", "woman_phone", "right", {}),
    ("plan30", "Al final de la semana", "calc_acc", "right", {}),
    ("plan30", "Semana dos", "notebook_calc", "right", {}),
    ("plan30", "Una referencia muy popular", "bank_calc", "card", {}),
    ("plan30", "Si hoy no te alcanza", "piggy_calc", "full", {}),
    ("plan30", "Semana tres", "scissors", "right", {}),
    ("plan30", "y escoge tu deuda", "card_hand2", "right", {}),
    ("plan30", "Semana cuatro", "phone_field", "right", {}),
    ("plan30", "y programa que", "woman_phone", "right", {}),
    ("plan30", "Págate primero", "savings_bills", "full", {}),
    ("plan30", "Y durante esos treinta días", "laptop_study", "full", {}),
    ("plan30", "Treinta minutos al día", "clock_wall", "full", {}),
    ("plan30", "Imagina que Andrés", "andres", "full", {}),
    ("plan30", "Pero por primera vez", "city_sunset", "full", {}),
    ("plan30", "Y ese pequeño cambio", "stairs", "full", {}),
    ("plan30", "de los que ponen", "rocket", "full", {}),
    # Para terminar
    ("escena6", "Trabajar duro te hace", "road_forest", "full", {}),
    ("escena6", "Pero trabajar duro sin", "alone_window", "full", {}),
    ("escena6", "El cambio empieza", "city_sunset", "full", {}),
    ("escena6", "y empiezas a preguntarte", "cranes", "full", {}),
    ("escena6", "Ahora dime tú", "phone_field", "full", {}),
    ("escena6", "Ganar mucho o saber", "andres", "split", {"img2": "camila"}),
    ("escena6", "Si este video te sirvió", "woman_phone", "full", {}),
    ("escena6", "porque en el próximo", "card_hand", "full", {}),
    ("escena6", "el dinero que parece", "card_hand2", "full", {}),
    ("escena6", "Nos vemos", "skyline", "full", {}),
]

SHOTS = sorted([(at(seg, ph) - 0.05, img, mode, opt) for seg, ph, img, mode, opt in _EDIT], key=lambda s: s[0])
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
    g("big", "escena0", "Y no lo son", 1.6, text="NO LO SON", color=RED),
    g("side", "escena0", "carga ladrillos", ("escena0", "trabaja más duro"), lines=["12 HORAS", "AL DÍA"], color=YEL),
    g("title", "escena0", "Entonces qué está pasando", 2.2, text="¿QUÉ ESTÁ PASANDO?", color=YEL),
    g("compare", "escena0", "la diferencia que casi", ("escena0", "Y al final"), a="GANAR DINERO", b="CONSTRUIR RIQUEZA"),
    g("side", "escena0", "Y al final", ("escena0", "ganes lo que ganes"), lines=["4", "DECISIONES"], color=YEL),
    g("sticker", "escena0", "la tercera es", 2.4, text="LA #3 ES LA CLAVE", color=YEL),

    g("lower", "escena1", "Te presento a Andrés", 3.0, name="ANDRÉS", sub="Vende su tiempo"),
    g("big", "escena1", "Se levanta", 1.9, text="5:00 AM", color=WHT),
    g("sticker", "escena1", "Dos horas de bus", 1.6, text="2 H DE BUS", color=YEL),
    g("sticker", "escena1", "Diez horas de trabajo", 1.6, text="10 H DE TRABAJO", color=YEL),
    g("lower", "escena1", "Y te presento a Camila", 3.0, name="CAMILA", sub="Construye activos"),
    g("side", "escena1", "Camila trabaja menos", ("escena1", "Pero tiene algo"), lines=["MENOS", "HORAS"], color=GRN),
    g("ticker", "escena1", "dinero que sigue entrando", ("escena1", "Los dos necesitan")),
    g("compare", "escena1", "Los dos necesitan", ("escena1", "La diferencia no es"), a="ANDRÉS", b="CAMILA"),

    g("table", "andres_mes", "Setecientos mil se van", ("andres_mes", "Andrés no está ahorrando"),
      rows=[("Arriendo", "$700.000", ("andres_mes", "Setecientos mil se van")),
            ("Mercado y comida", "$600.000", ("andres_mes", "Seiscientos mil en mercado")),
            ("Transporte", "$150.000", ("andres_mes", "Ciento cincuenta mil en transporte")),
            ("Servicios y celular", "$200.000", ("andres_mes", "Doscientos mil en servicios")),
            ("Cuota de la tarjeta", "$250.000", ("andres_mes", "Doscientos cincuenta mil en la cuota")),
            ("Salidas y gastos hormiga", "$150.000", ("andres_mes", "Y ciento cincuenta mil en salidas"))],
      total=("TOTAL", "$2.050.000", ("andres_mes", "Total")), income="INGRESO $2.000.000"),
    g("side", "andres_mes", "Andrés gana", ("andres_mes", "Parece suficiente"), lines=["$2.000.000", "AL MES"], color=GRN),
    g("big", "andres_mes", "Está cincuenta mil", 2.4, text="−$50.000", color=RED),
    g("title", "andres_mes", "la carrera de la rata", 2.6, text="LA CARRERA DE LA RATA", color=YEL),
    g("note", "andres_mes", "Robert Kiyosaki", 4.0, text="Robert Kiyosaki, «Padre rico, padre pobre» (1997)"),

    g("formula", "escena2", "estudia", ("escena2", "Y ojo ese camino"),
      steps=[("ESTUDIA", ("escena2", "estudia")), ("EMPLEO", ("escena2", "consigue un buen empleo")),
             ("TRABAJA DURO", ("escena2", "trabaja duro")), ("¿ESTABILIDAD?", ("escena2", "y tendrás una vida estable"))]),
    g("big", "escena2", "Y ese techo se llama", 2.6, text="24 HORAS", color=YEL),
    g("side", "escena2", "Hagamos la cuenta", ("escena2", "y trabajas unas"), lines=["$2.000.000", "AL MES"], color=WHT),
    g("side", "escena2", "y trabajas unas", ("escena2", "tu hora vale"), lines=["48 H × SEMANA", "≈ 208 H/MES"], color=WHT),
    g("counter", "escena2", "tu hora vale", ("escena2", "Quieres ganar el doble"), a=0, b=9615, fmt="${:,}", label="POR HORA", side="right"),
    g("side", "escena2", "trabajar el doble de horas", ("escena2", "conseguir que te paguen"), lines=["1", "MÁS HORAS"], color=RED),
    g("side", "escena2", "conseguir que te paguen", ("escena2", "o crear dinero"), lines=["2", "MÁS VALOR", "POR HORA"], color=YEL),
    g("side", "escena2", "o crear dinero", ("escena2", "La primera tiene un límite"), lines=["3", "DINERO SIN", "VENDER HORAS"], color=GRN),
    g("title", "escena2", "es donde empieza", 2.2, text="AQUÍ EMPIEZA LA RIQUEZA", color=GRN),

    g("title", "palancas", "La respuesta tiene un nombre", 2.8, text="APALANCAMIENTO", color=YEL),
    g("list", "palancas", "Y existen tres palancas", ("palancas", "Mira este ejemplo"),
      items=[("PERSONAS", ("palancas", "La primera el trabajo")), ("CAPITAL", ("palancas", "La segunda el capital")),
             ("PRODUCTOS QUE SE COPIAN", ("palancas", "Y la tercera la más poderosa"))]),
    g("side", "palancas", "Una profesora de matemáticas", ("palancas", "Si quiere ganar más"), lines=["$50.000", "POR CLASE"], color=WHT),
    g("side", "palancas", "Si quiere ganar más", ("palancas", "Pero si graba un curso"), lines=["MÁS INGRESO =", "MÁS CLASES"], color=RED),
    g("side", "palancas", "Pero si graba un curso", ("palancas", "cien estudiantes"), lines=["CURSO", "$80.000"], color=YEL),
    g("counter", "palancas", "cien estudiantes", ("palancas", "por un trabajo que hizo"), a=0, b=8000000, fmt="${:,}", label="100 ESTUDIANTES", side="left"),
    g("big", "palancas", "por un trabajo que hizo", 2.6, text="UNA SOLA VEZ", color=GRN),
    g("sticker", "palancas", "El apalancamiento no es", 2.6, text="NO ES DINERO FÁCIL", color=RED, fg=WHT),
    g("compare", "palancas", "Esa es la gran diferencia", ("palancas", "Camila construye cosas", True), a="VENDE HORAS", b="CONSTRUYE ACTIVOS"),

    g("title", "escena3", "ganar mucho no es", 2.6, text="GANAR MUCHO ≠ SER RICO", color=YEL),
    g("side", "escena3", "Imagina a alguien que gana quince", ("escena3", "Carro nuevo"), lines=["$15.000.000", "AL MES"], color=GRN),
    g("big", "escena3", "Quizá ninguno", 1.8, text="0 MESES", color=RED),
    g("side", "escena3", "Ahora imagina a alguien que gana tres", ("escena3", "no tiene deudas caras"), lines=["GANA $3.000.000", "VIVE CON $2.500.000"], color=GRN),
    g("side", "escena3", "no tiene deudas caras", ("escena3", "y cada mes guarda"), lines=["SIN DEUDAS", "CARAS"], color=WHT),
    g("side", "escena3", "y cada mes guarda", ("escena3", "Quién crees"), lines=["AHORRA", "CADA MES"], color=GRN),
    g("compare", "escena3", "Quién crees", ("escena3", "Para entenderlo"), a="GANA MÁS", b="CONSERVA MÁS"),
    g("side", "escena3", "Ingresos el dinero", ("escena3", "Gastos el dinero"), lines=["INGRESOS", "lo que entra"], color=GRN),
    g("side", "escena3", "Gastos el dinero", ("escena3", "Y patrimonio"), lines=["GASTOS", "lo que sale"], color=RED),
    g("side", "escena3", "Y patrimonio", ("escena3", "La riqueza no se mide"), lines=["PATRIMONIO", "tienes − debes"], color=YEL),

    g("title", "escena4", "Que compra y construye", 2.4, text="ACTIVOS", color=GRN),
    g("side", "escena4", "Un negocio bien administrado", ("escena4", "Un apartamento que se arrienda"), lines=["NEGOCIO", "utilidades"], color=GRN),
    g("side", "escena4", "Un apartamento que se arrienda", ("escena4", "Una inversión que da"), lines=["INMUEBLE", "arriendo"], color=GRN),
    g("side", "escena4", "Una inversión que da", ("escena4", "Un libro un curso"), lines=["INVERSIÓN", "rendimientos"], color=GRN),
    g("side", "escena4", "Un libro un curso", ("escena4", "Y sí también una habilidad"), lines=["CREACIONES", "regalías"], color=GRN),
    g("sticker", "escena4", "todos los activos tienen riesgo", 2.6, text="TODO ACTIVO TIENE RIESGO", color=RED, fg=WHT),
    g("side", "escena4", "La idea es aprender", ("escena4", "Y lo más poderoso"), lines=["APRENDER", "DIVERSIFICAR", "EMPEZAR PEQUEÑO"], color=YEL),
    g("chart", "escena4", "Si inviertes doscientos", ("escena4", "No por trabajar más horas")),
    g("counter", "escena4", "pero podrías terminar", ("escena4", "No por trabajar más horas"), a=48000000, b=143700000, fmt="${:,}", label="EN 20 AÑOS", side="center", y=330),
    g("note", "escena4", "Si inviertes doscientos", ("escena4", "No por trabajar más horas", True),
      text="Ejemplo hipotético: $200.000/mes, 10% anual compuesto, 20 años. Sin inflación ni impuestos. No es asesoría financiera."),

    g("title", "trampas", "duplicar tu plata", 2.4, text="«DUPLICA TU PLATA»", color=RED, fg=WHT),
    g("note", "trampas", "en dos mil ocho", 5.0, text="2008: captadoras ilegales DMG y DRFE (Colombia)"),
    g("side", "trampas", "Uno te garantizan", ("trampas", "Dos te presionan"), lines=["1", "GANANCIA", "GARANTIZADA"], color=RED),
    g("side", "trampas", "Dos te presionan", ("trampas", "Tres ganas dinero"), lines=["2", "PRESIÓN PARA", "ENTRAR YA"], color=RED),
    g("side", "trampas", "Tres ganas dinero", ("trampas", "Y cuatro nadie"), lines=["3", "PAGO POR", "TRAER GENTE"], color=RED),
    g("side", "trampas", "Y cuatro nadie", ("trampas", "Antes de entregar"), lines=["4", "NADIE EXPLICA", "LA GANANCIA"], color=RED),
    g("sticker", "trampas", "verifica si la entidad", 3.6, text="VERIFICA EN LA SUPERFINANCIERA", color=YEL),
    g("title", "trampas", "la deuda cara", 2.2, text="DEUDA CARA", color=RED, fg=WHT),

    g("title", "escena5", "Con cuatro decisiones", 2.2, text="4 DECISIONES", color=YEL),
    g("badge", "escena5", "Uno conoce tus números", ("escena5", "Dos invierte en tu"), n="1", text="CONOCE TUS\nNÚMEROS", side="left"),
    g("badge", "escena5", "Dos invierte en tu", ("escena5", "Tres la que más gente"), n="2", text="INVIERTE EN TU\nHABILIDAD", side="left"),
    g("badge", "escena5", "Tres la que más gente", ("escena5", "Si te aumentan"), n="3", text="SUBE EL SUELDO,\nNO LA VIDA", side="center"),
    g("side", "escena5", "Si te aumentan", ("escena5", "Así tu estilo de vida"), lines=["+$300.000", "$150.000 → AHORRO"], color=GRN),
    g("badge", "escena5", "Y cuatro construye", ("escena5", "Después estudia"), n="4", text="FONDO DE\nEMERGENCIA", side="center"),
    g("sticker", "escena5", "de tres a seis meses", 2.4, text="3 A 6 MESES DE GASTOS", color=YEL),

    g("side", "plan30", "Semana uno", ("plan30", "Semana dos"), lines=["SEMANA 1", "REGISTRA"], color=YEL),
    g("side", "plan30", "Semana dos", ("plan30", "Una referencia muy popular"), lines=["SEMANA 2", "ORGANIZA"], color=YEL),
    g("rule", "plan30", "Una referencia muy popular", ("plan30", "Si hoy no te alcanza")),
    g("big", "plan30", "empieza con el cinco", 2.2, text="EMPIEZA CON EL 5%", color=GRN),
    g("side", "plan30", "Semana tres", ("plan30", "Semana cuatro"), lines=["SEMANA 3", "RECORTA", "Y ATACA"], color=YEL),
    g("side", "plan30", "Semana cuatro", ("plan30", "Págate primero"), lines=["SEMANA 4", "AUTOMATIZA"], color=YEL),
    g("title", "plan30", "Págate primero", 2.4, text="PÁGATE PRIMERO A TI", color=GRN),
    g("big", "plan30", "Treinta minutos al día", 3.0, text="30 MIN/DÍA = 182 H/AÑO", color=YEL),
    g("big", "plan30", "termina el mes en verde", 2.2, text="+ EN VERDE", color=GRN),

    g("compare", "escena6", "Ganar mucho o saber", ("escena6", "Si este video te sirvió"), a="GANAR MUCHO", b="SABER ADMINISTRARLO"),
    g("subscribe", "escena6", "Si este video te sirvió", ("escena6", "porque en el próximo")),
    g("title", "escena6", "la trampa de las tarjetas", 3.4, text="PRÓXIMO: LA TRAMPA\nDE LAS TARJETAS", color=YEL),
]
GFX += CARDS
GFX.append(dict(kind="end", t0=END_SCREEN, t1=END))

# Camera hits: shake + colour split.
HITS = sorted({round(s[0], 3) for s in SHOTS if s[3].get("flash")} | {round(x["t0"], 3) for x in GFX if x["kind"] in ("title", "big")})

# Chapter starts, for the description and the music.
CHAPTERS = [(0.0, "Introducción")] + [(c["t0"], c["text"].replace("\n", " ").title() if c["kind"] == "chapter" else "") for c in CARDS if c["kind"] == "chapter"]


def caption_chunks():
    toks = []
    for seg, _ in SEGMENTS:
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


if __name__ == "__main__":
    print("END %.1f s = %d:%02d" % (END, END // 60, END % 60), "shots", len(SHOTS), "gfx", len(GFX))
    for c in CHAPTERS:
        print("%d:%02d %s" % (c[0] // 60, c[0] % 60, c[1]))
    durs = [(SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END_SCREEN) - SHOTS[i][0] for i in range(len(SHOTS))]
    long = [(round(SHOTS[i][0], 1), SHOTS[i][1], round(d, 1)) for i, d in enumerate(durs) if d > 7]
    short = [(round(SHOTS[i][0], 1), SHOTS[i][1], round(d, 2)) for i, d in enumerate(durs) if d < 0.7]
    print("long", long)
    print("short", short)
