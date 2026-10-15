import "./ZonaPaciente.css";

import { useQuery } from "@tanstack/react-query";
import { Navigate, Route, Routes } from "react-router";

import { PhoneIcon, StethoscopeIcon } from "../comunes/iconos";
import { consultorioPublico } from "../api/consultorio";
import { BotonSalir } from "../comunes/BotonSalir";
import { Marca } from "../comunes/piezas/Marca";
import { Tarjeta } from "../comunes/piezas/Tarjeta";
import { useCuenta } from "../comunes/sesion";

// Zona del paciente, pensada primero para celular.
export default function ZonaPaciente() {
  return (
    <div className="zona-paciente">
      <header className="zona-paciente__barra">
        <Marca conNombre />
        <BotonSalir className="zona-paciente__salir" />
      </header>
      <Routes>
        <Route index element={<Inicio />} />
        <Route path="*" element={<Navigate to="/paciente" replace />} />
      </Routes>
    </div>
  );
}

function saludo(hora = new Date().getHours()) {
  if (hora < 12) return "Buenos días,";
  if (hora < 19) return "Buenas tardes,";
  return "Buenas noches,";
}

function Inicio() {
  const cuenta = useCuenta();
  const consultorio = useQuery({ queryKey: ["consultorio-publico"], queryFn: consultorioPublico });

  return (
    <main className="zona-paciente__contenido">
      <div>
        <p className="texto-suave">{saludo()}</p>
        <h1>{cuenta.data?.nombres}</h1>
      </div>
      <Tarjeta nombre="Su consultorio">
        <div className="zona-paciente__consultorio">
          <span className="zona-paciente__icono" aria-hidden="true">
            <StethoscopeIcon />
          </span>
          {consultorio.data?.nombre ? (
            <div className="zona-paciente__datos">
              <h2>{consultorio.data.nombre}</h2>
              {consultorio.data.medico && (
                <span className="texto-suave">{consultorio.data.medico} · Medicina general</span>
              )}
              {consultorio.data.telefono && (
                <a href={`tel:${consultorio.data.telefono.replace(/\s/g, "")}`}>
                  <PhoneIcon aria-hidden="true" />
                  {consultorio.data.telefono}
                </a>
              )}
            </div>
          ) : (
            <p className="texto-suave">El consultorio todavía no ha registrado sus datos.</p>
          )}
        </div>
      </Tarjeta>
    </main>
  );
}
