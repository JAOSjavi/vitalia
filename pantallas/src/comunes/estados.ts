import type { EstadoDeCita } from "../api/citas";
import type { TonoDeEstado } from "./piezas/Estado";

export const ESTADOS_DE_CITA: Record<EstadoDeCita, { nombre: string; tono: TonoDeEstado }> = {
  confirmada: { nombre: "Confirmada", tono: "aro" },
  cancelada: { nombre: "Cancelada", tono: "rojo" },
  atendida: { nombre: "Atendida", tono: "verde" },
  no_asistio: { nombre: "No asistió", tono: "ambar" },
};
