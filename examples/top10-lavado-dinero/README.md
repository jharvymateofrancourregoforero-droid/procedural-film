# 10 formas de lavar dinero (y cómo los atraparon)

Video de YouTube en 16:9 (1920x1080, 30 fps) de **11:34** para el canal **El Precio del Poder**.
Es un video **educativo**: explica cómo criminales famosos lavaron dinero, con casos reales y verificados, y sobre todo cómo los atraparon. No da instrucciones; cierra con un consejo para protegerse (no prestar la cuenta bancaria, Nequi o Daviplata).
Usa fotos reales (Wikimedia Commons y StockSnap), la voz de ElevenLabs "Mauricio Viral", y música y efectos sintetizados con código. No usa imágenes ni música de IA.

- Miniatura: [`exports/miniatura.jpg`](exports/miniatura.jpg). Muestra "10 FORMAS DE LAVAR DINERO", un sello rojo "Y CÓMO LOS ATRAPARON" y dos casos: la torre de HSBC (multa de US$ 1.920 M) y un bitcoin (US$ 3.600 M incautados) (`python3 tools/thumbnail.py`).
- Título, descripción con capítulos, fuentes, créditos y etiquetas: [`exports/descripcion_youtube.txt`](exports/descripcion_youtube.txt).
- El MP4 (`exports/top10-lavado-dinero.mp4`) no se sube al repositorio por su tamaño. Se regenera con los pasos de abajo.

## Estructura

0:00 Introducción
1:35 #10 El pitufeo
2:30 #9 Negocios de fachada
3:22 #8 Los casinos
4:14 #7 Casas de lujo
5:08 #6 El arte
5:56 #5 Mercado negro del peso
6:50 #4 Empresas fantasma
7:39 #3 Criptomonedas
8:35 #2 Bancos que miran para otro lado
9:26 #1 1MDB: el robo de un país
10:20 La lección

## Casos y datos verificados

| # | Método | Caso real |
|---|---|---|
| 10 | Pitufeo (partir el efectivo) | Dennis Hastert: ~US$ 950.000 en más de 100 retiros; 15 meses de prisión (2016) |
| 9 | Negocios de fachada | La expresión "lavado de dinero" aparece con Watergate (1973); lo de Capone y las lavanderías es un mito; Capone cayó por impuestos (1931) |
| 8 | Casinos | Columbia Británica: C$ 376 M en efectivo sospechoso (2012–2015), C$ 279 M en billetes de 20; Comisión Cullen (2022) |
| 7 | Casas de lujo | EE. UU. exige identificar al dueño real en compras de lujo de contado por empresas (FinCEN, desde 2016); apartamento ligado a 1MDB confiscado en Nueva York |
| 6 | Arte | Edemar Cid Ferreira (Banco Santos): "Hannibal" de Basquiat, ~US$ 8 M, declarado en aduana por US$ 100; devuelto a Brasil |
| 5 | Mercado negro del peso | Cambio de dólares de los carteles en EE. UU. por pesos en Colombia a través de importadores (FinCEN) |
| 4 | Empresas fantasma | Papeles de Panamá (2016): 11,5 M de documentos, 214.488 empresas; Mossack Fonseca cerró en 2018 |
| 3 | Criptomonedas | Bitfinex: 119.754 BTC robados (2016); ~94.000 BTC recuperados en 2022 (~US$ 3.600 M); 5 años y 18 meses de prisión |
| 2 | Bancos que miran para otro lado | HSBC: US$ 881 M de carteles (2006–2010), US$ 1.920 M (2012); TD Bank: ~US$ 3.000 M (2024), +US$ 670 M movidos |
| 1 | 1MDB | +US$ 4.500 M desviados (2009–2015); yate, Monet, Van Gogh, mansiones y "El lobo de Wall Street"; Najib Razak condenado; Jho Low prófugo |

## Cómo está hecho

| Parte | Detalle |
|---|---|
| Voz | ElevenLabs `eleven_v4`, voz "Mauricio Viral". Son 13 bloques de una toma cada uno (unos 9.800 créditos). El eslogan del canal se reutiliza. Los tiempos por palabra salen de Scribe y están en `audio/words_*.json`. |
| Fotos | 56 fotos reales de Wikimedia Commons y StockSnap (CC0), encontradas con Openverse. Las licencias están en `photos/credits.json`. |
| Edición | `tools/render.py` y `tools/timeline.py`. Tiene 128 planos anclados a frases, tarjetas de ranking, contadores, comparaciones, diagramas de pasos, fichas, botón de suscripción y subtítulos palabra por palabra. |
| Música | Beat sintetizado en `tools/audio.py`. La música baja sola cuando habla la voz, y el total queda a -14 LUFS. |

## Volver a generar

```bash
python3 tools/audio.py
```

```bash
python3 tools/render.py
```

```bash
ffmpeg -y -i build/video.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v libx264 -preset medium -crf 23 -maxrate 3700k -bufsize 7400k -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart exports/top10-lavado-dinero.mp4
```

