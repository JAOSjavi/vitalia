import type { Cita } from "./citas";
import { enviar, llamar, pedir } from "./cliente";
import type { TipoDocumento } from "./cuentas";

export type TipoDeDocumento = "historia_clinica" | "examen" | "formula" | "imagen" | "otro";
export type EstadoDeLectura = "sin_leer" | "en_proceso" | "legible" | "no_legible";

export type Documento = {
  id: string;
  nombre: string;
  fecha_documento: string;
  tipo: TipoDeDocumento;
  formato: "pdf" | "jpg" | "png";
  tamano: number;
  estado_lectura: EstadoDeLectura;
  paginas: number | null;
  subido_en: string;
};

export type MisDocumentos = { documentos: Documento[]; ia_autorizada: boolean };

export type FichaDelPaciente = {
  paciente: {
    id: string;
    nombres: string;
    apellidos: string;
    tipo_documento: TipoDocumento;
    numero_documento: string;
    fecha_nacimiento: string;
    telefono: string;
    correo: string | null;
    activo: boolean;
  };
  ia_autorizada: boolean;
  citas: Cita[];
  documentos: Documento[];
};

export const TAMANO_MAXIMO = 20 * 1024 * 1024;

export function misDocumentos() {
  return pedir<MisDocumentos>("/api/v1/documentos");
}

export function subirDocumento(datos: {
  archivo: File;
  nombre: string;
  fecha_documento: string;
  tipo: TipoDeDocumento;
}) {
  const formulario = new FormData();
  formulario.set("archivo", datos.archivo);
  formulario.set("nombre", datos.nombre);
  formulario.set("fecha_documento", datos.fecha_documento);
  formulario.set("tipo", datos.tipo);
  return pedir<Documento>("/api/v1/documentos", { method: "POST", body: formulario });
}

/** Dirección para abrir el archivo en otra pestaña; con página, el visor de PDF salta a ella. */
export function direccionDelArchivo(id: string, pagina?: number) {
  const base = import.meta.env.VITE_API_URL ?? "";
  return `${base}/api/v1/documentos/${id}/archivo${pagina ? `#page=${pagina}` : ""}`;
}

export function eliminarDocumento(id: string) {
  return enviar<void>(`/api/v1/documentos/${id}`, "DELETE");
}

/** D1 es el primer documento que subió el paciente, igual que en las respuestas del asistente. */
export function etiquetasDeDocumentos(documentos: Documento[]) {
  const porSubida = [...documentos].sort((a, b) => (a.id < b.id ? -1 : 1));
  return new Map(porSubida.map((d, i) => [d.id, `D${i + 1}`]));
}

export function fichaDelPaciente(id: string) {
  return pedir<FichaDelPaciente>(`/api/v1/pacientes/${id}`);
}

export type Turno = { autor: "medico" | "asistente"; texto: string };

export type Origen = {
  etiqueta: string;
  documento_id: string;
  documento: string;
  pagina: number;
  frase: string;
  verificado: boolean;
};

export type Consultado = {
  documento_id: string;
  documento: string;
  fecha_documento: string;
  paginas: number[];
};

export type FinDeRespuesta = { origenes: Origen[]; consultado: Consultado[]; aviso: string };

type Evento =
  | { tipo: "texto"; texto: string }
  | ({ tipo: "fin" } & FinDeRespuesta)
  | { tipo: "error"; codigo: string; mensaje: string };

/** Una respuesta que se cortó a mitad de camino porque el proveedor falló. */
export class RespuestaInterrumpida extends Error {}

/**
 * Pregunta al asistente. El texto llega por partes, una línea JSON por evento: cada parte se
 * entrega a `alEscribir` y al final se devuelven las citas comprobadas y lo consultado.
 */
export async function preguntarAlAsistente(
  paciente: string,
  pregunta: string,
  conversacion: Turno[],
  alEscribir: (parte: string) => void,
): Promise<FinDeRespuesta> {
  const respuesta = await llamar(`/api/v1/pacientes/${paciente}/asistente/preguntas`, {
    method: "POST",
    headers: { "X-Vitalia": "1", "Content-Type": "application/json" },
    body: JSON.stringify({ pregunta, conversacion }),
  });

  let fin: FinDeRespuesta | null = null;
  const atender = (linea: string) => {
    if (!linea.trim()) return;
    const evento = JSON.parse(linea) as Evento;
    if (evento.tipo === "texto") alEscribir(evento.texto);
    else if (evento.tipo === "fin") fin = evento;
    else throw new RespuestaInterrumpida(evento.mensaje);
  };

  if (respuesta.body) {
    const lector = respuesta.body.pipeThrough(new TextDecoderStream()).getReader();
    let pendiente = "";
    for (;;) {
      const { value, done } = await lector.read();
      if (done) break;
      pendiente += value;
      const lineas = pendiente.split("\n");
      pendiente = lineas.pop() ?? "";
      lineas.forEach(atender);
    }
    atender(pendiente);
  } else {
    (await respuesta.text()).split("\n").forEach(atender);
  }
  if (!fin) throw new RespuestaInterrumpida("La respuesta llegó incompleta. Intente de nuevo.");
  return fin;
}
