import "./Bloqueos.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { Link, useSearchParams } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import {
  bloqueosEntre,
  cancelarCita,
  crearBloqueo,
  eliminarBloqueo,
  type Bloqueo,
  type Cita,
} from "../api/citas";
import { conMayuscula, diaIso, fechaLarga, hora } from "../comunes/fechas";
import { ArrowsLeftRightIcon, TrashIcon, XIcon } from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada } from "../comunes/piezas/Campo";
import { Nota } from "../comunes/piezas/Nota";
import { Tarjeta } from "../comunes/piezas/Tarjeta";

/** "2026-10-14" más un día, sin salir de la fecha escrita. */
function diaSiguiente(dia: string) {
  const fecha = new Date(`${dia}T12:00:00-05:00`);
  return diaIso(new Date(fecha.getTime() + 86_400_000));
}

/** Cómo se lee un bloqueo: "jueves 16 de octubre, de 2:00 p. m. a 5:00 p. m." o varios días. */
export function cuandoEsElBloqueo(bloqueo: Bloqueo) {
  const inicio = new Date(bloqueo.inicio);
  const fin = new Date(bloqueo.fin);
  const diaInicio = diaIso(inicio);
  const ultimoDia = diaIso(new Date(fin.getTime() - 1));
  const enteros = hora(inicio) === hora(new Date(`${diaInicio}T00:00:00-05:00`)) &&
    diaIso(fin) !== diaIso(new Date(fin.getTime() - 1));
  if (diaInicio === ultimoDia) {
    return enteros
      ? `${conMayuscula(fechaLarga(inicio))}, todo el día`
      : `${conMayuscula(fechaLarga(inicio))}, de ${hora(inicio)} a ${hora(fin)}`;
  }
  return enteros
    ? `Del ${fechaLarga(inicio)} al ${fechaLarga(new Date(fin.getTime() - 1))}`
    : `Del ${fechaLarga(inicio)}, ${hora(inicio)}, al ${fechaLarga(fin)}, ${hora(fin)}`;
}

/** La parte de un día que tapa el bloqueo: "todo el día", "de 2:00 p. m. a 5:00 p. m.",
 * "desde las 2:00 p. m." o "hasta las 11:00 a. m.". El día va como "2026-10-29". */
export function tramoDelDia(bloqueo: Bloqueo, dia: string) {
  const empiezaAntes = diaIso(bloqueo.inicio) < dia;
  const siguePorLaNoche = diaIso(bloqueo.fin) > dia;
  if (empiezaAntes && siguePorLaNoche) return "todo el día";
  if (siguePorLaNoche) {
    return hora(bloqueo.inicio) === hora(`${dia}T00:00:00-05:00`)
      ? "todo el día"
      : `desde las ${hora(bloqueo.inicio)}`;
  }
  if (empiezaAntes) return `hasta las ${hora(bloqueo.fin)}`;
  return `de ${hora(bloqueo.inicio)} a ${hora(bloqueo.fin)}`;
}