```bash
python3 tools/thumbnail.py
```

## Guion grabado

### Gancho
> En dos mil doce, uno de los bancos más grandes del mundo aceptó pagar casi dos mil millones de dólares. ¿La razón? Por sus ventanillas en México pasaron cientos de millones de dólares de los carteles... en cajas hechas a la medida exacta de la ventanilla. Eso es lavar dinero: hacer que la plata del crimen parezca ganada de forma legal. Hoy te traigo diez formas en que los criminales más famosos lavaron dinero... y cómo los atraparon. Ojo: esto no es un tutorial. Es todo lo contrario. Al final vas a entender por qué casi todos terminan cayendo... y cómo protegerte para que nunca te usen a ti.

### Lo básico
> Antes de arrancar, lo básico. Casi todo lavado de dinero tiene tres etapas. Uno: la colocación, meter la plata sucia al sistema financiero. Dos: la estratificación, moverla muchas veces para borrar su origen. Y tres: la integración, que la plata vuelva al dueño como si fuera limpia: una casa, una empresa, una inversión. Y del otro lado están los que vigilan. En Colombia existe la UIAF, la Unidad de Información y Análisis Financiero, que recibe los reportes de operaciones sospechosas de bancos, notarías y muchas empresas. Y en el mundo, el GAFI pone los estándares que siguen más de doscientos países y territorios. Con eso claro... vamos con lo bueno.

### Eslogan
> ¡Muy buenas, gente! Bienvenidos a El Precio del Poder. Aquí el dinero se gana... y el poder se aprende. ¡Arranca el top!

### #10
> Número diez: el pitufeo. Es el truco más viejo: en vez de mover una suma grande de una sola vez, la parten en muchos pedacitos para no llamar la atención. En Estados Unidos, los bancos tienen que reportar los movimientos en efectivo de más de diez mil dólares. Y partir la plata a propósito para esquivar ese reporte... ya es un delito por sí solo. Le pasó a Dennis Hastert, que había sido presidente de la Cámara de Representantes. Sacó cerca de novecientos cincuenta mil dólares en más de cien retiros pequeños, para comprar el silencio de una víctima de abusos que él había cometido décadas atrás. El banco notó el patrón, lo reportó, el FBI investigó... y en dos mil dieciséis lo condenaron a quince meses de prisión. La lección: los bancos no ven retiros sueltos. Ven patrones.

### #9
> Número nueve: los negocios de fachada. Un restaurante, un lavadero de carros, una tienda... que funciona de verdad, pero que reporta muchas más ventas de las que tiene. Así, la plata sucia entra mezclada con la limpia. Y un dato curioso: se dice que el término "lavado de dinero" viene de Al Capone y sus lavanderías... pero es un mito. La expresión se popularizó en mil novecientos setenta y tres, con el escándalo de Watergate. Y a Capone, por cierto, no lo encerraron por sus crímenes, sino por no pagar impuestos. ¿Y cómo los atrapan? Con números que no cuadran: un local pequeño con ventas de centro comercial, sin clientes, sin compras de inventario. Las autoridades comparan lo que declaras... con lo que de verdad es posible vender.

### #8
> Número ocho: los casinos. La idea es entrar con efectivo sucio, cambiarlo por fichas, jugar un poco... y salir con algo que parece una ganancia legal. En la provincia canadiense de Columbia Británica, entre dos mil doce y dos mil quince, los casinos recibieron unos trescientos setenta y seis millones de dólares canadienses en efectivo sospechoso. Doscientos setenta y nueve millones venían en billetes de veinte, amarrados en ladrillos. Llegaba gente con bolsas llenas de billetes pequeños... a apostar sumas enormes. El escándalo terminó en una investigación pública, la Comisión Cullen, que en dos mil veintidós señaló fallas de los casinos, de los reguladores y del gobierno. La lección: el efectivo en masa siempre deja huella.

### #7
> Número siete: las casas y los apartamentos de lujo. Una propiedad puede costar millones en una sola compra. Y si se paga de contado, a nombre de una empresa, nadie sabe quién es el verdadero dueño. Por eso ciudades como Miami o Nueva York se volvieron imanes de dinero sospechoso. En dos mil dieciséis, el Tesoro de Estados Unidos empezó a exigir que, en compras de lujo pagadas de contado por empresas, se identificara a la persona real que está detrás. Y la plata de uno de los fraudes más grandes de la historia terminó, entre otras cosas, en un apartamento de lujo en Nueva York... que la justicia estadounidense terminó confiscando. De ese caso te hablo en el número uno. La lección: detrás de cada empresa hay una persona. Y tarde o temprano la buscan.

### #6
> Número seis: el arte. Una pintura puede valer millones, cabe en una caja, y su precio es difícil de verificar. Edemar Cid Ferreira era el dueño del Banco Santos, en Brasil. El banco quebró en dos mil cinco con deudas de más de mil millones de dólares... pero él había comprado cientos de obras de arte. Una de ellas, un cuadro de Jean-Michel Basquiat llamado Hannibal, valía unos ocho millones de dólares. ¿Sabes con qué valor lo declararon en la aduana para meterlo a Estados Unidos? Cien dólares. Las autoridades lo encontraron en una bodega de Nueva York y, años después, la pintura volvió a Brasil. La lección: un precio absurdo no es un escondite. Es una alarma.

