# Top 10 formas de ganar dinero siendo adolescente

Video de YouTube en 16:9 (1920x1080, 30 fps) de **8:24** para el canal **El Precio del Poder**.
Usa fotos reales con licencia libre, la voz de ElevenLabs "Mauricio Viral", y música y efectos sintetizados con código. No usa imágenes ni música de IA.

- Miniatura: [`exports/miniatura.jpg`](exports/miniatura.jpg): pantalla dividida "VIO ESTE VIDEO → $$$" vs "NO LO VIO → $0", con "TOP 10 · FORMAS DE GANAR DINERO" al centro (`python3 tools/thumbnail_v4.py`). Versiones anteriores: `exports/miniatura_v1.jpg`, `miniatura_v2.jpg`, `miniatura_v3.jpg`.
- Títulos, descripción con capítulos, aviso legal, créditos y etiquetas: [`exports/descripcion_youtube.txt`](exports/descripcion_youtube.txt)
- El MP4 (`exports/top10-adolescentes.mp4`) no se sube al repositorio por su tamaño; se regenera con los pasos de abajo.

## Eslogan del canal

> ¡Muy buenas, gente! Bienvenidos a El Precio del Poder.
> Aquí el dinero se gana... y el poder se aprende.
> ¡Arranca el top!

Va después del gancho, con un logo animado ("EL PRECIO / DEL PODER" con la frase en dos tiempos), y vuelve en la despedida: "Esto fue El Precio del Poder. Recuerda: el dinero se gana... y el poder se aprende."

## Estructura

0:00 Introducción
0:37 #10 Lavar carros y motos
1:14 #9 Pasear y cuidar mascotas
1:49 #8 Vender postres y snacks
2:25 #7 Dar clases o tutorías
3:00 #6 El técnico del barrio
3:34 #5 Vender y revender
4:11 #4 Hecho a mano
4:47 #3 Editar videos y diseñar
5:22 #2 Redes para negocios
5:57 #1 Crear tu propio contenido
6:50 5 reglas de oro

Cada puesto abre con una tarjeta de ranking (número gigante en amarillo y el nombre del puesto). Durante el puesto aparece una etiqueta fija arriba a la derecha y los conceptos clave como chips, listas o pasos.

## Datos verificados

- Colombia: edad mínima de admisión al trabajo 15 años; de 15 a 17 se requiere autorización del inspector de trabajo (Código de la Infancia y la Adolescencia, Ley 1098 de 2006, art. 35).
- YouTube (AdSense): edad mínima 18 años para recibir pagos; un menor necesita que un padre o tutor maneje la cuenta de cobro.
- No se dan cifras de ganancias: dependen de la ciudad, el trabajo y el esfuerzo, y el video no promete ingresos.

## Cómo está hecho

| Parte | Detalle |
|---|---|
| Voz | ElevenLabs `eleven_v4`, voz "Mauricio Viral", 14 bloques de 1 toma cada uno (6.956 créditos). Tiempos por palabra con Scribe en `audio/words_*.json`. |
| Fotos | 98 fotos reales de StockSnap (CC0) y Wikimedia Commons, encontradas con Openverse; licencias en `photos/credits.json`. |
| Edición | `tools/render.py` y `tools/timeline.py`: 108 planos anclados a frases, tarjetas de ranking, chips, listas, pasos, botón de suscripción, subtítulos palabra por palabra, barridos, flashes, grano y viñeta. |
| Música | Beat funk/hip-hop a 96 bpm sintetizado en `tools/audio.py`, con una progresión distinta por puesto, caída y golpe en cada tarjeta y un tono más sobrio en las reglas de oro. |
| Mezcla | La música baja sola cuando habla la voz; total a -14 LUFS. |
| Miniatura | `tools/thumbnail.py`: recorte con OpenCV GrabCut (sin IA) sobre billetes casi en blanco y negro. |

## Volver a generar

```bash
python3 tools/audio.py
```

```bash
python3 tools/render.py
```

