# Gastos hormiga

Video vertical de 65 segundos (1080x1920, 30 fps) sobre los gastos hormiga: el café diario, el domicilio, el snack y la suscripción olvidada.
Está hecho con fotos reales con licencia libre, voz de ElevenLabs, y música y efectos sintetizados con código.
No usa imágenes ni música generadas con IA.

- Video final: [`exports/gastos-hormiga.mp4`](exports/gastos-hormiga.mp4)

## Por qué este tema

El gasto pequeño e impulsivo es tema recurrente en finanzas personales para jóvenes en 2026: el "loud budgeting" y los retos "no-buy" en TikTok, y notas de prensa sobre el aumento del gasto impulsivo entre menores de 30.
El gancho es una cuenta que cualquiera puede hacer: US$2 al día son US$730 al año.

## Guion

> ¿Sabías que tu cafecito de todos los días te puede costar más de diez mil dólares?
> No es broma. Se llaman gastos hormiga. Pequeñitos, invisibles... y te están vaciando la cuenta.
> Haz la cuenta: un café de dos dólares al día son setecientos treinta dólares al año. Súmale el domicilio del viernes, el snack de la tienda, y esa suscripción que ni usas.
> Y ojo: el gasto impulsivo está creciendo entre los jóvenes.
> Ahora viene lo bueno. Si esos setecientos treinta dólares los inviertes cada año al ocho por ciento... ¡en diez años tienes más de diez mil quinientos dólares!
> ¿Cómo frenarlo? Tres trucos.
> Uno: la regla de las veinticuatro horas. Antes de comprar algo que no planeaste, espera un día.
> Dos: revisa tus suscripciones hoy. La que no usaste este mes, ¡cancélala!
> Tres: anota cada gasto chiquito durante una semana. Te vas a sorprender.
> No se trata de dejar de vivir. Se trata de que tu plata trabaje para ti.
> Mándale esto al amigo que siempre dice: "es solo un cafecito".

La cifra: 730 × ((1,08¹⁰ − 1) / 0,08) = US$10.575, un aporte de US$730 al final de cada año al 8 % anual compuesto durante 10 años.
El video lo muestra como ejemplo, con la nota "Rendimiento no garantizado. No es asesoría financiera."

## Cómo está hecho

| Parte | Origen |
|---|---|
| Voz | ElevenLabs, modelo `eleven_v4`, voz "Mauricio Viral" (latina, enérgica). Tiempos por palabra con ElevenLabs Scribe en `audio/words.json`. |
| Fotos | 30 fotos reales de StockSnap (CC0) y Wikimedia Commons (CC BY / CC BY-SA), encontradas con Openverse. Lista abajo. |
| Música | Beat funk/hip-hop a 100 bpm sintetizado en `tools/audio.py`: bombo, caja, hi-hats, shaker, bajo y piano eléctrico, con swing y pequeñas variaciones humanas. Se corta, se filtra y redobla siguiendo la narración. |
| Efectos | Whoosh, pop, obturador de cámara, golpe grave, caja registradora, tic de contador y sello, también sintetizados. |
| Edición | `tools/render.py`: cortes sobre las palabras, zoom de entrada en cada corte, cámara en mano, tarjetas tipo foto impresa, barridos con desenfoque de movimiento, flashes, temblor y separación de color en los golpes, subtítulos palabra por palabra, contadores animados, gráfica de crecimiento, sello "CANCELADA", grano de película, viñeta y barra de progreso. |
| Mezcla | La música baja sola cuando habla la voz (sidechain) y el total queda a -14 LUFS. |

`tools/timeline.py` contiene la lista de planos, gráficos y golpes; cada tiempo sale de `audio/words.json`.

## Volver a generar

Necesita Python 3 con Pillow, numpy y scipy, y ffmpeg en el PATH.

```bash
python3 tools/audio.py
```

```bash
python3 tools/render.py
```

```bash
ffmpeg -y -i build/video.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 21 -maxrate 8M -bufsize 16M -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart exports/gastos-hormiga.mp4
```

`python3 tools/render.py --frames 4.2 31.5` guarda cuadros sueltos en `build/` para revisar sin renderizar todo.

## Créditos para la descripción del video

Las fotos CC BY y CC BY-SA piden atribución. Pega esto en la descripción al publicar:

```
Fotos: StockSnap (CC0) y Wikimedia Commons.
- "Hundred dollar bill 03" de Revisorweb (CC BY-SA 3.0, Wikimedia Commons)
- "Ant on leaf" de Luke Elstad (CC BY 2.5, Wikimedia Commons)
- "Safari ants" de Mehmet Karatay (CC BY-SA 3.0, Wikimedia Commons)
- "Paying with a Credit Card (28886645201)" de Hloom Templates (CC BY 2.0, Wikimedia Commons)
- "Food delivery driver in Qingdao" de Benlisquare (CC BY-SA 4.0, Wikimedia Commons)
- "Bamba snack" de Nsaum75 (CC BY-SA 3.0, Wikimedia Commons)
- "Netflix Streaming (40845736773)" de Ajay Suresh from New York, NY, USA (CC BY 2.0, Wikimedia Commons)
- "Hand Putting Deposit Into Piggy Bank (5737295175)" de Ken Teegardin from Boulder, Boulder (CC BY-SA 2.0, Wikimedia Commons)
- "80 1 dollar bills in a homemade banknote strap" de BrayLockBoy (CC BY-SA 4.0, Wikimedia Commons)
Voz: ElevenLabs.
```

