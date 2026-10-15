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

  /** Los mensajes por campo que manda el servidor cuando los datos no sirven. */
  get campos(): Record<string, string> {
    return this.codigo === "datos_invalidos" && this.detalle && typeof this.detalle === "object"
      ? (this.detalle as Record<string, string>)
      : {};
  }
}

export async function pedir<T>(ruta: string, opciones: RequestInit = {}): Promise<T> {
  const encabezados = new Headers(opciones.headers);
  // La API rechaza toda operación que modifica si no trae este encabezado.
  if ((opciones.method ?? "GET") !== "GET") encabezados.set("X-Vitalia", "1");
  if (opciones.body) encabezados.set("Content-Type", "application/json");

  const respuesta = await fetch(BASE + ruta, {
    ...opciones,
    headers: encabezados,
    credentials: "include",
  });
  if (!respuesta.ok) {
    const error = await respuesta.json().catch(() => null);
    throw new ErrorDeApi(
      respuesta.status,
      error?.codigo ?? "desconocido",
      error?.mensaje ?? "No se pudo completar la operación. Intente de nuevo.",
      error?.detalle,
    );
  }
  if (respuesta.status === 204) return undefined as T;
  return (await respuesta.json()) as T;
}

export function enviar<T>(ruta: string, metodo: "POST" | "PUT" | "DELETE", cuerpo?: unknown) {
  return pedir<T>(ruta, {
    method: metodo,
    body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
  });
}
