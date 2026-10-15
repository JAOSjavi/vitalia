import type { FieldError, UseFormRegisterReturn } from "react-hook-form";

import { IdentificationCardIcon } from "./iconos";
import { TIPOS_DE_DOCUMENTO } from "../api/cuentas";
import { Campo, Entrada } from "./piezas/Campo";

type Propiedades = {
  id: string;
  tipo: UseFormRegisterReturn;
  numero: UseFormRegisterReturn;
  error?: FieldError;
  nombresLargos?: boolean;
};

/** Tipo y número de documento, uno al lado del otro, como en el lienzo. */
export function CampoDeDocumento({ id, tipo, numero, error, nombresLargos }: Propiedades) {
  return (
    <Campo id={id} etiqueta="Documento" error={error?.message}>
      <div className="documento">
        <select aria-label="Tipo de documento" className="selector documento__tipo" {...tipo}>
          {TIPOS_DE_DOCUMENTO.map((t) => (
            <option key={t.valor} value={t.valor}>
              {nombresLargos ? t.nombre : t.corto}
            </option>
          ))}
        </select>
        <Entrada
          id={id}
          icono={<IdentificationCardIcon />}
          className="entrada__control--dato"
          autoComplete="username"
          invalido={Boolean(error)}
          aria-describedby={error ? `${id}-error` : undefined}
          {...numero}
        />
      </div>
    </Campo>
  );
}
