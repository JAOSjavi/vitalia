import "./ZonaMedico.css";

import { Navigate, NavLink, Route, Routes } from "react-router";

import { HospitalIcon } from "../comunes/iconos";
import { BotonSalir } from "../comunes/BotonSalir";
import { Marca } from "../comunes/piezas/Marca";
import { DatosDelConsultorio } from "./DatosDelConsultorio";

// Panel del médico, pensado primero para computador; en celular el menú pasa arriba.
export default function ZonaMedico() {
  return (
    <div className="zona-medico">
      <aside className="zona-medico__menu">
        <Marca conNombre />
        <nav aria-label="Panel del médico" className="zona-medico__enlaces">
          <NavLink to="/medico/consultorio" className="zona-medico__enlace">
            <HospitalIcon aria-hidden="true" />
            Consultorio
          </NavLink>
        </nav>
        <BotonSalir className="zona-medico__enlace zona-medico__salir" />
      </aside>
      <Routes>
        <Route index element={<Navigate to="consultorio" replace />} />
        <Route path="consultorio" element={<DatosDelConsultorio />} />
        <Route path="*" element={<Navigate to="/medico" replace />} />
      </Routes>
    </div>
  );
}
