import "./Calendario.css";

import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router";

import { citasEntre, type Cita } from "../api/citas";
import { ESTADOS_DE_CITA } from "../comunes/estados";
import { festivo } from "../comunes/festivos";
import { diaIso, hora } from "../comunes/fechas";
import { CaretLeftIcon, CaretRightIcon, PlusIcon } from "../comunes/iconos";
import { Estado } from "../comunes/piezas/Estado";

type Vista = "dia" | "semana" | "mes";

const MESES = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
];
const DIAS = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
const CABECERAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];
const NOMBRE_DE_VISTA: Record<Vista, string> = { dia: "Día", semana: "Semana", mes: "Mes" };

/** "2026-10-13" de una fecha local; el navegador del consultorio está en hora de Colombia. */
function clave(fecha: Date) {
  const mes = String(fecha.getMonth() + 1).padStart(2, "0");
  const dia = String(fecha.getDate()).padStart(2, "0");
  return `${fecha.getFullYear()}-${mes}-${dia}`;
}

function sumarDias(fecha: Date, dias: number) {
  return new Date(fecha.getFullYear(), fecha.getMonth(), fecha.getDate() + dias);
}

function lunesDe(fecha: Date) {
  return sumarDias(fecha, -((fecha.getDay() + 6) % 7));
}

function cuenta(n: number) {
  return n === 1 ? "1 cita" : `${n} citas`;
}

function tituloDelDia(fecha: Date) {
  return `${DIAS[fecha.getDay()]} ${fecha.getDate()} de ${MESES[fecha.getMonth()].toLowerCase()}`;
}

/** Los días que se ven: el mes completo en semanas de lunes a domingo, la semana o el día. */
function diasVisibles(vista: Vista, fecha: Date) {
  if (vista === "dia") return [fecha];
  if (vista === "semana") return Array.from({ length: 7 }, (_, i) => sumarDias(lunesDe(fecha), i));
  const primero = new Date(fecha.getFullYear(), fecha.getMonth(), 1);
  const inicio = lunesDe(primero);
  const dias: Date[] = [];
  for (let i = 0; i < 42; i++) {
    const dia = sumarDias(inicio, i);
    if (i >= 28 && i % 7 === 0 && dia.getMonth() !== fecha.getMonth()) break;
    dias.push(dia);
  }
  return dias;
}

function titulo(vista: Vista, fecha: Date) {
  if (vista === "mes") return `${MESES[fecha.getMonth()]} de ${fecha.getFullYear()}`;
  if (vista === "dia") return `${tituloDelDia(fecha)} de ${fecha.getFullYear()}`;
  const lunes = lunesDe(fecha);
  const domingo = sumarDias(lunes, 6);
  const mismoMes = lunes.getMonth() === domingo.getMonth();
  return mismoMes
    ? `${lunes.getDate()} al ${domingo.getDate()} de ${MESES[domingo.getMonth()].toLowerCase()}`
    : `${lunes.getDate()} de ${MESES[lunes.getMonth()].toLowerCase()} al ${domingo.getDate()} de ${MESES[domingo.getMonth()].toLowerCase()}`;
}

function mover(vista: Vista, fecha: Date, paso: 1 | -1) {
  if (vista === "dia") return sumarDias(fecha, paso);
  if (vista === "semana") return sumarDias(fecha, 7 * paso);
  return new Date(fecha.getFullYear(), fecha.getMonth() + paso, 1);
}