### #5
> Número cinco, y este nos toca de cerca: el mercado negro del peso. Así funcionaba: los carteles tenían montañas de dólares en Estados Unidos, pero necesitaban pesos en Colombia. Al mismo tiempo, había importadores colombianos que necesitaban dólares para comprar mercancía en el exterior. Un intermediario, el cambista, juntaba las dos cosas: le pagaba pesos al cartel en Colombia, y usaba esos dólares sucios para pagar la mercancía de los importadores. El dinero casi no cruzaba la frontera... pero el lavado sí. A veces, además, inflaban o rebajaban el precio en las facturas para esconder todavía más plata en el comercio. Las autoridades de Estados Unidos lo vienen persiguiendo desde los años noventa. La lección: el comercio también se audita.

### #4
> Número cuatro: las empresas fantasma en paraísos fiscales. Son empresas que existen en el papel, pero no tienen oficinas, ni empleados, ni actividad real. Sirven para esconder quién es el verdadero dueño del dinero. En dos mil dieciséis estallaron los Papeles de Panamá: más de once millones y medio de documentos filtrados de un bufete llamado Mossack Fonseca, con más de doscientas catorce mil empresas offshore, ligadas a gente de más de doscientos países y territorios. Ojo: tener una empresa en el exterior no es ilegal por sí solo. Pero la filtración abrió investigaciones en decenas de países, y el bufete terminó cerrando en dos mil dieciocho. La lección: los secretos financieros no son eternos.

### #3
> Número tres: las criptomonedas. Mucha gente cree que son imposibles de rastrear... y es justo al revés. En dos mil dieciséis, un hacker robó ciento diecinueve mil setecientos cincuenta y cuatro bitcoins del exchange Bitfinex. Él y su esposa pasaron años moviéndolos por miles de transacciones y cuentas falsas, para intentar borrar el rastro. Pero en la blockchain, cada movimiento queda registrado para siempre. En dos mil veintidós, los investigadores siguieron ese rastro, los arrestaron y recuperaron unos noventa y cuatro mil bitcoins, que entonces valían unos tres mil seiscientos millones de dólares: la incautación más grande en la historia del Departamento de Justicia de Estados Unidos. Él recibió cinco años de prisión; ella, dieciocho meses. La lección: en cripto, el rastro es permanente.

### #2
> Número dos: cuando el banco mira para otro lado. Entre dos mil seis y dos mil diez, el cartel de Sinaloa, en México, y el cartel del Norte del Valle, en Colombia, movieron al menos ochocientos ochenta y un millones de dólares a través de HSBC. Llegaban a depositar con cajas hechas a la medida de las ventanillas. En dos mil doce, el banco aceptó pagar mil novecientos veinte millones de dólares. Y la historia se repitió: en dos mil veinticuatro, TD Bank se declaró culpable en Estados Unidos y aceptó pagar unos tres mil millones de dólares, por dejar que redes criminales movieran más de seiscientos setenta millones por sus cuentas. La lección: hasta los bancos más grandes pagan caro cuando no vigilan.

### #1
> Y el número uno: robarle a un país entero. 1MDB era un fondo del gobierno de Malasia, creado para invertir en el desarrollo del país. Entre dos mil nueve y dos mil quince, se desviaron más de cuatro mil quinientos millones de dólares. El cerebro, según las autoridades, fue un financista llamado Jho Low. La plata pasó por bancos de varios países... y terminó en un yate de unos doscientos cincuenta millones, en cuadros de Monet y de Van Gogh, en mansiones... y, según la justicia de Estados Unidos, hasta ayudó a financiar la película El lobo de Wall Street. El ex primer ministro de Malasia, Najib Razak, fue condenado y está en prisión. Y Jho Low... sigue prófugo. La lección: puedes esconder el dinero un tiempo. Pero no para siempre.

### Cierre: la lección
> ¿Y qué tienen en común estos diez casos? Que todos dejaron rastro. Retiros con patrones raros, ventas que no cuadran, precios absurdos, documentos filtrados, una blockchain que nunca olvida. El lavado de dinero puede durar años... pero casi siempre termina igual: con multas, cárcel y bienes confiscados. Y aquí va la parte que sí te sirve a ti: nunca prestes tu cuenta bancaria, tu Nequi o tu Daviplata para recibir plata de otros, por más fácil que suene el negocio. Así es como reclutan a las mulas de dinero... y el que termina respondiendo ante la ley eres tú. Ahora dime en los comentarios: ¿cuál de estos casos te pareció más increíble? Suscríbete y activa la campanita. Esto fue El Precio del Poder. Recuerda: el dinero se gana... y el poder se aprende. ¡Nos vemos!