## Fotos

| Archivo | Título | Autor | Licencia | Enlace |
|---|---|---|---|---|
| `latte_art.jpg` | Latte Art | Burst | CC0 | [fuente](https://stocksnap.io/photo/latte-art-ERHOTDPNMV) |
| `hundred.jpg` | Hundred dollar bill 03 | Revisorweb | CC BY-SA 3.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=4529960) |
| `iced_girl.jpg` | People Girl | Seth Doyle | CC0 | [fuente](https://stocksnap.io/photo/people-girl-7YPU6791WW) |
| `ant_leaf.jpg` | Ant on leaf | Luke Elstad | CC BY 2.5 | [fuente](https://commons.wikimedia.org/w/index.php?curid=1349504) |
| `ant1.jpg` | Ant Insect | Mikhail Vasilyev | CC0 | [fuente](https://stocksnap.io/photo/ant-insect-RB34J9O17D) |
| `safari_ants.jpg` | Safari ants | Mehmet Karatay | CC BY-SA 3.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=2179109) |
| `card_pay.jpg` | Paying with a Credit Card (28886645201) | Hloom Templates | CC BY 2.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=67030803) |
| `barista.jpg` | Barista Coffee | Malidate Van | CC0 | [fuente](https://stocksnap.io/photo/barista-coffee-ZCW5B7GXFY) |
| `barista_latte.jpg` | Barista Latte | Burst | CC0 | [fuente](https://stocksnap.io/photo/barista-latte-DTKOOFPC06) |
| `calc2.jpg` | Accounting Finance | Wilfred Iven | CC0 | [fuente](https://stocksnap.io/photo/accounting-finance-JONMP7TPGK) |
| `delivery.jpg` | Food delivery driver in Qingdao | Benlisquare | CC BY-SA 4.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=167042710) |
| `bamba.jpg` | Bamba snack | Nsaum75 | CC BY-SA 3.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=7697006) |
| `netflix_stream.jpg` | Netflix Streaming (40845736773) | Ajay Suresh from New York, NY, USA | CC BY 2.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=78831943) |
| `mall_girl.jpg` | Shopping Mall | Burst | CC0 | [fuente](https://stocksnap.io/photo/shopping-mall-YGQT3KFPII) |
| `woman_phone2.jpg` | Woman Phone | Kristin Hardwick | CC0 | [fuente](https://stocksnap.io/photo/woman-phone-HOT99SLGGV) |
| `piggy_hand.jpg` | Hand Putting Deposit Into Piggy Bank (5737295175) | Ken Teegardin from Boulder, Boulder | CC BY-SA 2.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=38889562) |
| `strap.jpg` | 80 1 dollar bills in a homemade banknote strap | BrayLockBoy | CC BY-SA 4.0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=114302975) |
| `money_coins.jpg` | Money Coins | Negative Space | CC0 | [fuente](https://stocksnap.io/photo/money-coins-SDM03P88BO) |
| `piggy_cc0.jpg` | Piggy-bank-968302 | stevepb | CC0 | [fuente](https://commons.wikimedia.org/w/index.php?curid=58572647) |
| `coins_euro.jpg` | Euro Coin | Michal Jarmoluk | CC0 | [fuente](https://stocksnap.io/photo/euro-coin-KSSK8FBJ8E) |
| `hourglass.jpg` | Hourglass Arts | Daria Nepriakhina | CC0 | [fuente](https://stocksnap.io/photo/hourglass-arts-E1C68E9513) |
| `woman_phone.jpg` | Woman Phone | Studio 7042 | CC0 | [fuente](https://stocksnap.io/photo/woman-phone-20NNP2BSL6) |
| `apps.jpg` | Apps Smartphone | Mateusz Dach | CC0 | [fuente](https://stocksnap.io/photo/apps-smartphone-XLCKX6HJKD) |
| `remote.jpg` | Remote Control | 50Fish | CC0 | [fuente](https://stocksnap.io/photo/remote-control-XXNJAOGTCN) |
| `journal.jpg` | Journal Notepad | Cathryn Lavery | CC0 | [fuente](https://stocksnap.io/photo/journal-notepad-DPKNIIN5X3) |
| `notebook2.jpg` | Notebook Notepad | Wilfred Iven | CC0 | [fuente](https://stocksnap.io/photo/notebook-notepad-H5Y00D4OFT) |
| `friends1.jpg` | Group Friends | Helena Lopes | CC0 | [fuente](https://stocksnap.io/photo/group-friends-YBGQFVYDDC) |
| `cash2.jpg` | Money Cash | Tim Sullivan | CC0 | [fuente](https://stocksnap.io/photo/money-cash-RBE72WU7PK) |
| `friends3.jpg` | Friends Fun | Matt Moloney | CC0 | [fuente](https://stocksnap.io/photo/friends-fun-TK55STNQN8) |
| `coffee_cup.jpg` | Coffee Cup | Senior Living | CC0 | [fuente](https://stocksnap.io/photo/coffee-cup-KBPLPXZBRB) |

`photos/credits.json` guarda los mismos datos.
