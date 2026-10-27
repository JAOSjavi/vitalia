import "./ZonaPaciente.css";

import { NavLink, Navigate, Route, Routes, useLocation } from "react-router";

import { CalendarBlankIcon, HouseIcon } from "../comunes/iconos";
import { Agendar } from "./Agendar";
import { Inicio } from "./Inicio";
import { MisCitas } from "./MisCitas";

// Zona del paciente, pensada primero para celular.
export default function ZonaPaciente() {
  // Mientras agenda o mueve una cita, la barra de abajo cede su lugar a la elección.
  const enUnFlujo = /\/(agendar|mover)$/.test(useLocation().pathname);
  return (
    <div className="zona-paciente">
      <Routes>
        <Route index element={<Inicio />} />
        <Route path="citas" element={<MisCitas />} />
        <Route path="agendar" element={<Agendar />} />
        <Route path="citas/:cita/mover" element={<Agendar />} />
        <Route path="*" element={<Navigate to="/paciente" replace />} />
      </Routes>
      {!enUnFlujo && (
        <nav aria-label="Secciones" className="zona-paciente__secciones">
          <NavLink to="/paciente" end className="zona-paciente__seccion">
            <span className="zona-paciente__icono-seccion">
              <HouseIcon aria-hidden="true" />
            </span>
            Inicio
          </NavLink>
          <NavLink to="/paciente/citas" className="zona-paciente__seccion">
            <span className="zona-paciente__icono-seccion">
              <CalendarBlankIcon aria-hidden="true" />
            </span>
            Citas
          </NavLink>
        </nav>
      )}
    </div>
  );
}
