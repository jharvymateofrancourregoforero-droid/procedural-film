"""VIDEO 5 · Si perdieras todo mañana, ¿cómo volverías a empezar?"""


def build(E):
    S, G = E.shot, E.g
    shots = [
        S(None, "", "black"),
        S("Sin ahorros", "dark_window"),
        S("sin propiedades", "house_dark"),
        S("Qué harías para conseguir", "sunrise_mtn"),
        S("Primero buscaría", "lw_laptop"),
        S("Aprendería una habilidad", "lw_writing"),
        S("buscaría oportunidades laborales", "lw_desk"),
        S("o desarrollaría un servicio", "lw_papers"),
        S("Porque antes de pensar", "hands_typing"),
        S("Segundo controlaría", "lw_table"),
        S("Tercero separaría", "coin_hand"),
        S("Y cuarto estudiaría", "books_shelf"),
        S("Porque conseguir dinero", "workspace"),
        S("pero aprender a administrarlo", "wallst_book", "card", cy=1000),
        S("No necesitas comenzar siendo rico", "stairs_concrete"),
        S("Necesitas comenzar con una estrategia", "skyline_sunset"),
        S("Ahora te toca a ti", "city_street"),
        S("cuál sería tu primera decisión", "city_chicago"),
    ]
    gfx = [
        G("counter", 0.0, "Sin ahorros", a=0, b=0, size=260, y=900, run=0.1),
        G("chip", "Sin ahorros", "Qué harías para conseguir", text="SIN AHORROS", y=640, bg=(40, 40, 46), fg=(255, 255, 255)),
        G("chip", "sin inversiones", "Qué harías para conseguir", text="SIN INVERSIONES", y=760, bg=(40, 40, 46), fg=(255, 255, 255)),
        G("chip", "sin propiedades", "Qué harías para conseguir", text="SIN PROPIEDADES", y=880, bg=(40, 40, 46), fg=(255, 255, 255)),
        G("big", "tu primer millón", "Primero buscaría", text="TU PRIMER\nMILLÓN", size=150, track=3),
        G("chip", "Primero buscaría", "Porque antes de pensar", text="1 · GENERA INGRESOS", y=420, size=56),
        G("label", "Porque antes de pensar", "Segundo controlaría", text="PRIMERO PRODUCIR\nLUEGO MULTIPLICAR", size=86, style="gold", y=800),
        G("list", "Segundo controlaría", "Porque conseguir dinero", y=470,
          items=[("GENERA INGRESOS", "Primero buscaría"), ("CONTROLA GASTOS", "Segundo controlaría"),
                 ("FONDO DE EMERGENCIA", "Tercero separaría"), ("ESTUDIA ANTES DE INVERTIR", "Y cuarto estudiaría")]),
        G("label", "pero aprender a administrarlo", "No necesitas comenzar siendo rico", text="ADMINÍSTRALO", size=120, style="gold", y=430),
        G("label", "No necesitas comenzar siendo rico", "Necesitas comenzar con una estrategia", text="NO NECESITAS\nEMPEZAR RICO", size=100, y=800),
        G("chart", "Necesitas comenzar con una estrategia", "Ahora te toca a ti", fn=lambda x: x ** 1.8 + 0.1 * x, lo=0, y=1180, draw=2.6),
        G("big", "Necesitas comenzar con una estrategia", "Ahora te toca a ti", text="ESTRATEGIA", size=140, y=430, track=4),
        G("question", "Ahora te toca a ti", "END", text="¿CUÁL SERÍA TU\nPRIMERA DECISIÓN?", size=92, y=700,
          sub="Te leo en los comentarios"),
    ]
    return dict(
        shots=shots, gfx=gfx,
        hook=("SI PERDIERAS TODO", "¿CÓMO EMPEZARÍAS?"),
        thumb=dict(img="skyline_sunset", lines=("DE CERO A TU", "PRIMER MILLÓN"), y=0.30),
        merges=[(["cero", "pesos"], "$0")],
        reveal=E.at("No necesitas comenzar siendo rico"),
        hits=[E.at("Primero buscaría"), E.at("Segundo controlaría"), E.at("Tercero separaría"), E.at("Y cuarto estudiaría")],
        key=2,
    )
