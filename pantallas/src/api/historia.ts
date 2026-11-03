// Historia clínica del consultorio (diseno/03-api.md, E9).
import { enviar, pedir } from "./cliente";

export type Valor = string | number | boolean | null;

export type CampoDelFormulario = {
  nombre: string;
  clase: "texto" | "entero" | "decimal" | "opcion" | "si_no";
  obligatorio: boolean;
  lista: string | null;
  minimo: number | null;
  maximo: number | null;
  unidad: string | null;
  largo: number;
};

export type Formulario = {
  atencion: Record<string, CampoDelFormulario>;
  identificacion: Record<string, CampoDelFormulario>;
  listas: Record<string, Record<string, string>>;
};

export type Diagnostico = {
  codigo: string;
  nombre: string;
  tipo: string;
  principal: boolean;
};

export type Medicamento = {
  nombre: string;
  dosis: string;
  via: string;
  frecuencia: string;
  dias: number;
  indicaciones: string | null;
};

export type NotaAclaratoria = {
  texto: string;
  fecha: string;
  firma_nombre: string;
  firma_registro: string | null;
};

export type Atencion = {
  id: string;
  paciente_id: string;
  cita_id: string | null;
  estado: "abierta" | "cerrada";
  inicio: string;
  fin: string | null;
  guardada_en: string;
  datos: Record<string, Valor>;
  diagnosticos: Diagnostico[];
  medicamentos: Medicamento[];
  imc: number | null;
  firma: { nombre: string; registro: string | null; documento: string | null } | null;
  notas: NotaAclaratoria[];
};

export type Faltantes = { identificacion: string[]; atencion: string[] };

export type AtencionParaEscribir = {
  atencion: Atencion;
  identificacion: Record<string, Valor>;
  faltantes: Faltantes;
};

export function formulario() {
  return pedir<Formulario>("/api/v1/historia-clinica/formulario");
}

export function abrirAtencion(paciente: string, cita?: string | null) {
  return enviar<{ id: string }>(`/api/v1/pacientes/${paciente}/atenciones`, "POST", {
    cita_id: cita ?? null,
  });
}

export function verAtencion(atencion: string) {
  return pedir<AtencionParaEscribir>(`/api/v1/atenciones/${atencion}`);
}

export function guardarBorrador(
  atencion: string,
  cambios: {
    datos?: Record<string, Valor>;
    diagnosticos?: Omit<Diagnostico, "nombre">[];
    medicamentos?: Medicamento[];
  },
) {
  return enviar<{ guardada_en: string }>(`/api/v1/atenciones/${atencion}`, "PATCH", {
    datos: cambios.datos ?? {},
    diagnosticos: cambios.diagnosticos,
    medicamentos: cambios.medicamentos,
  });
}

export function cerrarAtencion(atencion: string, contrasena: string) {
  return enviar<{ fin: string }>(`/api/v1/atenciones/${atencion}/cierre`, "POST", { contrasena });
}

export function agregarNota(atencion: string, texto: string) {
  return enviar<void>(`/api/v1/atenciones/${atencion}/notas`, "POST", { texto });
}

export function guardarIdentificacion(paciente: string, datos: Record<string, Valor>) {
  return enviar<void>(`/api/v1/pacientes/${paciente}/identificacion`, "PUT", { datos });
}

export function historiaDelPaciente(paciente: string) {
  return pedir<Atencion[]>(`/api/v1/pacientes/${paciente}/atenciones`);
}

export function miHistoria() {
  return pedir<Atencion[]>("/api/v1/mi-historia");
}

export function buscarCie10(texto: string) {
  return pedir<{ codigo: string; nombre: string }[]>(
    `/api/v1/cie10?buscar=${encodeURIComponent(texto)}`,
  );
}
