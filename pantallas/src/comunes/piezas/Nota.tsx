import "./Nota.css";

import type { ReactNode } from "react";

type Propiedades = { tono?: "ambar" | "rojo"; children: ReactNode };

/** Aviso en caja blanca con un punto de color: ámbar para avisar, rojo para lo que falló. */
export function Nota({ tono = "ambar", children }: Propiedades) {
  return (
    <div className="nota" role={tono === "rojo" ? "alert" : "status"}>
      <span className={`nota__punto nota__punto--${tono}`} aria-hidden="true" />
      <div className="nota__texto">{children}</div>
    </div>
  );
}
