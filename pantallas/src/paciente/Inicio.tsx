import "./Inicio.css";

import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router";

import { inicioDelPaciente } from "../api/citas";
import { consultorioPublico } from "../api/consultorio";
import { BotonSalir } from "../comunes/BotonSalir";
import { conMayuscula, cuandoCorto, fechaLarga, hora } from "../comunes/fechas";
import {
  CalendarBlankIcon,
  CalendarPlusIcon,
  MapPinIcon,
  PhoneIcon,
  StethoscopeIcon,
} from "../comunes/iconos";
import { BotonEnlace } from "../comunes/piezas/Boton";
import { Tarjeta } from "../comunes/piezas/Tarjeta";
import { useCuenta } from "../comunes/sesion";

function saludo(horaDelDia = new Date().getHours()) {
  if (horaDelDia < 12) return "Buenos días,";
  if (horaDelDia < 19) return "Buenas tardes,";
  return "Buenas noches,";
}

/** P-04. La próxima cita con mover y cancelar, y el acceso para agendar (HU-020, CA-1 y CA-2). */
export function Inicio() {
  const cuenta = useCuenta();
  const inicio = useQuery({ queryKey: ["inicio"], queryFn: inicioDelPaciente });
  const consultorio = useQuery({ queryKey: ["consultorio-publico"], queryFn: consultorioPublico });
  const proxima = inicio.data?.proxima;

  return (
    <main>
      <header className="zona-paciente__encabezado">
        <div>
          <p className="texto-suave inicio__saludo">{saludo()}</p>
          <h1>{cuenta.data?.nombres}</h1>
        </div>
        <BotonSalir className="zona-paciente__salir" />
      </header>

      {inicio.data &&
        (proxima ? (
          <section className="inicio__proxima" aria-label="Su próxima cita">
            <div className="inicio__proxima-encabezado">
              <span className="inicio__rotulo">
                <CalendarBlankIcon aria-hidden="true" />
                Su próxima cita
              </span>
              <span className="inicio__cuando">
                <span className="inicio__punto" aria-hidden="true" />
                {cuandoCorto(proxima.inicio)}
              </span>
            </div>
            <div className="inicio__hora">
              <span>{hora(proxima.inicio)}</span>
              <span className="inicio__detalle">
                {conMayuscula(fechaLarga(proxima.inicio))} · {proxima.tipo}
              </span>
            </div>
            <div className="inicio__datos">
              {inicio.data.direccion && (
                <span>
                  <MapPinIcon aria-hidden="true" />
                  {inicio.data.direccion}
                </span>
              )}
              {inicio.data.puede_cambiarla ? (
                <div className="inicio__acciones">
                  <Link to={`/paciente/citas/${proxima.id}/mover`}>Mover</Link>
                  <Link to={`/paciente/citas?cancelar=${proxima.id}`}>Cancelar</Link>
                </div>
              ) : (
                <span>
                  <PhoneIcon aria-hidden="true" />
                  Para cambiarla, llame al {inicio.data.telefono ?? "consultorio"}
                </span>
              )}
            </div>
          </section>
        ) : (
          <Tarjeta nombre="Sin citas próximas">
            <div className="inicio__vacio">
              <h2>No tiene citas próximas</h2>
              <p className="texto-suave">Elija el tipo de cita, el día y la hora que le sirvan.</p>
            </div>
          </Tarjeta>
        ))}

      <BotonEnlace a="/paciente/agendar" clase={proxima ? "borde" : "principal"}>
        <CalendarPlusIcon />
        {proxima ? "Agendar otra cita" : "Agendar una cita"}
      </BotonEnlace>

      {consultorio.data?.nombre && (
        <Tarjeta nombre="Su consultorio">
          <div className="inicio__consultorio">
            <span className="inicio__icono" aria-hidden="true">
              <StethoscopeIcon />
            </span>
            <div>
              <h2>{consultorio.data.nombre}</h2>
              {consultorio.data.medico && (
                <span className="texto-suave">{consultorio.data.medico} · Medicina general</span>
              )}
            </div>
          </div>
        </Tarjeta>
      )}
    </main>
  );
}
