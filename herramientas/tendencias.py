"""Encuentra videos recientes de YouTube que están rindiendo por encima de su canal (outliers).

Uso:
  python herramientas/tendencias.py "consulta 1" "consulta 2" [--dias 14] [--region CO] [--top 12]

Requiere YOUTUBE_API_KEY (gratis en Google Cloud, YouTube Data API v3).
Cada consulta gasta ~100 unidades de una cuota diaria de 10.000.
"""
import argparse
import datetime as dt
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from comun import cargar_env, requerir

API = "https://www.googleapis.com/youtube/v3/"


def get(recurso, **params):
    url = API + recurso + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"YouTube API {e.code}: {e.read().decode('utf-8', 'ignore')[:300]}")


def segundos(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def main():
    p = argparse.ArgumentParser()
    p.add_argument("consultas", nargs="+")
    p.add_argument("--dias", type=int, default=14)
    p.add_argument("--region", default="CO")
    p.add_argument("--top", type=int, default=12)
    a = p.parse_args()

    cargar_env()
    clave = requerir("YOUTUBE_API_KEY")
    desde = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.dias)).strftime("%Y-%m-%dT%H:%M:%SZ")

    ids = []
    for q in a.consultas:
        r = get("search", part="id", q=q, type="video", order="viewCount", publishedAfter=desde,
                regionCode=a.region, relevanceLanguage="es", maxResults=25, key=clave)
        ids += [it["id"]["videoId"] for it in r.get("items", []) if it.get("id", {}).get("videoId")]
    ids = list(dict.fromkeys(ids))[:50]
    if not ids:
        print("Sin resultados.")
        return

    vids = get("videos", part="snippet,statistics,contentDetails", id=",".join(ids), key=clave).get("items", [])
    canales = list({v["snippet"]["channelId"] for v in vids})[:50]
    subs = {c["id"]: int(c.get("statistics", {}).get("subscriberCount", 0) or 0)
            for c in get("channels", part="statistics", id=",".join(canales), key=clave).get("items", [])}

    ahora = dt.datetime.now(dt.timezone.utc)
    filas = []
    for v in vids:
        sn, st = v["snippet"], v.get("statistics", {})
        vistas = int(st.get("viewCount", 0) or 0)
        pub = dt.datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00"))
        dias = max(0.5, (ahora - pub).total_seconds() / 86400)
        s = subs.get(sn["channelId"], 0)
        dur = segundos(v.get("contentDetails", {}).get("duration"))
        filas.append({
            "titulo": sn["title"][:80], "canal": sn["channelTitle"][:28], "vistas": vistas,
            "vd": int(vistas / dias), "ratio": round(vistas / s, 1) if s else 0,
            "tipo": "short" if dur <= 180 else f"{dur // 60}min", "id": v["id"],
        })
    filas.sort(key=lambda f: (f["ratio"], f["vd"]), reverse=True)

    print(f"{'ratio':>6} {'vistas/día':>10} {'tipo':>6}  título — canal")
    for f in filas[:a.top]:
        print(f"{f['ratio']:>6} {f['vd']:>10} {f['tipo']:>6}  {f['titulo']} — {f['canal']}")

    carpeta = Path("tendencias")
    carpeta.mkdir(exist_ok=True)
    (carpeta / f"youtube-{ahora:%Y-%m-%d}.json").write_text(
        json.dumps(filas[:a.top], ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