```bash
ffmpeg -y -i build/video.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v libx264 -preset medium -crf 23 -maxrate 3700k -bufsize 7400k -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart exports/top10-adolescentes.mp4
```

## Guion grabado

### Gancho
> ¿Tienes entre trece y diecisiete años y quieres tener tu propia plata, sin tener que pedirle a nadie?
>
> Hoy te traigo diez formas reales de ganar dinero siendo adolescente. Vamos de la más sencilla... a la que más puede crecer. Y quédate hasta el número uno, porque es la que puede cambiar tu futuro.
>
> Pero antes, una regla que no se negocia: todo esto, con permiso y acompañamiento de tus papás o de un adulto de confianza.

### Eslogan
> ¡Muy buenas, gente! Bienvenidos a El Precio del Poder.
>
> Aquí el dinero se gana... y el poder se aprende.
>
> ¡Arranca el top!

### #10
> Número diez: lavar carros y motos.
>
> Suena básico, pero funciona. Mucha gente del barrio no tiene tiempo para hacerlo, y prefiere pagarle a alguien de confianza.
>
> Solo necesitas un balde, jabón para carros, toallas de microfibra... y muchas ganas.
>
> Empieza con los vecinos que ya te conocen, haz un trabajo impecable y pídeles que te recomienden.
>
> Un buen tip: ofrece un plan fijo, por ejemplo, un lavado cada semana. Así tienes clientes que vuelven, y no tienes que salir a buscar todos los días.

### #9
> Número nueve: pasear y cuidar mascotas.
>
> Hay dueños que trabajan todo el día, y sus perros necesitan salir. Otros se van de viaje y no tienen con quién dejar a su gato. Si amas los animales, este trabajo casi no se siente como trabajo.
>
> Empieza con las mascotas de familiares y vecinos, sé puntual, y mándales fotos a los dueños durante el paseo. Eso genera confianza.
>
> Eso sí: acepta solo animales que puedas controlar, y nunca vayas solo a la casa de un desconocido.

### #8
> Número ocho: vender postres y snacks.
>
> Brownies, galletas, obleas, salpicón... lo que mejor te quede. Puedes vender en tu cuadra, a los amigos de tu familia, o por pedido en WhatsApp.
>
> La clave está en los números: anota cuánto te cuesta cada ingrediente, calcula cuánto te sale cada porción, y ponle un precio que te deje ganancia. Muchos venden un montón... y ganan casi nada, porque nunca hicieron esa cuenta.
>
> Y si quieres vender en el colegio, pide permiso primero.

### #7
> Número siete: dar clases o tutorías.
>
> Si eres bueno en matemáticas, en inglés o en cualquier materia, hay niños más pequeños que necesitan ayuda con las tareas... y papás dispuestos a pagar por eso.
>
> Y tienes una ventaja enorme: tú viste esos temas hace poco, y sabes explicarlos con palabras que un niño entiende.
>
> Empieza con los hermanos menores de tus amigos, en tu casa o en un lugar seguro, y siempre con un adulto enterado. Si lo haces bien, los papás te recomiendan solos.

### #6
> Número seis: ser el técnico del barrio.
>
> Para ti es normal configurar un celular, instalar WhatsApp, hacer una videollamada o pasar fotos al computador. Para muchos adultos mayores, eso es otro mundo.
>
> Puedes cobrar por enseñarles, por organizar su celular, o por ayudarles a usar sus aplicaciones de forma segura.
>
> Aquí la confianza lo es todo: nunca pidas contraseñas que no necesitas, y si hay pagos de por medio, que la persona siempre esté presente.

### #5
> Número cinco: vender lo que ya no usas... y después, revender.
>
> Revisa tu cuarto: ropa que ya no te queda, videojuegos, libros, accesorios. Todo eso puede ser dinero.
>
> Tómale buenas fotos, con luz natural, y publícalo con ayuda de un adulto en grupos de venta o en Marketplace.
>
> Cuando le cojas el ritmo, puedes pasar al siguiente nivel: comprar ropa de segunda en buen estado, lavarla, presentarla bien, y venderla un poco más cara. Eso se llama agregar valor.

