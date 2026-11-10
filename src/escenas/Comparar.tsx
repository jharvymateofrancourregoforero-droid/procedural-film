import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C} from '../estilo';
import type {Escena, Lado} from '../tipos';
import {Fondo} from './Fondo';

const Tarjeta: React.FC<{lado: Lado; color: string; p: number; vertical: boolean}> = ({lado, color, p, vertical}) => (
  <div
    style={{
      flex: 1, background: C.tarjeta, border: `2px solid ${color}55`, borderRadius: 24,
      padding: vertical ? '44px 40px' : '50px 46px', display: 'flex', flexDirection: 'column', gap: 14,
      alignItems: 'center', boxShadow: '0 20px 60px rgba(0,0,0,0.35)',
      opacity: p, transform: `translateY(${(1 - p) * 50}px) scale(${0.94 + 0.06 * p})`,
    }}
  >
    <div style={{color: C.suave, fontSize: vertical ? 42 : 40, fontWeight: 600, textAlign: 'center'}}>{lado.etiqueta}</div>
    <div style={{color, fontSize: vertical ? 104 : 110, fontWeight: 800, fontVariantNumeric: 'tabular-nums',
      whiteSpace: 'nowrap'}}>{lado.valor}</div>
  </div>
);

// A vs. B: dos tarjetas que entran escalonadas con un "VS" en medio.
export const Comparar: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const pa = spring({frame: f - 2, fps, config: {damping: 200}});
  const pb = spring({frame: f - 10, fps, config: {damping: 200}});
  const pv = spring({frame: f - 6, fps, config: {damping: 10, stiffness: 200}});
  if (!e.a || !e.b) return <Fondo src={e.fondo} />;

  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: vertical ? '0 70px 260px' : '0 140px', gap: 36}}>
        {e.titulo ? <div style={{color: C.texto, fontSize: vertical ? 58 : 54, fontWeight: 800, textAlign: 'center'}}>{e.titulo}</div> : null}
        <div style={{display: 'flex', flexDirection: vertical ? 'column' : 'row', gap: 26, width: '100%', alignItems: 'stretch'}}>
          <Tarjeta lado={e.a} color={C.acento} p={pa} vertical={vertical} />
          <div style={{alignSelf: 'center', color: C.texto, fontSize: 52, fontWeight: 800, opacity: pv,
            transform: `scale(${pv})`}}>VS</div>
          <Tarjeta lado={e.b} color={C.texto} p={pb} vertical={vertical} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
