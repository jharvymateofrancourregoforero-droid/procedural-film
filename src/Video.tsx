import React, {useEffect, useMemo, useState} from 'react';
import {
  AbsoluteFill, Easing, Html5Audio, Sequence, cancelRender, continueRender, delayRender, interpolate,
  staticFile, useCurrentFrame, useVideoConfig,
} from 'remotion';
import {C, fontFamily, zona} from './estilo';
import {Barras} from './escenas/Barras';
import {Cifra} from './escenas/Cifra';
import {Comparar} from './escenas/Comparar';
import {Linea} from './escenas/Linea';
import {Media} from './escenas/Media';
import {Texto} from './escenas/Texto';
import {Subtitulos} from './Subtitulos';
import type {Escena, Palabra, Plan} from './tipos';

const ESCENA_SIN_VOZ = 3; // s por escena cuando aún no hay voz (vista previa del ejemplo)

export const tiempos = (escenas: Escena[]) =>
  escenas.map((e, i) => ({
    ...e,
    inicio: e.inicio ?? i * ESCENA_SIN_VOZ,
    fin: e.fin ?? (i + 1) * ESCENA_SIN_VOZ,
  }));

const usarPalabras = (ruta?: string) => {
  const [palabras, setPalabras] = useState<Palabra[]>([]);
  const [handle] = useState(() => (ruta ? delayRender('Cargando subtítulos') : null));
  useEffect(() => {
    if (!ruta || handle === null) return;
    fetch(staticFile(ruta))
      .then((r) => r.json())
      .then((j: Palabra[]) => {
        setPalabras(j);
        continueRender(handle);
      })
      .catch((err) => cancelRender(err));
  }, [ruta, handle]);
  return palabras;
};

// Envuelve cada escena con su animación de entrada.
const Entrada: React.FC<{e: Escena; children: React.ReactNode}> = ({e, children}) => {
  const f = useCurrentFrame();
  const {width} = useVideoConfig();
  const p = interpolate(f, [0, 9], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  let estilo: React.CSSProperties = {};
  if (e.entrada === 'zoom') estilo = {transform: `scale(${1.18 - 0.18 * p})`};
  if (e.entrada === 'desliza') estilo = {transform: `translateX(${(1 - p) * width * 0.22}px)`, opacity: 0.3 + 0.7 * p};
  if (e.entrada === 'desenfoque') estilo = {filter: `blur(${(1 - p) * 22}px)`, transform: `scale(${1.06 - 0.06 * p})`};
  return <AbsoluteFill style={estilo}>{children}</AbsoluteFill>;
};

const Contenido: React.FC<{e: Escena; i: number}> = ({e, i}) => {
  switch (e.tipo) {
    case 'cifra': return <Cifra e={e} />;
    case 'barras': return <Barras e={e} />;
    case 'linea': return <Linea e={e} />;
    case 'texto': return <Texto e={e} />;
    case 'comparar': return <Comparar e={e} />;
    default: return <Media src={e.src} titulo={e.titulo} semilla={i} />;
  }
};

const Fuente: React.FC<{texto: string; vertical: boolean}> = ({texto, vertical}) => {
  const z = zona(vertical);
  return (
    <div style={{position: 'absolute', left: z.lados, bottom: vertical ? z.abajo - 40 : z.abajo - 50,
      color: C.suave, fontSize: vertical ? 26 : 22, fontWeight: 400, opacity: 0.85}}>
      Fuente: {texto.replace(/^fuente:\s*/i, '')}
    </div>
  );
};

// Volumen de la música: baja bajo la voz, sube en pausas, con fundidos.
const usarVolumen = (palabras: Palabra[], baseVol: number, fps: number, total: number) => {
  const tramos = useMemo(() => {
    const out: [number, number][] = [];
    for (const p of palabras) {
      const ult = out[out.length - 1];
      if (ult && p.s - ult[1] < 0.35) ult[1] = p.e;
      else out.push([p.s, p.e]);
    }
    return out;
  }, [palabras]);
  return (f: number) => {
    const t = f / fps;
    let d = Infinity;
    for (const [s, e] of tramos) {
      if (t >= s && t <= e) { d = 0; break; }
      d = Math.min(d, Math.abs(t - s), Math.abs(t - e));
    }
    const ducking = tramos.length ? interpolate(d, [0, 0.5], [0.45, 1], {extrapolateRight: 'clamp'}) : 1;
    const fundido = interpolate(f, [0, fps, total - fps * 1.5, total], [0, 1, 1, 0], {
      extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    });
    return baseVol * ducking * fundido;
  };
};

export const Video: React.FC<Plan> = (plan) => {
  const f = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = height > width;
  const escenas = useMemo(() => tiempos(plan.escenas), [plan.escenas]);
  const palabras = usarPalabras(plan.palabras);
  const volumen = usarVolumen(palabras, plan.volumen_musica ?? 0.18, fps, durationInFrames);
  const z = zona(vertical);
  const ocultar = useMemo(
    () => escenas.filter((e) => e.tipo === 'texto').map((e) => [e.inicio, e.fin] as [number, number]),
    [escenas],
  );

  return (
    <AbsoluteFill style={{backgroundColor: C.fondo, fontFamily}}>
      {escenas.map((e, i) => {
        const desde = Math.round(e.inicio * fps);
        const hasta = i + 1 < escenas.length ? Math.round(escenas[i + 1].inicio * fps) : durationInFrames;
        return (
          <Sequence key={i} from={desde} durationInFrames={Math.max(1, hasta - desde)} premountFor={fps}>
            <Entrada e={e}>
              <Contenido e={e} i={i} />
            </Entrada>
            {e.fuente ? <Fuente texto={e.fuente} vertical={vertical} /> : null}
            {e.sfx ? <Html5Audio src={staticFile(e.sfx)} volume={0.35} /> : null}
          </Sequence>
        );
      })}

      {plan.voz ? <Html5Audio src={staticFile(plan.voz)} /> : null}
      {plan.musica ? <Html5Audio src={staticFile(plan.musica)} loop volume={volumen} /> : null}
      {palabras.length ? <Subtitulos palabras={palabras} verde={plan.resaltar_verde} rojo={plan.resaltar_rojo} ocultar={ocultar} /> : null}

      <div style={{position: 'absolute', top: 0, left: 0, height: vertical ? 8 : 6,
        width: `${(f / durationInFrames) * 100}%`, background: C.acento, opacity: 0.9}} />

      {plan.aviso ? (
        <Sequence from={Math.max(0, durationInFrames - Math.round(fps * 2))}>
          <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: z.abajo + 10}}>
            <div style={{background: 'rgba(11,18,32,0.85)', border: `1px solid ${C.borde}`, color: C.texto,
              fontSize: vertical ? 30 : 26, padding: '14px 26px', borderRadius: 999}}>
              Contenido educativo. No es asesoría financiera.
            </div>
          </AbsoluteFill>
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
