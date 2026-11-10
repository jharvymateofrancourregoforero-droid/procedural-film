# Configuración del entorno en la nube (para explicar al usuario)

Se configura en claude.ai/code → selector de entorno → editar entorno.

## Acceso a red
Elige **Custom**, marca incluir los dominios predeterminados y agrega uno por línea:
```
api.elevenlabs.io
api.pexels.com
images.pexels.com
videos.pexels.com
pixabay.com
cdn.pixabay.com
www.googleapis.com
www.datos.gov.co
api.coingecko.com
*.yahoo.com
remotion.media
www.remotion.dev
```
(Opción simple: **Full**.) `remotion.media` y `www.remotion.dev` sirven para que Remotion descargue su navegador al renderizar.

## Variables de entorno (formato .env)
```
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
PEXELS_API_KEY=...
PIXABAY_API_KEY=...
YOUTUBE_API_KEY=...
```
Cualquiera con acceso al entorno puede leerlas. En planes Pro/Max es más seguro guardar ElevenLabs y Pexels como **Credenciales de API** del entorno:
- ElevenLabs: host `api.elevenlabs.io`, encabezado `xi-api-key`, sin prefijo.
- Pexels: host `api.pexels.com`, encabezado `Authorization`, sin prefijo.
Y en las variables escribe `ELEVENLABS_API_KEY=proxy` y `PEXELS_API_KEY=proxy`. Pixabay y YouTube van en la URL, así que deben ir como variables normales.

## Script de configuración (opcional, acelera las sesiones)
```bash
#!/bin/bash
apt update && apt install -y ffmpeg
```
Sin esto los scripts usan un ffmpeg portátil (imageio-ffmpeg) que se instala solo desde PyPI.

## Errores típicos
| Mensaje | Solución |
|---|---|
| `Falta ELEVENLABS_API_KEY` | Agregar la variable o la credencial |
| `Sin conexión con api.elevenlabs.io` / `403 Forbidden` del proxy | Agregar el dominio en Custom |
| Falla descargando Chrome Headless Shell | Agregar `remotion.media` y `www.remotion.dev` |
| ElevenLabs 401 | Clave incorrecta o credencial mal configurada |
