// Único lugar que habla con la API. Ningún componente llama a fetch por su cuenta.

// En local queda vacía y Vite reenvía; publicada, es la dirección de la API.
const BASE = import.meta.env.VITE_API_URL ?? "";

export class ErrorDeApi extends Error {
  readonly estado: number;
  readonly codigo: string;
  readonly detalle: unknown;

  constructor(estado: number, codigo: string, mensaje: string, detalle?: unknown) {
    super(mensaje);
    this.estado = estado;
    this.codigo = codigo;
    this.detalle = detalle;
  }
}

export async function pedir<T>(ruta: string, opciones: RequestInit = {}): Promise<T> {
  const respuesta = await fetch(BASE + ruta, { credentials: "include", ...opciones });
  if (!respuesta.ok) {
    const error = await respuesta.json().catch(() => null);
    throw new ErrorDeApi(
      respuesta.status,
      error?.codigo ?? "desconocido",
      error?.mensaje ?? "No se pudo completar la operación",
      error?.detalle,
    );
  }
  return (await respuesta.json()) as T;
}
