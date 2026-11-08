# El secreto de los ricos

Video de YouTube en 16:9 (1920x1080, 30 fps) de **12:15**: *Trabajas toda tu vida, pero ¿por qué nunca consigues ser rico?*
Es el Video 1 de la serie "El dinero, la riqueza y las decisiones que cambian tu futuro".
Usa fotos reales con licencia libre, la voz de ElevenLabs "Mauricio Viral", y música y efectos sintetizados con código.
No usa imágenes ni música generadas con IA.

- Miniaturas en el estilo "persona recortada sobre dinero" (3 variantes para la prueba A/B de YouTube): [`exports/miniatura_a.jpg`](exports/miniatura_a.jpg) "EL SECRETO / DE LOS RICOS", [`exports/miniatura_b.jpg`](exports/miniatura_b.jpg) "TRABAJAR MÁS / NO TE HACE RICO", [`exports/miniatura_c.jpg`](exports/miniatura_c.jpg) "ASÍ PIENSAN / LOS RICOS". `python3 tools/thumbnail.py` las regenera (necesita `opencv-python-headless`; el recorte usa GrabCut, sin IA).
- Miniatura anterior, más simple: [`exports/miniatura.jpg`](exports/miniatura.jpg)
- Títulos, descripción, capítulos, créditos y etiquetas listos para pegar: [`exports/descripcion_youtube.txt`](exports/descripcion_youtube.txt)
- El MP4 final (`exports/el-secreto-de-los-ricos-youtube.mp4`, unos 330 MiB a ~3,7 Mbps) no está en el repositorio porque supera el límite de 100 MB de GitHub; se regenera con los pasos de abajo. Para más calidad, sube `-maxrate` a 8M.

## Para publicar en YouTube

**Título:** Trabajas toda tu vida, pero ¿por qué nunca consigues ser rico?

**Texto de la miniatura:** TRABAJAR MÁS NO TE HARÁ RICO

**Descripción:**

```
Si trabajar duro te hiciera rico, las personas más ricas serían las que más horas trabajan. En este video vemos la diferencia entre ganar dinero y construir riqueza, con números en pesos colombianos y un plan de 30 días para empezar.

Capítulos
0:00 Introducción
0:41 Andrés y Camila
2:26 La trampa de vender tu tiempo
3:24 Las 3 palancas de la riqueza
5:03 Ingresos vs. patrimonio
5:59 El poder de los activos
7:14 Las trampas del dinero fácil
8:34 Cuatro decisiones
9:40 Tu plan de 30 días
11:12 Para terminar

Este video es educativo y no es asesoría financiera. Los ejemplos de inversión son hipotéticos: no incluyen inflación, impuestos ni comisiones, y ningún rendimiento está garantizado. Antes de invertir, verifica que la entidad esté vigilada por la Superintendencia Financiera de Colombia.

Fotos: StockSnap (CC0) y Wikimedia Commons.
- "Bogota Traffic Jam" de Tokota (CC BY 3.0, Wikimedia Commons)
- "Skyline downtown Bogota" de Tijs Zwinkels (CC BY-SA 2.0, Wikimedia Commons)
- "Bogota - Streets at night 009" de momentcaptured1 (CC BY 2.0, Wikimedia Commons)
- "Bogota - Streets at night 003" de momentcaptured1 (CC BY 2.0, Wikimedia Commons)
- "Av Américas Transmilenio Mundo Aventura.JPG" de Felipe Restrepo Acosta (CC BY-SA 3.0, Wikimedia Commons)
- "Sao Paulo Stock Exchange" de Rafael Matsunaga (CC BY 2.0, Wikimedia Commons)
- "Tienda de barrio" de Futuropopular (CC BY-SA 4.0, Wikimedia Commons)
- "Cafe Cacao 11162TM.jpg" de FirkinCat (CC BY-SA 3.0, Wikimedia Commons)
Voz: ElevenLabs.
```

La pantalla final (últimos 20 s) deja libres un recuadro a la izquierda para el próximo video y un círculo a la derecha para el botón de suscripción, para colocar ahí los elementos de pantalla final de YouTube.

## Qué cambió frente al guion original

1. **Gancho:** abre con una paradoja ("si trabajar duro te hiciera rico, los obreros serían millonarios") y promete 4 decisiones al final ("la tercera es la que más gente ignora").
2. **Personajes con nombre:** Andrés vende su tiempo; Camila construye activos. Vuelven en cada capítulo.
3. **Cifras concretas en pesos:** el presupuesto de Andrés (2.000.000 que terminan en −50.000), el valor de su hora (≈ $9.615), el curso de la profesora (100 × $80.000) y el interés compuesto (200.000 al mes durante 20 años ≈ $143,7 millones, con la nota de que es hipotético).
4. **Capítulos nuevos:** el mes de Andrés y la carrera de la rata, las 3 palancas (apalancamiento), las trampas del dinero fácil (DMG y DRFE en 2008, cuatro señales de alerta, gota a gota) y un plan de 30 días con la regla 50/30/20.
5. **Frases más cortas** para una voz enérgica, sin relleno ("fundamental", "considerablemente").
6. **Cierre** con pregunta para comentarios, suscripción y adelanto del Video 2 (la trampa de las tarjetas).

## Duración y bloques pendientes

El objetivo era más de 15 minutos. La cuenta de ElevenLabs llegó a su límite de 40.000 créditos y 4 bloques no se grabaron, así que el video quedó en 12:15.
Con estos 4 bloques (unos 4.800 créditos con una sola toma) pasaría de 16 minutos. Su texto está al final de este archivo.
Para añadirlos: guarda el MP3 en `audio/<nombre>.mp3`, sus tiempos por palabra en `audio/words_<nombre>.json`, agrega el bloque en `SEGMENTS` de `tools/timeline.py` y ancla sus planos en `_EDIT`. Las fotos para esos bloques ya están descargadas (postres, diseño, bola de nieve, barrio, carro usado).

## Cómo está hecho

