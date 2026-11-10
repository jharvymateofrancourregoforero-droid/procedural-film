"""Cifras financieras de fuentes abiertas, en formato compacto y listas para el plan.

Uso:
  python herramientas/datos.py trm [--serie 12]           TRM Colombia (datos.gov.co)
  python herramientas/datos.py cripto bitcoin ethereum    Precio USD/COP y cambio 24 h (CoinGecko)
  python herramientas/datos.py accion AAPL [--serie 12]   Acción o índice (Yahoo Finance; pip install yfinance)

--serie N imprime un arreglo "datos" de N puntos para pegar en una escena linea/barras.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

# Windows: evita errores de codificación al imprimir tildes y símbolos.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "finanzas-video/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def imprimir_serie(puntos, n, dec=0):
    """puntos: lista (etiqueta, valor) en orden cronológico; reduce a n puntos uniformes."""
    if not puntos:
        return
    if len(puntos) > n:
        paso = (len(puntos) - 1) / (n - 1)
        puntos = [puntos[round(i * paso)] for i in range(n)]
    datos = [{"etiqueta": e, "valor": round(v, dec)} for e, v in puntos]
    print('"datos": ' + json.dumps(datos, ensure_ascii=False))


def trm(a):
    # Dataset oficial "Tasa de Cambio Representativa del Mercado - Histórico" (Superfinanciera).
    limite = max(31, (a.serie or 0) * 31)
    url = ("https://www.datos.gov.co/resource/32sa-8pi3.json?" +
           urllib.parse.urlencode({"$order": "vigenciadesde DESC", "$limit": limite}))
    try:
        filas = get_json(url)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"No se pudo leer la TRM ({e}). Búscala en la web: Banco de la República.")
    if not filas:
        sys.exit("Sin datos de TRM.")
    hoy = float(filas[0]["valor"])
    fecha = filas[0]["vigenciadesde"][:10]
    print(f"TRM {fecha}: ${hoy:,.2f} COP".replace(",", "X").replace(".", ",").replace("X", "."))
    for dias in (7, 30):
        if len(filas) > dias:
            antes = float(filas[min(dias, len(filas) - 1)]["valor"])
            print(f"  cambio ~{dias} registros: {((hoy / antes) - 1) * 100:+.2f} %")
    print("Fuente: Superfinanciera vía datos.gov.co")
    if a.serie:
        mensual = {}
        for f in reversed(filas):
            y, m = f["vigenciadesde"][:4], int(f["vigenciadesde"][5:7])
            mensual[(y, m)] = float(f["valor"])  # último dato del mes
        puntos = [(f"{MESES[m - 1]} {y[2:]}", v) for (y, m), v in mensual.items()][-a.serie:]
        imprimir_serie(puntos, a.serie)


def cripto(a):
    ids = ",".join(a.extra or ["bitcoin"])
    url = ("https://api.coingecko.com/api/v3/simple/price?" +
           urllib.parse.urlencode({"ids": ids, "vs_currencies": "usd,cop", "include_24hr_change": "true"}))
    try:
        datos = get_json(url)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"No se pudo leer CoinGecko ({e}). Búscalo en la web.")
    for k, v in datos.items():
        print(f"{k}: US${v.get('usd', 0):,.2f} | COP ${v.get('cop', 0):,.0f} | 24 h {v.get('usd_24h_change', 0):+.2f} %")
    print("Fuente: CoinGecko")


def accion(a):
    try:
        import yfinance as yf
    except ImportError:
        sys.exit("Instala yfinance: pip install yfinance")
    ticker = (a.extra or ["^GSPC"])[0]
    hist = yf.Ticker(ticker).history(period="1y", interval="1mo" if a.serie else "1d")
    if hist.empty:
        sys.exit(f"Sin datos para {ticker}")
    ultimo, primero = float(hist["Close"].iloc[-1]), float(hist["Close"].iloc[0])
    print(f"{ticker}: {ultimo:,.2f} | cambio 1 año {((ultimo / primero) - 1) * 100:+.1f} %")
    print("Fuente: Yahoo Finance")
    if a.serie:
        puntos = [(f"{MESES[i.month - 1]} {str(i.year)[2:]}", float(v)) for i, v in hist["Close"].items()]
        imprimir_serie(puntos[-a.serie:], a.serie, 2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("fuente", choices=["trm", "cripto", "accion"])
    p.add_argument("extra", nargs="*")
    p.add_argument("--serie", type=int)
    a = p.parse_args()
    {"trm": trm, "cripto": cripto, "accion": accion}[a.fuente](a)


if __name__ == "__main__":
    main()
