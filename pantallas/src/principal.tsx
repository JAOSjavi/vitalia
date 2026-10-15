import "@fontsource/zilla-slab/latin-600.css";
import "@fontsource/zilla-slab/latin-700.css";
import "@fontsource/atkinson-hyperlegible-next/latin-400.css";
import "@fontsource/atkinson-hyperlegible-next/latin-600.css";
import "@fontsource/atkinson-hyperlegible-next/latin-700.css";
import "@fontsource/atkinson-hyperlegible-mono/latin-400.css";
import "@fontsource/atkinson-hyperlegible-mono/latin-600.css";
import "./comunes/estilos/variables.css";
import "./comunes/estilos/base.css";

import { MutationCache, QueryCache, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";

import { IconContext } from "./comunes/iconos";
import { ErrorDeApi } from "./api/cliente";
import { CLAVE_DE_LA_CUENTA } from "./comunes/sesion";
import { Rutas } from "./Rutas";

// Si la sesión vence mientras se usa la aplicación, se olvida la cuenta y las zonas con sesión
// llevan a ingresar de nuevo (HU-007, CA-2).
function siLaSesionTermino(error: Error) {
  if (error instanceof ErrorDeApi && error.codigo === "sin_sesion") {
    consultas.setQueryData(CLAVE_DE_LA_CUENTA, null);
  }
}

const consultas: QueryClient = new QueryClient({
  queryCache: new QueryCache({ onError: siLaSesionTermino }),
  mutationCache: new MutationCache({ onError: siLaSesionTermino }),
  defaultOptions: { queries: { retry: false, refetchOnWindowFocus: true } },
});

// Todos los iconos salen de Phosphor en un solo grosor, fijado aquí.
const ICONOS = { weight: "duotone", size: 22 } as const;

createRoot(document.getElementById("raiz")!).render(
  <StrictMode>
    <QueryClientProvider client={consultas}>
      <IconContext.Provider value={ICONOS}>
        <BrowserRouter>
          <Rutas />
        </BrowserRouter>
      </IconContext.Provider>
    </QueryClientProvider>
  </StrictMode>,
);
