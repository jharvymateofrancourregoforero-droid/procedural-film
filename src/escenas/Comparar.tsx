import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, fuerte} from '../estilo';
import type {Escena, Lado} from '../tipos';
import {Fondo} from './Fondo';

const Panel: React.FC<{lado: Lado; color: string; p: number; desde: number; vertical: boolean}> = ({lado, color, p, desde, vertical}) => (
  <div style={{
    flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 18,
    background: `linear-gradient(${vertical ? 180 : 135}deg, ${color}26, rgba(17,20,27,0.92) 70%)`,
    borderTop: `8px solid ${color}`, padding: vertical ? '50px 30px' : '40px 30px',
    transform: vertical ? `translateY(${(1 - p) * desde * 300}px)` : `translateX(${(1 - p) * desde * 500}px)`, opacity: p,
  }}>
    <div style={{color: C.texto, fontFamily: fuerte, fontWeight: 900, fontSize: vertical ? 44 : 44, textAlign: 'center',
      textTransform: 'uppercase', letterSpacing: 2}}>{lado.etiqueta}</div>
    <div style={{color, fontFamily: display, fontSize: vertical ? 170 : 210, lineHeight: 1, whiteSpace: 'nowrap',
      textShadow: `0 0 70px ${color}55`}}>{lado.valor}</div>
  </div>
);

// A vs. B en pantalla dividida: los paneles entran desde los lados y el "VS" cae en medio.
export const Comparar: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const pa = spring({frame: f, fps, config: {damping: 15, stiffness: 170}});
  const pb = spring({frame: f - 5, fps, config: {damping: 15, stiffness: 170}});
  const pv = spring({frame: f - 9, fps, config: {damping: 8, stiffness: 240}});
  if (!e.a || !e.b) return <Fondo src={e.fondo} />;
  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{flexDirection: vertical ? 'column' : 'row', padding: vertical ? '200px 50px 380px' : '120px 90px 190px', gap: 24}}>
        <Panel lado={e.a} color={C.acento} p={pa} desde={-1} vertical={vertical} />
        <Panel lado={e.b} color={C.texto} p={pb} desde={1} vertical={vertical} />
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingBottom: vertical ? 180 : 70}}>
        <div style={{width: 150, height: 150, borderRadius: '50%', background: C.acento, color: '#000', fontFamily: display,
          fontSize: 82, display: 'flex', justifyContent: 'center', alignItems: 'center', boxShadow: '0 0 0 10px #07080B, 0 20px 60px rgba(0,0,0,0.6)',
          transform: `scale(${pv}) rotate(${(1 - Math.min(1, pv)) * 90}deg)`}}>VS</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
