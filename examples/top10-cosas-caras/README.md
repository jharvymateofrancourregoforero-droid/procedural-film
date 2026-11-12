# Top 10 cosas más caras que se han comprado

Video de YouTube en 16:9 (1920x1080, 30 fps) de **13:29** para el canal **El Precio del Poder**.
Es una versión original y verificada del tema "Top 10 cosas más caras del mundo que han sido compradas". Cada precio es un récord confirmado con fuentes, y varios datos se actualizaron a 2024–2026.
Usa fotos reales (Wikimedia Commons y StockSnap), la voz de ElevenLabs "Mauricio Viral", y música y efectos sintetizados con código. No usa imágenes ni música de IA.

- Miniatura: [`exports/miniatura.jpg`](exports/miniatura.jpg). Muestra tres fotos reales (el estegosaurio Apex, el Salvator Mundi y el Mercedes 300 SLR) con sus precios y el texto "¿QUIÉN PAGA ESTO?" (`python3 tools/thumbnail.py`).
- Título, descripción con capítulos, fuentes, créditos y etiquetas: [`exports/descripcion_youtube.txt`](exports/descripcion_youtube.txt).
- El MP4 (`exports/top10-cosas-caras.mp4`) no se sube al repositorio por su tamaño. Se regenera con los pasos de abajo.

## Estructura

0:00 Introducción
0:36 #10 Pluma de huia
1:48 #9 Romanée-Conti 1945
3:04 #8 Estampilla One Cent Magenta
4:12 #7 Cámara Leica nº 105
5:21 #6 Patek Philippe Grandmaster Chime
6:25 #5 Códice Sassoon
7:29 #4 Dinosaurio Apex
8:30 #3 Diamante Pink Star
9:31 #2 Mercedes-Benz 300 SLR
10:35 Menciones honoríficas
11:15 #1 Salvator Mundi
12:23 La lección

Cada puesto tiene dos partes: el récord (precio, fecha y subasta) y la historia detrás del precio. Antes del #1 hay menciones honoríficas.

## El top (precio pagado, con comisión)

| # | Objeto | Precio | Venta |
|---|---|---|---|
| 10 | Pluma de huia | NZ$ 46.521 (≈ US$ 28.400) | Webb's, Auckland, mayo 2024 |
| 9 | Romanée-Conti 1945 (1 botella) | US$ 812.500 | Acker, Nueva York, marzo 2026 |
| 8 | One Cent Magenta (Guayana Británica, 1856) | US$ 8,3 M | Sotheby's, junio 2021 |
| 7 | Leica serie 0 nº 105 (de Oskar Barnack) | € 14,4 M (≈ US$ 15 M) | Leitz Photographica Auction, Viena, junio 2022 |
| 6 | Patek Philippe Grandmaster Chime 6300A-010 (acero) | CHF 31 M (≈ US$ 31 M) | Christie's / Only Watch, Ginebra, nov. 2019 |
| 5 | Códice Sassoon | US$ 38,1 M | Sotheby's Nueva York, mayo 2023 |
| 4 | Estegosaurio "Apex" | US$ 44,6 M | Sotheby's Nueva York, julio 2024 |
| 3 | Diamante Pink Star (59,6 ct) | US$ 71,2 M | Sotheby's Hong Kong, abril 2017 |
| 2 | Mercedes-Benz 300 SLR Uhlenhaut Coupé (1955) | € 135 M (≈ US$ 143 M) | RM Sotheby's, Stuttgart, mayo 2022 |
| 1 | Salvator Mundi (atribuido a Leonardo) | US$ 450,3 M | Christie's Nueva York, nov. 2017 |

Menciones honoríficas: whisky Macallan 1926 (≈ US$ 2,7 M, Sotheby's 2023), Ferrari 250 GTO de 1962 (US$ 51,7 M, RM Sotheby's 2023), "Shot Sage Blue Marilyn" de Warhol (US$ 195 M, Christie's 2022) y el retrato de Elisabeth Lederer de Klimt (US$ 236,4 M, Sotheby's 2025).

En el #6, el #3 y el Códice Leicester no hay fotos libres del objeto exacto. Por eso se usan imágenes de referencia, y un aviso en pantalla lo dice.

## Cómo está hecho

