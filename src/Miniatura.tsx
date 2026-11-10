import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {loadFont} from '@remotion/fonts';

// Miniatura de YouTube (1280×720): persona recortada con borde tipo sticker, tipografía relajada
// (Nunito redondeada + Caveat Brush manuscrita), cifra en tarjeta y flecha dibujada a mano.
loadFont({family: 'Nunito', url: staticFile('fuentes/nunito-latin-900-normal.woff2'), weight: '900'});
loadFont({family: 'Nunito', url: staticFile('fuentes/nunito-latin-800-normal.woff2'), weight: '800'});
loadFont({family: 'Caveat Brush', url: staticFile('fuentes/caveat-brush-latin-400-normal.woff2'), weight: '400'});

export type PropsMiniatura = {
  persona: string;          // PNG con fondo transparente (ruta en public/)
  fondo?: string;           // imagen de fondo difuminada (opcional)
  etiqueta: string;         // píldora superior
  linea1: string;           // texto redondeado
  linea2: string;           // texto manuscrito resaltado
  cifra: string;            // tarjeta roja
  nota: string;             // texto pequeño bajo la cifra
};

const AMARILLO = '#FFD84D';
const ROJO = '#FF4747';

export const Miniatura: React.FC<PropsMiniatura> = ({persona, fondo, etiqueta, linea1, linea2, cifra, nota}) => (
  <AbsoluteFill style={{background: 'radial-gradient(120% 120% at 78% 45%, #0E5C42 0%, #07281D 45%, #040A08 100%)', overflow: 'hidden'}}>
    {fondo ? (
      <Img src={staticFile(fondo)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
        opacity: 0.16, filter: 'blur(6px) saturate(0.6)'}} />
    ) : null}
    {/* puntos y brillo */}
    <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(255,255,255,0.10) 1.5px, transparent 1.5px)', backgroundSize: '26px 26px',
      maskImage: 'linear-gradient(90deg, black 0%, transparent 60%)', WebkitMaskImage: 'linear-gradient(90deg, black 0%, transparent 60%)'}} />
    <div style={{position: 'absolute', right: 40, top: 70, width: 620, height: 620, borderRadius: '50%',
      background: `radial-gradient(circle, ${AMARILLO}66 0%, ${AMARILLO}00 68%)`}} />

    {/* persona con borde blanco tipo sticker */}
    <Img src={staticFile(persona)} style={{position: 'absolute', right: -200, bottom: -10, height: 730,
      filter: 'drop-shadow(0 0 0 #fff) drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(0 18px 30px rgba(0,0,0,0.55))'}} />

    {/* textos */}
    <div style={{position: 'absolute', left: 64, top: 58, display: 'flex', flexDirection: 'column', alignItems: 'flex-start'}}>
      <div style={{background: '#fff', color: '#07281D', fontFamily: 'Nunito', fontWeight: 900, fontSize: 30,
        padding: '8px 22px', borderRadius: 999, letterSpacing: 1, boxShadow: '0 8px 20px rgba(0,0,0,0.3)'}}>{etiqueta}</div>
      <div style={{color: '#fff', fontFamily: 'Nunito', fontWeight: 900, fontSize: 132, lineHeight: 0.95, marginTop: 26,
        letterSpacing: -3, textShadow: '0 8px 24px rgba(0,0,0,0.45)'}}>{linea1}</div>
      <div style={{color: AMARILLO, fontFamily: 'Caveat Brush', fontSize: 158, lineHeight: 0.9, marginTop: 4, marginLeft: -4,
        transform: 'rotate(-4deg)', transformOrigin: 'left center', textShadow: '0 8px 24px rgba(0,0,0,0.5)'}}>{linea2}</div>
      <div style={{marginTop: 34, marginLeft: 6, transform: 'rotate(2deg)', display: 'flex', flexDirection: 'column', alignItems: 'flex-start'}}>
        <div style={{background: ROJO, color: '#fff', fontFamily: 'Nunito', fontWeight: 900, fontSize: 92, lineHeight: 1,
          padding: '12px 30px 16px', borderRadius: 26, boxShadow: '0 14px 34px rgba(255,71,71,0.45), inset 0 -6px 0 rgba(0,0,0,0.18)'}}>{cifra}</div>
        <div style={{color: '#fff', fontFamily: 'Caveat Brush', fontSize: 46, marginTop: 8, marginLeft: 14, opacity: 0.95}}>{nota}</div>
      </div>
    </div>

    {/* flecha dibujada a mano hacia la persona */}
    <svg width={1280} height={720} style={{position: 'absolute', inset: 0}}>
      <path d="M 548 600 C 600 640, 660 625, 688 552" fill="none" stroke="#fff" strokeWidth={9} strokeLinecap="round" />
      <path d="M 662 566 L 690 548 L 704 580" fill="none" stroke="#fff" strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  </AbsoluteFill>
);
