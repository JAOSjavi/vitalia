
import { SignOutIcon } from "./iconos";
import { useCerrarSesion } from "./sesion";

export function BotonSalir({ className }: { className?: string }) {
  const cerrar = useCerrarSesion();
  return (
    <button type="button" className={className} onClick={cerrar}>
      <SignOutIcon />
      Salir
    </button>
  );
}
