import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, fuerte} from '../estilo';
import type {Escena} from '../tipos';

// Intro tipo "logo": rayos que giran, título que golpea en dos tiempos con separación RGB y subtítulo espaciado.
export const Intro: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const palabras = (e.titulo ?? '').split(/\s+/).filter(Boolean);
  const ultima = palabras.pop() ?? '';
  const p1 = spring({frame: f, fps, config: {damping: 10, stiffness: 240}});
  const p2 = spring({frame: f - 7, fps, config: {damping: 9, stiffness: 260}});
  const ps = spring({frame: f - 16, fps, config: {damping: 200}});
  const glitch = (d: number) => {
    const k = interpolate(f - d, [0, 8], [14, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return k > 0.5 ? `${k}px 0 #ff1f4b, ${-k}px 0 #00e5ff` : '0 14px 50px rgba(0,0,0,0.6)';
  };
  const tam = vertical ? 210 : 260;

  return (
    <AbsoluteFill style={{backgroundColor: C.fondo, overflow: 'hidden'}}>
      <AbsoluteFill style={{
        background: `repeating-conic-gradient(from ${f * 0.8}deg at 50% 50%, rgba(255,212,0,0.10) 0deg 8deg, transparent 8deg 22deg)`,
        transform: 'scale(2)',
      }} />
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 50%, rgba(255,212,0,0.28), rgba(7,8,11,0.92) 55%)'}} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', gap: 10}}>
        <div style={{display: 'flex', flexDirection: vertical ? 'column' : 'row', alignItems: 'center', gap: vertical ? 0 : 40}}>
          <div style={{fontFamily: display, fontSize: tam, color: C.texto, lineHeight: 1, textTransform: 'uppercase',
            transform: `scale(${3 - 2 * Math.min(1, p1)})`, opacity: Math.min(1, p1 * 2), textShadow: glitch(0)}}>
            {palabras.join(' ')}
          </div>
          <div style={{fontFamily: display, fontSize: tam, color: C.acento, lineHeight: 1,
            transform: `scale(${3 - 2 * Math.min(1, p2)}) rotate(${(1 - Math.min(1, p2)) * -8}deg)`,
            opacity: Math.min(1, p2 * 2), textShadow: glitch(7)}}>{ultima}</div>
        </div>
        {e.subtitulo ? (
          <div style={{fontFamily: fuerte, fontWeight: 800, fontSize: vertical ? 40 : 46, color: C.texto,
            letterSpacing: interpolate(ps, [0, 1], [30, 10]), textTransform: 'uppercase', opacity: ps}}>
            {e.subtitulo}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
