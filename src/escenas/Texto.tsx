import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, fuerte} from '../estilo';
import type {Escena} from '../tipos';
import {Fondo} from './Fondo';

// Tipografía cinética: cada palabra entra de golpe (escala + desenfoque).
// Las palabras entre *asteriscos* llevan un marcador amarillo que se pinta de izquierda a derecha.
export const Texto: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = height > width;
  const fuente = e.titulo ?? e.texto;
  let resaltar = false;
  const piezas = fuente.split(/\s+/).filter(Boolean).map((p) => {
    if (p.startsWith('*')) resaltar = true;
    const item = {t: p.replace(/\*/g, ''), oro: resaltar};
    if (p.replace(/[.,;:!?…]+$/, '').endsWith('*')) resaltar = false;
    return item;
  });
  const n = piezas.length;
  const tam = vertical ? (n > 7 ? 110 : 140) : n <= 4 ? 190 : n <= 8 ? 150 : 118;
  const empuje = interpolate(f, [0, durationInFrames], [1, 1.06]);

  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{justifyContent: 'center', padding: vertical ? '0 70px' : '0 150px', transform: `scale(${empuje})`}}>
        <div style={{display: 'flex', flexWrap: 'wrap', gap: `${tam * 0.06}px ${tam * 0.22}px`, justifyContent: 'center',
          alignItems: 'center', textAlign: 'center'}}>
          {piezas.map((p, i) => {
            const s = spring({frame: f - i * 2, fps, config: {damping: 13, stiffness: 210}});
            const marca = interpolate(f - i * 2, [5, 11], [0, 100], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
            return (
              <span key={i} style={{
                fontFamily: display, fontSize: tam, lineHeight: 1.08, textTransform: 'uppercase',
                color: p.oro && marca > 50 ? '#000' : C.texto,
                display: 'inline-block', padding: p.oro ? `0 ${tam * 0.12}px` : 0,
                backgroundImage: p.oro ? `linear-gradient(${C.acento}, ${C.acento})` : undefined,
                backgroundRepeat: 'no-repeat', backgroundSize: `${marca}% 88%`, backgroundPosition: 'left center',
                opacity: Math.min(1, s * 2), filter: `blur(${(1 - Math.min(1, s)) * 10}px)`,
                transform: `scale(${1.7 - 0.7 * s}) rotate(${p.oro ? -2 : 0}deg)`,
                textShadow: p.oro ? 'none' : '0 8px 30px rgba(0,0,0,0.6)',
              }}>
                {p.t}
              </span>
            );
          })}
        </div>
        {e.subtitulo ? (
          <div style={{color: C.suave, fontFamily: fuerte, fontWeight: 800, fontSize: vertical ? 42 : 40, textAlign: 'center',
            marginTop: 40, textTransform: 'uppercase', letterSpacing: 3,
            opacity: spring({frame: f - n * 2 - 6, fps, config: {damping: 200}})}}>
            {e.subtitulo}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
