"""VIDEO 2 · Estás perdiendo dinero y probablemente no lo sabes."""


def build(E):
    S, G = E.shot, E.g
    shots = [
        S(None, "wallet_glasses"),
        S("y aun así estar perdiendo", "burn_cash"),
        S("Cómo es posible", "man_dark"),
        S("La respuesta es la inflación", "road_arrow"),
        S("Imagina que hoy puedes comprar", "fruit_market", "card", cy=1120, maxh=620),
        S("Pero los precios aumentan", "grocery", "card", cy=1120, maxh=620),
        S("Ahora necesitas", "bananas", "card", cy=1120, maxh=620),
        S("Ves el problema", "grocery_fridge"),
        S("Tus billetes siguen", "cash_hand", "card", cy=1000),
        S("pero su poder de compra", "mall_arcade"),
        S("Por eso ahorrar es importante", "piggy_calc", "card", cy=1000),
        S("cómo proteger el valor", "umbrella"),
        S("Existen alternativas", "office_windows"),
        S("aunque cada una tiene", "corridor_dark"),
        S("Te tengo una pregunta", "clock_old"),
        S("crees que cien mil pesos", "clock_pastel"),
        S("Responde sí o no", "city_dusk"),
    ]
    gfx = [
        G("big", "perdiendo dinero", 1.8, text="−$", style="red", size=220, y=820),
        G("big", "La respuesta es la inflación", "Imagina que hoy puedes comprar", text="INFLACIÓN", size=160, track=4),
        G("price", "Imagina que hoy puedes comprar", "Ves el problema", label="TU MERCADO", a=200000, b=220000,
          t_change=E.at("Pero los precios aumentan"), badge="+10 %", y=560),
        G("label", "Tus billetes siguen", "pero su poder de compra", text="MISMOS BILLETES", size=92, y=420),
        G("bar", "pero su poder de compra", "Por eso ahorrar es importante", label="PODER DE COMPRA", to=1 / 1.1, y=760),
        G("note", "pero su poder de compra", "Por eso ahorrar es importante",
          text="Con precios 10 % más altos, el mismo dinero\ncompra cerca del 91 % de lo que compraba.", y=1250),
        G("label", "cómo proteger el valor", "Existen alternativas", text="PROTEGE\nSU VALOR", size=110, style="gold", y=800),
        G("chip", "cedetés", "aunque cada una tiene", text="CDT", y=600, size=70),
        G("chip", "fondos de inversión", "aunque cada una tiene", text="FONDOS DE INVERSIÓN", y=740, size=56),
        G("label", "aunque cada una tiene", "Te tengo una pregunta", text="CADA UNA TIENE\nCONDICIONES Y RIESGOS", size=78, y=800),
        G("big", "cien mil pesos", "Responde sí o no", text="$100.000", size=170, y=640),
        G("label", "dentro de diez años", "Responde sí o no", text="¿DENTRO DE 10 AÑOS?", size=80, style="gold", y=820),
        G("question", "Responde sí o no", "END", text="¿COMPRARÁN\nLO MISMO?", size=110, y=640, options=["SÍ", "NO"],
          sub="Responde en los comentarios"),
    ]
    return dict(
        shots=shots, gfx=gfx,
        hook=("TU DINERO", "DESAPARECE"),
        thumb=dict(img="burn_cash", lines=("TU DINERO", "DESAPARECE"), y=0.30),
        merges=[(["un", "millón", "de", "pesos"], "$1.000.000"), (["doscientos", "mil", "pesos"], "$200.000"),
                (["diez", "por", "ciento"], "10 %"), (["doscientos", "veinte", "mil", "pesos"], "$220.000"),
                (["cedetés"], "CDT"), (["cien", "mil", "pesos"], "$100.000"), (["diez", "años"], "10 años")],
        reveal=E.at("La respuesta es la inflación"),
        hits=[E.at("Ahora necesitas")],
        key=-2,
    )
