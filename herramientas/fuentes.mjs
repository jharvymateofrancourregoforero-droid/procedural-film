// Copia las fuentes (paquetes npm @fontsource/*) a public/fuentes para renderizar sin internet.
// Inter: textos pequeños · Anton: titulares · Montserrat: subtítulos y etiquetas.
import {copyFileSync, existsSync, mkdirSync} from 'node:fs';

const fuentes = [
  ['inter', ['400', '600', '800']],
  ['anton', ['400']],
  ['montserrat', ['700', '800', '900']],
];
mkdirSync('public/fuentes', {recursive: true});
for (const [familia, pesos] of fuentes) {
  const origen = `node_modules/@fontsource/${familia}/files`;
  for (const peso of pesos) {
    const archivo = `${familia}-latin-${peso}-normal.woff2`;
    if (existsSync(`${origen}/${archivo}`) && !existsSync(`public/fuentes/${archivo}`)) {
      copyFileSync(`${origen}/${archivo}`, `public/fuentes/${archivo}`);
    }
  }
}
