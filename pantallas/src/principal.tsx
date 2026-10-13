import "@fontsource/zilla-slab/latin-600.css";
import "@fontsource/zilla-slab/latin-700.css";
import "@fontsource/atkinson-hyperlegible-next/latin-400.css";
import "@fontsource/atkinson-hyperlegible-next/latin-600.css";
import "@fontsource/atkinson-hyperlegible-next/latin-700.css";
import "@fontsource/atkinson-hyperlegible-mono/latin-400.css";
import "@fontsource/atkinson-hyperlegible-mono/latin-600.css";
import "./comunes/estilos/variables.css";
import "./comunes/estilos/base.css";

import { IconContext } from "@phosphor-icons/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";

import { Rutas } from "./Rutas";

const consultas = new QueryClient();

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
