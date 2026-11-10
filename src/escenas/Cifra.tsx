import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, colorTono, display, fuerte, numero} from '../estilo';
import type {Escena} from '../tipos';
import {Fondo} from './Fondo';

// Cifra gigante: contador rápido, golpe con temblor al llegar y resplandor del color del tono.
export const Cifra: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const vertical = height > width;
  const valor = e.valor ?? 0;
  const dur = Math.round(fps * 0.9);
  const actual = interpolate(f, [2, 2 + dur], [0, valor], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });
  const entra = spring({frame: f, fps, config: {damping: 200}});
  const golpe = spring({frame: f - 2 - dur, fps, config: {damping: 9, stiffness: 260}});
  const llegada = f - 2 - dur;
  const temblor = llegada >= 0 && llegada < 8 ? (8 - llegada) * 1.6 : 0;
  const color = colorTono(e.tono);
  const texto = `${e.prefijo ?? ''}${numero(valor, e.decimales ?? 0)}${e.sufijo ?? ''}`;
  const tam = Math.min(vertical ? 230 : 320, ((vertical ? 0.88 : 0.82) * width) / (texto.length * 0.47));

  return (
    <AbsoluteFill>
      <Fondo src={e.fondo} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: vertical ? '80px 60px 260px' : '60px 100px 140px'}}>
        {e.titulo ? (
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: entra,
            transform: `translateY(${(1 - entra) * -30}px)`}}>
            <div style={{color: C.texto, fontFamily: fuerte, fontWeight: 900, fontSize: vertical ? 48 : 46,
              textAlign: 'center', textTransform: 'uppercase', letterSpacing: 2}}>{e.titulo}</div>
            <div style={{height: 8, width: `${entra * 180}px`, background: C.acento, borderRadius: 4}} />
          </div>
        ) : null}
        <div style={{
          color, fontFamily: display, fontSize: tam, lineHeight: 1.05, whiteSpace: 'nowrap', marginTop: 10,
          fontVariantNumeric: 'tabular-nums',
          transform: `translate(${Math.sin(f * 2.1) * temblor}px, ${Math.cos(f * 2.7) * temblor}px) scale(${(0.85 + 0.15 * entra) * (1 + 0.08 * golpe * (1 - golpe) * 4)})`,
          textShadow: `0 0 90px ${color}66, 0 10px 0 rgba(0,0,0,0.35)`,
        }}>
          {e.prefijo ?? ''}{numero(actual, e.decimales ?? 0)}{e.sufijo ?? ''}
        </div>
        {e.subtitulo ? (
          <div style={{marginTop: 18, color: C.texto, fontFamily: fuerte, fontWeight: 800, fontSize: vertical ? 38 : 38,
            textAlign: 'center', padding: '10px 26px', borderRadius: 999, background: 'rgba(255,255,255,0.08)',
            border: `2px solid ${color}55`, opacity: golpe > 0.1 ? 1 : 0, transform: `scale(${0.9 + 0.1 * Math.min(1, golpe)})`}}>
            {e.subtitulo}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
