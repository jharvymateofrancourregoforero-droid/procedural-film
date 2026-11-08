# Instrucciones de producción

## Qué se usó

| Recurso | Herramienta | Estado |
|---|---|---|
| Narración | ElevenLabs `eleven_v4`, voz "Damián" | Generada, 1 toma por video |
| Tiempos por palabra | ElevenLabs Scribe | Generados (`words.json` en cada carpeta) |
| Imágenes | Fotos reales de StockSnap (CC0) y Wikimedia Commons (CC BY / BY-SA), vía Openverse | 87 fotos en `assets/photos/` |
| Video con IA (ElevenLabs, Veo, Kling…) | Disponible en el conector de ElevenLabs | **No usado**: el canal pidió contenido sin imágenes de IA y cada clip gasta muchos créditos |
| Clips de video reales (stock) | Pexels / Pixabay requieren API key; Wikimedia limita las descargas desde este entorno | **Pendiente**: sin acceso; se usaron fotos con movimiento de cámara |
| Música y efectos | Síntesis propia (`engine/shorts.py`) | Generados, sin licencias de terceros |
| Edición, gráficos, subtítulos | `engine/shorts.py` (Pillow + numpy + ffmpeg) | Generados |

## Identidad visual

- Paleta: negro profundo, gris oscuro, dorado metálico (degradado), blanco para textos; azul y rojo solo en gráficos cuando aplica.
- Etalonaje común: desaturación leve, contraste alto, sombras frías y altas luces cálidas, viñeta y grano fino.
- Tipografía: Inter Display Black para titulares (dorado metálico) e Inter Bold para apoyos.
- Movimiento: acercamientos y paneos suaves en cada foto, deriva de cámara sutil, fundidos de 0,22 s entre planos y un pequeño empuje de cámara en los golpes.
- Subtítulos: máximo 2 líneas, blancos con la palabra que se dice en dorado, a 1450 px de altura (zona segura de Shorts).
- Gancho: titular en blanco y dorado durante los primeros 3 segundos de cada video.
- Cierre: pregunta con botones de respuesta para motivar comentarios.

## Volver a generar un video

Requisitos: Python 3 con Pillow, numpy y scipy, y ffmpeg.

```bash
python3 engine/shorts.py VIDEO_01_RICOS
```

Esto escribe `video_final.mp4`, `subtitulos.srt` y `miniatura.png` dentro de la carpeta del video.
Para revisar cuadros sueltos sin renderizar todo:

```bash
python3 engine/shorts.py VIDEO_01_RICOS --frames 1.5 20 40
```

Cada `spec.py` define los planos (`S(frase, foto, modo)`) y los gráficos (`G(tipo, frase_inicio, frase_fin, ...)`), anclados a frases de la narración. Para cambiar una foto o un texto, edita el `spec.py` y vuelve a renderizar.

## Narración

`voz_original.mp3` es la toma de ElevenLabs. `narracion.mp3` es la versión usada: sin silencio inicial y, en V1 y V4, acelerada ×1,08 y ×1,04 con `atempo`, que no cambia el tono.

## Control de calidad

El resultado de cada punto está en `DOCUMENTACION/control_calidad.md`.
