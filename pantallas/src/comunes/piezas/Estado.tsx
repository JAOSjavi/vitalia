import "./Estado.css";

import type { ReactNode } from "react";

// "aro" es confirmada: un aro azul. "azul" es lo que sigue: punto azul lleno y texto azul.
export type TonoDeEstado = "verde" | "rojo" | "ambar" | "gris" | "aro" | "azul";

type Propiedades = {
  tono: TonoDeEstado;
  children: ReactNode;
};

// El nombre del estado va siempre escrito; el punto de color solo lo acompaña.
export function Estado({ tono, children }: Propiedades) {
  return (
    <span className={`estado estado--${tono}`}>
      <span className={`estado__punto estado__punto--${tono}`} aria-hidden="true" />
      {children}
    </span>
  );
}
