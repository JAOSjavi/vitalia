import "./Estado.css";

import type { ReactNode } from "react";

export type TonoDeEstado = "verde" | "rojo" | "ambar" | "gris";

type Propiedades = {
  tono: TonoDeEstado;
  children: ReactNode;
};

// El nombre del estado va siempre escrito; el punto de color solo lo acompaña.
export function Estado({ tono, children }: Propiedades) {
  return (
    <span className="estado">
      <span className={`estado__punto estado__punto--${tono}`} aria-hidden="true" />
      {children}
    </span>
  );
}
