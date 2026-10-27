import "./Inicio.css";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router";

import { inicioDelPaciente } from "../api/citas";
import { misDocumentos } from "../api/documentos";
import { BotonSalir } from "../comunes/BotonSalir";
import { conMayuscula, cuandoCorto, fechaLarga, hora } from "../comunes/fechas";
import {
  CalendarBlankIcon,
  CalendarPlusIcon,
  CaretRightIcon,
  FileTextIcon,
  MapPinIcon,
  PhoneIcon,
  PlusIcon,
} from "../comunes/iconos";
import { BotonEnlace } from "../comunes/piezas/Boton";
import { Tarjeta } from "../comunes/piezas/Tarjeta";
import { useCuenta } from "../comunes/sesion";

function saludo(horaDelDia = new Date().getHours()) {
  if (horaDelDia < 12) return "Buenos días,";
  if (horaDelDia < 19) return "Buenas tardes,";
  return "Buenas noches,";
}

function iniciales(nombres = "", apellidos = "") {
  return `${nombres.trim()[0] ?? ""}${(nombres.trim().split(" ")[1] ?? apellidos.trim())[0] ?? ""}`.toUpperCase();
}

/** P-04, como el tablero "Paciente · Inicio" del lienzo (HU-020, CA-1 y CA-2). */
export function Inicio() {
  const cuenta = useCuenta();
  const inicio = useQuery({ queryKey: ["inicio"], queryFn: inicioDelPaciente });
  const documentos = useQuery({ queryKey: ["mis-documentos"], queryFn: misDocumentos });
  const [menu, setMenu] = useState(false);
  const proxima = inicio.data?.proxima;
  const subidos = documentos.data?.documentos ?? [];
  const legibles = subidos.filter((d) => d.estado_lectura === "legible").length;

  return (
    <main>
      <header className="zona-paciente__encabezado">
        <div>
          <p className="texto-suave inicio__saludo">{saludo()}</p>
          <h1 className="inicio__nombre">{cuenta.data?.nombres}</h1>
        </div>
        <div className="inicio__perfil">
          <button
            type="button"
            className="inicio__avatar"
            aria-label="Mi perfil"
            aria-expanded={menu}
            onClick={() => setMenu(!menu)}
          >
            {iniciales(cuenta.data?.nombres, cuenta.data?.apellidos)}
          </button>
          {menu && (
            <div className="inicio__menu">
              <BotonSalir className="zona-paciente__salir" />
            </div>
          )}
        </div>
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
        {proxima ? <PlusIcon weight="bold" /> : <CalendarPlusIcon />}
        {proxima ? "Agendar otra cita" : "Agendar una cita"}
      </BotonEnlace>

      {documentos.data && (
        <Link to="/paciente/documentos" className="inicio__documentos">
          <span className="inicio__icono" aria-hidden="true">
            <FileTextIcon />
          </span>
          <span className="inicio__documentos-texto">
            <span className="inicio__documentos-titulo">Mis documentos</span>
            <span className="texto-suave">
              {subidos.length
                ? `${subidos.length} ${subidos.length === 1 ? "subido" : "subidos"} · ${legibles} ${legibles === 1 ? "legible" : "legibles"}`
                : "Suba sus historias, exámenes o fórmulas"}
            </span>
          </span>
          <CaretRightIcon aria-hidden="true" weight="bold" className="inicio__flecha" />
        </Link>
      )}
    </main>
  );
}
