// Fechas y horas siempre en hora de Colombia, con las funciones del propio navegador.

const ZONA = "America/Bogota";

function formato(opciones: Intl.DateTimeFormatOptions) {
  return new Intl.DateTimeFormat("es-CO", { timeZone: ZONA, ...opciones });
}

const HORA = formato({ hour: "numeric", minute: "2-digit", hour12: true });
const FECHA_LARGA = formato({ weekday: "long", day: "numeric", month: "long" });
const FECHA_CORTA = formato({ weekday: "short", day: "numeric", month: "short" });
const FECHA_CON_ANIO = formato({ day: "numeric", month: "short", year: "numeric" });
const DIA_DE_LA_SEMANA = formato({ weekday: "short" });
const MES = formato({ month: "short" });
const DIA = formato({ day: "numeric" });
// En el formato canadiense el día sale como "2026-10-14".
const DIA_ISO = new Intl.DateTimeFormat("en-CA", {
  timeZone: ZONA,
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
});

/** Un día "2026-10-14" se lee como el mediodía de ese día en Colombia: nunca cambia de fecha. */
export function deDia(dia: string) {
  return new Date(`${dia}T12:00:00-05:00`);
}

/** "9:00 a. m." con espacios que no se cortan: en celular la hora no se parte en dos líneas. */
export function hora(momento: string | Date) {
  return HORA.format(new Date(momento)).replace(/\s/g, " ");
}

export function fechaLarga(momento: string | Date) {
  return FECHA_LARGA.format(new Date(momento));
}

export function fechaCorta(momento: string | Date) {
  return FECHA_CORTA.format(new Date(momento)).replace(/\./g, "");
}

export function fechaConAnio(momento: string | Date) {
  return FECHA_CON_ANIO.format(new Date(momento)).replace(/\./g, "");
}

export function diaDeLaSemana(momento: string | Date) {
  return DIA_DE_LA_SEMANA.format(new Date(momento)).replace(/\./g, "");
}

export function mes(momento: string | Date) {
  return MES.format(new Date(momento)).replace(/\./g, "").toUpperCase();
}

export function diaDelMes(momento: string | Date) {
  return DIA.format(new Date(momento));
}

/** El día en Colombia, como "2026-10-14". */
export function diaIso(momento: string | Date) {
  return DIA_ISO.format(new Date(momento));
}

export function esManana(momento: string) {
  return Number(formato({ hour: "numeric", hour12: false }).format(new Date(momento))) < 12;
}

/** "Hoy", "Mañana" o el día de la semana con la fecha. */
export function cuando(momento: string, ahora = new Date()) {
  const dia = diaIso(momento);
  if (dia === diaIso(ahora)) return "Hoy";
  if (dia === diaIso(new Date(ahora.getTime() + 86_400_000))) return "Mañana";
  const texto = fechaLarga(momento);
  return texto.charAt(0).toUpperCase() + texto.slice(1);
}

export function conMayuscula(texto: string) {
  return texto.charAt(0).toUpperCase() + texto.slice(1);
}

/** Para una etiqueta corta: "Hoy", "Mañana" o "mar 13 oct". */
export function cuandoCorto(momento: string, ahora = new Date()) {
  const largo = cuando(momento, ahora);
  return largo === "Hoy" || largo === "Mañana" ? largo : fechaCorta(momento);
}
