import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C} from '../estilo';
import {Media} from './Media';

// Fondo de las escenas gráficas: degradado vivo + retícula sutil, o un clip oscurecido.
export const Fondo: React.FC<{src?: string | null}> = ({src}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  if (src) {
    return (
      <AbsoluteFill>
        <Media src={src} />
        <AbsoluteFill style={{backgroundColor: 'rgba(11,18,32,0.78)'}} />
      </AbsoluteFill>
    );
  }
  const x = interpolate(f, [0, durationInFrames], [30, 70]);
  return (
    <AbsoluteFill
      style={{
        backgroundColor: C.fondo,
        backgroundImage: [
          `radial-gradient(circle at ${x}% 30%, rgba(224,176,75,0.13), transparent 55%)`,
          `radial-gradient(circle at ${100 - x}% 85%, rgba(34,197,94,0.07), transparent 50%)`,
          'linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px)',
          'linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)',
        ].join(','),
        backgroundSize: 'auto, auto, 72px 72px, 72px 72px',
      }}
    />
  );
};
