import "./NuevaCita.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";
import { Link, useLocation, useNavigate, useParams, useSearchParams } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import {
  buscarPacientes,
  crearCita,
  moverCita,
  tiposDeCita,
  type Cita,
} from "../api/citas";
import { conMayuscula, fechaCorta, fechaLarga, hora } from "../comunes/fechas";
import { MagnifyingGlassIcon } from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada } from "../comunes/piezas/Campo";
import { Nota } from "../comunes/piezas/Nota";
import { Tarjeta } from "../comunes/piezas/Tarjeta";
import { SelectorDeEspacio } from "../comunes/SelectorDeEspacio";

type Paciente = { id: string; nombre: string };

/** M-03. Crear una cita para un paciente (HU-016) o mover una (HU-017), como médico. */
export function NuevaCita() {
  const { cita: citaId } = useParams();
  const [parametros] = useSearchParams();
  const cita = (useLocation().state as { cita?: Cita } | null)?.cita;
  const moviendo = Boolean(citaId);
  const navegar = useNavigate();
  const consultas = useQueryClient();

  const desdeLaLista = parametros.get("paciente");
  const [paciente, setPaciente] = useState<Paciente | null>(
    desdeLaLista ? { id: desdeLaLista, nombre: parametros.get("nombre") ?? "" } : null,
  );
  const [tipo, setTipo] = useState<string | null>(cita?.tipo_id ?? null);
  const [inicio, setInicio] = useState<string | null>(null);
  const [otraHora, setOtraHora] = useState({ dia: "", hora: "" });
  const [motivo, setMotivo] = useState("");
  const [fallo, setFallo] = useState<ReactNode>(null);
  const [alternativas, setAlternativas] = useState<string[]>([]);
  const tipos = useQuery({ queryKey: ["tipos-cita"], queryFn: tiposDeCita, enabled: !moviendo });

  if (moviendo && !cita) {
    return (
      <main className="zona-medico__contenido">
        <Nota>
          Abra la cita desde la <Link to="/medico/hoy">agenda de hoy</Link> para moverla.
        </Nota>
      </main>
    );
  }

  function usarOtraHora(valor: typeof otraHora) {
    setOtraHora(valor);
    // La hora escrita a mano se toma en hora de Colombia.
    setInicio(valor.dia && valor.hora ? `${valor.dia}T${valor.hora}:00-05:00` : null);
  }

  async function guardar(fueraDeHorario = false) {
    if (!inicio || !tipo) return;
    setFallo(null);
    setAlternativas([]);
    try {
      if (moviendo && citaId) {
        await moverCita(citaId, {
          inicio,
          motivo: motivo || undefined,
          confirmar_fuera_de_horario: fueraDeHorario,
        });
      } else if (paciente) {
        await crearCita({
          tipo_cita: tipo,
          inicio,
          paciente: paciente.id,
          confirmar_fuera_de_horario: fueraDeHorario,
        });
      }
      await consultas.invalidateQueries({ queryKey: ["agenda-hoy"] });
      navegar("/medico/hoy");
    } catch (error) {
      if (!(error instanceof ErrorDeApi)) {
        setFallo("No se pudo conectar con Vitalia. Intente de nuevo.");
      } else if (error.codigo === "fuera_de_horario") {
        setFallo(
          <>
            {error.message}
            <Boton clase="neutro" onClick={() => guardar(true)}>
              Darla de todas formas
            </Boton>
          </>,
        );
      } else if (error.codigo === "espacio_ocupado") {
        setFallo(error.message);
        setAlternativas((error.detalle as { alternativas: string[] }).alternativas);
        void consultas.invalidateQueries({ queryKey: ["disponibilidad"] });
      } else {
        setFallo(error.message);
      }
    }
  }

  return (
    <main className="zona-medico__contenido">
      <header>
        <h1 className="nueva-cita__titulo">{moviendo ? "Mover la cita" : "Nueva cita"}</h1>
        {moviendo && cita && (
          <p className="texto-suave">
            {cita.paciente} · {cita.tipo} · {fechaCorta(cita.inicio)} a las {hora(cita.inicio)}
          </p>
        )}
      </header>

      {!moviendo && (
        <Tarjeta nombre="Paciente">
          <div className="nueva-cita__seccion">
            <h2>Paciente</h2>
            {paciente ? (
              <div className="nueva-cita__elegido">
                <span className="nueva-cita__nombre">{paciente.nombre}</span>
                <button type="button" className="enlace" onClick={() => setPaciente(null)}>
                  Cambiar
                </button>
              </div>
            ) : (
              <BuscarPaciente alElegir={setPaciente} />
            )}
          </div>
        </Tarjeta>
      )}

      {!moviendo && paciente && (
        <Tarjeta nombre="Tipo de cita">
          <div className="nueva-cita__seccion">
            <h2>Tipo de cita</h2>
            <div className="nueva-cita__tipos" role="group" aria-label="Tipo de cita">
              {tipos.data?.map((t) => (
                <button
                  key={t.id}
                  type="button"
                  aria-pressed={t.id === tipo}
                  disabled={!t.activo}
                  onClick={() => {
                    setTipo(t.id);
                    setInicio(null);
                  }}
                >
                  {t.nombre}
                  <span className="texto-suave">{t.duracion_minutos} min</span>
                </button>
              ))}
            </div>
          </div>
        </Tarjeta>
      )}

      {tipo && (moviendo || paciente) && (
        <Tarjeta nombre="Día y hora">
          <div className="nueva-cita__seccion">
            <SelectorDeEspacio
              tipo={tipo}
              cita={citaId}
              elegido={inicio}
              alElegir={(elegido) => {
                setOtraHora({ dia: "", hora: "" });
                setInicio(elegido);
              }}
            />
            <details className="nueva-cita__otra">
              <summary>Otra hora, por fuera del horario</summary>
              <div className="rejilla">
                <Campo id="otra-dia" etiqueta="Día">
                  <Entrada
                    id="otra-dia"
                    type="date"
                    value={otraHora.dia}
                    onChange={(e) => usarOtraHora({ ...otraHora, dia: e.target.value })}
                  />
                </Campo>
                <Campo id="otra-hora" etiqueta="Hora">
                  <Entrada
                    id="otra-hora"
                    type="time"
                    value={otraHora.hora}
                    onChange={(e) => usarOtraHora({ ...otraHora, hora: e.target.value })}
                  />
                </Campo>
              </div>
            </details>
            {moviendo && (
              <Campo id="mover-motivo" etiqueta="Motivo del cambio (opcional)">
                <Entrada
                  id="mover-motivo"
                  value={motivo}
                  onChange={(e) => setMotivo(e.target.value)}
                  placeholder="El paciente lo verá en sus citas"
                />
              </Campo>
            )}
          </div>
        </Tarjeta>
      )}

      {fallo && <Nota tono="rojo">{fallo}</Nota>}
      {alternativas.length > 0 && (
        <div className="nueva-cita__alternativas" role="group" aria-label="Horas cercanas">
          {alternativas.map((a) => (
            <button key={a} type="button" onClick={() => setInicio(a)}>
              {fechaCorta(a)} · {hora(a)}
            </button>
          ))}
        </div>
      )}

      <div className="nueva-cita__acciones">
        {inicio && (
          <span>
            {conMayuscula(fechaLarga(inicio))} · <strong>{hora(inicio)}</strong>
          </span>
        )}
        <Boton clase="neutro" onClick={() => navegar(-1)}>
          Volver
        </Boton>
        <Boton disabled={!inicio || !tipo} onClick={() => guardar()}>
          {moviendo ? "Mover la cita" : "Crear la cita"}
        </Boton>
      </div>
    </main>
  );
}

function BuscarPaciente({ alElegir }: { alElegir: (paciente: Paciente) => void }) {
  const [texto, setTexto] = useState("");
  const resultado = useQuery({
    queryKey: ["pacientes", texto.trim(), 1],
    queryFn: () => buscarPacientes(texto, 1),
    enabled: texto.trim().length >= 2,
  });
  return (
    <div className="nueva-cita__buscar">
      <Entrada
        type="search"
        aria-label="Buscar paciente por nombre o documento"
        placeholder="Nombre o documento"
        icono={<MagnifyingGlassIcon />}
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
      />
      {resultado.data?.pacientes.map((p) => (
        <button
          key={p.id}
          type="button"
          className="nueva-cita__resultado"
          onClick={() => alElegir({ id: p.id, nombre: `${p.nombres} ${p.apellidos}` })}
        >
          <span className="nueva-cita__nombre">
            {p.nombres} {p.apellidos}
          </span>
          <span className="texto-suave">
            {p.tipo_documento} {p.numero_documento}
          </span>
        </button>
      ))}
      {resultado.data && !resultado.data.pacientes.length && (
        <p className="texto-suave">Ningún paciente coincide con la búsqueda.</p>
      )}
    </div>
  );
}