| Parte | Detalle |
|---|---|
| Voz | ElevenLabs `eleven_v4`, voz "Mauricio Viral", 11 bloques en `audio/`. Tiempos por palabra con ElevenLabs Scribe en `audio/words_*.json`. |
| Fotos | 144 fotos reales de StockSnap (CC0) y Wikimedia Commons (CC BY / CC BY-SA), encontradas con Openverse; 127 aparecen en el video. Hay tomas de Bogotá (TransMilenio, trancón, centro, tienda de barrio). |
| Edición | `tools/render.py`: 202 planos anclados a frases de la narración, con fotos a pantalla completa, en tarjeta, a un lado con texto al otro o en pantalla dividida. Incluye tarjetas de capítulo, rótulos con nombre, tabla del presupuesto, contadores, gráfica de interés compuesto, regla 50/30/20, botón de suscripción animado, subtítulos palabra por palabra, barridos, flashes, grano y viñeta. |
| Música | Beat funk/hip-hop a 96 bpm sintetizado en `tools/audio.py`, con una progresión distinta por capítulo, más sobrio en los capítulos serios y con caída y golpe en cada tarjeta. |
| Efectos | Whoosh, pop, obturador, golpe grave, caja registradora, tic de contador y clic, también sintetizados. |
| Mezcla | La música baja sola cuando habla la voz y el total queda a -14 LUFS. |

## Volver a generar

Necesita Python 3 con Pillow, numpy y scipy, y ffmpeg en el PATH.

```bash
python3 tools/audio.py
```

```bash
python3 tools/render.py
```

```bash
ffmpeg -y -i build/video.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v libx264 -preset medium -crf 23 -maxrate 3700k -bufsize 7400k -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart exports/el-secreto-de-los-ricos-youtube.mp4
```

`python3 tools/timeline.py` imprime la duración, los capítulos y los planos demasiado largos o cortos.
`python3 tools/render.py --frames 12 95` guarda cuadros sueltos en `build/` para revisar sin renderizar todo.

## Guion grabado

### Gancho
> Si trabajar duro te hiciera rico... las personas más ricas del mundo serían las que más horas trabajan. Y no lo son.
>
> Piénsalo: un obrero que carga ladrillos doce horas al día trabaja más duro que casi cualquier millonario. Entonces... ¿qué está pasando?
>
> En este video te voy a mostrar la diferencia que casi nadie te explica entre ganar dinero y construir riqueza. Y al final te dejo cuatro decisiones que puedes empezar a tomar este mismo mes, ganes lo que ganes.
>
> Quédate, porque la tercera es la que más gente ignora.

### 1. Andrés y Camila
> Te presento a Andrés. Se levanta a las cinco de la mañana. Dos horas de bus. Diez horas de trabajo. Llega a la casa sin energía... y al día siguiente, lo mismo.
>
> Y te presento a Camila. Camila trabaja menos horas que Andrés. Pero tiene algo que él no tiene: dinero que sigue entrando aunque ella esté dormida.
>
> Los dos necesitan dinero para vivir. La diferencia no es cuánto se esfuerzan. La diferencia es cómo producen su dinero... y qué hacen con él cuando llega.

> Vamos a ponerle números a la vida de Andrés.
>
> Andrés gana dos millones de pesos al mes. Parece suficiente... hasta que llega el día de pago.
>
> Setecientos mil se van en arriendo. Seiscientos mil en mercado y comida. Ciento cincuenta mil en transporte. Doscientos mil en servicios y celular. Doscientos cincuenta mil en la cuota de la tarjeta. Y ciento cincuenta mil en salidas, domicilios y gastos hormiga.
>
> Total: dos millones cincuenta mil pesos.
>
> Andrés no está ahorrando. Está cincuenta mil pesos en rojo. Y esa diferencia la cubre... con la misma tarjeta que ya está pagando.
>
> Mes a mes, la deuda crece un poquito. Y Andrés trabaja más para tapar el hueco.
>
> Robert Kiyosaki, en su libro Padre rico, padre pobre, le puso un nombre a esto: la carrera de la rata. Corres todos los días, te cansas, pero no avanzas, porque todo lo que entra vuelve a salir.
>
> Y ojo: Andrés no es flojo ni irresponsable. Andrés simplemente nunca aprendió a hacer otra cosa con su dinero. Y eso es exactamente lo que vamos a cambiar en este video.

### 2. La trampa de vender tu tiempo
> Desde niños nos enseñaron una fórmula: estudia, consigue un buen empleo, trabaja duro y tendrás una vida estable.
>
> Y ojo: ese camino no está mal. Un empleo te da estabilidad, experiencia y un ingreso fijo. El problema es otro.
>
> Si tu único ingreso depende de tus horas, tu dinero tiene un techo. Y ese techo se llama... veinticuatro horas.
>
> Hagamos la cuenta. Si ganas dos millones de pesos al mes y trabajas unas cuarenta y ocho horas a la semana, tu hora vale casi diez mil pesos.
>
> ¿Quieres ganar el doble? Tienes tres opciones: trabajar el doble de horas, conseguir que te paguen el doble por hora, o crear dinero que no dependa de tu hora.
>
> La primera tiene un límite: tu cuerpo y tu día. La segunda se logra con habilidades. Y la tercera... es donde empieza la riqueza.

### 3. Las 3 palancas de la riqueza
> Pero, ¿cómo se crea dinero que no dependa de tu hora? La respuesta tiene un nombre: apalancamiento.
>
> Apalancarte es usar algo distinto a tu propio tiempo para multiplicar tus resultados. Y existen tres palancas principales.
>
> La primera: el trabajo de otras personas. Piensa en la dueña de una panadería de barrio. Si ella sola hace el pan, solo puede vender lo que alcanzan sus manos. Pero si contrata a tres personas y organiza bien el negocio, el negocio produce mucho más de lo que ella sola podría producir.
>
> La segunda: el capital. Es poner tu dinero a trabajar. Un ahorro bien invertido gana rendimientos mientras tú haces otra cosa.
>
> Y la tercera, la más poderosa de esta época: los productos que se pueden copiar. Un video, un libro, un curso, una aplicación. Los haces una vez... y se pueden vender o ver miles de veces.
>
> Mira este ejemplo. Una profesora de matemáticas cobra cincuenta mil pesos por clase particular. Si quiere ganar más, tiene que dar más clases. Pero si graba un curso y lo vende en ochenta mil pesos, cien estudiantes le pagarían ocho millones... por un trabajo que hizo una sola vez.
>
> Ahora, no te voy a mentir: grabar ese curso, mejorarlo y conseguir esos cien estudiantes cuesta mucho trabajo. El apalancamiento no es dinero fácil. Es trabajo que, una vez hecho, sigue produciendo.
>
> Esa es la gran diferencia entre Andrés y Camila. Andrés vende horas. Camila construye cosas que trabajan por ella.

