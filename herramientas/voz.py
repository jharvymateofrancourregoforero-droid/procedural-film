"""Genera la narración con ElevenLabs, escena por escena, con caché y tiempos por palabra.

Uso:
  python herramientas/voz.py proyectos/<slug>/plan.json [--borrador] [--solo N] [--pausa 0.22]

Escribe en public/<slug>/: voz.wav, palabras.json y actualiza el plan (voz, palabras,
duracion, inicio/fin por escena). Solo cobra las escenas cuyo texto cambió.
"""
import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
import wave

from comun import cargar_env, carpeta_publica, clave as leer_clave, ffmpeg, guardar_plan, leer_plan, requerir, verificar_raiz

MODELO_FINAL = "eleven_multilingual_v2"
MODELO_BORRADOR = "eleven_flash_v2_5"
AJUSTES_BASE = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.2, "use_speaker_boost": True}
TASA = 44100


def llamar_api(texto, voz_id, modelo, ajustes, anterior, siguiente, clave):
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{voz_id}/with-timestamps"
           f"?output_format=mp3_44100_128")
    cuerpo = {"text": texto, "model_id": modelo, "voice_settings": ajustes}
    if anterior:
        cuerpo["previous_text"] = anterior
    if siguiente:
        cuerpo["next_text"] = siguiente
    cabeceras = {"Content-Type": "application/json"}
    if clave:  # sin clave: la inyecta el proxy si está guardada como credencial de API del entorno
        cabeceras["xi-api-key"] = clave
    req = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8"), method="POST", headers=cabeceras)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            datos = json.loads(r.read())
    except urllib.error.HTTPError as e:
        pista = " (revisa ELEVENLABS_API_KEY o la credencial del entorno)" if e.code in (401, 403) else ""
        sys.exit(f"ElevenLabs respondió {e.code}{pista}: {e.read().decode('utf-8', 'ignore')[:300]}")
    except urllib.error.URLError as e:
        sys.exit(f"Sin conexión con api.elevenlabs.io ({e.reason}). Permite ese dominio en el acceso a red del entorno.")
    alineacion = datos.get("alignment") or datos.get("normalized_alignment")
    if not alineacion:
        sys.exit("ElevenLabs no devolvió tiempos (alignment).")
    return base64.b64decode(datos["audio_base64"]), alineacion


def a_wav(mp3, wav):
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", mp3, "-ar", str(TASA), "-ac", "1",
                    "-c:a", "pcm_s16le", wav], check=True)


def leer_wav(ruta):
    with wave.open(ruta, "rb") as w:
        return w.readframes(w.getnframes())


def palabras_de(alineacion):
    """Convierte la alineación por caracteres en palabras [{w, s, e}]."""
    chars = alineacion["characters"]
    ini = alineacion["character_start_times_seconds"]
    fin = alineacion["character_end_times_seconds"]
    palabras, actual, s, e = [], "", None, None
    for c, a, b in zip(chars, ini, fin):
        if c.isspace():
            if actual:
                palabras.append({"w": actual, "s": s, "e": e})
            actual, s = "", None
            continue
        if s is None:
            s = a
        actual += c
        e = b
    if actual:
        palabras.append({"w": actual, "s": s, "e": e})
    return palabras


def main():
    p = argparse.ArgumentParser()
    p.add_argument("plan")
    p.add_argument("--borrador", action="store_true", help="modelo flash: más barato, para pruebas")
    p.add_argument("--solo", type=int, help="regenera solo esta escena (número desde 1)")
    p.add_argument("--pausa", type=float, default=0.22, help="silencio por defecto entre escenas (s)")
    a = p.parse_args()

    verificar_raiz()
    cargar_env()
    clave = leer_clave("ELEVENLABS_API_KEY")
    plan = leer_plan(a.plan)
    voz_id = plan.get("voz_id") or requerir("ELEVENLABS_VOICE_ID")
    modelo = MODELO_BORRADOR if a.borrador else (os.environ.get("ELEVENLABS_MODEL") or MODELO_FINAL)
    ajustes = {**AJUSTES_BASE, **(plan.get("voz_ajustes") or {})}

    slug = plan["slug"]
    base = carpeta_publica(slug)
    cache = base / "voz" / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    escenas = plan["escenas"]

    pcm_total = bytearray()
    todas = []
    cursor = 0.0
    nuevos_chars = 0
    reusadas = 0
    bytes_seg = TASA * 2  # mono, 16 bits

    for i, esc in enumerate(escenas):
        texto = (esc.get("texto") or "").strip()
        if not texto:
            sys.exit(f"La escena {i + 1} no tiene texto.")
        firma = json.dumps([texto, voz_id, modelo, ajustes], sort_keys=True, ensure_ascii=False)
        clave_cache = hashlib.sha1(firma.encode("utf-8")).hexdigest()[:16]
        mp3, wav, ali = (cache / f"{clave_cache}.{x}" for x in ("mp3", "wav", "json"))

        forzar = a.solo == i + 1
        if forzar or not (mp3.exists() and ali.exists()):
            anterior = escenas[i - 1].get("texto", "") if i > 0 else ""
            siguiente = escenas[i + 1].get("texto", "") if i + 1 < len(escenas) else ""
            audio, alineacion = llamar_api(texto, voz_id, modelo, ajustes, anterior, siguiente, clave)
            mp3.write_bytes(audio)
            ali.write_text(json.dumps(alineacion), encoding="utf-8")
            if wav.exists():
                wav.unlink()
            nuevos_chars += len(texto)
        else:
            reusadas += 1
        if not wav.exists():
            a_wav(str(mp3), str(wav))

        alineacion = json.loads(ali.read_text(encoding="utf-8"))
        palabras = palabras_de(alineacion)
        pcm = leer_wav(str(wav))
        dur = len(pcm) / bytes_seg

        # Recorta el silencio propio del clip para que las pausas las controle el plan.
        corte_ini = max(0.0, (palabras[0]["s"] if palabras else 0) - 0.06)
        corte_fin = min(dur, (palabras[-1]["e"] if palabras else dur) + 0.14)
        b0, b1 = int(corte_ini * TASA) * 2, int(corte_fin * TASA) * 2
        pcm_total += pcm[b0:b1]

        inicio = cursor
        for w in palabras:
            todas.append({"w": w["w"], "s": round(inicio + w["s"] - corte_ini, 3),
                          "e": round(inicio + w["e"] - corte_ini, 3)})
        cursor += (b1 - b0) / bytes_seg
        esc["inicio"] = round(inicio, 3)
        esc["fin"] = round(cursor, 3)

        if i + 1 < len(escenas):
            pausa = esc.get("pausa")
            if pausa is None:
                pausa = 0.4 if texto.endswith(("?", "…", "...")) else a.pausa
            pcm_total += b"\x00\x00" * int(pausa * TASA)
            cursor += int(pausa * TASA) / TASA

    salida = base / "voz.wav"
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TASA)
        w.writeframes(bytes(pcm_total))
    (base / "palabras.json").write_text(json.dumps(todas, ensure_ascii=False), encoding="utf-8")

    plan["voz"] = f"{slug}/voz.wav"
    plan["palabras"] = f"{slug}/palabras.json"
    plan["duracion"] = round(cursor + 0.9, 2)
    guardar_plan(a.plan, plan)

    print(f"Voz lista: {len(escenas)} escenas, {cursor:.1f} s, modelo {modelo}. "
          f"Generadas {len(escenas) - reusadas}, reutilizadas {reusadas}, "
          f"caracteres cobrados ~{nuevos_chars}.")


if __name__ == "__main__":
    main()
