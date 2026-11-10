import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, colorTono, numero} from '../estilo';
import type {Escena} from '../tipos';
import {Fondo} from './Fondo';

// Línea que se dibuja de izquierda a derecha; color según sube (verde) o baja (rojo) si no hay tono.
export const Linea: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const datos = (e.datos ?? []).slice(0, 24);
  if (datos.length < 2) return <Fondo src={e.fondo} />;

  const W = vertical ? 940 : 1500;
  const H = vertical ? 620 : 560;
  const pad = 30;
  const vals = datos.map((d) => d.valor);
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const rango = max - min || 1;
  const pts = datos.map((d, i) => ({
    x: pad + (i / (datos.length - 1)) * (W - pad * 2),
    y: pad + (1 - (d.valor - min) / rango) * (H - pad * 2),
  }));
  const camino = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
  const largo = pts.reduce((acc, p, i) => (i === 0 ? 0 : acc + Math.hypot(p.x - pts[i - 1].x, p.y - pts[i - 1].y)), 0);

  const progreso = interpolate(f, [4, 4 + fps * 1.1], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });
  const color = e.tono ? colorTono(e.tono) : vals[vals.length - 1] >= vals[0] ? C.positivo : C.negativo;
  const ultimo = pts[pts.length - 1];
  const fin = spring({frame: f - 4 - Math.round(fps * 1.1), fps, config: {damping: 14}});
  const entra = spring({frame: f, fps, config: {damping: 200}});

  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', gap: 30, paddingBottom: vertical ? 300 : 0}}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', width: W, gap: 20}}>
          <div style={{color: C.texto, fontSize: vertical ? 54 : 52, fontWeight: 800, opacity: entra, lineHeight: 1.1}}>
            {e.titulo ?? ''}
          </div>
          <div style={{color, fontSize: vertical ? 64 : 60, fontWeight: 800, fontVariantNumeric: 'tabular-nums',
            whiteSpace: 'nowrap', opacity: fin, transform: `scale(${0.85 + 0.15 * fin})`, transformOrigin: 'right bottom'}}>
            {e.prefijo ?? ''}{numero(vals[vals.length - 1], e.decimales ?? 0)}{e.sufijo ?? ''}
          </div>
        </div>
        <svg width={W} height={H} style={{overflow: 'visible'}}>
          {[0, 0.5, 1].map((t) => (
            <line key={t} x1={pad} x2={W - pad} y1={pad + t * (H - pad * 2)} y2={pad + t * (H - pad * 2)}
              stroke="rgba(255,255,255,0.08)" strokeWidth={2} />
          ))}
          <path d={camino} fill="none" stroke={color} strokeWidth={10} strokeLinecap="round" strokeLinejoin="round"
            strokeDasharray={largo} strokeDashoffset={largo * (1 - progreso)} />
          <circle cx={ultimo.x} cy={ultimo.y} r={16 * fin} fill={color} />
          <circle cx={ultimo.x} cy={ultimo.y} r={16 + 30 * fin} fill="none" stroke={color} strokeWidth={3}
            opacity={(1 - fin) * 0.8} />
        </svg>
        <div style={{display: 'flex', justifyContent: 'space-between', width: W, color: C.suave,
          fontSize: vertical ? 34 : 30, fontWeight: 600, opacity: entra}}>
          <span>{datos[0].etiqueta}</span>
          <span>{datos[datos.length - 1].etiqueta}</span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
