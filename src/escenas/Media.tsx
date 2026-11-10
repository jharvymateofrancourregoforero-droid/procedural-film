import React from 'react';
import {AbsoluteFill, Html5Video, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, display, zona} from '../estilo';
import {Fondo} from './Fondo';

const esVideo = (src: string) => /\.(mp4|webm|mov|m4v)$/i.test(src);

// Imagen o clip a pantalla completa: zoom y paneo lentos (4 direcciones), color con más contraste y viñeta.
export const Media: React.FC<{src?: string | null; titulo?: string; semilla?: number}> = ({src, titulo, semilla = 0}) => {
  const f = useCurrentFrame();
  const {durationInFrames, fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const z = zona(vertical);

  if (!src) {
    const s = spring({frame: f, fps, config: {damping: 14, stiffness: 180}});
    return (
      <AbsoluteFill>
        <Fondo />
        <AbsoluteFill style={{justifyContent: 'center', padding: `0 ${z.lados}px`}}>
          <div style={{color: C.texto, fontFamily: display, fontSize: vertical ? 120 : 130, textAlign: 'center',
            textTransform: 'uppercase', lineHeight: 1.02, opacity: s, transform: `scale(${1.3 - 0.3 * s})`}}>{titulo ?? ''}</div>
        </AbsoluteFill>
      </AbsoluteFill>
    );
  }

  const video = esVideo(src);
  const dir = semilla % 4;
  const t = interpolate(f, [0, durationInFrames], [0, 1]);
  const escala = video ? 1.02 + 0.06 * t : dir % 2 === 0 ? 1.06 + 0.14 * t : 1.2 - 0.14 * t;
  const tx = video ? 0 : dir === 0 ? -2.5 * t : dir === 1 ? 2.5 * (1 - t) : 0;
  const ty = video ? 0 : dir === 2 ? 2 - 4 * t : dir === 3 ? -2 + 4 * t : 0;
  const estilo: React.CSSProperties = {
    width: '100%', height: '100%', objectFit: 'cover',
    transform: `scale(${escala}) translate(${tx}%, ${ty}%)`,
    filter: 'contrast(1.12) saturate(1.2) brightness(0.9)',
  };
  const entra = spring({frame: f - 2, fps, config: {damping: 12, stiffness: 200}});

  return (
    <AbsoluteFill style={{backgroundColor: C.fondo, overflow: 'hidden'}}>
      {video ? <Html5Video src={staticFile(src)} muted loop style={estilo} /> : <Img src={staticFile(src)} style={estilo} />}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 45%, rgba(0,0,0,0.55) 100%)'}} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0) 25%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75) 100%)'}} />
      {titulo ? (
        <div style={{position: 'absolute', top: z.arriba + 40, left: z.lados}}>
          <div style={{background: C.acento, color: '#000', fontFamily: display, fontSize: vertical ? 84 : 80,
            textTransform: 'uppercase', padding: '6px 26px', lineHeight: 1.05, transform: `rotate(-2deg) scale(${entra})`,
            transformOrigin: 'left center', boxShadow: '0 12px 40px rgba(0,0,0,0.5)'}}>{titulo}</div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
