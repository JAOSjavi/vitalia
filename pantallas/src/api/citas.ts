import { enviar, pedir } from "./cliente";
import type { TipoDocumento } from "./cuentas";

export type EstadoDeCita = "confirmada" | "cancelada" | "atendida" | "no_asistio";

export type Cita = {
  id: string;
  paciente_id: string;
  paciente: string;
  tipo_id: string;
  tipo: string;
  inicio: string;
  fin: string;
  duracion_minutos: number;
  estado: EstadoDeCita;
  fuera_de_horario: boolean;
  motivo: string | null;
};

export type TipoDeCita = { id: string; nombre: string; duracion_minutos: number; activo: boolean };

export type Disponibilidad = {
  tipo: TipoDeCita;
  dias: string[];
  dia: string | null;
  horas: string[];
};

export type InicioDelPaciente = {
  proxima: Cita | null;
  puede_cambiarla: boolean;
  anticipacion_horas: number;
  telefono: string | null;
  direccion: string | null;
};

export type Pendiente = "horario" | "tipos_cita" | "consultorio";

export type AgendaDeHoy = {
  dia: string;
  citas: Cita[];
  proxima: Cita | null;
  pendientes: Pendiente[];
};

export type Franja = { dia_semana: number; hora_inicio: string; hora_fin: string };

export type PacienteEnLista = {
  id: string;
  nombres: string;
  apellidos: string;
  tipo_documento: TipoDocumento;
  numero_documento: string;
  telefono: string;
};

export type PaginaDePacientes = {
  pacientes: PacienteEnLista[];
  total: number;
  pagina: number;
  tamano: number;
};

export type CitaNueva = {
  tipo_cita: string;
  inicio: string;
  paciente?: string;
  confirmar_repetida?: boolean;
  confirmar_fuera_de_horario?: boolean;
};

export function tiposDeCita() {
  return pedir<TipoDeCita[]>("/api/v1/tipos-cita");
}

export function crearTipoDeCita(datos: { nombre: string; duracion_minutos: number }) {
  return enviar<TipoDeCita>("/api/v1/tipos-cita", "POST", datos);
}

export function editarTipoDeCita(
  id: string,
  cambio: Partial<Pick<TipoDeCita, "nombre" | "duracion_minutos" | "activo">>,
) {
  return pedir<TipoDeCita>(`/api/v1/tipos-cita/${id}`, {
    method: "PATCH",
    body: JSON.stringify(cambio),
  });
}

export function disponibilidad(tipo: string, dia?: string | null, cita?: string) {
  const parametros = new URLSearchParams({ tipo_cita: tipo });
  if (dia) parametros.set("fecha", dia);
  if (cita) parametros.set("cita", cita);
  return pedir<Disponibilidad>(`/api/v1/disponibilidad?${parametros}`);
}

export function crearCita(datos: CitaNueva) {
  return enviar<{ id: string }>("/api/v1/citas", "POST", datos);
}

export function misCitas() {
  return pedir<Cita[]>("/api/v1/citas");
}

export function moverCita(
  id: string,
  datos: { inicio: string; motivo?: string; confirmar_fuera_de_horario?: boolean },
) {
  return enviar<void>(`/api/v1/citas/${id}/mover`, "POST", datos);
}

export function cancelarCita(id: string, motivo?: string) {
  return enviar<void>(`/api/v1/citas/${id}/cancelar`, "POST", { motivo: motivo || null });
}

export function inicioDelPaciente() {
  return pedir<InicioDelPaciente>("/api/v1/yo/inicio");
}

export function agendaDeHoy() {
  return pedir<AgendaDeHoy>("/api/v1/agenda/hoy");
}

export function verHorario() {
  return pedir<{ franjas: Franja[] }>("/api/v1/horario");
}

export function guardarHorario(franjas: Franja[]) {
  return enviar<{ citas_afectadas: Cita[] }>("/api/v1/horario", "PUT", { franjas });
}

export function buscarPacientes(buscar: string, pagina = 1) {
  const parametros = new URLSearchParams({ pagina: String(pagina) });
  if (buscar.trim()) parametros.set("buscar", buscar.trim());
  return pedir<PaginaDePacientes>(`/api/v1/pacientes?${parametros}`);
}
