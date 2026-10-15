import "./Hoja.css";

import { useEffect, useRef, type ReactNode } from "react";

type Propiedades = {
  titulo: string;
  icono?: ReactNode;
  alCerrar: () => void;
  children: ReactNode;
};

/** Hoja que sube desde abajo sobre la pantalla, como la del tratamiento de datos. */
export function Hoja({ titulo, icono, alCerrar, children }: Propiedades) {
  const hoja = useRef<HTMLElement>(null);

  useEffect(() => {
    hoja.current?.focus();
    const conEscape = (evento: KeyboardEvent) => {
      if (evento.key === "Escape") alCerrar();
    };
    document.addEventListener("keydown", conEscape);
    return () => document.removeEventListener("keydown", conEscape);
  }, [alCerrar]);

  return (
    <div className="hoja">
      <div className="hoja__velo" aria-hidden="true" onClick={alCerrar} />
      <section
        ref={hoja}
        className="hoja__cuerpo"
        role="dialog"
        aria-modal="true"
        aria-labelledby="hoja-titulo"
        tabIndex={-1}
      >
        <span className="hoja__asa" aria-hidden="true" />
        <div className="hoja__encabezado">
          {icono && (
            <span className="hoja__icono" aria-hidden="true">
              {icono}
            </span>
          )}
          <h2 id="hoja-titulo">{titulo}</h2>
        </div>
        {children}
      </section>
    </div>
  );
}
