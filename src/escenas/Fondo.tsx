import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C} from '../estilo';
import {Media} from './Media';

// Fondo de las escenas gráficas: negro con brillo amarillo que se mueve, rayas diagonales y un giro de luz.
// Con `src`, usa la imagen muy oscurecida.
export const Fondo: React.FC<{src?: string | null}> = ({src}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  if (src) {
    return (
      <AbsoluteFill>
        <Media src={src} />
        <AbsoluteFill style={{backgroundColor: 'rgba(7,8,11,0.82)'}} />
      </AbsoluteFill>
    );
  }
  const x = interpolate(f, [0, durationInFrames], [28, 72]);
  return (
    <AbsoluteFill
      style={{
        backgroundColor: C.fondo,
        backgroundImage: [
          `radial-gradient(circle at ${x}% 38%, rgba(255,212,0,0.17), transparent 48%)`,
          `radial-gradient(circle at ${100 - x}% 92%, rgba(0,230,118,0.09), transparent 42%)`,
          'repeating-linear-gradient(115deg, rgba(255,255,255,0.028) 0 2px, transparent 2px 52px)',
        ].join(','),
        backgroundPosition: `0 0, 0 0, ${f * 1.2}px 0`,
      }}
    >
      <AbsoluteFill
        style={{
          background: `conic-gradient(from ${f * 0.25}deg at 50% 45%, rgba(255,212,0,0.05), transparent 12%, rgba(255,212,0,0.035) 25%, transparent 40%, rgba(255,212,0,0.05) 58%, transparent 72%)`,
        }}
      />
    </AbsoluteFill>
  );
};