| Parte | Detalle |
|---|---|
| Voz | ElevenLabs `eleven_v4`, voz "Mauricio Viral". Son 23 bloques de una toma cada uno (unos 12.000 créditos en total): 12 de la primera versión y 11 de la versión larga. El eslogan del canal se reutiliza del video anterior. Los tiempos por palabra salen de Scribe y están en `audio/words_*.json`. |
| Fotos | 75 fotos reales de Wikimedia Commons y StockSnap (CC0), encontradas con Openverse. Las licencias están en `photos/credits.json`. |
| Edición | `tools/render.py` y `tools/timeline.py`. Tiene 178 planos anclados a frases, tarjetas de ranking, contadores de precio, comparaciones "esperaban vs. pagaron", fichas, botón de suscripción y subtítulos palabra por palabra. |
| Música | Beat sintetizado en `tools/audio.py`, con caída y golpe en cada tarjeta. La música baja sola cuando habla la voz, y el total queda a -14 LUFS. |

## Volver a generar

```bash
python3 tools/audio.py
```

```bash
python3 tools/render.py
```

```bash
ffmpeg -y -i build/video.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v libx264 -preset medium -crf 23 -maxrate 3700k -bufsize 7400k -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart exports/top10-cosas-caras.mp4
```

```bash
python3 tools/thumbnail.py
```

## Guion grabado

### Gancho
> Una pluma que vale más que su peso en oro. Una botella de vino por la que pagaron más que por una casa. Y una pintura... que costó cuatrocientos cincuenta millones de dólares. Hoy te traigo las diez cosas más caras que alguien ha comprado de verdad, con récords confirmados. Y al final te digo qué tienen todas en común... porque ahí está la lección de dinero más importante de este video.

### Eslogan
> ¡Muy buenas, gente! Bienvenidos a El Precio del Poder. Aquí el dinero se gana... y el poder se aprende. ¡Arranca el top!

### #10
> Número diez: una pluma. Sí, una sola pluma. En mayo de dos mil veinticuatro, una pluma de huia se vendió en Nueva Zelanda por cuarenta y seis mil quinientos dólares neozelandeses, unos veintiocho mil dólares estadounidenses. El huia era un ave sagrada para el pueblo maorí, y se extinguió a principios del siglo veinte. Por eso cada pluma que queda es casi imposible de conseguir. Gramo por gramo, esa pluma vale más que el oro.

### #10 (la historia detrás)
> Y la historia de esta pluma es increíble. Para los maoríes, las plumas de huia eran un símbolo de rango: solo los jefes las usaban, y las guardaban en cajas talladas llamadas waka huia. Pero en mil novecientos uno, un guía maorí le puso una pluma de huia en el sombrero al duque de York, que estaba de visita en Nueva Zelanda... y se volvió moda en Europa. Todo el mundo quería una. Seis años después, en mil novecientos siete, se vio al último huia confirmado. Y ojo: la casa de subastas esperaba venderla en unos tres mil dólares neozelandeses. Se pagó más de quince veces eso.

### #9
> Número nueve: una botella de vino. En marzo de dos mil veintiséis, una botella de Romané Conti de mil novecientos cuarenta y cinco se subastó en Nueva York por ochocientos doce mil quinientos dólares. Es el vino más caro jamás vendido en una subasta. ¿Por qué tanto? Porque de esa cosecha solo se hicieron unas seiscientas botellas, y fue la última antes de que el viñedo arrancara sus vides más viejas. Cada botella que alguien se toma... deja una menos en el mundo.

### #9 (la historia detrás)
> Para entender ese precio, hay que ir a Borgoña, en Francia. El viñedo de Romané Conti mide menos de dos hectáreas: más o menos como dos canchas y media de fútbol. Y es uno de los más famosos del planeta. En mil novecientos cuarenta y cinco pasó algo único: después de esa cosecha, arrancaron las vides viejas y volvieron a sembrar. Durante seis años no salió ni una sola botella de Romané Conti. Por eso el cuarenta y cinco es casi una leyenda. El récord anterior, de dos mil dieciocho, había sido de quinientos cincuenta y ocho mil dólares... y esta botella lo superó por más de doscientos cincuenta mil.

### #8
> Número ocho: una estampilla. Un pedacito de papel de mil ochocientos cincuenta y seis, impreso en la Guayana Británica: el One Cent Magenta. Cuando salió, costaba un centavo. Y en dos mil veintiuno se vendió por ocho millones trescientos mil dólares. ¿La razón? Es la única que se conoce en el mundo. No hay otra. Y cuando algo es único, el precio lo pone quien más lo desea.

