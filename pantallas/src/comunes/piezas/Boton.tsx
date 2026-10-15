import "./Boton.css";

import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Link } from "react-router";

export type ClaseDeBoton = "principal" | "borde" | "neutro";

type Propiedades = ButtonHTMLAttributes<HTMLButtonElement> & {
  clase?: ClaseDeBoton;
  children: ReactNode;
};

export function Boton({ clase = "principal", className, type = "button", ...resto }: Propiedades) {
  return <button type={type} className={`boton boton--${clase} ${className ?? ""}`} {...resto} />;
}

/** Un enlace que se ve como botón: lleva a otra pantalla. */
export function BotonEnlace({
  a,
  clase = "principal",
  children,
}: {
  a: string;
  clase?: ClaseDeBoton;
  children: ReactNode;
}) {
  return (
    <Link to={a} className={`boton boton--${clase}`}>
      {children}
    </Link>
  );
}
