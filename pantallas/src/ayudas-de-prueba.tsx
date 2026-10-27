import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render } from "@testing-library/react";
import type { ReactNode } from "react";
import { MemoryRouter, Route, Routes, useLocation } from "react-router";
import { vi } from "vitest";

// "texto" es para las respuestas que llegan por partes, como las del asistente.
type Respuesta = { estado?: number; cuerpo?: unknown; texto?: string };

/** Reemplaza la API: cada "MÉTODO /ruta" devuelve lo indicado y queda anotado lo que se pidió. */
export function apiDeMentira(respuestas: Record<string, Respuesta>) {
  const pedidos: { clave: string; cuerpo: unknown; encabezados: Headers }[] = [];
  vi.stubGlobal(
    "fetch",
    vi.fn(async (ruta: string, opciones: RequestInit = {}) => {
      const clave = `${opciones.method ?? "GET"} ${ruta}`;
      pedidos.push({
        clave,
        // Un archivo llega como formulario y se guarda tal cual; lo demás es JSON.
        cuerpo:
          typeof opciones.body === "string" ? JSON.parse(opciones.body) : (opciones.body ?? undefined),
        encabezados: new Headers(opciones.headers),
      });
      const respuesta = respuestas[clave] ?? { estado: 404, cuerpo: { codigo: "no_existe" } };
      const estado = respuesta.estado ?? 200;
      return {
        ok: estado < 400,
        status: estado,
        json: async () => respuesta.cuerpo,
        text: async () => respuesta.texto ?? JSON.stringify(respuesta.cuerpo),
        body: null,
      };
    }),
  );
  return pedidos;
}

function Ubicacion() {
  return <output data-testid="ubicacion">{useLocation().pathname}</output>;
}

/** Muestra una pantalla dentro de un navegador de mentira que empieza en la ruta dada. */
export function mostrar(ruta: string, pantallas: Record<string, ReactNode>) {
  const consultas = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={consultas}>
      <MemoryRouter initialEntries={[ruta]}>
        <Routes>
          {Object.entries(pantallas).map(([camino, pantalla]) => (
            <Route key={camino} path={camino} element={pantalla} />
          ))}
          <Route path="*" element={null} />
        </Routes>
        <Ubicacion />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}
