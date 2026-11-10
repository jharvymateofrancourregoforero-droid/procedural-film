import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';
import type {Tono} from './tipos';

// Fuente Inter incluida en public/fuentes: funciona sin internet.
export const fontFamily = 'Inter';
for (const peso of ['400', '600', '800']) {
  loadFont({family: fontFamily, url: staticFile(`fuentes/inter-latin-${peso}-normal.woff2`), weight: peso});
}

export const C = {
  fondo: '#0B1220',
  tarjeta: '#162033',
  borde: 'rgba(255,255,255,0.08)',
  texto: '#F5F7FA',
  suave: '#A7B0C0',
  positivo: '#22C55E',
  negativo: '#EF4444',
  acento: '#E0B04B',
  neutro: '#64748B',
};

export const colorTono = (t?: Tono) =>
  t === 'positivo' ? C.positivo : t === 'negativo' ? C.negativo : t === 'neutro' ? C.texto : C.acento;

export const numero = (v: number, dec = 0) =>
  new Intl.NumberFormat('es-CO', {minimumFractionDigits: dec, maximumFractionDigits: dec}).format(v);

// Zona segura de Shorts: arriba 250 px y abajo 350 px ocupados por la interfaz.
export const zona = (vertical: boolean) =>
  vertical ? {arriba: 260, abajo: 380, lados: 70} : {arriba: 70, abajo: 90, lados: 110};
