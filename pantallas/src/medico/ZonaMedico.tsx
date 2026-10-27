import "./ZonaMedico.css";

import { useQuery } from "@tanstack/react-query";
import { Navigate, NavLink, Route, Routes } from "react-router";

import { verConsultorio } from "../api/consultorio";
import {
  CalendarBlankIcon,
  CalendarCheckIcon,
  ClipboardTextIcon,
  CreditCardIcon,
  SignOutIcon,
  SlidersHorizontalIcon,
  UsersIcon,
} from "../comunes/iconos";
import { Marca } from "../comunes/piezas/Marca";
import { useCerrarSesion } from "../comunes/sesion";
import { Calendario } from "./Calendario";
import { Configuracion } from "./Configuracion";
import { DatosDelConsultorio } from "./DatosDelConsultorio";
import { Ficha } from "./Ficha";
import { Hoy } from "./Hoy";
import { NuevaCita } from "./NuevaCita";
import { Pacientes } from "./Pacientes";

export function iniciales(nombre: string) {
  return nombre
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((parte) => parte[0])
    .join("")
    .toUpperCase();
}

// Panel del médico, como en el lienzo (Médico · Hoy): menú a la izquierda y, abajo, quién
// está conectado. Bitácora y Cobro aparecen como "Pronto" hasta que existan (HU-037, HU-026).
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
          <NavLink to="/medico/calendario" className="zona-medico__enlace">
            <CalendarBlankIcon aria-hidden="true" />
            Calendario
          </NavLink>
          <NavLink to="/medico/pacientes" className="zona-medico__enlace">
            <UsersIcon aria-hidden="true" />
            Pacientes
          </NavLink>
          <NavLink to="/medico/configuracion" className="zona-medico__enlace">
            <SlidersHorizontalIcon aria-hidden="true" />
            Configuración
          </NavLink>
          <span className="zona-medico__enlace zona-medico__enlace--pronto" aria-disabled="true">
            <ClipboardTextIcon aria-hidden="true" />
            <span className="zona-medico__texto">Bitácora</span>
            <span className="zona-medico__pronto">Pronto</span>
          </span>
          <span className="zona-medico__enlace zona-medico__enlace--pronto" aria-disabled="true">
            <CreditCardIcon aria-hidden="true" />
            <span className="zona-medico__texto">Cobro</span>
            <span className="zona-medico__pronto">Pronto</span>
          </span>
        </nav>
        <QuienEsta />
      </aside>
      <Routes>
        <Route index element={<Navigate to="hoy" replace />} />
        <Route path="hoy" element={<Hoy />} />
        <Route path="calendario" element={<Calendario />} />
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

/** El médico conectado, con su registro profesional y el botón para salir. */
function QuienEsta() {
  const consultorio = useQuery({ queryKey: ["consultorio"], queryFn: verConsultorio });
  const cerrar = useCerrarSesion();
  const datos = consultorio.data;
  const nombre = datos
    ? `${datos.medico_nombres.split(" ")[0]} ${datos.medico_apellidos.split(" ")[0]}`.trim()
    : "";

  return (
    <div className="zona-medico__quien">
      <span className="zona-medico__avatar" aria-hidden="true">
        {iniciales(nombre)}
      </span>
      <div className="zona-medico__datos">
        <span className="zona-medico__nombre">{nombre}</span>
        {datos?.registro_profesional && (
          <span className="zona-medico__registro">{datos.registro_profesional}</span>
        )}
      </div>
      <button type="button" className="zona-medico__salir" aria-label="Cerrar sesión" onClick={cerrar}>
        <SignOutIcon aria-hidden="true" />
      </button>
    </div>
  );
}
