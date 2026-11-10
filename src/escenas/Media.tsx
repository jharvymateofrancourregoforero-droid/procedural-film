import React from 'react';
import {AbsoluteFill, Html5Video, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, zona} from '../estilo';
import {Fondo} from './Fondo';

const esVideo = (src: string) => /\.(mp4|webm|mov|m4v)$/i.test(src);

// Clip o foto a pantalla completa con zoom lento (Ken Burns).
export const Media: React.FC<{src?: string | null; titulo?: string; semilla?: number}> = ({src, titulo, semilla = 0}) => {
  const f = useCurrentFrame();
  const {durationInFrames, fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const z = zona(vertical);

  if (!src) {
    // Sin clip: fondo de marca con el título al centro, para que la escena nunca quede vacía.
    const s = spring({frame: f, fps, config: {damping: 200}});
    return (
      <AbsoluteFill>
        <Fondo />
        <AbsoluteFill style={{justifyContent: 'center', padding: `0 ${z.lados}px`}}>
          <div style={{color: C.texto, fontSize: vertical ? 78 : 76, fontWeight: 800, textAlign: 'center',
            lineHeight: 1.1, opacity: s, transform: `translateY(${(1 - s) * 30}px)`}}>{titulo ?? ''}</div>
        </AbsoluteFill>
      </AbsoluteFill>
    );
  }

  const video = esVideo(src);
  const escala = interpolate(f, [0, durationInFrames], video ? [1.0, 1.06] : [1.02, 1.12]);
  const dir = semilla % 2 === 0 ? 1 : -1;
  const mover = video ? 0 : interpolate(f, [0, durationInFrames], [0, 2.5 * dir]);
  const estilo: React.CSSProperties = {
    width: '100%', height: '100%', objectFit: 'cover',
    transform: `scale(${escala}) translateX(${mover}%)`,
  };
  const entra = spring({frame: f - 2, fps, config: {damping: 200}});

  return (
    <AbsoluteFill style={{backgroundColor: C.fondo, overflow: 'hidden'}}>
      {video ? <Html5Video src={staticFile(src)} muted loop style={estilo} /> : <Img src={staticFile(src)} style={estilo} />}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(11,18,32,0.55) 0%, rgba(11,18,32,0) 30%, rgba(11,18,32,0) 55%, rgba(11,18,32,0.7) 100%)'}} />
      {titulo ? (
        <div
          style={{
            position: 'absolute', top: z.arriba + 20, left: z.lados, right: z.lados,
            color: C.texto, fontSize: vertical ? 74 : 72, fontWeight: 800, lineHeight: 1.08,
            textShadow: '0 4px 24px rgba(0,0,0,0.6)',
            opacity: entra, transform: `translateY(${(1 - entra) * 30}px)`,
          }}
        >
          {titulo}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
