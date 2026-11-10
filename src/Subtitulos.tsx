import React, {useMemo} from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, zona} from './estilo';
import type {Palabra} from './tipos';

const NUMEROS = /^(\d|cero|uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|veinte|veinti|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien|ciento|doscient|trescient|cuatrocient|quinient|seiscient|setecient|ochocient|novecient|mil|millón|millones|billón|por ciento|%|\$)/i;

const limpiar = (w: string) => w.replace(/^[¿¡"«(]+|[,.;:"»)]+$/g, '');
const base = (w: string) => limpiar(w).replace(/[?!¿¡]/g, '').toLowerCase();

type Grupo = {palabras: Palabra[]; s: number; e: number};

// Agrupa 1–3 palabras, cortando en puntuación o en pausas.
const agrupar = (palabras: Palabra[]): Grupo[] => {
  const grupos: Grupo[] = [];
  let actual: Palabra[] = [];
  palabras.forEach((p, i) => {
    actual.push(p);
    const sig = palabras[i + 1];
    const corte = actual.length >= 3 || /[.,;:?!…]$/.test(p.w) || !sig || sig.s - p.e > 0.3 ||
      (actual.length === 2 && limpiar(p.w).length > 9);
    if (corte) {
      grupos.push({palabras: actual, s: actual[0].s, e: actual[actual.length - 1].e});
      actual = [];
    }
  });
  return grupos;
};

export const Subtitulos: React.FC<{palabras: Palabra[]; verde?: string[]; rojo?: string[]; ocultar?: [number, number][]}> = ({
  palabras, verde = [], rojo = [], ocultar = [],
}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const t = f / fps;
  const grupos = useMemo(() => agrupar(palabras), [palabras]);
  const sv = useMemo(() => new Set(verde.map((x) => x.toLowerCase())), [verde]);
  const sr = useMemo(() => new Set(rojo.map((x) => x.toLowerCase())), [rojo]);

  const g = grupos.find((x, i) => t >= x.s - 0.05 && t < Math.min(x.e + 0.35, grupos[i + 1]?.s ?? Infinity));
  // No duplica el texto en escenas `texto`, donde la frase ya está en pantalla.
  if (!g || ocultar.some(([a, b]) => t >= a && t < b)) return null;
  const z = zona(vertical);

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div
        style={{
          position: 'absolute', left: z.lados, right: z.lados,
          top: vertical ? height * 0.7 : undefined, bottom: vertical ? undefined : z.abajo + 40,
          display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: '0 30px',
        }}
      >
        {g.palabras.map((p, i) => {
          const activa = t >= p.s && t < p.e + 0.05;
          const pasada = t >= p.e;
          const b = base(p.w);
          const color = sv.has(b) ? C.positivo : sr.has(b) ? C.negativo : NUMEROS.test(b) ? C.acento : activa ? C.acento : C.texto;
          const pop = spring({frame: f - Math.round(p.s * fps), fps, config: {damping: 14, stiffness: 220}, durationInFrames: 8});
          return (
            <span
              key={i}
              style={{
                color: activa || pasada || sv.has(b) || sr.has(b) || NUMEROS.test(b) ? color : C.texto,
                opacity: t >= p.s - 0.02 ? 1 : 0.35,
                fontSize: vertical ? 82 : 66, fontWeight: 800, lineHeight: 1.15,
                transform: `scale(${activa ? 1 + 0.07 * pop : 1})`, display: 'inline-block',
                WebkitTextStroke: `${vertical ? 10 : 8}px rgba(0,0,0,0.85)`, paintOrder: 'stroke fill',
                textShadow: '0 6px 18px rgba(0,0,0,0.55)',
              }}
            >
              {limpiar(p.w)}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
