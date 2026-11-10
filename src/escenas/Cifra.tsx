import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, colorTono, numero} from '../estilo';
import type {Escena} from '../tipos';
import {Fondo} from './Fondo';

// Contador animado: sube de 0 al valor con easeOutCubic.
export const Cifra: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const valor = e.valor ?? 0;
  const dur = Math.round(fps * 1.2);
  const actual = interpolate(f, [3, 3 + dur], [0, valor], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });
  const entra = spring({frame: f, fps, config: {damping: 200}});
  const golpe = spring({frame: f - 3 - dur, fps, config: {damping: 12, stiffness: 180}});
  const color = colorTono(e.tono);

  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: vertical ? '80px 80px 220px' : 120, gap: 18}}>
        {e.titulo ? (
          <div style={{color: C.suave, fontSize: vertical ? 50 : 46, fontWeight: 600, textAlign: 'center', opacity: entra}}>
            {e.titulo}
          </div>
        ) : null}
        <div
          style={{
            color, fontWeight: 800, fontSize: vertical ? 190 : 210, lineHeight: 1,
            fontVariantNumeric: 'tabular-nums', letterSpacing: -4, whiteSpace: 'nowrap',
            transform: `scale(${(0.9 + 0.1 * entra) * (1 + 0.04 * golpe * (1 - golpe))})`,
            textShadow: `0 0 60px ${color}40`,
          }}
        >
          {e.prefijo ?? ''}
          {numero(actual, e.decimales ?? 0)}
          {e.sufijo ?? ''}
        </div>
        {e.subtitulo ? (
          <div style={{color: C.texto, fontSize: vertical ? 42 : 40, textAlign: 'center', opacity: golpe > 0.1 ? 1 : 0}}>
            {e.subtitulo}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
