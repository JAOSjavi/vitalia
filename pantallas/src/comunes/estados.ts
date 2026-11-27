import type { EstadoDeCita } from "../api/citas";
import type { EstadoDeLectura, TipoDeDocumento } from "../api/documentos";
import type { TonoDeEstado } from "./piezas/Estado";

export const ESTADOS_DE_CITA: Record<EstadoDeCita, { nombre: string; tono: TonoDeEstado }> = {
  confirmada: { nombre: "Confirmada", tono: "aro" },
  cancelada: { nombre: "Cancelada", tono: "rojo" },
  atendida: { nombre: "Atendida", tono: "verde" },
  no_asistio: { nombre: "No asistió", tono: "ambar" },
};

export const ESTADOS_DE_LECTURA: Record<EstadoDeLectura, { nombre: string; tono: TonoDeEstado }> = {
  legible: { nombre: "Legible", tono: "verde" },
  en_proceso: { nombre: "Leyendo", tono: "azul" },
  sin_leer: { nombre: "Sin leer", tono: "gris" },
  no_legible: { nombre: "No legible", tono: "rojo" },
};

export const TIPOS_DE_DOCUMENTO: Record<TipoDeDocumento, string> = {
  historia_clinica: "Historia clínica",
  examen: "Examen",
  formula: "Fórmula",
  imagen: "Imagen",
  otro: "Otro",
};
