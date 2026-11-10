import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, fuerte} from '../estilo';
import type {Escena} from '../tipos';
import {Fondo} from './Fondo';

// Tarjeta de capítulo: número gigante en contorno, etiqueta amarilla ("CIFRA #1") y título que cae de golpe.
export const Capitulo: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = height > width;
  const etiqueta = e.etiqueta ?? (e.numero ? `CIFRA #${e.numero}` : '');
  const pe = spring({frame: f, fps, config: {damping: 200}, durationInFrames: 10});
  const pt = spring({frame: f - 4, fps, config: {damping: 11, stiffness: 220}});
  const ps = spring({frame: f - 12, fps, config: {damping: 200}});
  const deriva = interpolate(f, [0, durationInFrames], [0, -80]);
  const linea = interpolate(f, [0, 12], [0, 100], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill>
      <Fondo />
      {e.numero ? (
        <div style={{position: 'absolute', right: vertical ? -40 : 60, top: vertical ? 120 : -120, fontFamily: display,
          fontSize: vertical ? 900 : 1150, lineHeight: 1, color: 'transparent', WebkitTextStroke: `5px ${C.acento}55`,
          transform: `translateX(${deriva}px)`, opacity: pe}}>{e.numero}</div>
      ) : null}
      <AbsoluteFill style={{justifyContent: 'center', padding: vertical ? '0 70px' : '0 160px', gap: 26}}>
        <div style={{width: `${linea}%`, height: 6, background: C.acento}} />
        {etiqueta ? (
          <div style={{alignSelf: 'flex-start', background: C.acento, color: '#000', fontFamily: fuerte, fontWeight: 900,
            fontSize: vertical ? 44 : 44, letterSpacing: 4, padding: '8px 22px', transform: `scaleX(${pe})`,
            transformOrigin: 'left center'}}>{etiqueta}</div>
        ) : null}
        <div style={{color: C.texto, fontFamily: display, fontSize: vertical ? 150 : 200, lineHeight: 0.98,
          textTransform: 'uppercase', opacity: Math.min(1, pt * 2), filter: `blur(${(1 - Math.min(1, pt)) * 12}px)`,
          transform: `scale(${2 - Math.min(1, pt)})`, transformOrigin: 'left center',
          textShadow: '0 12px 40px rgba(0,0,0,0.6)'}}>{e.titulo}</div>
        {e.subtitulo ? (
          <div style={{color: C.acento, fontFamily: fuerte, fontWeight: 900, fontSize: vertical ? 56 : 60,
            textTransform: 'uppercase', opacity: ps, transform: `translateY(${(1 - ps) * 30}px)`}}>{e.subtitulo}</div>
        ) : null}
        <div style={{width: `${linea * 0.6}%`, height: 6, background: C.texto, opacity: 0.85}} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
