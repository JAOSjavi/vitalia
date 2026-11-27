// Festivos de Colombia (Ley 51 de 1983). Unos caen en su fecha; otros se corren al lunes
// siguiente; y los de Semana Santa y los que dependen de ella salen de la fecha de Pascua.

function clave(fecha: Date) {
  const mes = String(fecha.getMonth() + 1).padStart(2, "0");
  const dia = String(fecha.getDate()).padStart(2, "0");
  return `${fecha.getFullYear()}-${mes}-${dia}`;
}

function sumarDias(fecha: Date, dias: number) {
  return new Date(fecha.getFullYear(), fecha.getMonth(), fecha.getDate() + dias);
}

/** Si no cae en lunes, pasa al lunes siguiente. */
function alLunes(fecha: Date) {
  const faltan = (8 - fecha.getDay()) % 7;
  return sumarDias(fecha, faltan);
}

/** Domingo de Pascua, con el cálculo de Meeus para el calendario gregoriano. */
function pascua(anio: number) {
  const a = anio % 19;
  const b = Math.floor(anio / 100);
  const c = anio % 100;
  const d = Math.floor(b / 4);
  const e = b % 4;
  const f = Math.floor((b + 8) / 25);
  const g = Math.floor((b - f + 1) / 3);
  const h = (19 * a + b - d - g + 15) % 30;
  const i = Math.floor(c / 4);
  const k = c % 4;
  const l = (32 + 2 * e + 2 * i - h - k) % 7;
  const m = Math.floor((a + 11 * h + 22 * l) / 451);
  const mes = Math.floor((h + l - 7 * m + 114) / 31);
  const dia = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(anio, mes - 1, dia);
}

const memoria = new Map<number, Map<string, string>>();

/** Los festivos de un año, por día "2026-10-12", con su nombre. */
export function festivosDe(anio: number) {
  const guardados = memoria.get(anio);
  if (guardados) return guardados;
  const p = pascua(anio);
  const lista: [Date, string][] = [
    [new Date(anio, 0, 1), "Año Nuevo"],
    [alLunes(new Date(anio, 0, 6)), "Reyes Magos"],
    [alLunes(new Date(anio, 2, 19)), "San José"],
    [sumarDias(p, -3), "Jueves Santo"],
    [sumarDias(p, -2), "Viernes Santo"],
    [new Date(anio, 4, 1), "Día del Trabajo"],
    [sumarDias(p, 43), "Ascensión del Señor"],
    [sumarDias(p, 64), "Corpus Christi"],
    [sumarDias(p, 71), "Sagrado Corazón"],
    [alLunes(new Date(anio, 5, 29)), "San Pedro y San Pablo"],
    [new Date(anio, 6, 20), "Día de la Independencia"],
    [new Date(anio, 7, 7), "Batalla de Boyacá"],
    [alLunes(new Date(anio, 7, 15)), "Asunción de la Virgen"],
    [alLunes(new Date(anio, 9, 12)), "Día de la Raza"],
    [alLunes(new Date(anio, 10, 1)), "Todos los Santos"],
    [alLunes(new Date(anio, 10, 11)), "Independencia de Cartagena"],
    [new Date(anio, 11, 8), "Inmaculada Concepción"],
    [new Date(anio, 11, 25), "Navidad"],
  ];
  const festivos = new Map(lista.map(([fecha, nombre]) => [clave(fecha), nombre]));
  memoria.set(anio, festivos);
  return festivos;
}

export function festivo(fecha: Date) {
  return festivosDe(fecha.getFullYear()).get(clave(fecha)) ?? null;
}
