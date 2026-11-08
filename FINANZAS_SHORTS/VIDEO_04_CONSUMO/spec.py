"""VIDEO 4 · Tu cerebro podría estar haciéndote gastar más dinero."""


def build(E):
    S, G = E.shot, E.g
    shots = [
        S(None, "store_neon"),
        S("y después te preguntaste", "woman_think"),
        S("Las ofertas", "mall_blue"),
        S("y las compras a cuotas", "card_shop", "card", cy=1100, maxh=600),
        S("Cuando ves un producto", "phone_hand"),
        S("Pero si te dicen", "phone_hand2"),
        S("El problema es que dividir", "calc_hand", "card", cy=1050),
        S("Aquí tienes una estrategia", "chess_pawn", "card", cy=1050),
        S("espera veinticuatro horas", "clock_white"),
        S("Después pregúntate", "woman_window"),
        S("realmente lo necesito", "coffee_room"),
        S("A veces la mejor compra", "night_neon"),
        S("Ahora sé sincero", "shopping", "card", cy=1050),
        S("eres de los que compran", "store_made", "split", img2="watch_antique"),
        S("Escribe impulsivo", "mall_glass"),
    ]
    gfx = [
        G("chip", "Las ofertas", "Cuando ves un producto", text="OFERTAS", y=420),
        G("chip", "los descuentos", "Cuando ves un producto", text="DESCUENTOS", y=540),
        G("chip", "compras a cuotas", "Cuando ves un producto", text="CUOTAS", y=660),
        G("split_price", "Cuando ves un producto", "El problema es que dividir", total="$1.000.000",
          at_split="pequeñas cuotas", split="12 CUOTAS DE $83.333", foot="(sin contar intereses)", y=760),
        G("label", "dividir el precio", "Aquí tienes una estrategia", text="DIVIDIR EL PRECIO\nNO LO HACE MÁS BARATO", size=78,
          style="gold", y=420),
        G("label", "Aquí tienes una estrategia", "espera veinticuatro horas", text="UNA ESTRATEGIA\nSENCILLA", size=100, y=430),
        G("clock", "espera veinticuatro horas", "Después pregúntate", y=720, text="24 HORAS", sweep=2.4),
        G("list", "realmente lo necesito", "A veces la mejor compra", y=500,
          items=[("¿LO NECESITO?", "realmente lo necesito"), ("¿PUEDO PAGARLO?", "Puedo pagarlo"),
                 ("¿EN QUÉ MÁS LO USARÍA?", "Qué otra cosa")]),
        G("big", "A veces la mejor compra", "Ahora sé sincero", text="LA MEJOR COMPRA\nES LA QUE NO HACES", size=92, y=780),
        G("compare", "eres de los que compran", "Escribe impulsivo", a="IMPULSIVO", b="ESTRATÉGICO", sa="red"),
        G("question", "Escribe impulsivo", "END", text="¿IMPULSIVO O\nESTRATÉGICO?", size=96, y=640,
          options=["IMPULSIVO", "ESTRATÉGICO"], osize=48, sub="Escríbelo en los comentarios"),
    ]
    return dict(
        shots=shots, gfx=gfx,
        hook=("ANTES DE COMPRAR", "NO COMPRES TODAVÍA"),
        thumb=dict(img="store_neon", lines=("NO COMPRES", "TODAVÍA"), y=0.30),
        merges=[(["un", "millón", "de", "pesos"], "$1.000.000"), (["veinticuatro", "horas"], "24 horas")],
        reveal=E.at("Aquí tienes una estrategia"),
        hits=[E.at("El problema es que dividir")],
        key=-4,
    )
