import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C} from '../estilo';
import type {Escena} from '../tipos';
import {Fondo} from './Fondo';

// Frase clave palabra a palabra. Las palabras entre *asteriscos* van en dorado.
export const Texto: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const fuente = e.titulo ?? e.texto;
  let resaltar = false;
  const piezas = fuente.split(/\s+/).filter(Boolean).map((p) => {
    const abre = p.startsWith('*');
    if (abre) resaltar = true;
    const limpio = p.replace(/\*/g, '');
    const item = {t: limpio, oro: resaltar};
    if (p.endsWith('*') || p.replace(/[.,;:!?…]+$/, '').endsWith('*')) resaltar = false;
    return item;
  });
  const tam = vertical ? (piezas.length > 8 ? 84 : 104) : piezas.length > 10 ? 80 : 96;

  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{justifyContent: 'center', padding: vertical ? '0 80px' : '0 180px'}}>
        <div style={{display: 'flex', flexWrap: 'wrap', gap: `${tam * 0.12}px ${tam * 0.26}px`,
          justifyContent: 'center', textAlign: 'center'}}>
          {piezas.map((p, i) => {
            const s = spring({frame: f - i * 3, fps, config: {damping: 16, stiffness: 160}});
            return (
              <span key={i} style={{color: p.oro ? C.acento : C.texto, fontSize: tam, fontWeight: 800, lineHeight: 1.05,
                opacity: s, transform: `translateY(${(1 - s) * 40}px)`, display: 'inline-block'}}>
                {p.t}
              </span>
            );
          })}
        </div>
        {e.subtitulo ? (
          <div style={{color: C.suave, fontSize: vertical ? 42 : 38, textAlign: 'center', marginTop: 34,
            opacity: spring({frame: f - piezas.length * 3 - 4, fps, config: {damping: 200}})}}>
            {e.subtitulo}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
