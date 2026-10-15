import { ErrorDeApi, enviar, pedir } from "./cliente";

export type Rol = "medico" | "paciente";
export type TipoDocumento = "CC" | "CE" | "PA" | "PT";

export const TIPOS_DE_DOCUMENTO: { valor: TipoDocumento; corto: string; nombre: string }[] = [
  { valor: "CC", corto: "Cédula", nombre: "Cédula de ciudadanía" },
  { valor: "CE", corto: "Cédula de extranjería", nombre: "Cédula de extranjería" },
  { valor: "PA", corto: "Pasaporte", nombre: "Pasaporte" },
  { valor: "PT", corto: "Permiso por protección temporal", nombre: "Permiso por protección temporal" },
];

export type Sesion = { rol: Rol; vence: string };

export type MiCuenta = {
  usuario_id: string;
  rol: Rol;
  tipo_documento: TipoDocumento;
  numero_documento: string;
  nombres: string;
  apellidos: string;
  correo: string | null;
};

export type TextoDeAutorizacion = {
  id: string;
  tipo: "datos" | "ia";
  version: number;
  vigente_desde: string;
  puntos: { titulo: string; texto: string; resaltado: boolean }[];
  contenido: string;
};

export type Documento = { tipo_documento: TipoDocumento; numero_documento: string };

export type Registro = Documento & {
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string;
  telefono: string;
  correo: string;
  contrasena: string;
  texto_datos: string;
  texto_ia: string | null;
};

export type PuestaEnMarcha = Documento & {
  enlace: string;
  nombres: string;
  apellidos: string;
  correo: string;
  contrasena: string;
};

/** La cuenta de quien tiene la sesión abierta, o null si no hay sesión. */
export async function miCuenta(): Promise<MiCuenta | null> {
  try {
    return await pedir<MiCuenta>("/api/v1/yo");
  } catch (error) {
    if (error instanceof ErrorDeApi && error.estado === 401) return null;
    throw error;
  }
}

export function ingresar(datos: Documento & { contrasena: string }) {
  return enviar<Sesion>("/api/v1/sesion", "POST", datos);
}

export function cerrarSesion() {
  return enviar<void>("/api/v1/sesion", "DELETE");
}

export function registrarse(datos: Registro) {
  return enviar<Sesion>("/api/v1/cuentas/registro", "POST", datos);
}

export function ponerEnMarcha(datos: PuestaEnMarcha) {
  return enviar<Sesion>("/api/v1/puesta-en-marcha", "POST", datos);
}

export function textoDeAutorizacion(tipo: "datos" | "ia") {
  return pedir<TextoDeAutorizacion>(`/api/v1/autorizaciones/texto?tipo=${tipo}`);
}
