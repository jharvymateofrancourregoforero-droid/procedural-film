export type Tipo = 'media' | 'cifra' | 'barras' | 'linea' | 'texto' | 'comparar';
export type Tono = 'acento' | 'positivo' | 'negativo' | 'neutro';
export type Entrada = 'corte' | 'zoom' | 'desliza' | 'desenfoque';

export type Dato = {etiqueta: string; valor: number};
export type Lado = {etiqueta: string; valor: string};

export type Escena = {
  texto: string;
  tipo: Tipo;
  inicio?: number;
  fin?: number;
  query?: string;
  src?: string | null;
  fondo_query?: string;
  fondo?: string | null;
  titulo?: string;
  subtitulo?: string;
  valor?: number;
  prefijo?: string;
  sufijo?: string;
  decimales?: number;
  tono?: Tono;
  datos?: Dato[];
  destacar?: number;
  a?: Lado;
  b?: Lado;
  fuente?: string;
  entrada?: Entrada;
  sfx?: string;
  pausa?: number;
};

export type Plan = {
  slug?: string;
  titulo?: string;
  formato?: 'vertical' | 'horizontal';
  voz?: string;
  palabras?: string;
  musica?: string;
  volumen_musica?: number;
  aviso?: boolean;
  resaltar_verde?: string[];
  resaltar_rojo?: string[];
  duracion?: number;
  escenas: Escena[];
};

export type Palabra = {w: string; s: number; e: number};
