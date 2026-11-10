"""Previa (una hoja con 4 fotogramas) o render final con audio a -14 LUFS.

Uso:
  python herramientas/exportar.py proyectos/<slug>/plan.json --previa [--formato vertical]
  python herramientas/exportar.py proyectos/<slug>/plan.json --formato vertical|horizontal|ambos

Si la sesión es nueva (nube), regenera voz.wav desde la caché y re-descarga los medios: sin costo.
Salidas en entregas/ (se versionan en git para descargarlas desde GitHub).
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from comun import PUBLIC, ffmpeg, leer_plan, verificar_raiz

FPS = 30
COMPOS = {"vertical": ("FinanzasVertical", "9x16"), "horizontal": ("FinanzasHorizontal", "16x9")}
ENTREGAS = Path("entregas")
HERR = Path(__file__).resolve().parent


def npx():
    return shutil.which("npx") or shutil.which("npx.cmd") or sys.exit("Falta Node.js (npx) en el PATH.")


def navegador():
    """Usa un Chrome ya instalado si existe; si no, Remotion descarga el suyo (requiere remotion.media)."""
    propio = os.environ.get("REMOTION_BROWSER_EXECUTABLE")
    if propio:
        return [f"--browser-executable={propio}"]
    for nombre in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        ruta = shutil.which(nombre)
        if ruta and "snap" not in os.path.realpath(ruta):
            return [f"--browser-executable={ruta}"]
    return []


def correr(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        salida = (r.stderr or r.stdout)
        lineas = [x for x in salida.splitlines() if not x.strip().startswith("at ")]
        print("\n".join(lineas[-25:]))
        if "remotion.media" in salida or "chrome-headless-shell" in salida:
            print("→ Permite remotion.media y www.remotion.dev en el acceso a red del entorno.")
        sys.exit(f"Falló: {' '.join(str(c) for c in cmd[:4])}…")


def asegurar_recursos(ruta_plan, plan):
    """En una sesión nueva faltan los archivos que no van en git: los regenera gratis."""
    if plan.get("voz") and not (PUBLIC / plan["voz"]).exists():
        print("Regenerando voz.wav desde la caché…")
        subprocess.run([sys.executable, str(HERR / "voz.py"), ruta_plan], check=True)
    faltan = any(e.get(c) and not (PUBLIC / e[c]).exists() for e in plan["escenas"] for c in ("src", "fondo"))
    if faltan:
        print("Recuperando medios…")
        subprocess.run([sys.executable, str(HERR / "medios.py"), ruta_plan], check=True)


def momentos_clave(escenas):
    """Gancho, primera cifra o zoom, primera gráfica y cierre (sin repetir)."""
    elegidas = [0]
    for criterio in (lambda e: e.get("entrada") == "zoom" or e.get("tipo") == "cifra",
                     lambda e: e.get("tipo") in ("linea", "barras", "comparar")):
        for i, e in enumerate(escenas):
            if i not in elegidas and criterio(e):
                elegidas.append(i)
                break
    if len(escenas) - 1 not in elegidas:
        elegidas.append(len(escenas) - 1)
    for i in range(len(escenas)):
        if len(elegidas) >= 4:
            break
        if i not in elegidas:
            elegidas.append(i)
    return sorted(elegidas[:4])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("plan")
    p.add_argument("--previa", action="store_true")
    p.add_argument("--formato", default="vertical", choices=["vertical", "horizontal", "ambos"])
    a = p.parse_args()

    verificar_raiz()
    plan = leer_plan(a.plan)
    slug = plan["slug"]
    if "inicio" not in plan["escenas"][0]:
        sys.exit("Primero genera la voz (voz.py): faltan los tiempos de las escenas.")
    asegurar_recursos(a.plan, plan)
    plan = leer_plan(a.plan)

    Path("out").mkdir(exist_ok=True)
    ENTREGAS.mkdir(exist_ok=True)
    formatos = ["vertical", "horizontal"] if a.formato == "ambos" else [a.formato]
    extra = [f"--props={a.plan}", *navegador()]

    if a.previa:
        comp, sufijo = COMPOS[formatos[0]]
        cuadros = []
        for n, i in enumerate(momentos_clave(plan["escenas"]), 1):
            e = plan["escenas"][i]
            t = min(e["fin"] - 0.1, e["inicio"] + 1.6)
            salida = f"out/{slug}-previa-{n}.jpg"
            correr([npx(), "remotion", "still", "src/index.ts", comp, salida, *extra,
                    f"--frame={int(t * FPS)}", "--image-format=jpeg"])
            cuadros.append(salida)
            print(f"Previa {n}: escena {i + 1} ({e.get('tipo')})")
        hoja = ENTREGAS / f"{slug}-previa-{sufijo}.jpg"
        alto = 720 if comp == "FinanzasVertical" else 400
        entradas = [x for c in cuadros for x in ("-i", c)]
        filtro = "".join(f"[{k}:v]scale=-2:{alto}[v{k}];" for k in range(len(cuadros)))
        filtro += "".join(f"[v{k}]" for k in range(len(cuadros))) + f"hstack=inputs={len(cuadros)}"
        if len(cuadros) == 1:
            filtro = f"[0:v]scale=-2:{alto}"
        correr([ffmpeg(), "-y", "-loglevel", "error", *entradas, "-filter_complex", filtro, "-q:v", "4", str(hoja)])
        print(f"Hoja de previa: {hoja}")
        return

    for f in formatos:
        comp, sufijo = COMPOS[f]
        crudo = f"out/{slug}-{sufijo}-crudo.mp4"
        final = ENTREGAS / f"{slug}-{sufijo}.mp4"
        correr([npx(), "remotion", "render", "src/index.ts", comp, crudo, *extra,
                "--codec=h264", "--crf=20", "--audio-bitrate=192k"])
        correr([ffmpeg(), "-y", "-loglevel", "error", "-i", crudo, "-c:v", "copy",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", str(final)])
        Path(crudo).unlink(missing_ok=True)
        mb = final.stat().st_size / 1e6
        print(f"Render listo: {final} ({mb:.1f} MB)")


if __name__ == "__main__":
    main()
