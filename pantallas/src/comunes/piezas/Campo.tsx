import "./Campo.css";

import { forwardRef, useState, type InputHTMLAttributes, type ReactNode } from "react";

import { EyeIcon, EyeSlashIcon } from "../iconos";

type Propiedades = {
  id: string;
  etiqueta: string;
  error?: string;
  ayuda?: string;
  children: ReactNode;
};

/** Etiqueta, control y, debajo, la ayuda o lo que le falta al dato. */
export function Campo({ id, etiqueta, error, ayuda, children }: Propiedades) {
  return (
    <div className="campo">
      <label htmlFor={id} className="campo__etiqueta">
        {etiqueta}
      </label>
      {children}
      {error ? (
        <p id={`${id}-error`} className="campo__error" role="alert">
          <span className="campo__punto" aria-hidden="true" />
          {error}
        </p>
      ) : (
        ayuda && (
          <p id={`${id}-ayuda`} className="campo__ayuda">
            {ayuda}
          </p>
        )
      )}
    </div>
  );
}

type PropiedadesDeEntrada = InputHTMLAttributes<HTMLInputElement> & {
  icono?: ReactNode;
  invalido?: boolean;
};

/** Caja de texto con icono opcional. Se usa con register() de React Hook Form. */
export const Entrada = forwardRef<HTMLInputElement, PropiedadesDeEntrada>(function Entrada(
  { icono, invalido, className, ...resto },
  referencia,
) {
  return (
    <div className={`entrada ${invalido ? "entrada--invalida" : ""}`}>
      {icono && (
        <span className="entrada__icono" aria-hidden="true">
          {icono}
        </span>
      )}
      <input
        ref={referencia}
        className={`entrada__control ${className ?? ""}`}
        aria-invalid={invalido || undefined}
        {...resto}
      />
    </div>
  );
});

/** Contraseña con el botón para mostrarla mientras se escribe. */
export const EntradaDeContrasena = forwardRef<HTMLInputElement, PropiedadesDeEntrada>(
  function EntradaDeContrasena({ icono, invalido, ...resto }, referencia) {
    const [visible, setVisible] = useState(false);
    return (
      <div className={`entrada entrada--con-boton ${invalido ? "entrada--invalida" : ""}`}>
        {icono && (
          <span className="entrada__icono" aria-hidden="true">
            {icono}
          </span>
        )}
        <input
          ref={referencia}
          type={visible ? "text" : "password"}
          className="entrada__control"
          aria-invalid={invalido || undefined}
          {...resto}
        />
        <button
          type="button"
          className="entrada__boton"
          aria-label={visible ? "Ocultar la contraseña" : "Mostrar la contraseña"}
          aria-pressed={visible}
          onClick={() => setVisible(!visible)}
        >
          {visible ? <EyeSlashIcon /> : <EyeIcon />}
        </button>
      </div>
    );
  },
);