/** M-09. Bloquear un tiempo del horario y ver los próximos bloqueos (HU-009). */
export function Bloqueos() {
  const consultas = useQueryClient();
  const [parametros] = useSearchParams();
  const hoy = diaIso(new Date());
  const diaInicial = parametros.get("dia") ?? hoy;
  const [desde, setDesde] = useState(diaInicial);
  const [hasta, setHasta] = useState(diaInicial);
  const [todoElDia, setTodoElDia] = useState(true);
  const [horaDesde, setHoraDesde] = useState("08:00");
  const [horaHasta, setHoraHasta] = useState("12:00");
  const [motivo, setMotivo] = useState("");
  const [errores, setErrores] = useState<Record<string, string>>({});
  const [afectadas, setAfectadas] = useState<Cita[]>([]);
  const [aviso, setAviso] = useState<string | null>(null);
  const [guardando, setGuardando] = useState(false);

  const ahora = new Date();
  const proximos = useQuery({
    queryKey: ["bloqueos", "proximos"],
    queryFn: () => bloqueosEntre(ahora, new Date(ahora.getTime() + 365 * 86_400_000)),
  });

  async function refrescar() {
    await Promise.all([
      consultas.invalidateQueries({ queryKey: ["bloqueos"] }),
      consultas.invalidateQueries({ queryKey: ["agenda-hoy"] }),
      consultas.invalidateQueries({ queryKey: ["calendario"] }),
    ]);
  }

  async function guardar(evento: FormEvent) {
    evento.preventDefault();
    setErrores({});
    setAviso(null);
    const inicio = `${desde}T${todoElDia ? "00:00" : horaDesde}:00-05:00`;
    const fin = todoElDia ? `${diaSiguiente(hasta)}T00:00:00-05:00` : `${hasta}T${horaHasta}:00-05:00`;
    setGuardando(true);
    try {
      await crearBloqueo({ inicio, fin, motivo });
      setAfectadas([]);
      setMotivo("");
      setAviso("El bloqueo quedó guardado. Ese tiempo ya no se ofrece a los pacientes.");
      await refrescar();
    } catch (error) {
      if (error instanceof ErrorDeApi && error.codigo === "bloqueo_con_citas") {
        setAfectadas((error.detalle as { citas: Cita[] }).citas);
      } else if (error instanceof ErrorDeApi) {
        setErrores(Object.keys(error.campos).length ? error.campos : { general: error.message });
      } else {
        setErrores({ general: "No se pudo conectar con Vitalia. Intente de nuevo." });
      }
    } finally {
      setGuardando(false);
    }
  }

  return (
    <main className="zona-medico__contenido zona-medico__contenido--angosto">
      <header className="bloqueos__encabezado">
        <h1>Bloquear horario</h1>
        <p className="texto-suave">
          El tiempo bloqueado deja de ofrecerse para agendar. Si ya tiene citas, primero hay que
          moverlas o cancelarlas.
        </p>
      </header>

      <Tarjeta nombre="Nuevo bloqueo">
        <form className="bloqueos__formulario" onSubmit={guardar}>
          <div className="bloqueos__fila">
            <Campo id="bloqueo-desde" etiqueta="Desde" error={errores.inicio}>
              <Entrada
                id="bloqueo-desde"
                type="date"
                min={hoy}
                value={desde}
                onChange={(e) => {
                  setDesde(e.target.value);
                  if (e.target.value > hasta) setHasta(e.target.value);
                }}
              />
            </Campo>
            <Campo id="bloqueo-hasta" etiqueta="Hasta" error={errores.fin}>
              <Entrada
                id="bloqueo-hasta"
                type="date"
                min={desde}
                value={hasta}
                onChange={(e) => setHasta(e.target.value)}
              />
            </Campo>
          </div>
          <label className="casilla" htmlFor="bloqueo-todo-el-dia">
            <input
              id="bloqueo-todo-el-dia"
              type="checkbox"
              checked={todoElDia}
              onChange={(e) => setTodoElDia(e.target.checked)}
            />
            <span>Todo el día</span>
          </label>
          {!todoElDia && (
            <div className="bloqueos__fila">
              <Campo id="bloqueo-hora-desde" etiqueta="Desde la hora">
                <Entrada
                  id="bloqueo-hora-desde"
                  type="time"
                  value={horaDesde}
                  onChange={(e) => setHoraDesde(e.target.value)}
                />
              </Campo>
              <Campo id="bloqueo-hora-hasta" etiqueta="Hasta la hora">
                <Entrada
                  id="bloqueo-hora-hasta"
                  type="time"
                  value={horaHasta}
                  onChange={(e) => setHoraHasta(e.target.value)}
                />
              </Campo>
            </div>
          )}
          <Campo
            id="bloqueo-motivo"
            etiqueta="Motivo"
            error={errores.motivo}
            ayuda="Solo lo ve usted. Por ejemplo: congreso médico, vacaciones."
          >
            <Entrada
              id="bloqueo-motivo"
              value={motivo}
              maxLength={120}
              onChange={(e) => setMotivo(e.target.value)}
            />
          </Campo>
          {errores.general && <Nota tono="rojo">{errores.general}</Nota>}
          {aviso && <Nota>{aviso}</Nota>}
          <div className="bloqueos__botones">
            <Boton type="submit" disabled={guardando}>
              Guardar el bloqueo
            </Boton>
          </div>
        </form>
      </Tarjeta>

      {afectadas.length > 0 && (
        <CitasAfectadas
          citas={afectadas}
          motivo={motivo}
          alCancelar={(id) => setAfectadas((lista) => lista.filter((c) => c.id !== id))}
        />
      )}

      <Tarjeta nombre="Próximos bloqueos">
        <div className="bloqueos__lista">
          <h2>Próximos bloqueos</h2>
          {proximos.data && !proximos.data.length && (
            <p className="texto-suave">No hay bloqueos por delante.</p>
          )}
          {proximos.data?.map((bloqueo) => (
            <FilaDeBloqueo key={bloqueo.id} bloqueo={bloqueo} alEliminar={refrescar} />
          ))}
        </div>
      </Tarjeta>
    </main>
  );
}