### #8 (la historia detrás)
> Su historia parece de película. En mil ochocientos cincuenta y seis, a la Guayana Británica no llegaron a tiempo las estampillas desde Inglaterra, así que un periódico local imprimió unas de emergencia. En mil ochocientos setenta y tres, un niño escocés de doce años la encontró entre papeles viejos de su familia... y la vendió por seis chelines. Después pasó por las manos de los coleccionistas más ricos del mundo. Y un dato curioso: en dos mil catorce se había vendido por casi nueve millones y medio de dólares. O sea que en dos mil veintiuno... se vendió más barata. Hasta lo más raro del mundo puede bajar de precio.

### #7
> Número siete: una cámara de fotos. Una Leica de la serie cero, fabricada en Alemania hace más de cien años. Esta en particular, la número ciento cinco, perteneció a Oskar Barnack, el hombre que creó la cámara Leica. En dos mil veintidós se subastó en Viena por catorce millones cuatrocientos mil euros, unos quince millones de dólares. Esperaban venderla en tres millones... y terminó costando casi cinco veces más.

### #7 (la historia detrás)
> ¿Y por qué una cámara vieja vale tanto? Porque esta cambió la historia. Oskar Barnack sufría de asma, y las cámaras de su época eran enormes y pesadas. Así que diseñó una pequeña, que usaba la misma película de treinta y cinco milímetros del cine. Esa idea dio origen a la fotografía moderna: casi todas las cámaras que vinieron después copiaron ese formato. Y de la serie cero, la de prueba, se fabricaron apenas unas veinte. Esta era la de su propio creador. No compraron una cámara... compraron el comienzo de la fotografía que hoy conocemos.

### #6
> Número seis: un reloj. El Patek Philippe Grandmaster Chime, en acero. Tiene veinte funciones, entre ellas cinco formas distintas de dar la hora con sonido. Y solo existe uno en acero. En dos mil diecinueve se subastó en Ginebra por treinta y un millones de dólares. ¿Y sabes qué es lo mejor? Era una subasta benéfica: el dinero fue para investigar la distrofia muscular de Duchenne.

### #6 (la historia detrás)
> Este reloj es una locura de ingeniería. Tiene mil trescientas sesenta y seis piezas, y dos caras: puedes girar la caja y usarlo por cualquiera de los dos lados. Patek Philippe lo creó para celebrar sus ciento setenta y cinco años, y casi todos los que hizo son de oro. Por eso el de acero es tan especial: es una pieza única. Con ese precio se convirtió en el reloj de pulsera más caro jamás vendido en una subasta. El récord anterior era el Rolex Daytona de Paul Newman, con diecisiete millones ochocientos mil dólares. ¡Casi lo duplicó!

### #5
> Número cinco: un libro. El Códice Sassoon, la Biblia hebrea casi completa más antigua que se conoce, de hace unos mil cien años. En dos mil veintitrés se vendió en Nueva York por treinta y ocho millones cien mil dólares: el manuscrito más caro jamás subastado. Lo compró un exembajador de Estados Unidos... y lo donó a un museo en Tel Aviv, para que cualquiera pueda verlo.

### #5 (la historia detrás)
> El Códice Sassoon tiene más de mil años y está escrito a mano sobre pergamino. Lleva el nombre de David Sassoon, un coleccionista que lo compró en mil novecientos veintinueve. Antes de esta venta, el manuscrito más caro del mundo era el Códice Leicester, de Leonardo da Vinci, que Bill Gates compró en mil novecientos noventa y cuatro por unos treinta millones ochocientos mil dólares. El Sassoon lo superó. Y fíjate en algo: el comprador pudo quedárselo en su casa... y prefirió que lo viera todo el mundo. Eso también es poder.

### #4
> Número cuatro: un dinosaurio. Un esqueleto de estegosaurio casi completo, de unos ciento cincuenta millones de años, al que llamaron Apex. Lo encontraron en un terreno privado en Colorado. La casa de subastas esperaba venderlo en unos seis millones de dólares... pero en julio de dos mil veinticuatro el multimillonario Ken Griffin pagó cuarenta y cuatro millones seiscientos mil dólares. Es el fósil más caro de la historia.

### #4 (la historia detrás)
> A Apex lo encontró Jason Cooper, un paleontólogo, en su propio terreno, en un pueblo de Colorado que se llama, literalmente... Dinosaur. Mide unos tres metros de alto y ocho de largo, y conserva doscientos cincuenta y cuatro de sus trescientos diecinueve huesos. El récord anterior lo tenía Stan, un Tiranosaurio Rex vendido en dos mil veinte por treinta y un millones ochocientos mil dólares. Y lo mejor: Griffin se lo prestó a un museo en Nueva York, y hoy cualquiera puede ir a verlo.

