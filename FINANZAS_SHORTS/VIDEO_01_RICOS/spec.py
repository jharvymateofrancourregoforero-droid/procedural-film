"""VIDEO 1 · ¿Por qué los ricos se hacen más ricos?"""


def build(E):
    S, G = E.shot, E.g
    shots = [
        S(None, "woman_laptop", "split", img2="sunset_person"),
        S("mientras otras consiguen", "biz_suit"),
        S("que su dinero produzca", "money_curr"),
        S("La diferencia está", "skyline_fog"),
        S("los activos", "skyscraper_up"),
        S("Mientras algunos utilizan", "mall_glass"),
        S("para consumir", "shopper_walk"),
        S("otros destinan una parte", "store_p"),
        S("adquirir inversiones", "bolsa_sp", "card", cy=1000),
        S("desarrollar fuentes de ingresos", "office_desk"),
        S("No significa que todos", "chess_board"),
        S("pero existe un principio", "stairs_city"),
        S("construir patrimonio requiere", "skyscraper2"),
        S("más que recibir un salario", "watch_wrist"),
        S("Y aquí viene lo interesante", "mountain_person"),
        S("Puedes empezar aprendiendo", "woman_writing"),
        S("desarrollando habilidades", "library_woman"),
        S("y construyendo pequeños activos", "plant_growth"),
        S("Ahora responde con sinceridad", "city_bldgs"),
        S("si mañana recibieras", "cash_hands", "card", cy=1050),
        S("lo gastarías", "shopper_bags", "split", img2="plant_pot2"),
        S("Escribe gastar o invertir", "city_chicago"),
    ]
    gfx = [
        G("big", "cuarenta años", 1.6, text="40 AÑOS", y=800),
        G("big", "los activos", "Mientras algunos utilizan", text="ACTIVOS", size=170, track=6),
        G("label", "para consumir", "otros destinan una parte", text="CONSUMIR", style="red", size=110, y=820),
        G("chip", "construir negocios", "desarrollar fuentes de ingresos", text="NEGOCIOS", y=420),
        G("chip", "adquirir inversiones", "desarrollar fuentes de ingresos", text="INVERSIONES", y=540),
        G("label", "desarrollar fuentes de ingresos", "No significa que todos", text="FUENTES DE\nINGRESOS", size=96, style="gold", y=820),
        G("label", "No significa que todos", "pero existe un principio", text="NO HAY UNA SOLA\nESTRATEGIA", size=80, y=820),
        G("chart", "construir patrimonio requiere", "Y aquí viene lo interesante", fn=lambda x: x ** 2.2 + 0.08, lo=0, y=1150,
          draw=3.2),
        G("label", "más que recibir un salario", "Y aquí viene lo interesante", text="PATRIMONIO ≠ SALARIO", size=78, style="gold", y=420),
        G("big", "no necesitas ser millonario", "Puedes empezar aprendiendo", text="NO NECESITAS\nSER MILLONARIO", size=100, y=760),
        G("list", "Puedes empezar aprendiendo", "Ahora responde con sinceridad", y=470,
          items=[("ADMINISTRA TUS INGRESOS", "Puedes empezar aprendiendo"), ("DESARROLLA HABILIDADES", "desarrollando habilidades"),
                 ("CONSTRUYE ACTIVOS", "y construyendo pequeños activos")]),
        G("counter", "un millón de pesos", "lo gastarías", a=0, b=1000000, label="ADICIONALES", y=420, size=140),
        G("compare", "lo gastarías", "Escribe gastar o invertir", a="GASTAR", b="INVERTIR", sa="red"),
        G("question", "Escribe gastar o invertir", "END", text="¿GASTAR\nO INVERTIR?", size=110, y=640,
          options=["GASTAR", "INVERTIR"], sub="Escríbelo en los comentarios"),
    ]
    return dict(
        shots=shots, gfx=gfx,
        hook=("¿POR QUÉ LOS RICOS", "SE HACEN MÁS RICOS?"),
        thumb=dict(img="skyscraper_up", lines=("LOS RICOS", "JUEGAN DIFERENTE"), y=0.32),
        merges=[(["cuarenta", "años"], "40 años"), (["un", "millón", "de", "pesos"], "$1.000.000")],
        reveal=E.at("Y aquí viene lo interesante"),
        hits=[E.at("los activos"), E.at("construir patrimonio requiere")],
        key=0,
    )
