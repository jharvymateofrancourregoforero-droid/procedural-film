import React from 'react';
import {CalculateMetadataFunction, Composition, Still} from 'remotion';
import ejemplo from '../proyectos/ejemplo/plan.json';
import type {Plan} from './tipos';
import {tiempos, Video} from './Video';
import {Miniatura} from './Miniatura';
import type {PropsMiniatura} from './Miniatura';

const FPS = 30;

const calcular: CalculateMetadataFunction<Plan> = ({props}) => {
  const escenas = tiempos(props.escenas);
  const ultima = escenas[escenas.length - 1];
  const dur = props.duracion ?? (ultima ? ultima.fin + 0.9 : 5);
  return {durationInFrames: Math.max(FPS, Math.ceil(dur * FPS))};
};

const base = ejemplo as unknown as Plan;

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="FinanzasVertical" component={Video} width={1080} height={1920} fps={FPS}
      durationInFrames={FPS * 10} defaultProps={base} calculateMetadata={calcular} />
    <Composition id="FinanzasHorizontal" component={Video} width={1920} height={1080} fps={FPS}
      durationInFrames={FPS * 10} defaultProps={base} calculateMetadata={calcular} />
    <Still id="Miniatura" component={Miniatura} width={1280} height={720} defaultProps={{
      persona: '', etiqueta: 'COLOMBIA 2027', linea1: 'Tu plata', linea2: 'perdió valor', cifra: '−$59.266', nota: 'por cada millón',
    } as PropsMiniatura} />
  </>
);
