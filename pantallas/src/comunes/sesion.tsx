import { useQuery, useQueryClient } from "@tanstack/react-query";
import type { ReactNode } from "react";
import { Navigate, useNavigate } from "react-router";

import { cerrarSesion, miCuenta, type Rol } from "../api/cuentas";
import { Nota } from "./piezas/Nota";

export const CLAVE_DE_LA_CUENTA = ["yo"] as const;

export function useCuenta() {
  return useQuery({ queryKey: CLAVE_DE_LA_CUENTA, queryFn: miCuenta, retry: false });
}

export function inicioDe(rol: Rol) {
  return rol === "medico" ? "/medico" : "/paciente";
}

/** Muestra su contenido solo a quien tiene sesión con ese rol; a los demás los lleva a su sitio. */
export function ConSesion({ rol, children }: { rol: Rol; children: ReactNode }) {
  const cuenta = useCuenta();
  if (cuenta.isPending) return null;
  if (cuenta.isError) return <SinConexion />;
  if (!cuenta.data) return <Navigate to="/ingresar" replace />;
  if (cuenta.data.rol !== rol) return <Navigate to={inicioDe(cuenta.data.rol)} replace />;
  return children;
}

/** La dirección raíz: cada quien a su inicio, o a ingresar. */
export function PuertaDeEntrada() {
  const cuenta = useCuenta();
  if (cuenta.isPending) return null;
  if (cuenta.isError) return <SinConexion />;
  return <Navigate to={cuenta.data ? inicioDe(cuenta.data.rol) : "/ingresar"} replace />;
}

export function useCerrarSesion() {
  const consultas = useQueryClient();
  const navegar = useNavigate();
  return async () => {
    try {
      await cerrarSesion();
    } finally {
      // Nada de la sesión queda en memoria: al volver atrás no se ve información (HU-007).
      consultas.clear();
      navegar("/ingresar", { replace: true });
    }
  };
}

function SinConexion() {
  return (
    <main className="pantalla-movil">
      <Nota tono="rojo">No se pudo conectar con Vitalia. Revise su conexión e intente de nuevo.</Nota>
    </main>
  );
}
