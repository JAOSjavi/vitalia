import { lazy, Suspense } from "react";
import { Route, Routes } from "react-router";

// Cada zona se descarga solo al entrar: el paciente no baja el panel del médico, ni al revés.
const ZonaPaciente = lazy(() => import("./paciente/ZonaPaciente"));
const ZonaMedico = lazy(() => import("./medico/ZonaMedico"));

export function Rutas() {
  return (
    <Suspense fallback={null}>
      <Routes>
        <Route path="/paciente/*" element={<ZonaPaciente />} />
        <Route path="/medico/*" element={<ZonaMedico />} />
      </Routes>
    </Suspense>
  );
}
