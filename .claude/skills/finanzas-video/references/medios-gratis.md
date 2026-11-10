# Medios gratis y sus licencias

## Con script (automático)
| Fuente | Qué | Clave | Licencia |
|---|---|---|---|
| **Pexels** | Videos y fotos | `PEXELS_API_KEY` (gratis en pexels.com/api; variable del entorno) | Uso gratis, comercial incluido; atribución recomendada |
| **Pixabay** | Videos y fotos | `PIXABAY_API_KEY` (gratis en pixabay.com/api/docs) | Uso gratis, comercial incluido; no revender el archivo tal cual |

`medios.py` prueba Pexels videos → Pixabay videos → Pexels fotos, y anota los créditos en `creditos.txt`. Pega esos créditos en la descripción del video.

## Manual (el usuario descarga una vez y reutiliza)
| Fuente | Uso | Nota |
|---|---|---|
| **Biblioteca de audio de YouTube** | Música | Algunas pistas piden atribución: revísalo por pista |
| **Pixabay Music / SFX** | Música y efectos | Sin atribución obligatoria |
| **Mixkit** | Música, efectos, clips | Licencia gratuita propia |
| **Freesound** | Efectos | Filtra por CC0 para evitar atribución |
| **Wikimedia Commons** | Fotos históricas (billetes antiguos, edificios, mapas) | La licencia varía por archivo; atribuye según indique |
| **NASA / dominio público** | Espacio, tierra | Generalmente dominio público |

Pon los archivos manuales en `public/<slug>/mis/` y referencia la ruta en `src` (o en `public/musica/` y `public/sfx/` si se reutilizan).

## Datos gratis
- Banco de la República (tasas, TRM, series), DANE (IPC, desempleo), datos.gov.co (TRM vía API, que usa `datos.py trm`), Superfinanciera (tasas de CDT y crédito).
- Global: FRED, Banco Mundial, CoinGecko (cripto, vía `datos.py cripto`), Yahoo Finance (acciones, vía `datos.py accion`; requiere `pip install yfinance`).

## Qué NO usar
- Clips de noticieros, películas o series, logos de bancos o marcas como protagonista, fotos de personas públicas o capturas de otros youtubers.
- Música comercial, aunque sean pocos segundos.

## Consultas que funcionan mejor (en inglés)
Concretas, con objeto + acción + encuadre: `"hand counting banknotes close up"`, `"stock market screen red numbers"`, `"woman paying with phone in store"`, `"piggy bank coins slow motion"`, `"city skyline night aerial"`, `"supermarket receipt long"`.
Evita: `"money"`, `"finance"`, `"business"` (demasiado genéricas y repetidas).
