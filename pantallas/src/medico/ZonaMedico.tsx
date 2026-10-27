import "./ZonaMedico.css";

import { Navigate, NavLink, Route, Routes } from "react-router";

import { CalendarCheckIcon, GearSixIcon, HospitalIcon, UsersIcon } from "../comunes/iconos";
import { BotonSalir } from "../comunes/BotonSalir";
import { Marca } from "../comunes/piezas/Marca";
import { Configuracion } from "./Configuracion";
import { DatosDelConsultorio } from "./DatosDelConsultorio";
import { Ficha } from "./Ficha";
import { Hoy } from "./Hoy";
import { NuevaCita } from "./NuevaCita";
import { Pacientes } from "./Pacientes";

// Panel del médico, pensado primero para computador; en celular el menú pasa arriba.
// Calendario, Bitácora y Cobro del lienzo llegan con sus historias (HU-022, HU-037, HU-026).
export default function ZonaMedico() {
  return (
    <div className="zona-medico">
      <aside className="zona-medico__menu">
        <Marca conNombre />
        <nav aria-label="Panel del médico" className="zona-medico__enlaces">
          <NavLink to="/medico/hoy" className="zona-medico__enlace">
            <CalendarCheckIcon aria-hidden="true" />
            Hoy
          </NavLink>
          <NavLink to="/medico/pacientes" className="zona-medico__enlace">
            <UsersIcon aria-hidden="true" />
            Pacientes
          </NavLink>
          <NavLink to="/medico/configuracion" className="zona-medico__enlace">
            <GearSixIcon aria-hidden="true" />
            Configuración
          </NavLink>
          <NavLink to="/medico/consultorio" className="zona-medico__enlace">
            <HospitalIcon aria-hidden="true" />
            Consultorio
          </NavLink>
        </nav>
        <BotonSalir className="zona-medico__enlace zona-medico__salir" />
      </aside>
      <Routes>
        <Route index element={<Navigate to="hoy" replace />} />
        <Route path="hoy" element={<Hoy />} />
        <Route path="pacientes" element={<Pacientes />} />
        <Route path="pacientes/:paciente" element={<Ficha />} />
        <Route path="citas/nueva" element={<NuevaCita />} />
        <Route path="citas/:cita/mover" element={<NuevaCita />} />
        <Route path="configuracion" element={<Configuracion />} />
        <Route path="consultorio" element={<DatosDelConsultorio />} />
        <Route path="*" element={<Navigate to="/medico" replace />} />
      </Routes>
    </div>
  );
}
