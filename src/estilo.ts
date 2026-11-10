import type {CSSProperties} from 'react';
import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';
import type {Tono} from './tipos';

// Fuentes incluidas en public/fuentes: funcionan sin internet.
// Anton = titulares (condensada y gruesa) · Montserrat = subtítulos y etiquetas · Inter = textos pequeños.
export const fontFamily = 'Inter';
export const display = 'Anton';
export const fuerte = 'Montserrat';

const cargar = (family: string, archivo: string, weight: string) =>
  loadFont({family, url: staticFile(`fuentes/${archivo}`), weight});
for (const p of ['400', '600', '800']) cargar('Inter', `inter-latin-${p}-normal.woff2`, p);
cargar('Anton', 'anton-latin-400-normal.woff2', '400');
for (const p of ['700', '800', '900']) cargar('Montserrat', `montserrat-latin-${p}-normal.woff2`, p);

// Paleta de alto contraste: negro, amarillo, verde dinero y rojo alerta.
export const C = {
  fondo: '#07080B',
  tarjeta: '#11141B',
  borde: 'rgba(255,255,255,0.10)',
  texto: '#FFFFFF',
  suave: '#A3ACBA',
  positivo: '#00E676',
  negativo: '#FF3B3B',
  acento: '#FFD400',
  neutro: '#5B6575',
};

export const colorTono = (t?: Tono) =>
  t === 'positivo' ? C.positivo : t === 'negativo' ? C.negativo : t === 'neutro' ? C.texto : C.acento;

export const numero = (v: number, dec = 0) =>
  new Intl.NumberFormat('es-CO', {minimumFractionDigits: dec, maximumFractionDigits: dec}).format(v);

// Contorno negro grueso para que el texto se lea sobre cualquier imagen.
export const contorno = (px: number): CSSProperties => ({
  WebkitTextStroke: `${px}px #000`,
  paintOrder: 'stroke fill',
});

// Zona segura de Shorts: arriba 250 px y abajo 350 px ocupados por la interfaz.
export const zona = (vertical: boolean) =>
  vertical ? {arriba: 260, abajo: 380, lados: 70} : {arriba: 70, abajo: 90, lados: 110};
