// Las mismas reglas del servidor, para avisar mientras se escribe. Quien decide es el servidor.

const SEPARADORES = /[\s.-]/g;

export function faltasDeLaContrasena(contrasena: string, numeroDocumento: string): string | true {
  const faltas = [];
  if (contrasena.length < 8) faltas.push("Debe tener al menos 8 caracteres");
  if (!/\d/.test(contrasena)) faltas.push("Debe incluir al menos un número");
  const documento = numeroDocumento.replace(SEPARADORES, "").toUpperCase();
  if (documento && contrasena.replace(SEPARADORES, "").toUpperCase().includes(documento)) {
    faltas.push("No puede contener su número de documento");
  }
  return faltas.length ? faltas.join(". ") : true;
}

export function esMayorDeEdad(fechaDeNacimiento: string, hoy = new Date()): boolean {
  const [anio, mes, dia] = fechaDeNacimiento.split("-").map(Number);
  const cumplio = hoy.getMonth() + 1 > mes || (hoy.getMonth() + 1 === mes && hoy.getDate() >= dia);
  return hoy.getFullYear() - anio - (cumplio ? 0 : 1) >= 18;
}

export const CORREO = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
export const TELEFONO = /^\+?\d{7,15}$/;

export function sinSeparadores(valor: string) {
  return valor.replace(/[\s()-]/g, "");
}