### #4
> Número cuatro: hacer y vender cosas con tus manos.
>
> Pulseras, aretes, llaveros, tarjetas, velas, stickers, ropa personalizada. Lo hecho a mano tiene algo que lo hecho en fábrica no tiene: es único. Y si lo personalizas con el nombre de alguien o con un diseño especial, la gente paga más.
>
> Las fechas especiales son tu temporada alta: Amor y Amistad, Navidad, el Día de la Madre. Prepárate con tiempo, y muestra tus productos en redes.

### #3
> Número tres: editar videos y hacer diseños.
>
> Hoy todos los negocios necesitan contenido: la peluquería, la panadería, el gimnasio del barrio. Y tú puedes hacerlo con herramientas gratis, como CapCut o Canva, desde tu celular.
>
> Empieza armando un portafolio: edita tres o cuatro videos de ejemplo, aunque sean con tus propias fotos. Luego ofrécele a un negocio cercano hacerle un video de prueba. Si les gusta, ya tienes tu primer cliente.
>
> Y cada trabajo que haces es una habilidad que vale más con el tiempo.

### #2
> Número dos: manejar las redes sociales de negocios pequeños.
>
> Muchos dueños de negocio saben vender en su local, pero no tienen tiempo, ni idea, de cómo publicar en Instagram o en TikTok. Tú sí.
>
> Puedes ofrecer un plan mensual: tomar fotos, escribir las publicaciones, responder mensajes, y mostrarles cuánta gente vio su contenido. Esto ya no es un trabajo de una tarde: es un servicio que se paga cada mes.
>
> Eso sí: todo acuerdo de dinero, con un adulto presente y por escrito.

### #1
> Y el número uno: crear tu propio contenido.
>
> Un canal de YouTube, una cuenta de TikTok, un blog o un pódcast sobre algo que te apasione: videojuegos, música, dibujo, deportes, tips de estudio.
>
> ¿Por qué es el número uno? Porque es lo único de esta lista que puede seguir trabajando por ti mientras duermes. Un video que haces hoy lo pueden ver miles de personas dentro de dos años.
>
> Pero ojo: no da plata rápido. Construir una audiencia puede tomar meses, o años. Y plataformas como YouTube exigen tener dieciocho años para recibir pagos, así que la cuenta de cobro la debe manejar tu papá, tu mamá o tu tutor legal.
>
> Lo bueno es que todo lo que aprendes en el camino, grabar, editar, hablar en cámara, vender una idea, te sirve para cualquier cosa que hagas después.

### 5 reglas de oro
> Antes de que salgas a ganar plata, cinco reglas de oro.
>
> Uno: todo, con permiso y acompañamiento de un adulto. En Colombia, por ejemplo, para trabajar con un empleador la edad mínima es quince años, y entre los quince y los diecisiete se necesita una autorización del inspector de trabajo.
>
> Dos: tu seguridad primero. Nunca vayas solo a la casa de un desconocido, y no compartas tu dirección ni tus datos con cualquiera.
>
> Tres: el colegio no se negocia. Tus estudios son tu mejor inversión.
>
> Cuatro: ahorra una parte de todo lo que ganes, aunque sea poquito.
>
> Y cinco: huye del dinero fácil. Apuestas, pirámides, o gurús que prometen hacerte rico en una semana... solo te van a quitar lo que tanto te costó ganar.

### Cierre
> Ahora dime tú en los comentarios: ¿cuál de estas diez vas a probar primero? Y si ya ganas tu propia plata, cuéntanos cómo lo haces, para que otros se inspiren.
>
> Si este video te sirvió, compártelo con ese amigo que siempre anda sin plata, suscríbete y activa la campanita.
>
> Esto fue El Precio del Poder. Recuerda: el dinero se gana... y el poder se aprende. ¡Nos vemos!
