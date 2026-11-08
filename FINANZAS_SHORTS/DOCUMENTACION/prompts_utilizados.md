# Prompts utilizados

Este proyecto no usó generación de imágenes ni de video con IA. Todas las imágenes son fotografías reales con licencia libre; la música y los efectos se sintetizaron con código.
Los únicos servicios de IA fueron ElevenLabs: texto a voz para la narración y Scribe para los tiempos de cada palabra.

## Narración (ElevenLabs)

| Parámetro | Valor |
|---|---|
| Modelo | `eleven_v4` |
| Voz | Damián - Deep, Rich and Resonant (`BPwS5yO6aXvwg8auqNwS`), masculina, español latino neutro |
| Tomas | 1 por video (para ahorrar créditos) |
| Créditos | 4.530 en total (V1 973, V2 776, V3 891, V4 912, V5 978), más 54 de una prueba previa |
| Ajuste posterior | V1 acelerado ×1,08 y V4 ×1,04 con `atempo` (sin cambiar el tono) para entrar en la duración pedida |
| Transcripción | `eleven_scribe_v1`, sin costo de créditos |

Para que la voz no leyera mal las cifras se escribieron en palabras ("doscientos mil pesos"); en los subtítulos se convierten a números. "CDT" se escribió "cedetés" para que se pronunciara como en Colombia.
Las etiquetas entre corchetes ([serious], [curious], [excited]) son indicaciones de interpretación de `eleven_v4`; no se pronuncian.

### VIDEO_01_RICOS

```
[serious] ¿Por qué algunas personas trabajan cuarenta años y siguen dependiendo de su salario, mientras otras consiguen que su dinero produzca más dinero? La diferencia está en algo que muchas personas nunca aprenden: los activos. Mientras algunos utilizan todo su dinero para consumir, otros destinan una parte a construir negocios, adquirir inversiones y desarrollar fuentes de ingresos. No significa que todos los ricos tengan la misma estrategia, pero existe un principio fundamental: construir patrimonio requiere algo más que recibir un salario. [curious] Y aquí viene lo interesante: no necesitas ser millonario para comenzar. Puedes empezar aprendiendo a administrar tus ingresos, desarrollando habilidades y construyendo pequeños activos progresivamente. Ahora responde con sinceridad: si mañana recibieras un millón de pesos adicionales, ¿lo gastarías... o intentarías convertirlo en una fuente de ingresos? Escribe "gastar" o "invertir" en los comentarios.
```

### VIDEO_02_INFLACION

```
[serious] Puedes tener un millón de pesos guardado... y aun así estar perdiendo dinero. ¿Cómo es posible? La respuesta es la inflación. Imagina que hoy puedes comprar un mercado con doscientos mil pesos. Pero los precios aumentan un diez por ciento. Ahora necesitas doscientos veinte mil pesos para comprar aproximadamente lo mismo. ¿Ves el problema? Tus billetes siguen siendo los mismos, pero su poder de compra disminuyó. Por eso, ahorrar es importante, pero también necesitas comprender cómo proteger el valor de tu dinero. Existen alternativas como los cedetés y los fondos de inversión, aunque cada una tiene condiciones y riesgos diferentes. [curious] Te tengo una pregunta: ¿crees que cien mil pesos hoy comprarán lo mismo dentro de diez años? Responde sí o no.
```

### VIDEO_03_INTERES_COMPUESTO

```
[curious] Imagina invertir cien dólares y conseguir que tu dinero crezca sin añadir un solo dólar más. No es magia: es interés compuesto. Imagina que consigues una rentabilidad hipotética del diez por ciento anual, y reinviertes todas tus ganancias. El primer año tienes ciento diez dólares. El segundo, ciento veintiuno. El tercero, ciento treinta y tres dólares, aproximadamente. ¿Notas algo? Cada año, los rendimientos también comienzan a producir nuevos rendimientos. [excited] Y aquí viene lo sorprendente: manteniendo ese mismo supuesto matemático durante aproximadamente veinticuatro años, tus cien dólares se convertirían en cerca de novecientos ochenta y cuatro dólares. ¡Casi diez veces más! [serious] Pero recuerda: es una simulación, no una rentabilidad garantizada. Ahora dime: ¿qué prefieres? ¿Recibir mil dólares hoy... o aprender a construir patrimonio a largo plazo?
```

### VIDEO_04_CONSUMO

```
[curious] ¿Alguna vez has comprado algo que realmente no necesitabas... y después te preguntaste por qué lo hiciste? Las ofertas, los descuentos y las compras a cuotas pueden influir en nuestras decisiones. Cuando ves un producto que cuesta un millón de pesos, puedes pensarlo dos veces. Pero si te dicen que puedes pagarlo en pequeñas cuotas, posiblemente te parezca mucho más accesible. [serious] El problema es que dividir el precio no significa que el producto sea más barato. Aquí tienes una estrategia sencilla: antes de comprar algo que no necesitas inmediatamente, espera veinticuatro horas. Después pregúntate: ¿realmente lo necesito? ¿Puedo pagarlo? ¿Qué otra cosa podría hacer con ese dinero? A veces, la mejor compra es la que decides no hacer. Ahora sé sincero: ¿eres de los que compran inmediatamente, o de los que comparan y esperan? Escribe "impulsivo" o "estratégico" en los comentarios.
```

### VIDEO_05_PRIMER_MILLON

```
[serious] Imagina que mañana despiertas con cero pesos en tu cuenta. Sin ahorros, sin inversiones y sin propiedades. ¿Qué harías para conseguir tu primer millón? Primero, buscaría una manera de generar ingresos. Aprendería una habilidad que tenga demanda, buscaría oportunidades laborales, o desarrollaría un servicio que pueda ofrecer a otras personas. Porque antes de pensar en multiplicar el dinero, necesitas aprender a producirlo. Segundo, controlaría mis gastos. Tercero, separaría una parte de mis ingresos para construir un fondo de emergencia. Y cuarto, estudiaría alternativas de inversión antes de arriesgar mi dinero. Porque conseguir dinero es importante, pero aprender a administrarlo es lo que puede ayudarte a construir un futuro financiero más sólido. No necesitas comenzar siendo rico. Necesitas comenzar con una estrategia. [curious] Ahora te toca a ti: si tuvieras que comenzar desde cero, ¿cuál sería tu primera decisión? Te leo en los comentarios.
```

## Imágenes (Openverse)

Búsquedas en la API de Openverse (`api.openverse.org/v1/images/`) con `license_type=commercial`, fuentes StockSnap y Wikimedia Commons, y `aspect_ratio=tall` para tener fotos verticales que llenen el formato 9:16.
Términos usados: businessman, city skyline, skyscraper, office, laptop, money, coins, gold, shopping, mall, store, credit card, phone, clock, watch, piggy bank, wallet, studying, books, working, man thinking, woman thinking, night city, sunrise, chess, stairs, mountain, road, coffee, notebook, house, apartment, plant, window, city street.
Las fotos se descargaron con el proxy de miniaturas de Openverse (`/thumb/?full_size=true`), porque el CDN de StockSnap empezó a responder 403.
Licencias y autores de cada foto: `assets/photos/credits.json`.

## Música y efectos

No hay prompts. `engine/shorts.py` los sintetiza con numpy: pads cinematográficos, piano en ostinato, pulso grave y tic de reloj a 84 bpm, con un tono distinto por video; whooshes, tics de contador, campanas y golpes graves para los efectos.