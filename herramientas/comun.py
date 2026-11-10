"""Utilidades compartidas: claves, rutas del proyecto, ffmpeg y lectura/escritura del plan."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Windows y terminales en la nube: evita errores de codificación al imprimir tildes y símbolos.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

RAIZ = Path.cwd()
PUBLIC = RAIZ / "public"


def cargar_env():
    """Carga .env si existe (en la nube las claves llegan como variables del entorno o por el proxy)."""
    for carpeta in [RAIZ, *RAIZ.parents]:
        archivo = carpeta / ".env"
        if archivo.exists():
            for linea in archivo.read_text(encoding="utf-8").splitlines():
                linea = linea.strip()
                if not linea or linea.startswith("#") or "=" not in linea:
                    continue
                clave, valor = linea.split("=", 1)
                os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))
            return


def clave(nombre):
    """None = no configurada. "" = la inyecta el proxy (valor `proxy` en las variables del entorno,
    con la clave guardada como credencial de API). Otro valor = la clave misma."""
    valor = os.environ.get(nombre, "").strip()
    if not valor:
        return None
    return "" if valor.lower() in ("proxy", "proxy-injected") else valor


def requerir(nombre):
    valor = clave(nombre)
    if not valor:
        sys.exit(f"Falta {nombre}: agrégala en las variables del entorno en la nube (o en .env).")
    return valor


def ffmpeg():
    """ffmpeg del sistema o, si no hay, el binario de imageio-ffmpeg (se instala desde PyPI)."""
    ruta = shutil.which("ffmpeg")
    if ruta:
        return ruta
    try:
        import imageio_ffmpeg  # noqa: F401
    except ImportError:
        print("Instalando ffmpeg portátil (imageio-ffmpeg)…")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "imageio-ffmpeg"], check=False)
        try:
            import imageio_ffmpeg  # noqa: F401
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages",
                            "imageio-ffmpeg"], check=True)
            import imageio_ffmpeg  # noqa: F401
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def verificar_raiz():
    if not (RAIZ / "package.json").exists() or not PUBLIC.exists():
        sys.exit("Ejecuta este script desde la raíz del proyecto (donde están package.json y public/).")


def leer_plan(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        sys.exit(f"No existe {ruta}")
    plan = json.loads(ruta.read_text(encoding="utf-8"))
    if not plan.get("slug"):
        plan["slug"] = ruta.parent.name
    if not plan.get("escenas"):
        sys.exit("El plan no tiene escenas.")
    return plan


def guardar_plan(ruta, plan):
    Path(ruta).write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def carpeta_publica(slug):
    carpeta = PUBLIC / slug
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta
