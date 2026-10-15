import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router";

import { Ingresar } from "./comunes/Ingresar";
import { ConSesion, PuertaDeEntrada } from "./comunes/sesion";

// Cada zona se descarga solo al entrar: el paciente no baja el panel del médico, ni al revés.
const ZonaPaciente = lazy(() => import("./paciente/ZonaPaciente"));
const CrearCuenta = lazy(() => import("./paciente/CrearCuenta"));
const ZonaMedico = lazy(() => import("./medico/ZonaMedico"));
const PuestaEnMarcha = lazy(() => import("./medico/PuestaEnMarcha"));

export function Rutas() {
  return (
    <Suspense fallback={null}>
      <Routes>
        <Route path="/" element={<PuertaDeEntrada />} />
        <Route path="/ingresar" element={<Ingresar />} />
        <Route path="/crear-cuenta" element={<CrearCuenta />} />
        <Route path="/puesta-en-marcha" element={<PuestaEnMarcha />} />
        <Route
          path="/paciente/*"
          element={
            <ConSesion rol="paciente">
              <ZonaPaciente />
            </ConSesion>
          }
        />
        <Route
          path="/medico/*"
          element={
            <ConSesion rol="medico">
              <ZonaMedico />
            </ConSesion>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}
