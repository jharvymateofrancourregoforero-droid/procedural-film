"""VIDEO 3 · 100 dólares pueden enseñarte una lección millonaria."""


def build(E):
    S, G = E.shot, E.g
    shots = [
        S(None, "hundred"),
        S("sin añadir un solo dólar", "strap"),
        S("No es magia", "gold_lights"),
        S("Imagina que consigues", "office_work"),
        S("y reinviertes", "coins", "card", cy=1000),
        S("El primer año", "gold_power"),
        S("Notas algo", "snowball", "card", cy=1000),
        S("los rendimientos también", "savings_bills", "card", cy=1000),
        S("Y aquí viene lo sorprendente", "skyscraper3"),
        S("tus cien dólares", "office_ext"),
        S("Pero recuerda", "street_fog"),
        S("Ahora dime", "road_rural"),
        S("Recibir mil dólares hoy", "piggy_cc0", "split", img2="road_travel"),
    ]
    gfx = [
        G("big", "es interés compuesto", "Imagina que consigues", text="INTERÉS\nCOMPUESTO", size=140, track=3),
        G("chip", "rentabilidad hipotética", "y reinviertes", text="10 % ANUAL · HIPOTÉTICO", y=480, size=54),
        G("label", "y reinviertes", "El primer año", text="REINVIERTES\nLAS GANANCIAS", size=92, style="gold", y=420),
        G("dark", "El primer año", "Notas algo", amount=120),
        G("steps", "El primer año", "Notas algo", y=440,
          items=[("INICIO · US$100", E.at("El primer año") - 0.01), ("AÑO 1 · US$110", "ciento diez"),
                 ("AÑO 2 · US$121", "El segundo"), ("AÑO 3 · US$133", "El tercero")]),
        G("coins", "El primer año", "Notas algo", y=1240,
          stacks=[(5, 0.0), (6, "ciento diez"), (7, "El segundo"), (8, "El tercero")]),
        G("label", "los rendimientos también", "Y aquí viene lo sorprendente", text="RENDIMIENTOS QUE\nPRODUCEN RENDIMIENTOS",
          size=78, style="gold", y=420),
        G("chart", "Y aquí viene lo sorprendente", "Casi diez veces", fn=lambda x: 100 * 1.1 ** (24 * x), lo=0, y=1200,
          draw=4.0, xlabels=[(0, "0"), (0.5, "12 años"), (1, "24 años")]),
        G("counter", "tus cien dólares", "Pero recuerda", a=100, b=984.97, cur="US$", dec=2, size=130, y=420,
          label="EN 24 AÑOS", run=2.2),
        G("big", "Casi diez veces", "Pero recuerda", text="×9,8", size=240, y=820),
        G("note", "Y aquí viene lo sorprendente", "Ahora dime",
          text="Simulación: US$100 al 10 % anual compuesto durante 24 años,\nsin aportes, impuestos ni comisiones. No es una promesa.", y=1250),
        G("label", "Pero recuerda", "Ahora dime", text="SIMULACIÓN\nNO GARANTIZADA", size=100, y=800),
        G("compare", "Recibir mil dólares hoy", "END", a="US$1.000 HOY", b="PATRIMONIO", sa="white", vs=False, ya=480, yb=1230),
        G("question", "construir patrimonio a largo plazo", "END", text="¿QUÉ PREFIERES?", size=92, y=900),
    ]
    return dict(
        shots=shots, gfx=gfx,
        hook=("100 DÓLARES", "UNA LECCIÓN MILLONARIA"),
        thumb=dict(img="gold_power", lines=("EL DINERO", "SE MULTIPLICA"), y=0.30),
        merges=[(["cien", "dólares"], "US$100"), (["diez", "por", "ciento"], "10 %"), (["ciento", "diez", "dólares"], "US$110"),
                (["ciento", "veintiuno"], "US$121"), (["ciento", "treinta", "y", "tres", "dólares"], "US$133"),
                (["veinticuatro", "años"], "24 años"), (["novecientos", "ochenta", "y", "cuatro", "dólares"], "US$984"),
                (["diez", "veces"], "10 veces"), (["mil", "dólares"], "US$1.000")],
        reveal=E.at("Y aquí viene lo sorprendente"),
        hits=[E.at("ciento diez"), E.at("El segundo"), E.at("El tercero")],
        key=3,
    )