### 4. Ingresos vs. patrimonio
> Ahora, una verdad incómoda: ganar mucho no es lo mismo que ser rico.
>
> Imagina a alguien que gana quince millones al mes. Carro nuevo, ropa de marca, viajes cada tres meses. Pero gasta todo lo que gana... y un poquito más con la tarjeta. Si mañana pierde ese empleo, ¿cuántos meses aguanta? Quizá ninguno.
>
> Ahora imagina a alguien que gana tres millones, pero vive con dos y medio, no tiene deudas caras y cada mes guarda una parte. ¿Quién crees que va a estar mejor en diez años?
>
> Para entenderlo, necesitas tres palabras.
>
> Ingresos: el dinero que entra.
>
> Gastos: el dinero que sale para sostener tu estilo de vida.
>
> Y patrimonio: lo que tienes, menos lo que debes.
>
> La riqueza no se mide por lo que entra. Se mide por lo que se queda... y por lo que crece.

### 5. El poder de los activos
> Entonces, ¿qué hace diferente a Camila? Que compra y construye activos.
>
> Un activo es algo que tiene valor y que puede ponerte dinero en el bolsillo, o valer más con el tiempo.
>
> Un negocio bien administrado que deja utilidades. Un apartamento que se arrienda. Una inversión que da rendimientos. Un libro, un curso o una canción que paga regalías.
>
> Y sí: también una habilidad. Aprender inglés, programación o ventas puede multiplicar lo que vale tu hora.
>
> Ahora, la parte que nadie te dice en los videos de riqueza rápida: todos los activos tienen riesgo. Un negocio puede quebrar, un apartamento se puede quedar sin arrendatario, una inversión puede bajar. Por eso la idea no es apostar. La idea es aprender, diversificar y empezar pequeño.
>
> Y lo más poderoso de un activo es el tiempo. Si inviertes doscientos mil pesos al mes durante veinte años, con un rendimiento hipotético del diez por ciento anual, habrías puesto cuarenta y ocho millones... pero podrías terminar con más de ciento cuarenta millones. No por trabajar más horas, sino por darle tiempo a tu dinero.

### 6. Las trampas del dinero fácil
> Y ya que hablamos de hacer crecer el dinero, tengo que advertirte sobre las trampas.
>
> Cada cierto tiempo aparece alguien que promete duplicar tu plata en pocos meses. Y la historia de Colombia tiene un ejemplo doloroso: en dos mil ocho, miles de personas perdieron sus ahorros en captadoras ilegales como DMG y DRFE. Prometían rendimientos enormes... hasta que el dinero dejó de llegar.
>
> Aprende estas cuatro señales de alerta.
>
> Uno: te garantizan ganancias muy altas y sin riesgo. En las inversiones reales, más rendimiento casi siempre significa más riesgo.
>
> Dos: te presionan para entrar ya, antes de que se acabe el cupo.
>
> Tres: ganas dinero por traer a más personas.
>
> Y cuatro: nadie te puede explicar, de forma clara, de dónde sale la ganancia.
>
> Antes de entregar tu dinero, verifica si la entidad está vigilada por la Superintendencia Financiera de Colombia.
>
> Y hay otra trampa igual de peligrosa: la deuda cara. Los préstamos gota a gota, los avances de tarjeta, las compras a muchas cuotas. Cada peso que pagas en intereses es un peso que deja de trabajar para ti... y empieza a trabajar para otro.

### 7. Cuatro decisiones
> Muy bien. ¿Cómo empiezas si hoy eres Andrés? Con cuatro decisiones.
>
> Uno: conoce tus números. Durante un mes, anota cada peso que entra y cada peso que sale. No puedes mejorar lo que no mides.
>
> Dos: invierte en tu habilidad más rentable. Es el activo que nadie te puede quitar, y el que más rápido sube el valor de tu hora.
>
> Tres, la que más gente ignora: cuando te suban el sueldo, no te subas la vida. Si te aumentan trescientos mil pesos, deja que al menos la mitad se vaya directo al ahorro. Así tu estilo de vida sube... pero tu patrimonio sube más rápido.
>
> Y cuatro: construye primero un fondo de emergencia de tres a seis meses de gastos. Después, estudia opciones de inversión que vayan con tus metas y con el riesgo que puedes aguantar. Y si tienes dudas, busca asesoría de un profesional autorizado.
>
> No se trata de renunciar mañana a tu empleo ni de buscar dinero fácil. Se trata de usar tu sueldo de hoy como la herramienta que construye tu libertad de mañana.

### 8. Tu plan de 30 días
> Y para que esto no se quede en teoría, te dejo un plan de treinta días. Un paso por semana.
>
> Semana uno: registra. Anota absolutamente todo lo que gastas, hasta el tinto de la esquina. Puede ser en una libreta o en una aplicación. Al final de la semana vas a ver, con tus propios ojos, a dónde se va tu plata.
>
> Semana dos: organiza. Arma tu presupuesto. Una referencia muy popular es la regla cincuenta, treinta, veinte: cincuenta por ciento para necesidades, treinta para gustos, y veinte para ahorro y pago de deudas. Si hoy no te alcanza para el veinte, empieza con el cinco. Lo importante no es el monto: es el hábito.
>
> Semana tres: recorta y ataca. Cancela lo que no usas, renegocia lo que puedas, y escoge tu deuda más cara para pagarla primero.
>
> Semana cuatro: automatiza. Abre una cuenta de ahorro separada, y programa que el día de pago una parte se vaya directo ahí. Págate primero a ti, antes que a nadie más.
>
> Y durante esos treinta días, dedica media hora diaria a aprender una habilidad que suba el valor de tu hora. Treinta minutos al día son más de ciento ochenta horas al año.
>
> Imagina que Andrés hace esto. No se vuelve millonario en un mes. Pero, por primera vez en años, termina el mes en verde. Y ese pequeño cambio, repetido durante años, es el que separa a los que trabajan por dinero... de los que ponen el dinero a trabajar para ellos.

