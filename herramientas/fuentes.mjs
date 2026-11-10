// Copia la fuente Inter (paquete npm @fontsource/inter) a public/fuentes para renderizar sin internet.
import {copyFileSync, existsSync, mkdirSync} from 'node:fs';

const origen = 'node_modules/@fontsource/inter/files';
mkdirSync('public/fuentes', {recursive: true});
for (const peso of ['400', '600', '800']) {
  const archivo = `inter-latin-${peso}-normal.woff2`;
  if (existsSync(`${origen}/${archivo}`) && !existsSync(`public/fuentes/${archivo}`)) {
    copyFileSync(`${origen}/${archivo}`, `public/fuentes/${archivo}`);
  }
}
