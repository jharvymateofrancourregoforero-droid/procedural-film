import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, colorTono, display, fuerte, numero} from '../estilo';
import type {Escena} from '../tipos';
import {Fondo} from './Fondo';

// Barras horizontales que crecen escalonadas; una barra destacada en color.
export const Barras: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const datos = (e.datos ?? []).slice(0, 5);
  const max = Math.max(...datos.map((d) => Math.abs(d.valor)), 1);
  const destacar = e.destacar ?? datos.findIndex((d) => d.valor === Math.max(...datos.map((x) => x.valor)));
  const alto = vertical ? 100 : 86;

  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{justifyContent: 'center', padding: vertical ? '0 70px 300px' : '0 160px', gap: vertical ? 30 : 24}}>
        {e.titulo ? (
          <div style={{color: C.texto, fontFamily: display, fontSize: vertical ? 84 : 88, textTransform: 'uppercase', lineHeight: 1, marginBottom: 20}}>{e.titulo}</div>
        ) : null}
        {datos.map((d, i) => {
          const p = spring({frame: f - 4 - i * 4, fps, config: {damping: 200}, durationInFrames: Math.round(fps * 0.9)});
          const color = i === destacar ? colorTono(e.tono) : C.neutro;
          return (
            <div key={i} style={{display: 'flex', flexDirection: 'column', gap: 10}}>
              <div style={{color: C.suave, fontFamily: fuerte, fontSize: vertical ? 36 : 32, fontWeight: 800, textTransform: 'uppercase', letterSpacing: 1}}>{d.etiqueta}</div>
              <div style={{display: 'flex', alignItems: 'center', gap: 20}}>
                <div
                  style={{
                    height: alto, width: `${Math.max(2, (Math.abs(d.valor) / max) * 78 * p)}%`,
                    background: `linear-gradient(90deg, ${color}aa, ${color})`, borderRadius: 6,
                    boxShadow: i === destacar ? `0 0 40px ${color}55` : 'none',
                  }}
                />
                <div style={{color: i === destacar ? color : C.texto, fontFamily: display, fontSize: vertical ? 72 : 76,
                  fontVariantNumeric: 'tabular-nums', opacity: p, whiteSpace: 'nowrap'}}>
                  {e.prefijo ?? ''}{numero(d.valor * p, e.decimales ?? 0)}{e.sufijo ?? ''}
                </div>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
