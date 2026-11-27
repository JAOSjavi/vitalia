import type { Cita } from "./citas";
import { enviar, pedir } from "./cliente";

export type MedioDePago =
  "efectivo" | "transferencia" | "tarjeta_debito" | "tarjeta_credito";
export type Ambiente = "pruebas" | "produccion" | "de_mentira";

export const MEDIOS_DE_PAGO: Record<MedioDePago, string> = {
  efectivo: "Efectivo",
  transferencia: "Transferencia",
  tarjeta_debito: "Tarjeta débito",
  tarjeta_credito: "Tarjeta crédito",
};

export type Factura = {
  cita_id: string;
  numero: string;
  cufe: string;
  concepto: string;
  valor: number;
  medio_pago: MedioDePago;
  enlace_publico: string | null;
  enlace_qr: string | null;
  ambiente: Ambiente;
  emitida_en: string;
};

export type Cobro = { cita: Cita; factura: Factura | null };
export type ListaDeCobros = { ambiente: Ambiente; cobros: Cobro[] };

export function verCobros() {
  return pedir<ListaDeCobros>("/api/v1/cobros");
}

/** Las facturas del paciente de la sesión, la más reciente primero. */
export function misFacturas() {
  return pedir<Factura[]>("/api/v1/yo/facturas");
}

export function facturar(citaId: string, valor: number, medio: MedioDePago) {
  return enviar<Factura>(`/api/v1/citas/${citaId}/factura`, "POST", {
    valor,
    medio_pago: medio,
  });
}

/** El PDF se abre en otra pestaña: la sesión va en la cookie, así que basta la dirección. */
export function direccionDelPdf(citaId: string) {
  return `${import.meta.env.VITE_API_URL ?? ""}/api/v1/citas/${citaId}/factura/pdf`;
}
