import { enviar, pedir } from "./cliente";

export type ConsultorioPublico = {
  nombre: string | null;
  telefono: string | null;
  medico: string | null;
};

export type Consultorio = {
  nombre: string | null;
  direccion: string | null;
  telefono: string | null;
  correo: string | null;
  medico_nombres: string;
  medico_apellidos: string;
  registro_profesional: string | null;
};

export function consultorioPublico() {
  return pedir<ConsultorioPublico>("/api/v1/consultorio/publico");
}

export function verConsultorio() {
  return pedir<Consultorio>("/api/v1/consultorio");
}

export function guardarConsultorio(datos: Consultorio) {
  return enviar<void>("/api/v1/consultorio", "PUT", datos);
}
