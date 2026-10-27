import "./Hoy.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import { agendaDeHoy, cancelarCita, type Cita, type Pendiente } from "../api/citas";
import { ESTADOS_DE_CITA } from "../comunes/estados";
import { conMayuscula, fechaLarga, hora } from "../comunes/fechas";
import { ArrowsLeftRightIcon, CalendarPlusIcon, XIcon } from "../comunes/iconos";
import { Boton, BotonEnlace } from "../comunes/piezas/Boton";
import { Campo, Entrada } from "../comunes/piezas/Campo";
import { Estado } from "../comunes/piezas/Estado";
import { Nota } from "../comunes/piezas/Nota";
import { Tarjeta } from "../comunes/piezas/Tarjeta";

const PENDIENTES: Record<Pendiente, { texto: string; a: string }> = {
  horario: { texto: "el horario de atención", a: "/medico/configuracion" },
  tipos_cita: { texto: "los tipos de cita", a: "/medico/configuracion" },
  consultorio: { texto: "los datos del consultorio", a: "/medico/consultorio" },
};

function iniciales(nombre: string) {
  return nombre
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((parte) => parte[0])
    .join("")
    .toUpperCase();
}

/** M-01. Las citas de hoy por hora, con paciente, tipo y estado (HU-021, HU-017, HU-001 CA-4). */
export function Hoy() {
  const agenda = useQuery({ queryKey: ["agenda-hoy"], queryFn: agendaDeHoy });
  const ahora = Date.now();
  const citas = agenda.data?.citas ?? [];
  // La que sigue: la primera confirmada que todavía no termina.
  const sigue = citas.find((c) => c.estado === "confirmada" && Date.parse(c.fin) > ahora);

  return (
    <main className="zona-medico__contenido">
      <header className="hoy__encabezado">
        <div>
          <span className="texto-suave">
            {conMayuscula(fechaLarga(new Date()))} · {hora(new Date())}
          </span>
          <h1>Agenda de hoy</h1>
        </div>
        <BotonEnlace a="/medico/citas/nueva">
          <CalendarPlusIcon />
          Nueva cita
        </BotonEnlace>
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

      {agenda.data && !citas.length && (
        <Nota>
          {agenda.data.proxima
            ? `Hoy no tiene citas. La próxima es el ${fechaLarga(agenda.data.proxima.inicio)} a las ${hora(agenda.data.proxima.inicio)}, con ${agenda.data.proxima.paciente}.`
            : "Hoy no tiene citas, y no hay citas agendadas más adelante."}
        </Nota>
      )}

      {citas.length > 0 && (
        <Tarjeta nombre="Citas de hoy">
          <div className="hoy__cabecera">
            <h2>
              {citas.length} {citas.length === 1 ? "cita" : "citas"}
            </h2>
            <span className="texto-suave">
              {citas.filter((c) => c.estado === "atendida").length} atendidas ·{" "}
              {citas.filter((c) => c.estado === "confirmada").length} por atender
            </span>
          </div>
          {citas.map((cita) => (
            <FilaDeCita key={cita.id} cita={cita} sigue={cita.id === sigue?.id} />
          ))}
        </Tarjeta>
      )}
    </main>
  );
}

function FilaDeCita({ cita, sigue }: { cita: Cita; sigue: boolean }) {
  const consultas = useQueryClient();
  const [cancelando, setCancelando] = useState(false);
  const [motivo, setMotivo] = useState("");
  const [fallo, setFallo] = useState<string | null>(null);
  const cambiable = cita.estado === "confirmada" && Date.parse(cita.fin) > Date.now();
  const estado = sigue ? { nombre: "Sigue", tono: "azul" as const } : ESTADOS_DE_CITA[cita.estado];

  async function cancelar() {
    setFallo(null);
    try {
      await cancelarCita(cita.id, motivo);
      await consultas.invalidateQueries({ queryKey: ["agenda-hoy"] });
    } catch (error) {
      setFallo(
        error instanceof ErrorDeApi
          ? (Object.values(error.campos)[0] ?? error.message)
          : "No se pudo cancelar la cita.",
      );
    }
  }

  return (
    <div className="hoy__cita">
      <div className="hoy__fila">
        <div className="hoy__hora">
          <span>{hora(cita.inicio)}</span>
          <span className="texto-suave">{cita.duracion_minutos} min</span>
        </div>
        <span className="hoy__avatar" aria-hidden="true">
          {iniciales(cita.paciente)}
        </span>
        <div className="hoy__paciente">
          <span className="hoy__nombre">{cita.paciente}</span>
          <span className="texto-suave">
            {cita.tipo}
            {cita.fuera_de_horario ? " · por fuera del horario" : ""}
          </span>
        </div>
        <div className="hoy__acciones">
          <Estado tono={estado.tono}>{estado.nombre}</Estado>
          {cambiable && !cancelando && (
            <>
              <Link
                to={`/medico/citas/${cita.id}/mover`}
                state={{ cita }}
                className="hoy__accion"
                aria-label={`Mover la cita de ${cita.paciente}`}
              >
                <ArrowsLeftRightIcon />
              </Link>
              <button
                type="button"
                className="hoy__accion"
                aria-label={`Cancelar la cita de ${cita.paciente}`}
                onClick={() => setCancelando(true)}
              >
                <XIcon />
              </button>
            </>
          )}
        </div>
      </div>
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
            <Boton onClick={cancelar}>Cancelar la cita</Boton>
          </div>
        </div>
      )}
    </div>
  );
}