### Para terminar
> Trabajar duro te hace avanzar. Pero trabajar duro sin estrategia te puede dejar en el mismo lugar durante años.
>
> El cambio empieza el día que dejas de preguntarte solo cuánto vas a ganar este mes... y empiezas a preguntarte qué estás construyendo con lo que ganas.
>
> Ahora dime tú en los comentarios: ¿qué es más importante para ser rico? ¿Ganar mucho... o saber administrarlo?
>
> Si este video te sirvió, suscríbete y activa la campanita, porque en el próximo vamos a hablar de la trampa de las tarjetas de crédito: el dinero que parece tuyo... pero no lo es.
>
> ¡Nos vemos!

## Bloques escritos, sin grabar

**El enemigo silencioso** (después de "Ingresos vs. patrimonio")

> Y aquí aparece un enemigo silencioso. Se llama la inflación del estilo de vida.
> Funciona así: te suben el sueldo, y sin darte cuenta cambias el celular, te pasas a un apartamento más caro, pides más domicilios. Seis meses después, ganas más... pero te sobra lo mismo que antes: nada.
> Hay una idea que lo resume muy bien: los gastos crecen hasta alcanzar los ingresos. No importa cuánto ganes; si no pones un límite, siempre vas a encontrar en qué gastarlo.
> Por eso hay gente con sueldos altos que vive con la misma angustia que alguien que gana el mínimo.
> En mil novecientos noventa y seis, dos investigadores, Thomas Stanley y William Danko, publicaron un libro llamado El millonario de al lado. Estudiaron a personas millonarias en Estados Unidos, y encontraron algo que sorprendió a muchos: buena parte de ellas vivía por debajo de sus posibilidades. Casas normales, carros usados, presupuesto ajustado.
> Es decir: muchos de los que parecen ricos no lo son. Y muchos de los que son ricos... no lo parecen.
> Ahora, un ejercicio para ti. Toma papel y lápiz. Suma lo que tienes: tus ahorros, lo que valdría tu moto o tu carro si los vendieras hoy, cualquier inversión. Y réstale todo lo que debes: tarjetas, créditos, préstamos. Ese número es tu patrimonio.
> Si te da negativo, tranquilo. Le pasa a muchísima gente. No es una sentencia: es tu punto de partida. Lo importante es que, de aquí a un año, ese número sea más grande que hoy.

**La magia del tiempo: Ana y Bruno** (después de "El poder de los activos")

> Déjame mostrarte por qué el tiempo vale más que la cantidad. Te presento a Ana y a Bruno.
> Ana empieza a invertir a los veinticinco años. Pone doscientos mil pesos al mes durante solo diez años, y a los treinta y cinco deja de aportar. No mete un peso más.
> Bruno empieza tarde, a los treinta y cinco. Pone los mismos doscientos mil pesos al mes, pero durante treinta años, hasta los sesenta y cinco.
> Ana aportó veinticuatro millones. Bruno aportó setenta y dos millones. El triple.
> ¿Quién tiene más a los sesenta y cinco? Con el mismo rendimiento hipotético del diez por ciento anual... Ana termina con casi setecientos millones. Bruno, con poco más de cuatrocientos millones.
> Ana puso la tercera parte del dinero... y terminó con más. ¿La diferencia? Diez años de ventaja.
> Eso es el interés compuesto: ganas rendimientos sobre tu dinero, y después ganas rendimientos sobre esos rendimientos. Es una bola de nieve.
> Hay un truco para entenderlo rápido: la regla del setenta y dos. Divide setenta y dos entre la tasa de rendimiento, y te da más o menos los años que tarda tu dinero en duplicarse. Al diez por ciento, se duplica cada siete años, aproximadamente.
> Pero el interés compuesto también funciona al revés. Se llama inflación. Si los precios suben un cinco por ciento al año, en diez años un millón de pesos guardado debajo del colchón compraría lo que hoy compran unos seiscientos catorce mil pesos.
> Por eso no basta con guardar. Hay que hacer que el dinero crezca, al menos, al ritmo de los precios.

Cifras: con 10 % anual compuesto mensualmente, Ana termina con ≈ $697,5 millones y Bruno con ≈ $412,6 millones; 1.000.000 / 1,05¹⁰ ≈ 613.913.

**Cómo empezó Camila** (después de "Las 3 palancas")

> Y para que no pienses que Camila nació con suerte, déjame contarte cómo empezó.
> Camila, igual que Andrés, arrancó con un sueldo normal. La diferencia es que, desde el primer mes, separó un diez por ciento antes de gastar cualquier cosa.
> Los fines de semana empezó a vender postres a sus compañeros de trabajo. No era un gran negocio, pero le enseñó a vender, a cobrar y a llevar cuentas.
> Con lo que ganó, pagó un curso de diseño. Con el tiempo, empezó a vender plantillas digitales por internet: las diseñaba una vez, y se vendían muchas veces.
> Cada peso extra que le entraba no se iba en un celular nuevo. Se iba a su fondo de emergencia, y después a inversiones sencillas y reguladas.
> ¿Le funcionó todo? No. Tuvo meses malos, productos que nadie compró y errores que le costaron plata.
> Pero después de varios años, Camila tiene algo que Andrés todavía no tiene: varias fuentes de ingreso. Si una falla, las otras la sostienen. Y eso, más que cualquier lujo, es libertad.

**Resumen en 60 segundos** (antes de "Para terminar")

