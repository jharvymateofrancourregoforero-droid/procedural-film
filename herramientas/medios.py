"""Descarga clips y fotos gratis (Pexels → Pixabay → Pexels fotos) para cada escena.

Uso:
  python herramientas/medios.py proyectos/<slug>/plan.json [--forzar]

Procesa escenas `media` sin `src` y escenas con `fondo_query` sin `fondo`.
Guarda en public/<slug>/medios/ y anota créditos en public/<slug>/creditos.txt.
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

from comun import RAIZ, PUBLIC, cargar_env, carpeta_publica, clave, guardar_plan, leer_plan, verificar_raiz

UA = {"User-Agent": "finanzas-video/1.0"}


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  aviso: {url.split('?')[0]} respondió {e.code}")
    except Exception as e:  # noqa: BLE001
        print(f"  aviso: {e}")
    return None


def descargar(url, destino):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r, open(destino, "wb") as f:
        while True:
            bloque = r.read(1 << 16)
            if not bloque:
                break
            f.write(bloque)


def mejor_archivo(archivos, vertical, alto_obj):
    """Elige el archivo de la orientación correcta más cercano a la resolución objetivo."""
    cands = []
    for f in archivos:
        w, h, link = f.get("width") or 0, f.get("height") or 0, f.get("link") or f.get("url")
        if not link or not w or not h:
            continue
        if (h > w) != vertical:
            continue
        lado = max(w, h)
        if lado < 1000:
            continue
        cands.append((abs(lado - alto_obj), lado > 2600, link, w, h))
    if not cands:
        return None
    cands.sort(key=lambda c: (c[1], c[0]))
    return cands[0]


def pexels_video(q, vertical, dur, usados, clave):
    orient = "portrait" if vertical else "landscape"
    url = ("https://api.pexels.com/videos/search?" +
           urllib.parse.urlencode({"query": q, "orientation": orient, "per_page": 15, "size": "medium"}))
    datos = get_json(url, {"Authorization": clave} if clave else None)
    if not datos:
        return None
    vids = sorted(datos.get("videos", []), key=lambda v: (v.get("duration", 0) < dur, 0))
    for v in vids:
        if f"pexels-{v['id']}" in usados:
            continue
        arch = mejor_archivo(v.get("video_files", []), vertical, 1920)
        if arch:
            autor = (v.get("user") or {}).get("name", "autor")
            return {"id": f"pexels-{v['id']}", "url": arch[2], "ext": "mp4", "dur": v.get("duration", 0),
                    "credito": f"Video de {autor} en Pexels: {v.get('url', '')}"}
    return None


def pixabay_video(q, vertical, dur, usados, clave):
    url = ("https://pixabay.com/api/videos/?" +
           urllib.parse.urlencode({"key": clave, "q": q[:100], "per_page": 20, "safesearch": "true"}))
    datos = get_json(url)
    if not datos:
        return None
    hits = sorted(datos.get("hits", []), key=lambda h: h.get("duration", 0) < dur)
    for h in hits:
        if f"pixabay-{h['id']}" in usados:
            continue
        archivos = [{"width": x.get("width"), "height": x.get("height"), "link": x.get("url")}
                    for x in (h.get("videos") or {}).values()]
        arch = mejor_archivo(archivos, vertical, 1920)
        if arch:
            return {"id": f"pixabay-{h['id']}", "url": arch[2], "ext": "mp4", "dur": h.get("duration", 0),
                    "credito": f"Video de {h.get('user', 'autor')} en Pixabay: {h.get('pageURL', '')}"}
    return None


def pexels_foto(q, vertical, usados, clave):
    orient = "portrait" if vertical else "landscape"
    url = ("https://api.pexels.com/v1/search?" +
           urllib.parse.urlencode({"query": q, "orientation": orient, "per_page": 10}))
    datos = get_json(url, {"Authorization": clave} if clave else None)
    if not datos:
        return None
    for f in datos.get("photos", []):
        if f"pexelsf-{f['id']}" in usados:
            continue
        src = f.get("src") or {}
        link = src.get("large2x") or src.get("original")
        if link:
            return {"id": f"pexelsf-{f['id']}", "url": link, "ext": "jpg", "dur": 0,
                    "credito": f"Foto de {f.get('photographer', 'autor')} en Pexels: {f.get('url', '')}"}
    return None


def buscar(q, vertical, dur, usados, claves):
    pex, pix = claves
    for intento in (
        (lambda: pexels_video(q, vertical, dur, usados, pex)) if pex is not None else None,
        (lambda: pixabay_video(q, vertical, dur, usados, pix)) if pix else None,
        (lambda: pexels_foto(q, vertical, usados, pex)) if pex is not None else None,
    ):
        if intento:
            r = intento()
            if r:
                return r
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("plan")
    p.add_argument("--forzar", action="store_true", help="vuelve a buscar aunque ya haya src")
    a = p.parse_args()

    verificar_raiz()
    cargar_env()

    plan = leer_plan(a.plan)
    slug = plan["slug"]
    base = carpeta_publica(slug)
    carpeta = base / "medios"
    carpeta.mkdir(exist_ok=True)
    vertical = plan.get("formato", "vertical") != "horizontal"
    creditos_ruta = base / "creditos.txt"
    creditos = creditos_ruta.read_text(encoding="utf-8").splitlines() if creditos_ruta.exists() else []
    usados = {c.split("|", 1)[0].strip() for c in creditos if "|" in c}

    # Sesión nueva en la nube: los medios no van en git; se re-descargan de su URL guardada (sin buscar).
    recuperados = 0
    for e in plan["escenas"]:
        for campo in ("src", "fondo"):
            ruta, url = e.get(campo), e.get(f"{campo}_url")
            if ruta and url and not (PUBLIC / ruta).exists():
                (PUBLIC / ruta).parent.mkdir(parents=True, exist_ok=True)
                try:
                    descargar(url, PUBLIC / ruta)
                    recuperados += 1
                except Exception as err:  # noqa: BLE001
                    print(f"  aviso: no se pudo recuperar {ruta} ({err}); se buscará otro")
                    e[campo] = None
    if recuperados:
        print(f"Recuperados {recuperados} medios desde sus URL guardadas.")

    tareas = []
    for i, e in enumerate(plan["escenas"]):
        if e.get("tipo") == "media" and e.get("query") and (a.forzar or not e.get("src")):
            tareas.append((i, "src", e["query"]))
        if e.get("fondo_query") and (a.forzar or not e.get("fondo")):
            tareas.append((i, "fondo", e["fondo_query"]))

    if not tareas:
        if recuperados:
            guardar_plan(a.plan, plan)
        print("Nada que buscar: todas las escenas ya tienen medio.")
        return

    claves = (clave("PEXELS_API_KEY"), clave("PIXABAY_API_KEY"))
    if claves[0] is None and not claves[1]:
        sys.exit("Falta PEXELS_API_KEY o PIXABAY_API_KEY en las variables del entorno (o en .env).")

    faltan = 0
    for i, campo, q in tareas:
        e = plan["escenas"][i]
        dur = max(2.0, (e.get("fin") or 0) - (e.get("inicio") or 0))
        r = buscar(q, vertical, dur, usados, claves)
        if not r:
            faltan += 1
            print(f"{i + 1:>2} ✗ sin resultados para '{q}' — cambia la query")
            continue
        nombre = f"{i + 1:02d}_{campo}_{r['id']}.{r['ext']}"
        try:
            descargar(r["url"], carpeta / nombre)
        except Exception as err:  # noqa: BLE001
            faltan += 1
            print(f"{i + 1:>2} ✗ falló la descarga ({err})")
            continue
        e[campo] = f"{slug}/medios/{nombre}"
        e[f"{campo}_url"] = r["url"]
        usados.add(r["id"])
        creditos.append(f"{r['id']} | {r['credito']}")
        corto = " (más corto que la escena: irá en bucle)" if r["dur"] and r["dur"] < dur else ""
        print(f"{i + 1:>2} ✓ {r['id']} {r['dur'] or 'foto'}{'s' if r['dur'] else ''}{corto}")

    creditos_ruta.write_text("\n".join(creditos) + "\n", encoding="utf-8")
    guardar_plan(a.plan, plan)
    print(f"Listo: {len(tareas) - faltan}/{len(tareas)} medios. Créditos en public/{slug}/creditos.txt")


if __name__ == "__main__":
    main()