/** M-02, como el tablero "Médico · Calendario" del lienzo, con vista de día, semana y mes (HU-022). */
export function Calendario() {
  const hoy = new Date();
  const [vista, setVista] = useState<Vista>("mes");
  const [fecha, setFecha] = useState(hoy);
  const [elegido, setElegido] = useState(clave(hoy));

  const dias = diasVisibles(vista, fecha);
  const desde = new Date(`${clave(dias[0])}T00:00:00-05:00`);
  const hasta = new Date(`${clave(sumarDias(dias[dias.length - 1], 1))}T00:00:00-05:00`);
  const citas = useQuery({
    queryKey: ["calendario", desde.toISOString(), hasta.toISOString()],
    queryFn: () => citasEntre(desde, hasta),
    placeholderData: keepPreviousData,
  });

  // Las canceladas no ocupan el día: no se cuentan ni se muestran.
  const porDia = new Map<string, Cita[]>();
  for (const cita of citas.data ?? []) {
    if (cita.estado === "cancelada") continue;
    const dia = diaIso(cita.inicio);
    porDia.set(dia, [...(porDia.get(dia) ?? []), cita]);
  }

  function elegir(dia: Date) {
    setElegido(clave(dia));
    if (vista === "mes" && dia.getMonth() !== fecha.getMonth()) setFecha(dia);
  }

  function cambiarVista(nueva: Vista) {
    setVista(nueva);
    const [a, m, d] = elegido.split("-").map(Number);
    setFecha(new Date(a, m - 1, d));
  }

  function pasar(paso: 1 | -1) {
    const nueva = mover(vista, fecha, paso);
    setFecha(nueva);
    if (vista !== "mes") setElegido(clave(vista === "dia" ? nueva : lunesDe(nueva)));
  }

  function irAHoy() {
    setFecha(hoy);
    setElegido(clave(hoy));
  }

  const [a, m, d] = elegido.split("-").map(Number);
  const diaElegido = new Date(a, m - 1, d);
  const unidad = vista === "dia" ? "Día" : vista === "semana" ? "Semana" : "Mes";

  return (
    <main className="zona-medico__contenido">
      <header className="calendario__encabezado">
        <h1>Calendario</h1>
        <div className="calendario__herramientas">
          <div role="group" aria-label="Vista" className="calendario__vistas">
            {(["dia", "semana", "mes"] as const).map((opcion) => (
              <button
                key={opcion}
                type="button"
                aria-pressed={vista === opcion}
                onClick={() => cambiarVista(opcion)}
              >
                {NOMBRE_DE_VISTA[opcion]}
              </button>
            ))}
          </div>
          <Link to={`/medico/citas/nueva?dia=${elegido}`} className="calendario__nueva">
            <PlusIcon aria-hidden="true" weight="bold" />
            Nueva cita
          </Link>
        </div>
      </header>

      <div className="calendario__barra">
        <div className="calendario__navegar">
          <button
            type="button"
            className="calendario__flecha"
            aria-label={`${unidad} anterior`}
            onClick={() => pasar(-1)}
          >
            <CaretLeftIcon aria-hidden="true" weight="bold" />
          </button>
          <h2 className="calendario__titulo">{titulo(vista, fecha)}</h2>
          <button
            type="button"
            className="calendario__flecha"
            aria-label={`${unidad} siguiente`}
            onClick={() => pasar(1)}
          >
            <CaretRightIcon aria-hidden="true" weight="bold" />
          </button>
          <button type="button" className="calendario__hoy" onClick={irAHoy}>
            Hoy
          </button>
        </div>
        <ul aria-label="Convenciones" className="calendario__convenciones">
          <li>
            <span className="calendario__marca calendario__marca--hoy" aria-hidden="true" />
            Hoy
          </li>
          <li>
            <span className="calendario__marca calendario__marca--citas" aria-hidden="true" />
            Con citas
          </li>
          <li>
            <span className="calendario__marca calendario__marca--festivo" aria-hidden="true" />
            Festivo
          </li>
        </ul>
      </div>

      <div className="calendario__cuerpo">
        {vista === "mes" && (
          <div className="calendario__desliza">
            <div className="calendario__mes">
              {CABECERAS.map((nombre) => (
                <span key={nombre} className="calendario__cabecera">
                  {nombre}
                </span>
              ))}
              {dias.map((dia) => {
                const k = clave(dia);
                const lista = porDia.get(k) ?? [];
                const deFestivo = festivo(dia);
                const enMes = dia.getMonth() === fecha.getMonth();
                const finDeSemana = dia.getDay() === 0 || dia.getDay() === 6;
                return (
                  <button
                    key={k}
                    type="button"
                    aria-pressed={k === elegido}
                    aria-label={`${tituloDelDia(dia)}, ${lista.length ? cuenta(lista.length) : "sin citas"}`}
                    className={[
                      "calendario__celda",
                      !enMes || finDeSemana ? "calendario__celda--apagada" : "",
                      k === elegido ? "calendario__celda--elegida" : "",
                    ].join(" ")}
                    onClick={() => elegir(dia)}
                  >
                    <span
                      className={`calendario__numero ${k === clave(hoy) ? "calendario__numero--hoy" : ""} ${enMes ? "" : "calendario__numero--fuera"}`}
                    >
                      {dia.getDate()}
                    </span>
                    {lista.length > 0 && (
                      <span className="calendario__ficha">
                        <span className="calendario__marca calendario__marca--citas" aria-hidden="true" />
                        {cuenta(lista.length)}
                      </span>
                    )}
                    {deFestivo && (
                      <span className="calendario__ficha">
                        <span className="calendario__marca calendario__marca--festivo" aria-hidden="true" />
                        Festivo
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {vista === "semana" && (
          <div className="calendario__desliza">
            <div className="calendario__semana">
              {dias.map((dia, indice) => {
                const k = clave(dia);
                const lista = porDia.get(k) ?? [];
                const deFestivo = festivo(dia);
                return (
                  <section
                    key={k}
                    aria-label={tituloDelDia(dia)}
                    className={`calendario__columna ${k === elegido ? "calendario__columna--elegida" : ""}`}
                  >
                    <button
                      type="button"
                      aria-pressed={k === elegido}
                      className="calendario__columna-cabecera"
                      onClick={() => elegir(dia)}
                    >
                      <span className="calendario__cabecera-dia">{CABECERAS[indice]}</span>
                      <span
                        className={`calendario__numero ${k === clave(hoy) ? "calendario__numero--hoy" : ""}`}
                      >
                        {dia.getDate()}
                      </span>
                    </button>
                    {deFestivo && (
                      <span className="calendario__ficha">
                        <span className="calendario__marca calendario__marca--festivo" aria-hidden="true" />
                        Festivo
                      </span>
                    )}
                    {lista.map((cita) => (
                      <Link
                        key={cita.id}
                        to={`/medico/pacientes/${cita.paciente_id}`}
                        className="calendario__bloque"
                      >
                        <span className="calendario__bloque-hora">{hora(cita.inicio)}</span>
                        <span className="calendario__bloque-nombre">{cita.paciente}</span>
                        <span className="calendario__bloque-tipo">{cita.tipo}</span>
                      </Link>
                    ))}
                  </section>
                );
              })}
            </div>
          </div>
        )}

        <DiaElegido
          dia={diaElegido}
          citas={porDia.get(elegido) ?? []}
          ancho={vista === "dia"}
        />
      </div>
    </main>
  );
}

function DiaElegido({ dia, citas, ancho }: { dia: Date; citas: Cita[]; ancho: boolean }) {
  const deFestivo = festivo(dia);
  return (
    <section
      aria-live="polite"
      aria-label="Día seleccionado"
      className={`calendario__panel ${ancho ? "calendario__panel--ancho" : ""}`}
    >
      <div className="calendario__panel-cabecera">
        <div>
          <span className="calendario__rotulo">Día seleccionado</span>
          <h2>{tituloDelDia(dia)}</h2>
        </div>
        <span className="calendario__cuenta">{citas.length ? cuenta(citas.length) : "Sin citas"}</span>
      </div>
      {deFestivo && (
        <p className="calendario__aviso">
          <span className="calendario__marca calendario__marca--festivo" aria-hidden="true" />
          <span>Festivo: {deFestivo}.</span>
        </p>
      )}
      {citas.length > 0 ? (
        <div className="calendario__citas">
          {citas.map((cita) => (
            <div key={cita.id} className="calendario__cita">
              <span className="calendario__cita-hora">{hora(cita.inicio)}</span>
              <div className="calendario__cita-datos">
                <Link to={`/medico/pacientes/${cita.paciente_id}`} className="calendario__cita-nombre">
                  {cita.paciente}
                </Link>
                <span className="texto-suave">{cita.tipo}</span>
              </div>
              <Estado tono={ESTADOS_DE_CITA[cita.estado].tono}>
                {ESTADOS_DE_CITA[cita.estado].nombre}
              </Estado>
            </div>
          ))}
        </div>
      ) : (
        <p className="calendario__vacio">No hay citas este día.</p>
      )}
      <Link to={`/medico/citas/nueva?dia=${clave(dia)}`} className="calendario__agendar">
        <PlusIcon aria-hidden="true" weight="bold" />
        Agendar en este día
      </Link>
    </section>
  );
}
