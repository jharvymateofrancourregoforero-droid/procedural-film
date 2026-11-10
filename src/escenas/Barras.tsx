import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, colorTono, numero} from '../estilo';
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
  const alto = vertical ? 96 : 72;

  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{justifyContent: 'center', padding: vertical ? '0 70px 300px' : '0 160px', gap: vertical ? 30 : 24}}>
        {e.titulo ? (
          <div style={{color: C.texto, fontSize: vertical ? 58 : 54, fontWeight: 800, marginBottom: 16}}>{e.titulo}</div>
        ) : null}
        {datos.map((d, i) => {
          const p = spring({frame: f - 4 - i * 4, fps, config: {damping: 200}, durationInFrames: Math.round(fps * 0.9)});
          const color = i === destacar ? colorTono(e.tono) : C.neutro;
          return (
            <div key={i} style={{display: 'flex', flexDirection: 'column', gap: 10}}>
              <div style={{color: C.suave, fontSize: vertical ? 38 : 32, fontWeight: 600}}>{d.etiqueta}</div>
              <div style={{display: 'flex', alignItems: 'center', gap: 20}}>
                <div
                  style={{
                    height: alto, width: `${Math.max(2, (Math.abs(d.valor) / max) * 78 * p)}%`,
                    background: color, borderRadius: 16,
                    boxShadow: i === destacar ? `0 0 40px ${color}55` : 'none',
                  }}
                />
                <div style={{color: i === destacar ? color : C.texto, fontSize: vertical ? 48 : 42, fontWeight: 800,
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
