import React, {useEffect, useMemo, useState} from 'react';
import {
  AbsoluteFill, Easing, Html5Audio, Sequence, cancelRender, continueRender, delayRender, interpolate,
  staticFile, useCurrentFrame, useVideoConfig,
} from 'remotion';
import {C, fontFamily, fuerte, zona} from './estilo';
import {Barras} from './escenas/Barras';
import {Capitulo} from './escenas/Capitulo';
import {Cifra} from './escenas/Cifra';
import {Comparar} from './escenas/Comparar';
import {Intro} from './escenas/Intro';
import {Linea} from './escenas/Linea';
import {Media} from './escenas/Media';
import {Texto} from './escenas/Texto';
import {Subtitulos} from './Subtitulos';
import type {Escena, Palabra, Plan} from './tipos';

const ESCENA_SIN_VOZ = 3; // s por escena cuando aún no hay voz (vista previa del ejemplo)
const SIN_SUBTITULOS = new Set(['texto', 'capitulo', 'intro']);
const CON_DESTELLO = new Set(['cifra', 'capitulo', 'intro']);

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

// Transición de entrada. Sin `entrada` explícita, las imágenes alternan golpe de zoom y barrido.
const Entrada: React.FC<{e: Escena; i: number; children: React.ReactNode}> = ({e, i, children}) => {
  const f = useCurrentFrame();
  const {width} = useVideoConfig();
  const p = interpolate(f, [0, 7], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const tipo = e.entrada ?? (e.tipo === 'media' ? (i % 3 === 0 ? 'desliza' : 'zoom') : e.tipo === 'cifra' ? 'zoom' : 'corte');
  let estilo: React.CSSProperties = {};
  if (tipo === 'zoom') estilo = {transform: `scale(${1.16 - 0.16 * p})`};
  if (tipo === 'desliza') estilo = {transform: `translateX(${(1 - p) * width * 0.18 * (i % 2 ? -1 : 1)}px)`, filter: `blur(${(1 - p) * 18}px)`};
  if (tipo === 'desenfoque') estilo = {filter: `blur(${(1 - p) * 26}px)`, transform: `scale(${1.08 - 0.08 * p})`};
  // temblor de cámara al inicio de intro y capítulos
  if (e.tipo === 'intro' || e.tipo === 'capitulo') {
    const k = interpolate(f, [4, 16], [10, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    estilo = {...estilo, transform: `${estilo.transform ?? ''} translate(${Math.sin(f * 2.3) * k}px, ${Math.cos(f * 3.1) * k}px)`};
  }
  return <AbsoluteFill style={estilo}>{children}</AbsoluteFill>;
};

const Destello: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 5], [0.55, 0], {extrapolateRight: 'clamp'});
  return o > 0 ? <AbsoluteFill style={{backgroundColor: '#fff', opacity: o, mixBlendMode: 'screen'}} /> : null;
};

const Contenido: React.FC<{e: Escena; i: number}> = ({e, i}) => {
  switch (e.tipo) {
    case 'cifra': return <Cifra e={e} />;
    case 'barras': return <Barras e={e} />;
    case 'linea': return <Linea e={e} />;
    case 'texto': return <Texto e={e} />;
    case 'comparar': return <Comparar e={e} />;
    case 'capitulo': return <Capitulo e={e} />;
    case 'intro': return <Intro e={e} />;
    default: return <Media src={e.src} titulo={e.titulo} semilla={i} />;
  }
};

