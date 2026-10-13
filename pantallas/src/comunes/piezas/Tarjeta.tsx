import "./Tarjeta.css";

import type { ReactNode } from "react";

type Propiedades = {
  nombre: string;
  children: ReactNode;
};

export function Tarjeta({ nombre, children }: Propiedades) {
  return (
    <section className="tarjeta" aria-label={nombre}>
      {children}
    </section>
  );
}
