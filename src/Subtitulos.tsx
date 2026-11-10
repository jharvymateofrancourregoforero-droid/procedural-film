import React, {useMemo} from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, contorno, fuerte, zona} from './estilo';
import type {Palabra} from './tipos';

const NUMEROS = /^(\d|cero|uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|veinte|veinti|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien|ciento|doscient|trescient|cuatrocient|quinient|seiscient|setecient|ochocient|novecient|mil|millón|millones|billón|por ciento|%|\$)/i;

const limpiar = (w: string) => w.replace(/^[¿¡"«(…]+|[,.;:"»)…]+$/g, '');
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
      (actual.length === 2 && limpiar(p.w).length > 8);
    if (corte) {
      grupos.push({palabras: actual, s: actual[0].s, e: actual[actual.length - 1].e});
      actual = [];
    }
  });
  return grupos;
};

// Subtítulos estilo redes: mayúsculas gruesas con contorno; la palabra que suena salta en amarillo.
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

  const gi = grupos.findIndex((x, i) => t >= x.s - 0.05 && t < Math.min(x.e + 0.3, grupos[i + 1]?.s ?? Infinity));
  if (gi < 0 || ocultar.some(([a, b]) => t >= a && t < b)) return null;
  const g = grupos[gi];
  const z = zona(vertical);
  const entra = spring({frame: f - Math.round(g.s * fps), fps, config: {damping: 12, stiffness: 260}, durationInFrames: 8});
  const tam = vertical ? 92 : 80;

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{
        position: 'absolute', left: z.lados, right: z.lados,
        top: vertical ? height * 0.68 : undefined, bottom: vertical ? undefined : z.abajo + 70,
        display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: `0 ${tam * 0.42}px`,
        transform: `scale(${0.85 + 0.15 * entra}) translateY(${(1 - entra) * 18}px)`,
      }}>
        {g.palabras.map((p, i) => {
          const activa = t >= p.s && t < p.e + 0.05;
          const b = base(p.w);
          const especial = sv.has(b) ? C.positivo : sr.has(b) ? C.negativo : NUMEROS.test(b) ? C.positivo : null;
          const pop = spring({frame: f - Math.round(p.s * fps), fps, config: {damping: 10, stiffness: 300}, durationInFrames: 7});
          return (
            <span key={i} style={{
              fontFamily: fuerte, fontWeight: 900, fontSize: tam, lineHeight: 1.12, textTransform: 'uppercase',
              color: activa ? C.acento : especial ?? C.texto,
              opacity: t >= p.s - 0.02 ? 1 : 0.55,
              transform: `scale(${activa ? 1 + 0.14 * pop : 1}) rotate(${activa ? (i % 2 ? 1.5 : -1.5) * pop : 0}deg)`,
              display: 'inline-block', ...contorno(vertical ? 14 : 12),
              textShadow: '0 8px 22px rgba(0,0,0,0.7)',
            }}>
              {limpiar(p.w)}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