### #3
> Número tres: un diamante. El Pink Star: un diamante rosado de casi sesenta quilates. En bruto pesaba ciento treinta y dos quilates, y tardaron dos años en cortarlo y pulirlo. En dos mil diecisiete se subastó en Hong Kong por setenta y un millones doscientos mil dólares: la joya más cara jamás vendida en una subasta. Su comprador le cambió el nombre en honor a su padre.

### #3 (la historia detrás)
> El Pink Star salió de una mina de De Beers en Sudáfrica, en mil novecientos noventa y nueve. Y tiene la máxima calificación: rosado vivo intenso, y sin ninguna imperfección por dentro. Pero lo más loco es que no era su primera subasta. En dos mil trece, un comprador ofreció ochenta y tres millones de dólares... y nunca pagó. La casa de subastas tuvo que quedarse con el diamante. Cuatro años después, el grupo joyero Chow Tai Fook se lo llevó en Hong Kong, en apenas cinco minutos de puja.

### #2
> Número dos: un carro. Y no, no es un Ferrari. Es un Mercedes-Benz trescientos SLR Uhlenhaut Coupé, de mil novecientos cincuenta y cinco. Solo se fabricaron dos. En mayo de dos mil veintidós, uno de ellos se vendió por ciento treinta y cinco millones de euros, unos ciento cuarenta y tres millones de dólares. Superó el récord anterior por más de noventa millones de euros. Es el carro más caro de la historia.

### #2 (la historia detrás)
> Este carro nació para las carreras. Mercedes lo construyó a partir del trescientos SLR, el que ganó la Mille Miglia de mil novecientos cincuenta y cinco con Stirling Moss. Pero ese mismo año, después de un terrible accidente en Le Mans, Mercedes se retiró de las competencias, y estos coupés nunca corrieron. Uno se lo quedó Rudolf Uhlenhaut, el ingeniero jefe de pruebas, como su carro de la empresa: podía pasar de los doscientos ochenta kilómetros por hora. Por eso lleva su nombre. Y el dinero de la venta fue a un fondo de becas para jóvenes.

### Menciones honoríficas
> Antes del número uno, unas menciones honoríficas que se quedaron muy cerca. Un whisky Macallan de mil novecientos veintiséis: unos dos millones setecientos mil dólares por una sola botella. Un Ferrari doscientos cincuenta GTO de mil novecientos sesenta y dos: cincuenta y un millones setecientos mil. La Marilyn de Andy Warhol: ciento noventa y cinco millones. Y en dos mil veinticinco, un retrato de Gustav Klimt se vendió por doscientos treinta y seis millones de dólares: la segunda obra de arte más cara jamás subastada. Pero ninguna se acerca al número uno.

### #1
> Y el número uno: una pintura. El Salvator Mundi, atribuido a Leonardo da Vinci. Una pintura de Jesús de apenas sesenta y cinco centímetros de alto. En noviembre de dos mil diecisiete se vendió en Christie's, en Nueva York, por cuatrocientos cincuenta millones trescientos mil dólares. Es la obra de arte más cara jamás vendida. ¿Lo más raro? Desde ese día, casi nadie la ha vuelto a ver en público.

### #1 (la historia detrás)
> Y su historia es la más increíble del top. En mil novecientos cincuenta y ocho, esta misma pintura se vendió por cuarenta y cinco libras, porque pensaban que era una copia. En dos mil cinco, unos comerciantes de arte la compraron por poco más de mil dólares, la restauraron... y los expertos dijeron que podía ser de Leonardo. En dos mil trece se vendió por ochenta millones, después por ciento veintisiete millones y medio... y en dos mil diecisiete, por cuatrocientos cincuenta. Hoy todavía hay expertos que dudan de que la haya pintado Leonardo. Y de él quedan menos de veinte pinturas en el mundo.

### Cierre: la lección
> ¿Y qué tienen en común estas diez cosas? Tres cosas. Uno: son escasas. Casi no hay... o son únicas. Dos: tienen una historia que nadie más puede contar. Y tres: hubo alguien dispuesto a pagar. Porque al final, el precio no lo pone el objeto: lo pone quien lo desea. Y esa misma regla mueve tu dinero. Lo escaso vale más. Por eso, la habilidad más escasa que tengas... es la que más te van a pagar. Ahora dime en los comentarios: si tuvieras cuarenta y cuatro millones de dólares, ¿te comprarías un dinosaurio? Suscríbete y activa la campanita. Esto fue El Precio del Poder. Recuerda: el dinero se gana... y el poder se aprende. ¡Nos vemos!