const Fuente: React.FC<{texto: string; vertical: boolean}> = ({texto, vertical}) => {
  const z = zona(vertical);
  return (
    <div style={{position: 'absolute', left: z.lados, bottom: vertical ? z.abajo - 40 : z.abajo - 55,
      color: '#fff', fontSize: vertical ? 24 : 21, fontWeight: 600, opacity: 0.75, fontFamily,
      background: 'rgba(0,0,0,0.45)', padding: '4px 12px', borderRadius: 6}}>
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

// Efecto de sonido automático por tipo de escena, con al menos 1,2 s entre efectos.
const sfxAuto = (escenas: ReturnType<typeof tiempos>, sfx: Plan['sfx']) => {
  if (!sfx) return escenas.map((e) => e.sfx ?? null);
  let ultimo = -Infinity;
  let medias = 0;
  return escenas.map((e) => {
    let s: string | undefined = e.sfx;
    if (!s) {
      if (e.tipo === 'intro' || e.tipo === 'capitulo') s = sfx.impacto;
      else if (e.tipo === 'cifra') s = (e.prefijo ?? '').includes('$') ? sfx.caja ?? sfx.pop : sfx.pop;
      else if (e.tipo === 'texto' || e.tipo === 'comparar' || e.tipo === 'barras' || e.tipo === 'linea') s = sfx.whoosh;
      else if (e.tipo === 'media' && medias++ % 3 === 0) s = sfx.whoosh;
    }
    if (!s || e.inicio - ultimo < 1.2) return null;
    ultimo = e.inicio;
    return s;
  });
};

export const Video: React.FC<Plan> = (plan) => {
  const f = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = height > width;
  const t = f / fps;
  const escenas = useMemo(() => tiempos(plan.escenas), [plan.escenas]);
  const palabras = usarPalabras(plan.palabras);
  const volumen = usarVolumen(palabras, plan.volumen_musica ?? 0.18, fps, durationInFrames);
  const efectos = useMemo(() => sfxAuto(escenas, plan.sfx), [escenas, plan.sfx]);
  const z = zona(vertical);
  const ocultar = useMemo(
    () => escenas.map((e, i) => [e.inicio, escenas[i + 1]?.inicio ?? e.fin + 1, e.tipo] as const)
      .filter(([, , tipo]) => SIN_SUBTITULOS.has(tipo)).map(([a, b]) => [a, b] as [number, number]),
    [escenas],
  );
  const capitulos = useMemo(() => escenas.filter((e) => e.tipo === 'capitulo'), [escenas]);
  const total = durationInFrames / fps;
  const ultimoHasta = <T extends {inicio: number}>(xs: T[]) => [...xs].reverse().find((x) => x.inicio <= t);
  const actual = ultimoHasta(escenas);
  const cap = ultimoHasta(capitulos);
  const enTarjeta = actual?.tipo === 'capitulo' || actual?.tipo === 'intro';

  return (
    <AbsoluteFill style={{backgroundColor: C.fondo, fontFamily}}>
      {escenas.map((e, i) => {
        const desde = Math.round(e.inicio * fps);
        const hasta = i + 1 < escenas.length ? Math.round(escenas[i + 1].inicio * fps) : durationInFrames;
        return (
          <Sequence key={i} from={desde} durationInFrames={Math.max(1, hasta - desde)} premountFor={fps}>
            <Entrada e={e} i={i}>
              <Contenido e={e} i={i} />
            </Entrada>
            {CON_DESTELLO.has(e.tipo) ? <Destello /> : null}
            {e.fuente ? <Fuente texto={e.fuente} vertical={vertical} /> : null}
            {efectos[i] ? <Html5Audio src={staticFile(efectos[i] as string)} volume={plan.volumen_sfx ?? 0.35} /> : null}
          </Sequence>
        );
      })}

      {/* viñeta */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,0.45) 100%)', pointerEvents: 'none'}} />

      {plan.voz ? <Html5Audio src={staticFile(plan.voz)} /> : null}
      {plan.musica ? <Html5Audio src={staticFile(plan.musica)} loop volume={volumen} /> : null}
      {palabras.length ? <Subtitulos palabras={palabras} verde={plan.resaltar_verde} rojo={plan.resaltar_rojo} ocultar={ocultar} /> : null}

      {/* etiqueta del capítulo actual */}
      {cap && !enTarjeta && cap.titulo ? (
        <div style={{position: 'absolute', top: z.arriba - 18, left: z.lados - 30, display: 'flex', alignItems: 'center', gap: 0,
          fontFamily: fuerte, fontWeight: 900, fontSize: vertical ? 30 : 26, textTransform: 'uppercase', letterSpacing: 1}}>
          <div style={{background: C.acento, color: '#000', padding: '6px 14px'}}>{cap.numero ? `#${cap.numero}` : '★'}</div>
          <div style={{background: 'rgba(0,0,0,0.65)', color: '#fff', padding: '6px 16px'}}>{cap.titulo}</div>
        </div>
      ) : null}

      {/* barra de progreso con marcas de capítulo */}
      <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: vertical ? 10 : 8, background: 'rgba(255,255,255,0.12)'}}>
        <div style={{height: '100%', width: `${(f / durationInFrames) * 100}%`, background: C.acento}} />
        {capitulos.map((c, i) => (
          <div key={i} style={{position: 'absolute', top: 0, left: `${(c.inicio / total) * 100}%`, width: 4, height: '100%',
            background: '#000'}} />
        ))}
      </div>

      {plan.aviso ? (
        <Sequence from={Math.max(0, durationInFrames - Math.round(fps * 2.5))}>
          <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: z.abajo + 10}}>
            <div style={{background: C.acento, color: '#000', fontFamily: fuerte, fontWeight: 800,
              fontSize: vertical ? 30 : 28, padding: '12px 28px', textTransform: 'uppercase', letterSpacing: 1}}>
              Contenido educativo. No es asesoría financiera.
            </div>
          </AbsoluteFill>
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
