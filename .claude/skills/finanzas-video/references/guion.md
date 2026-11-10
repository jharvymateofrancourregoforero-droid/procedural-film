# Guion: llamativo, curioso y natural

## Formatos
| | 9:16 Short | 16:9 Largo |
|---|---|---|
| Duración | 35–60 s (máx. 90) | 6–10 min |
| Palabras | 90–150 (≈ 2,5 palabras/s) | 900–1.500 |
| Escenas | 12–22, de 1,5 a 4 s | 60–120, de 3 a 8 s |
| Estructura | Gancho → Problema → Explicación → Dato clave → Cierre | Gancho → Promesa → 3–5 bloques con re-gancho cada 60–90 s → Resumen → CTA |

Un mismo plan puede renderizarse en ambos formatos, pero un largo **no** es un short estirado: escribe un plan propio para cada uno.

## El gancho (primeros 2 s; 5–10 palabras)
Elige UNO y varía entre videos:
1. **Cifra en contexto:** "Pagaste tres veces este celular sin saberlo."
2. **Contraintuitivo:** "Ahorrar en tu cuenta de ahorros te hace más pobre."
3. **Pregunta con tensión:** "¿Por qué el dólar sube cuando nadie compra dólares?"
4. **Consecuencia directa:** "Si tienes tarjeta de crédito, esto te cuesta plata cada mes."
5. **Historia en una línea:** "En 1999, un CDT pagaba 30 %. Hoy no llega a 10."
6. **Error común:** "El error que comete casi todo el que recibe la prima."

Prohibido: "Hola, bienvenidos", "En este video te voy a…", promesas de riqueza.

## Técnicas de retención
- **Bucle abierto:** plantea una pregunta al inicio y respóndela en el dato clave.
- **Concreto > abstracto:** "$1.200.000 al mes" mejor que "mucho dinero".
- **Segunda persona:** "tú", "tu plata", "tu bolsillo".
- **Analogías cotidianas:** arepa, bus, mercado, Nequi.
- **Contraste:** antes/después, Colombia vs. otro país, lo que crees vs. lo que pasa.
- **Re-gancho (largos):** "Pero eso no es lo más raro…", "Y aquí viene lo que nadie dice…".
- **Cierre con valor:** una acción concreta + CTA corto. Nunca un "suscríbete" vacío.

## Escritura para voz (ElevenLabs)
- Frases cortas (máx. 15 palabras). Una idea por escena.
- **Escribe las cifras como se pronuncian** en `texto`: "doce coma cinco por ciento", "un millón doscientos mil pesos". En pantalla la escena muestra los dígitos.
- Siglas difíciles en su forma hablada: "te erre eme" solo si la voz falla con "TRM"; prueba primero con `--borrador`.
- Usa puntuación para el ritmo: coma = pausa breve, punto = pausa, "…" = suspenso. Las preguntas reciben una pausa mayor de forma automática.
- Evita los paréntesis, las comillas y los emojis en `texto`.

## Elegir el tipo visual de cada escena
| La narración dice… | `tipo` |
|---|---|
| Contexto, situación, emoción | `media` (clip de stock) |
| Una cifra protagonista | `cifra` |
| Cambio en el tiempo | `linea` |
| Comparar 2–5 valores | `barras` |
| A vs. B | `comparar` |
| Una frase clave o una revelación | `texto` |

Reglas de variedad:
- `media` ≈ 40–55 % de las escenas. Nunca 3 escenas seguidas del mismo `tipo`.
- Máximo 3 escenas con gráfica (`linea` o `barras`) en un short.
- La escena del **dato clave** usa `cifra` o `texto` con `"entrada": "zoom"` (el punch-in). Máximo 2 por video.
- Primera escena: `cifra`, `texto` o un `media` muy llamativo. Debe entenderse sin sonido.
