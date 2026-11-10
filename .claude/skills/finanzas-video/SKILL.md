---
name: finanzas-video
description: Produce videos de finanzas para YouTube en 9:16 (Shorts) y 16:9 (videos largos) — busca temas en tendencia en la web, escribe guiones con gancho, genera la voz con ElevenLabs, descarga medios gratis (Pexels/Pixabay) y renderiza con Remotion con edición orgánica. Úsala cuando el usuario pida ideas, guiones o videos de finanzas, economía, inversión o dinero.
---

# Videos de finanzas (9:16 y 16:9)

Pipeline: **tendencias → idea → plan.json → voz → medios → previa → render → commit**.
Los scripts hacen el trabajo pesado; tú solo decides y escribes el `plan.json`.
Todo se ejecuta desde la raíz del repositorio.

## Reglas de ahorro de tokens (obligatorias)

1. **Carga las referencias solo en el paso que las necesita** (indicado abajo). No las leas todas al inicio.
2. **Nunca leas** `palabras.json`, audios, videos, `node_modules/`, `public/` ni el código de `herramientas/`. Los scripts imprimen resúmenes cortos: confía en ellos.
3. **Un solo archivo de trabajo por video:** `proyectos/<slug>/plan.json`. Lo escribes una vez; los cambios posteriores se hacen con `Edit` puntual, nunca reescribiendo el archivo.
4. **No modifiques la plantilla** (`src/`) salvo que el usuario lo pida explícitamente.
5. **Previa:** puedes abrir UNA vez la hoja `entregas/<slug>-previa-*.jpg` para detectar errores visuales evidentes. No abras fotogramas sueltos.
6. **Investigación con tope:** máximo 6 búsquedas web por sesión de ideas. Guarda el resumen en `tendencias/AAAA-MM-DD.md` y reutilízalo durante la semana.
7. **Respuestas cortas:** al terminar cada paso, 1–3 líneas. Nada de explicar código.
8. **Cifras = scripts o fuentes, nunca de memoria.** Usa `herramientas/datos.py` o una fuente web citada.

## Entorno en la nube (Claude Code web)

- Cada sesión empieza con un clon limpio. El hook de inicio instala `node_modules` solo. Si `npx remotion` falla por falta de dependencias, ejecuta `npm install`.
- `exportar.py` regenera solo lo que no va en git (`voz.wav` desde la caché de voz y los medios desde sus URL guardadas), **sin volver a cobrar ElevenLabs**.
- Las claves llegan como variables del entorno. Si un script dice que falta una clave o no hay conexión, dile al usuario exactamente qué variable o dominio agregar (ver `references/nube.md`) y detente.
- **Al terminar cada video:** haz commit y push de `proyectos/<slug>/`, `public/<slug>/` (lo no ignorado) y `entregas/`. El usuario descarga el MP4 desde GitHub.

## Flujo por video

### 1. Tendencias e ideas  → lee `references/tendencias.md`
- Si existe un archivo en `tendencias/` de los últimos 7 días, úsalo y no busques de nuevo.
- Si no: WebSearch (máx. 4–6 consultas) + `python herramientas/tendencias.py "consulta 1" "consulta 2"` (solo si hay `YOUTUBE_API_KEY`).
- Entrega **5 ideas** en una tabla: título provisional, ángulo curioso, por qué es tendencia, dato clave, formato sugerido (9:16 / 16:9 / ambos).
- Espera a que el usuario elija.

### 2. Datos  → solo si el guion lleva cifras
```
python herramientas/datos.py trm --serie 12
python herramientas/datos.py cripto bitcoin ethereum
python herramientas/datos.py accion AAPL --serie 12
```
`--serie N` imprime el arreglo `datos` listo para pegar en una escena `linea` o `barras`. Si el script no tiene red, usa WebSearch en la fuente oficial.
Para otras cifras (inflación, tasas, salario mínimo…) usa WebSearch en la fuente oficial y anota `fuente` en la escena.

### 3. Guion + plan  → lee `references/guion.md` y `references/plan.md`
Escribe `proyectos/<slug>/plan.json` directamente (guion y visuales en un solo paso, dividido en escenas). Muéstrale al usuario **solo la narración** numerada por escena, para aprobación.

### 4. Voz (ElevenLabs)
```
python herramientas/voz.py proyectos/<slug>/plan.json              # final
python herramientas/voz.py proyectos/<slug>/plan.json --borrador   # modelo flash, ~mitad de créditos
python herramientas/voz.py proyectos/<slug>/plan.json --solo 4     # regenera solo la escena 4
```
Genera por escena con caché: si cambias el texto de una escena, solo esa se regenera y se cobra. El script escribe tiempos (`inicio`, `fin`) y subtítulos palabra por palabra.

### 5. Medios gratis  → lee `references/medios-gratis.md` solo si algo falla o necesitas otra fuente
```
python herramientas/medios.py proyectos/<slug>/plan.json
```
Busca en Pexels y Pixabay según la `query` de cada escena (en inglés), elige un clip lo bastante largo y de la orientación correcta, y anota los créditos en `public/<slug>/creditos.txt`. Si una escena queda sin medio, cambia su `query` con `Edit` y vuelve a ejecutar (solo procesa escenas sin `src`).

### 6. Previa y render  → lee `references/edicion.md` solo si el usuario pide ajustes de ritmo o estilo
```
python herramientas/exportar.py proyectos/<slug>/plan.json --previa
python herramientas/exportar.py proyectos/<slug>/plan.json --formato vertical
python herramientas/exportar.py proyectos/<slug>/plan.json --formato ambos
```
La previa crea una hoja con 4 fotogramas clave en `entregas/`. Haz commit y push para que el usuario la vea, y renderiza solo cuando la apruebe. El render normaliza el audio a −14 LUFS y deja `entregas/<slug>-9x16.mp4` y/o `entregas/<slug>-16x9.mp4`.

### 7. Publicación
Escribe `proyectos/<slug>/publicacion.md` con: 3 títulos (curiosidad / cifra / pregunta), descripción de 2–3 líneas, 3–5 hashtags, los créditos de `creditos.txt` y, si aplica, la línea *"Contenido educativo. No es asesoría financiera."* Luego commit y push.

## Reglas de contenido

- **Original siempre:** cada video lleva análisis, ejemplo o ángulo propio. YouTube desmonetiza el contenido masivo y repetitivo ("contenido no auténtico"). Varía los ganchos, la música y la estructura entre videos.
- **Exactitud:** nada de cifras inventadas; toda cifra en pantalla lleva `fuente`. Si falta un dato, pregunta.
- **Responsabilidad:** sin promesas de ganancia ("seguro", "garantizado", "sin riesgo"). En inversión, cripto o productos financieros, pon `"aviso": true`.
- **Voz sintética:** recuerda al usuario marcar en YouTube la casilla de contenido alterado o sintético cuando aplique.
- Idioma de narración: español latinoamericano. Moneda por defecto: COP, y USD cuando aplique.
- **Música:** solo pistas libres que el usuario haya puesto en `public/musica/`. Si la carpeta está vacía, omite `musica` y avísale.
