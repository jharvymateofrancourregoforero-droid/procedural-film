# Búsqueda de tendencias (finanzas)

Objetivo: 5 ideas con potencial real de clics, en máximo 6 búsquedas.

## 1. Noticias y conversación (WebSearch, 3–4 consultas)
Usa consultas cortas y con fecha actual. Rota entre estas familias:
- **Colombia:** "dólar hoy Colombia", "Banco de la República tasas", "inflación Colombia <mes>", "salario mínimo <año>", "DIAN <tema>", "Nequi / Bancolombia novedades".
- **LatAm / global:** "Fed tasas <mes>", "bitcoin hoy", "bolsa Wall Street hoy", "oro precio récord", "recesión <año>".
- **Finanzas personales (evergreen):** "errores con tarjeta de crédito", "CDT vs fondo de inversión", "interés compuesto ejemplo".

Fuentes preferidas: Banco de la República, DANE, Superfinanciera, Portafolio, La República, Valora Analitik, Bloomberg Línea, Reuters. Evita foros y SEO basura.

## 2. Outliers de YouTube (script, 1–2 llamadas)
```
python herramientas/tendencias.py "finanzas personales" "dólar Colombia" --dias 14 --region CO
```
Imprime los videos recientes con más vistas por día y la razón **vistas/suscriptores**. Una razón mayor a 3 indica un tema que funciona más allá del tamaño del canal: copia el **ángulo**, nunca el contenido.
Cuota gratuita: unas 90 búsquedas al día. Usa 1 o 2 consultas por sesión.

## 3. Puntuación (mental, no la escribas completa)
Puntúa cada candidato de 1 a 3 en:
- **Curiosidad:** ¿contradice algo que la gente cree? ¿Tiene un "¿por qué?" natural?
- **Relevancia:** ¿afecta el bolsillo del espectador esta semana?
- **Visual:** ¿tiene datos graficables (serie, comparación, cifra impactante)?
- **Vida útil:** noticia (dura días) vs evergreen (dura meses). Mezcla ambas en las 5 ideas.

## 4. Entrega
Una sola tabla con 5 filas:

| # | Título provisional | Ángulo curioso | Por qué ahora | Dato clave | Formato |
|---|---|---|---|---|---|

Después guarda la tabla y las fuentes (solo URL y título) en `tendencias/AAAA-MM-DD.md`, para no repetir la búsqueda en la misma semana.

## Ángulos que suelen funcionar
- Contraintuitivo: "Ahorrar en CDT te está haciendo perder plata (si…)".
- Cifra absurda en contexto: "Esto es lo que cuesta un café si lo pagas con tarjeta a 36 cuotas".
- Comparación: "Colombia vs México: quién paga más impuestos".
- Historia corta: "El día que el dólar llegó a…".
- Error común: "3 cosas que nunca debes hacer con tu prima".
- Explicación de noticia: "Qué significa para tu bolsillo que el Banco de la República…".