function CitasAfectadas({
  citas,
  motivo,
  alCancelar,
}: {
  citas: Cita[];
  motivo: string;
  alCancelar: (id: string) => void;
}) {
  const consultas = useQueryClient();
  const [fallo, setFallo] = useState<string | null>(null);

  async function cancelar(cita: Cita) {
    setFallo(null);
    try {
      await cancelarCita(cita.id, motivo.trim());
      await consultas.invalidateQueries({ queryKey: ["agenda-hoy"] });
      alCancelar(cita.id);
    } catch (error) {
      setFallo(
        error instanceof ErrorDeApi
          ? (Object.values(error.campos)[0] ?? error.message)
          : "No se pudo cancelar la cita.",
      );
    }
  }

  return (
    <section aria-label="Citas en ese tiempo" className="bloqueos__afectadas">
      <Nota tono="ambar">
        Ese tiempo tiene {citas.length === 1 ? "una cita agendada" : `${citas.length} citas agendadas`}.
        Muévalas o cancélelas y vuelva a guardar el bloqueo. Al cancelar, el paciente ve el motivo
        del bloqueo.
      </Nota>
      {fallo && <Nota tono="rojo">{fallo}</Nota>}
      {citas.map((cita) => (
        <div key={cita.id} className="bloqueos__cita">
          <div className="bloqueos__cita-datos">
            <span className="bloqueos__cita-cuando">
              {conMayuscula(fechaLarga(cita.inicio))} · {hora(cita.inicio)}
            </span>
            <span>
              <strong>{cita.paciente}</strong> <span className="texto-suave">· {cita.tipo}</span>
            </span>
          </div>
          <div className="bloqueos__cita-acciones">
            <Link
              to={`/medico/citas/${cita.id}/mover`}
              state={{ cita }}
              className="boton boton--borde bloqueos__accion"
            >
              <ArrowsLeftRightIcon aria-hidden="true" />
              Mover
            </Link>
            <Boton
              clase="neutro"
              className="bloqueos__accion bloqueos__cancelar"
              disabled={!motivo.trim()}
              title={motivo.trim() ? undefined : "Escriba primero el motivo del bloqueo"}
              onClick={() => cancelar(cita)}
            >
              <XIcon aria-hidden="true" weight="bold" />
              Cancelar
            </Boton>
          </div>
        </div>
      ))}
    </section>
  );
}

function FilaDeBloqueo({ bloqueo, alEliminar }: { bloqueo: Bloqueo; alEliminar: () => Promise<void> }) {
  const [confirmando, setConfirmando] = useState(false);
  const [fallo, setFallo] = useState<string | null>(null);

  async function eliminar() {
    setFallo(null);
    try {
      await eliminarBloqueo(bloqueo.id);
      await alEliminar();
    } catch (error) {
      setFallo(error instanceof ErrorDeApi ? error.message : "No se pudo eliminar el bloqueo.");
    }
  }

  return (
    <div className="bloqueos__bloqueo">
      <span className="bloqueos__punto" aria-hidden="true" />
      <div className="bloqueos__bloqueo-datos">
        <span className="bloqueos__bloqueo-cuando">{cuandoEsElBloqueo(bloqueo)}</span>
        <span className="texto-suave">{bloqueo.motivo}</span>
        {fallo && <span className="bloqueos__fallo">{fallo}</span>}
      </div>
      {confirmando ? (
        <div className="bloqueos__confirmar">
          <Boton clase="neutro" className="bloqueos__accion" onClick={() => setConfirmando(false)}>
            No
          </Boton>
          <Boton className="bloqueos__accion" onClick={eliminar}>
            Sí, eliminar
          </Boton>
        </div>
      ) : (
        <button
          type="button"
          className="bloqueos__eliminar"
          aria-label={`Eliminar el bloqueo: ${bloqueo.motivo}`}
          onClick={() => setConfirmando(true)}
        >
          <TrashIcon aria-hidden="true" />
        </button>
      )}
    </div>
  );
}
