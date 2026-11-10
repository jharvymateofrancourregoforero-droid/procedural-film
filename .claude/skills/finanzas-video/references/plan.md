# Formato de `proyectos/<slug>/plan.json`

El plan es a la vez el guion, el desglose de escenas y las props de Remotion. Las rutas son relativas a `public/`.
Los campos marcados con (auto) los rellenan los scripts: **no los escribas**.

```json
{
  "slug": "cdt-vs-inflacion",
  "titulo": "Tu CDT está perdiendo contra la inflación",
  "formato": "vertical",
  "voz_id": "",
  "voz_ajustes": { "stability": 0.45, "similarity_boost": 0.8, "style": 0.2, "speed": 1.0 },
  "musica": "musica/curiosidad.mp3",
  "volumen_musica": 0.18,
  "aviso": true,
  "resaltar_verde": ["gana", "sube", "ahorras"],
  "resaltar_rojo": ["pierdes", "cae", "deuda"],
  "escenas": [
    {
      "texto": "Tu CDT te paga intereses… pero igual pierdes plata.",
      "tipo": "texto",
      "titulo": "Tu CDT te paga… pero *pierdes* plata",
      "entrada": "corte"
    },
    {
      "texto": "Mira esto.",
      "tipo": "media",
      "query": "worried man looking at bank statement",
      "pausa": 0.15
    },
    {
      "texto": "Un CDT a un año paga hoy cerca del nueve por ciento.",
      "tipo": "cifra",
      "valor": 9.1, "decimales": 1, "sufijo": " %",
      "titulo": "Tasa CDT a 1 año", "tono": "acento",
      "fuente": "Superfinanciera, nov. 2026",
      "sfx": "sfx/pop.mp3"
    },
    {
      "texto": "Y la inflación de los últimos doce meses va así.",
      "tipo": "linea",
      "titulo": "Inflación anual (%)",
      "datos": [{"etiqueta": "Ene", "valor": 5.2}, {"etiqueta": "Oct", "valor": 4.6}],
      "decimales": 1, "sufijo": " %",
      "fuente": "DANE"
    },
    {
      "texto": "Si te quedas con el uno por ciento de diferencia, ¿de verdad ganas?",
      "tipo": "comparar",
      "a": { "etiqueta": "CDT", "valor": "9,1 %" },
      "b": { "etiqueta": "Inflación", "valor": "4,6 %" },
      "entrada": "desliza"
    }
  ]
}
```
`voz.py` añade después `voz`, `palabras`, `duracion` e `inicio`/`fin` en cada escena; `medios.py` añade `src` y `fondo`.

## Campos de escena
| Campo | Tipos | Descripción |
|---|---|---|
| `texto` | todos | Narración. **Obligatorio.** Cifras escritas como se pronuncian. |
| `tipo` | — | `media`, `cifra`, `barras`, `linea`, `texto`, `comparar` |
| `query` | media (y `fondo`) | Búsqueda en inglés, 3–6 palabras, concreta y visual. |
| `src` | media | (auto) Lo rellena `medios.py`. También puedes poner un archivo propio: `"<slug>/mis/clip.mp4"`. |
| `fondo_query` | cifra, barras, linea, texto, comparar | Opcional: clip oscurecido detrás del gráfico. (auto) → `fondo`. |
| `titulo` | todos | Texto en pantalla. En `texto`, las palabras entre `*asteriscos*` van en dorado. |
| `subtitulo` | cifra, texto | Línea secundaria pequeña. |
| `valor`, `prefijo`, `sufijo`, `decimales` | cifra | El contador animado. Ej.: `"prefijo": "$", "valor": 1.2, "sufijo": " M"`. |
| `tono` | cifra, linea, barras | `acento` (dorado), `positivo`, `negativo`, `neutro`. |
| `datos` | barras, linea | `[{"etiqueta": "...", "valor": n}]`. Barras ≤ 5, línea ≤ 24 puntos. |
| `destacar` | barras | Índice de la barra destacada (base 0). |
| `a`, `b` | comparar | `{"etiqueta": "...", "valor": "texto ya formateado"}` |
| `fuente` | todos | Se muestra en pequeño. Obligatoria si hay cifras. |
| `entrada` | todos | `corte` (por defecto), `zoom` (punch-in), `desliza`, `desenfoque`. Máx. 4 no-corte por video, sin repetir seguidas. |
| `sfx` | todos | Efecto al inicio de la escena, ej. `"sfx/pop.mp3"`. Máx. uno cada 3 s. |
| `pausa` | todos | Silencio tras la escena en s (por defecto 0,22; 0,4 tras una pregunta). Úsala para pausas dramáticas antes de una cifra. |
| `inicio`, `fin` | todos | (auto) Tiempos en s escritos por `voz.py`. |

## Campos globales
- `formato`: orientación con la que se buscan los medios (`vertical` u `horizontal`). El render puede hacer ambos.
- `voz_id`: si está vacío se usa `ELEVENLABS_VOICE_ID` del `.env`.
- `musica`: una pista de `public/musica/`. Elige según el tono del video y no repitas la misma en videos consecutivos.
- `aviso`: muestra "Contenido educativo. No es asesoría financiera." al final.
- `resaltar_verde` / `resaltar_rojo`: palabras que se colorean en los subtítulos (las cifras habladas van en dorado automáticamente).
