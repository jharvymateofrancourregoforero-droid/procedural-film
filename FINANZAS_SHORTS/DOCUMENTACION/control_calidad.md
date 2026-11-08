# Control de calidad

| Video | Duración | Resolución | Tamaño | Planos | Subtítulos |
|---|---|---|---|---|---|
| VIDEO_01_RICOS | 56.7 s | 1080x1920 | 66 MB | 22 | 36 |
| VIDEO_02_INFLACION | 49.1 s | 1080x1920 | 57 MB | 17 | 28 |
| VIDEO_03_INTERES_COMPUESTO | 56.9 s | 1080x1920 | 66 MB | 13 | 31 |
| VIDEO_04_CONSUMO | 56.4 s | 1080x1920 | 66 MB | 15 | 35 |
| VIDEO_05_PRIMER_MILLON | 59.3 s | 1080x1920 | 69 MB | 18 | 37 |

| Comprobación | Resultado |
|---|---|
| Narración completa | Sí. La transcripción de cada audio coincide palabra por palabra con el guion. |
| Errores de pronunciación | Las cifras se dieron a la voz en palabras y "CDT" como "cedetés". No pude escuchar los audios: revisar de oído antes de publicar. |
| Subtítulos sincronizados | Sí. Salen de los tiempos por palabra de ElevenLabs Scribe; cada bloque tiene como máximo 2 líneas. |
| Cifras correctas | 200.000 × 1,10 = 220.000. Poder de compra 1 / 1,10 ≈ 91 %. 100 × 1,1 = 110; 110 × 1,1 = 121; 121 × 1,1 = 133,1; 100 × 1,1²⁴ = 984,97 (×9,85, "casi diez veces"). 1.000.000 / 12 = 83.333. |
| Sin estadísticas inventadas | Sí. Solo hay ejemplos hipotéticos, marcados como tales en pantalla. |
| Imágenes acordes a la narración | Sí. Cada plano está anclado a una frase; ninguna foto se repite dentro del mismo video. |
| Pantallas negras accidentales | Ninguna (`blackdetect`). El Video 5 abre a propósito con fondo negro y el contador "$0". |
| La música no tapa la voz | Voz ≈ -16,5 LUFS frente a la música ≈ -27 LUFS antes de bajar automáticamente bajo la voz. |
| Volumen final | -14,4 a -14,6 LUFS, el estándar de YouTube. |
| Resolución | 1080x1920, 30 fps, H.264 + AAC. |
| Reproducción | Los cinco archivos se decodifican completos con ffmpeg sin errores. |
| Cierre completo | Cada video termina con su pregunta y 1,6 s de margen después de la última palabra. |

## Dependencias pendientes

- **Clips de video reales:** no hay acceso a bancos de video. Pexels y Pixabay piden API key y Wikimedia limita las descargas desde este entorno. Con una API key de Pexels se pueden reemplazar algunas fotos por clips.
- **Video generado con IA:** está disponible en el conector de ElevenLabs, pero no se usó por la línea "sin IA" del canal y por su costo en créditos.
