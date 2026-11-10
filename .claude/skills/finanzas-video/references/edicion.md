# Edición orgánica: qué hace la plantilla y qué ajustas tú

La plantilla ya aplica las reglas base. Solo ajustas el `plan.json`.

## Lo que la plantilla hace sola
- Corta cada escena exactamente al final de la palabra (tiempos de ElevenLabs), con pausas controladas entre escenas.
- Zoom lento (Ken Burns) en clips e imágenes; los videos de stock entran en bucle si son cortos.
- Subtítulos palabra por palabra, de 1 a 3 palabras, con la palabra activa resaltada y un pequeño pop.
- Contadores y gráficas con easing (`easeOutCubic` / `spring`), nunca lineales.
- Música con *ducking* suave: baja bajo la voz, sube en las pausas y tiene fundidos de entrada y salida.
- Barra de progreso fina y zona segura respetada en 9:16.

## Palancas de ritmo (en el plan)
| Quieres… | Cambia… |
|---|---|
| Más tensión antes de una cifra | `"pausa": 0.5` en la escena anterior |
| Más ritmo | Divide escenas largas en dos; acorta frases |
| Un momento "wow" | `"entrada": "zoom"` + `"sfx": "sfx/hit.mp3"` en esa escena |
| Cambio de sección | `"entrada": "desliza"` o `"desenfoque"` |
| Menos música | `"volumen_musica": 0.12` |
| Voz más viva | `"voz_ajustes": {"style": 0.35, "stability": 0.35}` y vuelve a generar |
| Voz más rápida | `"speed": 1.08` (máx. 1.15 para que siga sonando natural) |

## Señales de edición robótica (y cómo corregirlas)
- **Todas las escenas duran lo mismo** → mezcla frases de 3 y de 12 palabras.
- **Mismo tipo visual repetido** → alterna `media` con gráficos o `texto`.
- **Transición en cada corte** → vuelve a `corte`; las transiciones solo marcan secciones.
- **Música plana todo el video** → cambia de pista o súbela en el cierre (escena final sin narración larga).
- **Clips de stock genéricos** ("business man smiling") → `query` más concreta y con acción: "hand counting colombian pesos", "credit card swipe close up", "empty wallet on table".
