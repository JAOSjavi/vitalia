import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router";

import { abrirAtencion } from "../api/historia";
import { StethoscopeIcon } from "../comunes/iconos";

/**
 * Abre la atención del paciente (o la que ya tiene abierta) y lleva a ella (HU-042, CA-1 y CA-6).
 * Desde Hoy va con la cita; desde la ficha, sin cita.
 */
export function BotonAtender({
  paciente,
  cita,
  className,
  texto = "Atender",
}: {
  paciente: string;
  cita?: string;
  className?: string;
  texto?: string;
}) {
  const ir = useNavigate();
  const abrir = useMutation({
    mutationFn: () => abrirAtencion(paciente, cita),
    onSuccess: ({ id }) => ir(`/medico/atenciones/${id}`),
  });
  return (
    <button
      type="button"
      className={className}
      disabled={abrir.isPending}
      onClick={() => abrir.mutate()}
      title={abrir.isError ? "No se pudo abrir la atención. Intente de nuevo." : undefined}
    >
      <StethoscopeIcon aria-hidden="true" />
      {abrir.isError ? "Intente de nuevo" : texto}
    </button>
  );
}
