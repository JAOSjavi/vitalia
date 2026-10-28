import "./Hoy.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import {
  agendaDeHoy,
  cancelarCita,
  marcarAsistencia,
  verHorario,
  type Cita,
  type Franja,
  type Pendiente,
  type Bloqueo,
  type QuienSigue,
} from "../api/citas";
import { ESTADOS_DE_CITA } from "../comunes/estados";
import { conMayuscula, diaIso, fechaLarga, hora } from "../comunes/fechas";
import {
  ArrowRightIcon,
  ArrowsLeftRightIcon,
  CheckIcon,
  ClockIcon,
  FileTextIcon,
  LockKeyIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  SparkleIcon,
  UserMinusIcon,
  XIcon,
} from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada } from "../comunes/piezas/Campo";
import { Estado } from "../comunes/piezas/Estado";
import { Nota } from "../comunes/piezas/Nota";
import { tramoDelDia } from "./Bloqueos";
import { iniciales } from "./ZonaMedico";

const PENDIENTES: Record<Pendiente, { texto: string; a: string }> = {
  horario: { texto: "el horario de atención", a: "/medico/configuracion" },
  tipos_cita: { texto: "los tipos de cita", a: "/medico/configuracion" },
  consultorio: { texto: "los datos del consultorio", a: "/medico/consultorio" },
};

/** "08:00:00" como en el lienzo: "8:00 a. m."; el mediodía es "12:00 m.". */
function horaDeFranja(hhmm: string) {
  const [h, m] = hhmm.split(":").map(Number);
  if (h === 12 && m === 0) return "12:00 m.";
  const sufijo = h < 12 ? "a. m." : "p. m.";
  return `${h % 12 || 12}:${String(m).padStart(2, "0")} ${sufijo}`;
}

/** Los tiempos sin atención entre dos franjas del día, para mostrarlos entre las citas. */
function pausasDelDia(franjas: Franja[], dia: Date) {
  const isoDia = ((dia.getDay() + 6) % 7) + 1;
  const deHoy = franjas
    .filter((f) => f.dia_semana === isoDia)
    .sort((a, b) => a.hora_inicio.localeCompare(b.hora_inicio));
  return deHoy.slice(1).map((f, i) => ({ desde: deHoy[i].hora_fin, hasta: f.hora_inicio }));
}