> Hagamos un resumen rápido, por si te perdiste algo.
> Uno: trabajar más horas tiene un techo, y ese techo son las veinticuatro horas del día.
> Dos: la riqueza no es lo que ganas. Es tu patrimonio: lo que tienes, menos lo que debes.
> Tres: cuidado con la inflación del estilo de vida. Si cada aumento se va en gastos, nunca vas a avanzar.
> Cuatro: los activos y el apalancamiento te permiten ganar dinero sin vender más horas.
> Cinco: el tiempo es tu mejor aliado. Empezar diez años antes puede valer más que poner el triple de dinero.
> Y seis: desconfía del dinero fácil y de la deuda cara.
> Si te quedas solo con una idea, que sea esta: tu sueldo es una herramienta... no la meta.

## Fotos

| Archivo | Título | Autor | Licencia | Enlace |
|---|---|---|---|---|
| `airplane.jpg` | Airplane Travel | Eva Darron | CC0 | [fuente](https://stocksnap.io/photo/airplane-travel-TMYUIRV0BQ) |
| `alarm_blue.jpg` | Clock Time | Negative Space | CC0 | [fuente](https://stocksnap.io/photo/clock-time-72R81VRMM0) |
| `alarm_dark.jpg` | Clock Time | Ryan McGuire | CC0 | [fuente](https://stocksnap.io/photo/clock-time-AEE06BA0EA) |
| `alarm_pink.jpg` | Still Items | Mpho Mojapelo | CC0 | [fuente](https://stocksnap.io/photo/still-items-UZAO7L631Q) |
| `alarm_vintage.jpg` | Vintage Alarm | Aphiwat Chuangchoem | CC0 | [fuente](https://stocksnap.io/photo/vintage-alarm-1HDO9I6J22) |
| `alone_window.jpg` | Alone Hoodie | Chuttersnap | CC0 | [fuente](https://stocksnap.io/photo/alone-hoodie-XZCLXHGALF) |
| `andres.jpg` | Man Laptop | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/man-laptop-ZIDI38HLCF) |
| `andres2.jpg` | Man Working | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/man-working-MGSIIACGM6) |
| `apartment.jpg` | Apartment Building | Matt Bango | CC0 | [fuente](https://stocksnap.io/photo/apartment-building-2T9NFO4RNI) |
| `apartment2.jpg` | Apartment Building | Matt Bango | CC0 | [fuente](https://stocksnap.io/photo/apartment-building-VWKJCVGD8F) |
| `baker.jpg` | People Men | Clem Onojeghuo | CC0 | [fuente](https://stocksnap.io/photo/people-men-TADXW1KLGW) |
| `bakery.jpg` | Bread Pastry | Roman Kraft | CC0 | [fuente](https://stocksnap.io/photo/bread-pastry-73EV0ODLNO) |
| `bananas.jpg` | Bananas Fruits | Ryan McGuire | CC0 | [fuente](https://stocksnap.io/photo/bananas-fruits-D0C5D92CD9) |
| `bank_calc.jpg` | Bank Finance | Artsy Crafty | CC0 | [fuente](https://stocksnap.io/photo/bank-finance-OLL4BSGLBE) |
| `biz_coffee.jpg` | Business Man | Direct Media | CC0 | [fuente](https://stocksnap.io/photo/business-man-7BQNRHB6EX) |
| `biz_laugh.jpg` | Business Man | Direct Media | CC0 | [fuente](https://stocksnap.io/photo/business-man-HQLFQ0FSK0) |
| `biz_stress.jpg` | Business Man | Direct Media | CC0 | [fuente](https://stocksnap.io/photo/business-man-VISYYURYFA) |
| `biz_think.jpg` | Businessman Thinking | Burst | CC0 | [fuente](https://stocksnap.io/photo/businessman-thinking-TGG4JHNHB8) |
| `bolsa_sp.jpg` | Sao Paulo Stock Exchange | Rafael Matsunaga | CC BY 2.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=2282311) |
| `book_read.jpg` | Books Reading | Aaron Burden | CC0 | [fuente](https://stocksnap.io/photo/books-reading-CN63QSUO8C) |
| `box.jpg` | Cardboard Box | Matt Bango | CC0 | [fuente](https://stocksnap.io/photo/cardboard-box-USP4WCYPBW) |
| `brain.jpg` | Idea Brain | Bango Renders | CC0 | [fuente](https://stocksnap.io/photo/idea-brain-5NLKT00MVB) |
| `bread_basket.jpg` | Bread Pastry | Expect Best | CC0 | [fuente](https://stocksnap.io/photo/bread-pastry-FVC3WO0970) |
| `bread_shop.jpg` | Vintage Bakery | Daria Shevtsova | CC0 | [fuente](https://stocksnap.io/photo/vintage-bakery-ZAG3KUMDTW) |
| `bricks.jpg` | Bricks Wall | Jonas Nilsson Lee | CC0 | [fuente](https://stocksnap.io/photo/bricks-wall-4YCB0VAY1L) |
| `bricks_tools.jpg` | Construction Tools | The World is a Stage | CC0 | [fuente](https://stocksnap.io/photo/construction-tools-EJZBX7UMTV) |
| `bulb.jpg` | Lights Lightbulb | Krzysztof%20Puszczy%u0144ski | CC0 | [fuente](https://stocksnap.io/photo/lights-lightbulb-Z3VPU4IDKE) |
| `burn_money.jpg` | Money Hand | Jp Valery | CC0 | [fuente](https://stocksnap.io/photo/money-hand-QZTMMLUZOP) |
| `bus_people.jpg` | Diverse bus passengers (Unsplash) | Søren Astrup Jørgensen sorenastrup664 | CC0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=61847392) |
| `cafe_cacao.jpg` | File:Cafe Cacao 11162TM.jpg | FirkinCat | CC BY-SA 3.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=16790560) |
| `cake_slice.jpg` | Cake Dessert | Adrianna Calvo | CC0 | [fuente](https://stocksnap.io/photo/cake-dessert-NYBRCP91R9) |
| `calc_acc.jpg` | Accounting Finance | Wilfred Iven | CC0 | [fuente](https://stocksnap.io/photo/accounting-finance-JONMP7TPGK) |
| `calc_hand.jpg` | Calculator Calendar | Tevarak | CC0 | [fuente](https://stocksnap.io/photo/calculator-calendar-RFVHCUGML3) |
| `calendar_desk.jpg` | Calendar Display | Jeff Sheldon | CC0 | [fuente](https://stocksnap.io/photo/calendar-display-ZI905NZJY1) |
| `calendar_jan.jpg` | Date January | Brooke Lark | CC0 | [fuente](https://stocksnap.io/photo/date-january-UMIOY6CVUM) |
| `camila.jpg` | Woman Working | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/woman-working-HIOJW30YKD) |
| `camila2.jpg` | Woman Working | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/woman-working-GZLDAMHFU4) |
| `card_hand.jpg` | Creditcard Money | Michal Jarmoluk | CC0 | [fuente](https://stocksnap.io/photo/creditcard-money-71MH9ATF4S) |
| `card_hand2.jpg` | Creditcard Money | Michal Jarmoluk | CC0 | [fuente](https://stocksnap.io/photo/creditcard-money-09LJGFBK1X) |
| `card_shop.jpg` | Ecommerce Shopping | Negative Space | CC0 | [fuente](https://stocksnap.io/photo/ecommerce-shopping-RZWM4T2UAD) |
| `cash_fan.jpg` | Bills Money | Shopify | CC0 | [fuente](https://stocksnap.io/photo/bills-money-11HX337XXR) |
| `cash_hand.jpg` | Hand Holding | Jp Valery | CC0 | [fuente](https://stocksnap.io/photo/hand-holding-LPLPKWISYS) |
| `cash_hands.jpg` | Hand Holding | Jp Valery | CC0 | [fuente](https://stocksnap.io/photo/hand-holding-3Q9K0EFSPN) |
| `checklist.jpg` | Todo List | Freestocks.org | CC0 | [fuente](https://stocksnap.io/photo/todo-list-TVEUBLIOSK) |
| `chess_dark.jpg` | Piece Chess | George Becker | CC0 | [fuente](https://stocksnap.io/photo/piece-chess-9BIDKGNA0L) |
| `chess_fall.jpg` | Piece Chess | George Becker | CC0 | [fuente](https://stocksnap.io/photo/piece-chess-X41WJB6PXS) |
| `chess_game.jpg` | Chess Game | Lou Levit | CC0 | [fuente](https://stocksnap.io/photo/chess-game-308ED74931) |
| `chess_pawn.jpg` | Piece Chess | George Becker | CC0 | [fuente](https://stocksnap.io/photo/piece-chess-EIAVGJCHN1) |
| `city_sunset.jpg` | City Sunset | Candace McDaniel | CC0 | [fuente](https://stocksnap.io/photo/city-sunset-0VHJUGBJDP) |
| `clock_vintage.jpg` | Vintage Clock | Jiyeon Park | CC0 | [fuente](https://stocksnap.io/photo/vintage-clock-EIW9MO2ZFG) |
| `clock_wall.jpg` | Clock Time | Ales Krivec | CC0 | [fuente](https://stocksnap.io/photo/clock-time-C2799653AA) |
| `code.jpg` | Programming Code | One Idea LLC | CC0 | [fuente](https://stocksnap.io/photo/programming-code-1STVFMTBJY) |
| `code2.jpg` | Coding Business | Marc Chouinard | CC0 | [fuente](https://stocksnap.io/photo/coding-business-DZ1EFM9PIK) |
| `coins.jpg` | Coins Money | Karol Dach | CC0 | [fuente](https://stocksnap.io/photo/coins-money-VPSD8JT149) |
| `cranes.jpg` | Cranes Construction | Wyncliffe | CC0 | [fuente](https://stocksnap.io/photo/cranes-construction-KOKXBB635S) |
| `cupcake_pink.jpg` | Cupcake Dessert | Foodie Girl | CC0 | [fuente](https://stocksnap.io/photo/cupcake-dessert-KFXB4EEAOR) |
| `cupcakes.jpg` | Cupcakes Icing | Brian Chan | CC0 | [fuente](https://stocksnap.io/photo/cupcakes-icing-KDOALRLDV8) |
| `design_desk.jpg` | Office Work | Thomas Litangen | CC0 | [fuente](https://stocksnap.io/photo/office-work-3TJ6NCTIRT) |
| `dice.jpg` | Lucky Dice | Candace McDaniel | CC0 | [fuente](https://stocksnap.io/photo/lucky-dice-X8CPTKKQEX) |
| `family.jpg` | Family Home | Direct Media | CC0 | [fuente](https://stocksnap.io/photo/family-home-CBOFZY8SFU) |
| `frantic.jpg` | Frantic Eyes | QASIM SADIQ | CC0 | [fuente](https://stocksnap.io/photo/frantic-eyes-M558J8TZDJ) |
| `freedom.jpg` | Freedom Man | Bruce Mars | CC0 | [fuente](https://stocksnap.io/photo/freedom-man-K23VREDBTW) |
| `fruit_market.jpg` | Fruit Market | Daria Shevtsova | CC0 | [fuente](https://stocksnap.io/photo/fruit-market-E4J3BP6ZNJ) |
| `garden.jpg` | Indoor Garden | Mary | CC0 | [fuente](https://stocksnap.io/photo/indoor-garden-LZYYAHIG4E) |
| `grocery.jpg` | Drinks Food | wu yi | CC0 | [fuente](https://stocksnap.io/photo/drinks-food-8JM7H9ZB0J) |
| `hamilton.jpg` | Money Cash | Tim Sullivan | CC0 | [fuente](https://stocksnap.io/photo/money-cash-Z89ZJWCE6K) |
| `handshake.jpg` | Work Business | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/work-business-J5LXKNDREC) |
| `handshake2.jpg` | Work Business | Matt Moloney | CC0 | [fuente](https://stocksnap.io/photo/work-business-WQ2JMRIIQB) |
| `keyboard.jpg` | Macbook Laptop | Skitter Photo | CC0 | [fuente](https://stocksnap.io/photo/macbook-laptop-CJSRRVR4JE) |
| `keys.jpg` | Keys Door | WDnet Studio | CC0 | [fuente](https://stocksnap.io/photo/keys-door-Z1TKDI29FZ) |
| `kid_homework.jpg` | Child Homework | Direct Media | CC0 | [fuente](https://stocksnap.io/photo/child-homework-GV5GIEXDBA) |
| `kid_writing.jpg` | Child Kid | Martin Vorel | CC0 | [fuente](https://stocksnap.io/photo/child-kid-X6077HDEQH) |
| `laptop_study.jpg` | Laptop Apple | Stanley Dai | CC0 | [fuente](https://stocksnap.io/photo/laptop-apple-BUFBDV2NQW) |
| `library.jpg` | Books Library | Patrik Goethe | CC0 | [fuente](https://stocksnap.io/photo/books-library-EB9B6BC1F6) |
| `luxcar_in.jpg` | Luxury Car | Burst | CC0 | [fuente](https://stocksnap.io/photo/luxury-car-KADJ2NKMYQ) |
| `luxcar_in2.jpg` | Luxury Car | Burst | CC0 | [fuente](https://stocksnap.io/photo/luxury-car-CLCT9SWF9E) |
| `mic.jpg` | Microphone Audio | Maciej Korsan | CC0 | [fuente](https://stocksnap.io/photo/microphone-audio-IQVHQYS3GL) |
| `mic_guitar.jpg` | Microphone Condenser | Kelly Sikkema | CC0 | [fuente](https://stocksnap.io/photo/microphone-condenser-4C9TCUEARS) |
| `money_machine.jpg` | Equipment Banking | vedanti | CC0 | [fuente](https://stocksnap.io/photo/equipment-banking-E5LS3DUAG6) |
| `motos.jpg` | Motorbike Motorcycle | Skitter Photo | CC0 | [fuente](https://stocksnap.io/photo/motorbike-motorcycle-6F4302CB15) |
| `mountain.jpg` | Mountain Valley | Brodie Vissers | CC0 | [fuente](https://stocksnap.io/photo/mountain-valley-RQQGZIFM7U) |
| `mountain2.jpg` | Mountain Valley | Brodie Vissers | CC0 | [fuente](https://stocksnap.io/photo/mountain-valley-S1MTGHEBU4) |
| `night_person.jpg` | Dark Night | Tyson Dudley | CC0 | [fuente](https://stocksnap.io/photo/dark-night-TMQPS2OUGE) |
| `night_street.jpg` | Bogota - Streets at night 003 | momentcaptured1 | CC BY 2.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=12602145) |
| `notebook_calc.jpg` | Finance Flatlay | Artsy Crafty | CC0 | [fuente](https://stocksnap.io/photo/finance-flatlay-LPD3QR7VQG) |
| `office_man.jpg` | Man Laptop | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/man-laptop-HYRSHH13TD) |
| `office_women.jpg` | Woman Designer | Christina Morillo | CC0 | [fuente](https://stocksnap.io/photo/woman-designer-BEHESPSFYR) |
| `old_building.jpg` | Apartment Building | Roman Kraft | CC0 | [fuente](https://stocksnap.io/photo/apartment-building-EJ9K0OTJ6V) |
| `old_car.jpg` | Car Automobile | Skitter Photo | CC0 | [fuente](https://stocksnap.io/photo/car-automobile-45AE0493EF) |
| `pen.jpg` | Fountain Pen | Vintage RS | CC0 | [fuente](https://stocksnap.io/photo/fountain-pen-CJETOU0HKX) |
| `pen_paper.jpg` | Writing Paper | Helloquence | CC0 | [fuente](https://stocksnap.io/photo/writing-paper-KU273L0WTW) |
| `phone_field.jpg` | Mobile Smartphone | Kaboompics.com | CC0 | [fuente](https://stocksnap.io/photo/mobile-smartphone-QFEXEVWKFD) |
| `piggy_calc.jpg` | Piggy Bank | Artsy Crafty | CC0 | [fuente](https://stocksnap.io/photo/piggy-bank-ZLEVSWFWZC) |
| `plant_pot.jpg` | Minimal White | Tom Swinnen | CC0 | [fuente](https://stocksnap.io/photo/minimal-white-JETTZWAHZV) |
| `podcast.jpg` | Recording Studio | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/recording-studio-YA3HZPUFYL) |
| `rain_building.jpg` | Raining Raindrops | Rowan Heuvel | CC0 | [fuente](https://stocksnap.io/photo/raining-raindrops-AWI4TCQWK3) |
| `rain_window.jpg` | Rain Window | Mary | CC0 | [fuente](https://stocksnap.io/photo/rain-window-UL48EW7VNB) |
| `red_car.jpg` | People Couple | Clem Onojeghuo | CC0 | [fuente](https://stocksnap.io/photo/people-couple-HI60TXVHGB) |
| `road_closed.jpg` | Road Closed | Matt Bango | CC0 | [fuente](https://stocksnap.io/photo/road-closed-AMCJH0MCCH) |
| `road_forest.jpg` | Road Rural | Brandon Morgan | CC0 | [fuente](https://stocksnap.io/photo/road-rural-TAS2O83WG0) |
| `rocket.jpg` | Space Rocket | SpaceX | CC0 | [fuente](https://stocksnap.io/photo/space-rocket-QLXO02GEWL) |
| `rocket_trail.jpg` | Rockets Rocketship | SpaceX | CC0 | [fuente](https://stocksnap.io/photo/rockets-rocketship-1WKW24WDX7) |
| `runner.jpg` | Man Running | The Lazy Artist Gallery | CC0 | [fuente](https://stocksnap.io/photo/man-running-APW0W8GBMM) |
| `sales.jpg` | Woman Working | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/woman-working-GRXCYQMQTQ) |
| `savings_bills.jpg` | Bills Cash | Shopify | CC0 | [fuente](https://stocksnap.io/photo/bills-cash-RG4XMMLSNU) |
| `scissors.jpg` | Pink Scissors | Mike Birdy | CC0 | [fuente](https://stocksnap.io/photo/pink-scissors-X4A4FSCTBM) |
| `seedlings.jpg` | Seedlings Growing | Solo Shutter | CC0 | [fuente](https://stocksnap.io/photo/seedlings-growing-FSKMJDOOMB) |
| `seedlings2.jpg` | Seedlings Growing | Solo Shutter | CC0 | [fuente](https://stocksnap.io/photo/seedlings-growing-RI9D5RQ77B) |
| `shopping.jpg` | Window Shopping | Bruce Mars | CC0 | [fuente](https://stocksnap.io/photo/window-shopping-E1WZHWID6J) |
| `shopping2.jpg` | Woman Glasses | Bruce Mars | CC0 | [fuente](https://stocksnap.io/photo/woman-glasses-5LADXP8XUW) |
| `skyline.jpg` | Skyline downtown Bogota | Tijs Zwinkels | CC BY-SA 2.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=21381809) |
| `sleep_woman.jpg` | Woman Sleeping | Bruce Mars | CC0 | [fuente](https://stocksnap.io/photo/woman-sleeping-H1Z9XKGSBQ) |
| `snow.jpg` | Snow Winter | Elliott Chau | CC0 | [fuente](https://stocksnap.io/photo/snow-winter-ZKBPKSFZ7I) |
| `snowball.jpg` | Snowball Snow | Aaron Burden | CC0 | [fuente](https://stocksnap.io/photo/snowball-snow-B04IEZP9RE) |
| `sofa_tired.jpg` | Thinking Man | LinkedIn Sales Navigator | CC0 | [fuente](https://stocksnap.io/photo/thinking-man-0XI3PE0LIO) |
| `stairs.jpg` | Stairs Steps | Eric Haidara | CC0 | [fuente](https://stocksnap.io/photo/stairs-steps-L0G2A5R6VK) |
| `stock_red.jpg` | Stock Market | Altered Reality | CC0 | [fuente](https://stocksnap.io/photo/stock-market-BI0OXVDDLY) |
| `stock_red2.jpg` | Stocks Graph | 50Fish | CC0 | [fuente](https://stocksnap.io/photo/stocks-graph-MEDIALY3UV) |
| `stop_sign.jpg` | Stop Sign | Bob Richards | CC0 | [fuente](https://stocksnap.io/photo/stop-sign-2CJWIT0OVR) |
| `student_book.jpg` | Guy Man | Shopify | CC0 | [fuente](https://stocksnap.io/photo/guy-man-H0VXBZUZP3) |
| `students.jpg` | People Girls | Brodie Vissers | CC0 | [fuente](https://stocksnap.io/photo/people-girls-N444PJYUP9) |
| `suburb.jpg` | Neighborhood Houses | Qusai Akoud | CC0 | [fuente](https://stocksnap.io/photo/neighborhood-houses-E1WPGCLOC3) |
| `suburb2.jpg` | Suburban Street | Mike Moloney | CC0 | [fuente](https://stocksnap.io/photo/suburban-street-JDQIGEGDBB) |
| `swatches.jpg` | Color Swatches | Tim Sullivan | CC0 | [fuente](https://stocksnap.io/photo/color-swatches-VYSZEM4UWE) |
| `team.jpg` | Business Team | Direct Media | CC0 | [fuente](https://stocksnap.io/photo/business-team-W6PNBNYHM6) |
| `team2.jpg` | Team Meeting | Startup Stock Photos | CC0 | [fuente](https://stocksnap.io/photo/team-meeting-JBW2PXDOL6) |
| `think_dark.jpg` | Dark Man | Matthew Henry | CC0 | [fuente](https://stocksnap.io/photo/dark-man-XN9ZVVA8MO) |
| `think_wall.jpg` | Guy Man | Startup Stock Photos | CC0 | [fuente](https://stocksnap.io/photo/guy-man-SWRREC0K3A) |
| `tienda.jpg` | Tienda de barrio | Futuropopular | CC BY-SA 4.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=163143958) |
| `tm_night.jpg` | Bogota - Streets at night 009 | momentcaptured1 | CC BY 2.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=12602141) |
| `tm_station.jpg` | File:Av Américas Transmilenio Mundo Aventura.JPG | Felipe Restrepo Acosta | CC BY-SA 3.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=24064103) |
| `todo.jpg` | Checklist Goals | Glenn Carstens-Peters | CC0 | [fuente](https://stocksnap.io/photo/checklist-goals-TBJ9OPDGMK) |
| `track.jpg` | Running Track | Mateusz Dach | CC0 | [fuente](https://stocksnap.io/photo/running-track-TTPC0MC6RF) |
| `traffic.jpg` | Bogota Traffic Jam | Tokota | CC BY 3.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=77855116) |
| `umbrella.jpg` | Red Umbrella | Gabriel Santiago | CC0 | [fuente](https://stocksnap.io/photo/red-umbrella-45JIYYO371) |
| `video_cam.jpg` | Technology Camera | Donald Tong | CC0 | [fuente](https://stocksnap.io/photo/technology-camera-H0O97B44CT) |
| `videographer.jpg` | Videographer Cameraman | Leeroy | CC0 | [fuente](https://stocksnap.io/photo/videographer-cameraman-OQT16Q7SG7) |
| `wallst_book.jpg` | Macbook Laptop | Raymond Sam | CC0 | [fuente](https://stocksnap.io/photo/macbook-laptop-CSHQVPTWL8) |
| `watches.jpg` | Wood Watch | Burst | CC0 | [fuente](https://stocksnap.io/photo/wood-watch-IVZDQN85VY) |
| `woman_phone.jpg` | Woman Smartphone | Icons8 team | CC0 | [fuente](https://stocksnap.io/photo/woman-smartphone-MLEPUKHYUU) |
| `worker_belt.jpg` | Construction Worker | Leeroy | CC0 | [fuente](https://stocksnap.io/photo/construction-worker-6B70C91911) |
| `worker_hat.jpg` | Construction Zone | Leeroy | CC0 | [fuente](https://stocksnap.io/photo/construction-zone-6EAB6C3900) |
| `writing.jpg` | Woman Writing | JESHOOTS.com | CC0 | [fuente](https://stocksnap.io/photo/woman-writing-FFSUL8TZD3) |
| `wrong_way.jpg` | Wrong Way | Bob Richards | CC0 | [fuente](https://stocksnap.io/photo/wrong-way-W93CXLGFQX) |

`photos/credits.json` guarda los mismos datos.
