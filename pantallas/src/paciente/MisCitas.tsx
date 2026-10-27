import "./MisCitas.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Link, useLocation, useSearchParams } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import { cancelarCita, inicioDelPaciente, misCitas, type Cita } from "../api/citas";
import { ESTADOS_DE_CITA } from "../comunes/estados";
import { cuando, diaDelMes, fechaConAnio, fechaLarga, hora, mes } from "../comunes/fechas";
import { ArrowsLeftRightIcon, ClockIcon, PhoneIcon, PlusIcon, XIcon } from "../comunes/iconos";
import { Boton, BotonEnlace } from "../comunes/piezas/Boton";
import { Estado } from "../comunes/piezas/Estado";
import { Nota } from "../comunes/piezas/Nota";

/** "Hoy", "Mañana" o el día de la semana: la fecha ya va en el bloque de al lado. */
function diaCorto(momento: string) {
  const dia = cuando(momento);
  return dia === "Hoy" || dia === "Mañana" ? dia : dia.split(" ")[0];
}

/** P-06. Próximas primero, en orden de fecha; luego las anteriores (HU-013, HU-014, HU-015). */
export function MisCitas() {
  const consultas = useQueryClient();
  const citas = useQuery({ queryKey: ["mis-citas"], queryFn: misCitas });
  const inicio = useQuery({ queryKey: ["inicio"], queryFn: inicioDelPaciente });
  const [parametros, setParametros] = useSearchParams();
  const aviso = (useLocation().state as { aviso?: string } | null)?.aviso;
  const [fallo, setFallo] = useState<string | null>(null);
  const porCancelar = parametros.get("cancelar");

  const ahora = Date.now();
  const lista = citas.data ?? [];
  const proximas = lista.filter((c) => c.estado === "confirmada" && Date.parse(c.fin) > ahora);
  const anteriores = lista.filter((c) => !proximas.includes(c)).reverse();
  const horas = inicio.data?.anticipacion_horas ?? 24;

  async function cancelar(cita: Cita) {
    setFallo(null);
    try {
      await cancelarCita(cita.id);
      setParametros({});
      await consultas.invalidateQueries({ queryKey: ["mis-citas"] });
      await consultas.invalidateQueries({ queryKey: ["inicio"] });
    } catch (error) {
      setFallo(error instanceof ErrorDeApi ? error.message : "No se pudo cancelar la cita.");
    }
  }

  return (
    <main>
      <header className="zona-paciente__encabezado">
        <h1>Mis citas</h1>
        <Link to="/paciente/agendar" className="mis-citas__agendar">
          <PlusIcon aria-hidden="true" weight="bold" />
          Agendar
        </Link>
      </header>
      {aviso && <Nota>{aviso}</Nota>}
      {fallo && <Nota tono="rojo">{fallo}</Nota>}

      {citas.data && !lista.length && (
        <Nota>
          Todavía no tiene citas. <Link to="/paciente/agendar">Agende la primera</Link>
        </Nota>
      )}

      {proximas.length > 0 && (
        <section className="mis-citas__grupo">
          <h2>Próximas</h2>
          {proximas.map((cita) => {
            const puede = Date.parse(cita.inicio) - ahora > horas * 3_600_000;
            return (
              <article key={cita.id} className="mis-citas__cita">
                <div className="mis-citas__fila">
                  <span
                    className={`mis-citas__fecha ${cuando(cita.inicio) === "Hoy" ? "mis-citas__fecha--hoy" : ""}`}
                    aria-hidden="true"
                  >
                    <span>{mes(cita.inicio)}</span>
                    <span className="mis-citas__dia">{diaDelMes(cita.inicio)}</span>
                  </span>
                  <div className="mis-citas__datos">
                    <span className="mis-citas__tipo">{cita.tipo}</span>
                    <span className="texto-suave">
                      <ClockIcon aria-hidden="true" />
                      {diaCorto(cita.inicio)} · {hora(cita.inicio)} · {cita.duracion_minutos} min
                    </span>
                  </div>
                  <Estado tono={ESTADOS_DE_CITA[cita.estado].tono}>
                    {ESTADOS_DE_CITA[cita.estado].nombre}
                  </Estado>
                </div>
                {cita.motivo && <p className="texto-suave mis-citas__motivo">{cita.motivo}</p>}
                {!puede ? (
                  <>
                    <Nota>
                      Faltan menos de {horas} horas. Para moverla o cancelarla, llame al
                      consultorio.
                    </Nota>
                    {inicio.data?.telefono && (
                      <a
                        className="mis-citas__telefono"
                        href={`tel:${inicio.data.telefono.replace(/\s/g, "")}`}
                      >
                        <PhoneIcon aria-hidden="true" />
                        {inicio.data.telefono}
                      </a>
                    )}
                  </>
                ) : porCancelar === cita.id ? (
                  <Nota tono="rojo">
                    <span>
                      ¿Cancelar la cita del {fechaLarga(cita.inicio)} a las {hora(cita.inicio)}? El
                      espacio quedará libre para otra persona.
                    </span>
                    <div className="mis-citas__acciones">
                      <Boton clase="neutro" onClick={() => setParametros({})}>
                        No
                      </Boton>
                      <Boton onClick={() => cancelar(cita)}>Sí, cancelar</Boton>
                    </div>
                  </Nota>
                ) : (
                  <div className="mis-citas__acciones">
                    <BotonEnlace a={`/paciente/citas/${cita.id}/mover`} clase="borde">
                      <ArrowsLeftRightIcon />
                      Mover
                    </BotonEnlace>
                    <Boton
                      clase="neutro"
                      className="mis-citas__cancelar"
                      onClick={() => setParametros({ cancelar: cita.id })}
                    >
                      <XIcon />
                      Cancelar
                    </Boton>
                  </div>
                )}
              </article>
            );
          })}
        </section>
      )}

      {anteriores.length > 0 && (
        <section className="mis-citas__grupo">
          <h2>Anteriores</h2>
          <div className="mis-citas__anteriores">
            {anteriores.map((cita) => (
              <div key={cita.id} className="mis-citas__anterior">
                <div className="mis-citas__datos">
                  <span className="mis-citas__tipo">{cita.tipo}</span>
                  <span className="texto-suave">
                    {fechaConAnio(cita.inicio).replace(/ de /g, " ")} · {hora(cita.inicio)}
                  </span>
                  {cita.motivo && (
                    <span className="texto-suave mis-citas__motivo">Motivo: {cita.motivo}</span>
                  )}
                </div>
                <Estado tono={ESTADOS_DE_CITA[cita.estado].tono}>
                  {ESTADOS_DE_CITA[cita.estado].nombre}
                </Estado>
              </div>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