/** Hora del día en Colombia como "14:30:00", para compararla con las franjas. */
function horaEnColombia(momento: string) {
  return new Intl.DateTimeFormat("en-GB", {
    timeZone: "America/Bogota",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date(momento));
}

function inicioDe(fila: { tipo: "cita"; cita: Cita } | { tipo: "bloqueo"; bloqueo: Bloqueo }) {
  return fila.tipo === "cita" ? fila.cita.inicio : fila.bloqueo.inicio;
}

/** M-01, como el tablero "Médico · Hoy" del lienzo (HU-021, HU-017, HU-018, HU-001 CA-4). */
export function Hoy() {
  const agenda = useQuery({ queryKey: ["agenda-hoy"], queryFn: agendaDeHoy });
  const horario = useQuery({ queryKey: ["horario"], queryFn: verHorario });
  const navegar = useNavigate();
  const [buscado, setBuscado] = useState("");
  const ahora = new Date();
  const citas = agenda.data?.citas ?? [];
  const activas = citas.filter((c) => c.estado !== "cancelada");
  const sigue = citas.find((c) => c.id === agenda.data?.sigue?.cita_id);
  const atendidas = activas.filter((c) => c.estado === "atendida").length;
  const porAtender = activas.filter((c) => c.estado === "confirmada").length;
  const pausas = pausasDelDia(horario.data?.franjas ?? [], ahora);

  function buscar(evento: FormEvent) {
    evento.preventDefault();
    navegar(`/medico/pacientes?buscar=${encodeURIComponent(buscado.trim())}`);
  }

  // Citas y bloqueos en orden de hora; cada pausa va antes de lo primero que empieza después.
  type Fila =
    | { tipo: "cita"; cita: Cita }
    | { tipo: "bloqueo"; bloqueo: Bloqueo }
    | { tipo: "pausa"; desde: string; hasta: string };
  type Evento = Exclude<Fila, { tipo: "pausa" }>;
  const eventos: Evento[] = [
    ...citas.map((cita) => ({ tipo: "cita" as const, cita })),
    ...(agenda.data?.bloqueos ?? []).map((bloqueo) => ({ tipo: "bloqueo" as const, bloqueo })),
  ].sort((a, b) => inicioDe(a).localeCompare(inicioDe(b)));
  const filas: Fila[] = [];
  const pendientesDePausa = [...pausas];
  for (const evento of eventos) {
    const empieza = horaEnColombia(inicioDe(evento));
    while (pendientesDePausa.length && empieza >= pendientesDePausa[0].hasta) {
      filas.push({ tipo: "pausa", ...pendientesDePausa.shift()! });
    }
    filas.push(evento);
  }

  return (
    <main className="zona-medico__contenido">
      <header className="hoy__encabezado">
        <div className="hoy__titulo">
          <span className="texto-suave">
            {conMayuscula(fechaLarga(ahora))} de {ahora.getFullYear()} ·{" "}
            {hora(ahora)}
          </span>
          <h1>Agenda de hoy</h1>
        </div>
        <div className="hoy__herramientas">
          <form role="search" className="hoy__buscar" onSubmit={buscar}>
            <MagnifyingGlassIcon aria-hidden="true" />
            <label htmlFor="buscar-paciente" className="visualmente-oculto">
              Buscar paciente
            </label>
            <input
              id="buscar-paciente"
              type="search"
              placeholder="Buscar paciente por nombre o documento"
              value={buscado}
              onChange={(evento) => setBuscado(evento.target.value)}
            />
          </form>
          <Link to="/medico/citas/nueva" className="hoy__nueva">
            <PlusIcon aria-hidden="true" weight="bold" />
            Nueva cita
          </Link>
        </div>
      </header>

      {agenda.data && agenda.data.pendientes.length > 0 && (
        <Nota>
          <span>
            Falta configurar{" "}
            {agenda.data.pendientes.map((p, indice) => (
              <span key={p}>
                {indice > 0 && (indice === agenda.data.pendientes.length - 1 ? " y " : ", ")}
                <Link to={PENDIENTES[p].a}>{PENDIENTES[p].texto}</Link>
              </span>
            ))}
            . Mientras falten, los pacientes no pueden agendar.
          </span>
        </Nota>
      )}

      <div className="hoy__cuerpo">
        {agenda.data && !citas.length && !agenda.data.bloqueos.length ? (
          <div className="hoy__lista hoy__lista--vacia">
            <Nota>
              {agenda.data.proxima
                ? `Hoy no tiene citas. La próxima es el ${fechaLarga(agenda.data.proxima.inicio)} a las ${hora(agenda.data.proxima.inicio)}, con ${agenda.data.proxima.paciente}.`
                : "Hoy no tiene citas, y no hay citas agendadas más adelante."}
            </Nota>
          </div>
        ) : (
          filas.length > 0 && (
            <section aria-label="Citas de hoy" className="hoy__lista">
              <div className="hoy__cabecera">
                <h2>
                  {activas.length} {activas.length === 1 ? "cita" : "citas"}
                </h2>
                <span className="texto-suave">
                  {atendidas} {atendidas === 1 ? "atendida" : "atendidas"} · {porAtender} por atender
                </span>
              </div>
              {filas.map((fila) =>
                fila.tipo === "bloqueo" ? (
                  <div key={`bloqueo-${fila.bloqueo.id}`} className="hoy__pausa hoy__bloqueo">
                    <span className="hoy__punto-bloqueo" aria-hidden="true" />
                    {conMayuscula(tramoDelDia(fila.bloqueo, diaIso(ahora)))} · Bloqueo:{" "}
                    {fila.bloqueo.motivo}
                  </div>
                ) : fila.tipo === "pausa" ? (
                  <div key={`pausa-${fila.desde}`} className="hoy__pausa">
                    <ClockIcon aria-hidden="true" />
                    {horaDeFranja(fila.desde)} a {horaDeFranja(fila.hasta)} · Sin atención
                  </div>
                ) : (
                  <FilaDeCita
                    key={fila.cita.id}
                    cita={fila.cita}
                    sigue={fila.cita.id === sigue?.id}
                  />
                ),
              )}
            </section>
          )
        )}

        {agenda.data && (
          <aside aria-label="Resumen" className="hoy__resumen">
            {sigue && agenda.data.sigue && <TarjetaSigue cita={sigue} datos={agenda.data.sigue} />}
            <section className="hoy__avance">
              <h2>Avance del día</h2>
              <div className="hoy__progreso">
                <div
                  role="img"
                  aria-label={`${atendidas} de ${activas.length} citas atendidas`}
                  className="hoy__barra"
                >
                  <span style={{ width: `${activas.length ? (atendidas / activas.length) * 100 : 0}%` }} />
                </div>
                <span className="texto-suave">
                  {atendidas} de {activas.length} citas atendidas
                </span>
              </div>
            </section>
            <div className="hoy__rapidos">
              <Link to="/medico/bloqueos" className="hoy__rapido">
                <LockKeyIcon aria-hidden="true" />
                Bloquear horario
              </Link>
            </div>
          </aside>
        )}
      </div>
    </main>
  );
}

function TarjetaSigue({ cita, datos }: { cita: Cita; datos: QuienSigue }) {
  const minutos = Math.round((Date.parse(cita.inicio) - Date.now()) / 60_000);
  const falta =
    minutos <= 0 ? "ahora" : minutos < 60 ? `en ${minutos} min` : `en ${Math.floor(minutos / 60)} h`;
  return (
    <section className="hoy__sigue" aria-label="La cita que sigue">
      <div className="hoy__sigue-cabecera">
        <span className="hoy__sigue-rotulo">Sigue · {hora(cita.inicio)}</span>
        <span className="hoy__sigue-falta">{falta}</span>
      </div>
      <div className="hoy__sigue-nombre">
        <h2>{cita.paciente}</h2>
        <span>
          {cita.tipo} · {cita.duracion_minutos} min · {datos.edad} años
        </span>
      </div>
      <ul className="hoy__sigue-datos">
        <li>
          <FileTextIcon aria-hidden="true" />
          {datos.documentos === 0
            ? "Sin documentos subidos"
            : `${datos.documentos} ${datos.documentos === 1 ? "documento subido" : "documentos subidos"}, ${datos.legibles} ${datos.legibles === 1 ? "legible" : "legibles"}`}
        </li>
        <li>
          <SparkleIcon aria-hidden="true" />
          {datos.ia_autorizada ? "Asistente de IA autorizado" : "Asistente de IA sin autorizar"}
        </li>
      </ul>
      <Link to={`/medico/pacientes/${cita.paciente_id}`} className="hoy__sigue-ficha">
        Abrir la ficha
        <ArrowRightIcon aria-hidden="true" weight="bold" />
      </Link>
    </section>
  );
}

function FilaDeCita({ cita, sigue }: { cita: Cita; sigue: boolean }) {
  const consultas = useQueryClient();
  const [cancelando, setCancelando] = useState(false);
  const [motivo, setMotivo] = useState("");
  const [fallo, setFallo] = useState<string | null>(null);
  const ahora = Date.now();
  // La asistencia se marca aunque la hora ya haya pasado; mover y cancelar, solo antes.
  const marcable = cita.estado === "confirmada";
  const cambiable = marcable && Date.parse(cita.fin) > ahora;
  const marcada = cita.estado === "atendida" || cita.estado === "no_asistio";
  const yaEmpezo = Date.parse(cita.inicio) <= ahora;
  const estado = sigue ? { nombre: "Sigue", tono: "azul" as const } : ESTADOS_DE_CITA[cita.estado];

  async function hacer(accion: () => Promise<void>, error: string) {
    setFallo(null);
    try {
      await accion();
      await consultas.invalidateQueries({ queryKey: ["agenda-hoy"] });
    } catch (problema) {
      setFallo(
        problema instanceof ErrorDeApi
          ? (Object.values(problema.campos)[0] ?? problema.message)
          : error,
      );
    }
  }

  const corregirA = cita.estado === "atendida" ? "no_asistio" : "atendida";

  return (
    <div className={`hoy__cita ${sigue ? "hoy__cita--sigue" : ""}`}>
      <div className="hoy__fila">
        <div className={`hoy__hora ${cita.estado === "confirmada" ? "hoy__hora--pendiente" : ""}`}>
          <span>{hora(cita.inicio)}</span>
          <span className="hoy__duracion">{cita.duracion_minutos} min</span>
        </div>
        <span className="hoy__avatar" aria-hidden="true">
          {iniciales(cita.paciente)}
        </span>
        <div className="hoy__paciente">
          <Link to={`/medico/pacientes/${cita.paciente_id}`} className="hoy__nombre">
            {cita.paciente}
          </Link>
          <span className="texto-suave">
            {cita.tipo}
            {cita.fuera_de_horario ? " · por fuera del horario" : ""}
          </span>
        </div>
        <div className="hoy__acciones">
          <Estado tono={estado.tono}>{estado.nombre}</Estado>
          {marcada && (
            <button
              type="button"
              className="hoy__corregir"
              onClick={() => hacer(() => marcarAsistencia(cita.id, corregirA), "No se pudo corregir.")}
            >
              Corregir
            </button>
          )}
          {marcable && !cancelando && (
            <>
              <button
                type="button"
                className={`hoy__atendida ${sigue ? "hoy__atendida--sigue" : ""}`}
                onClick={() =>
                  hacer(() => marcarAsistencia(cita.id, "atendida"), "No se pudo marcar.")
                }
              >
                <CheckIcon aria-hidden="true" weight="bold" />
                Atendida
              </button>
              <button
                type="button"
                className="hoy__accion"
                aria-label={`Marcar que ${cita.paciente} no asistió`}
                title={yaEmpezo ? undefined : "Se marca cuando la hora de la cita ya pasó"}
                disabled={!yaEmpezo}
                onClick={() =>
                  hacer(() => marcarAsistencia(cita.id, "no_asistio"), "No se pudo marcar.")
                }
              >
                <UserMinusIcon aria-hidden="true" />
              </button>
            </>
          )}
          {cambiable && !cancelando && (
            <>
              <Link
                to={`/medico/citas/${cita.id}/mover`}
                state={{ cita }}
                className="hoy__accion"
                aria-label={`Mover la cita de ${cita.paciente}`}
              >
                <ArrowsLeftRightIcon aria-hidden="true" />
              </Link>
              <button
                type="button"
                className="hoy__accion hoy__accion--cancelar"
                aria-label={`Cancelar la cita de ${cita.paciente}`}
                onClick={() => setCancelando(true)}
              >
                <XIcon aria-hidden="true" weight="bold" />
              </button>
            </>
          )}
        </div>
      </div>
      {fallo && !cancelando && (
        <div className="hoy__fallo">
          <Nota tono="rojo">{fallo}</Nota>
        </div>
      )}
      {cancelando && (
        <div className="hoy__cancelar">
          <Campo id={`motivo-${cita.id}`} etiqueta="Motivo de la cancelación" error={fallo ?? undefined}>
            <Entrada
              id={`motivo-${cita.id}`}
              value={motivo}
              onChange={(evento) => setMotivo(evento.target.value)}
              placeholder="El paciente lo verá en sus citas"
            />
          </Campo>
          <div className="hoy__botones">
            <Boton clase="neutro" onClick={() => setCancelando(false)}>
              Volver
            </Boton>
            <Boton
              onClick={() =>
                hacer(async () => {
                  await cancelarCita(cita.id, motivo);
                  setCancelando(false);
                }, "No se pudo cancelar la cita.")
              }
            >
              Cancelar la cita
            </Boton>
          </div>
        </div>
      )}
    </div>
  );
}
