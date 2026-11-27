import "./Ajustes.css";

import type { ReactNode } from "react";

import { ComputerIcon, MoonIcon, SunIcon } from "./iconos";
import { type Tema, useTema } from "./tema";

const OPCIONES: { tema: Tema; nombre: string; detalle: string; icono: ReactNode }[] = [
  {
    tema: "sistema",
    nombre: "Según el dispositivo",
    detalle: "Claro de día y oscuro de noche, si su celular o computador lo hace así.",
    icono: <ComputerIcon aria-hidden="true" />,
  },
  { tema: "claro", nombre: "Claro", detalle: "Fondo claro y letra oscura.", icono: <SunIcon aria-hidden="true" /> },
  { tema: "oscuro", nombre: "Oscuro", detalle: "Fondo oscuro y letra clara.", icono: <MoonIcon aria-hidden="true" /> },
];

/** Ajustes de la pantalla, iguales para el paciente y el médico (D-34). */
export function Ajustes({ className = "" }: { className?: string }) {
  const [tema, cambiar] = useTema();
  return (
    <main className={`ajustes ${className}`}>
      <header className="ajustes__encabezado">
        <h1>Ajustes</h1>
      </header>
      <fieldset className="ajustes__grupo">
        <legend className="ajustes__titulo">Apariencia</legend>
        <p className="texto-suave ajustes__ayuda">El cambio se guarda en este dispositivo.</p>
        <div className="ajustes__opciones">
          {OPCIONES.map((o) => (
            <label key={o.tema} className="ajustes__opcion">
              <input
                type="radio"
                name="tema"
                value={o.tema}
                checked={tema === o.tema}
                onChange={() => cambiar(o.tema)}
              />
              <span className="ajustes__icono">{o.icono}</span>
              <span className="ajustes__texto">
                <span className="ajustes__nombre">{o.nombre}</span>
                <span className="texto-suave">{o.detalle}</span>
              </span>
            </label>
          ))}
        </div>
      </fieldset>
    </main>
  );
}
