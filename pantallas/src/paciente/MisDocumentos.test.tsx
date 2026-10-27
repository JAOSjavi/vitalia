import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { MisDocumentos } from "./MisDocumentos";

function documento(cambios: Record<string, unknown>) {
  return {
    id: "d1",
    nombre: "Control de presión",
    fecha_documento: "2026-08-20",
    tipo: "historia_clinica",
    formato: "pdf",
    tamano: 40_000,
    estado_lectura: "legible",
    paginas: 3,
    subido_en: "2026-10-27T15:00:00Z",
    ...cambios,
  };
}

const LISTA = {
  ia_autorizada: true,
  documentos: [
    documento({}),
    documento({
      id: "d2",
      nombre: "Fórmula médica",
      tipo: "formula",
      formato: "jpg",
      estado_lectura: "no_legible",
      paginas: 1,
    }),
  ],
};

function pantalla() {
  return mostrar("/paciente/documentos", { "/paciente/documentos": <MisDocumentos /> });
}

test("muestra cada documento con su estado, para verlo, y si autorizó el asistente", async () => {
  apiDeMentira({ "GET /api/v1/documentos": { cuerpo: LISTA } });
  pantalla();

  const lista = await screen.findByRole("region", { name: "Documentos subidos" });
  expect(screen.getByRole("heading", { name: "2 documentos subidos" })).toBeInTheDocument();
  expect(within(lista).getByText("Historia clínica · 20 ago 2026 · 3 pág.")).toBeInTheDocument();
  expect(within(lista).getByText("Fórmula · 20 ago 2026 · foto")).toBeInTheDocument();
  expect(within(lista).getByText("Legible")).toBeInTheDocument();
  expect(within(lista).getByText("No legible")).toBeInTheDocument();
  expect(within(lista).getByText(/Pruebe con una foto más nítida/)).toBeInTheDocument();
  expect(within(lista).getAllByRole("link", { name: "Ver" })[0]).toHaveAttribute(
    "href",
    "/api/v1/documentos/d1/archivo",
  );
  expect(screen.getByText("Asistente de IA autorizado")).toBeInTheDocument();
});

test("eliminar pide confirmación antes de borrar", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/documentos": { cuerpo: LISTA },
    "DELETE /api/v1/documentos/d1": { estado: 204 },
  });
  pantalla();

  await userEvent.click(await screen.findByRole("button", { name: "Eliminar Control de presión" }));
  expect(screen.getByRole("alert")).toHaveTextContent("La doctora y el asistente dejarán de verlo.");
  expect(pedidos.some((p) => p.clave.startsWith("DELETE"))).toBe(false);

  await userEvent.click(screen.getByRole("button", { name: "Sí, eliminar" }));

  await screen.findByRole("button", { name: "Eliminar Control de presión" });
  expect(pedidos.some((p) => p.clave === "DELETE /api/v1/documentos/d1")).toBe(true);
});

test("sube cada archivo con su nombre desde la hoja y la cierra al terminar", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/documentos": { cuerpo: { ia_autorizada: false, documentos: [] } },
    "POST /api/v1/documentos": { estado: 201, cuerpo: documento({ estado_lectura: "en_proceso" }) },
  });
  pantalla();
  await screen.findByText(/Todavía no ha subido documentos/);

  await userEvent.click(screen.getByRole("button", { name: "Subir" }));
  const hoja = screen.getByRole("dialog", { name: "Subir documentos" });
  const pdf = new File(["%PDF-1.4"], "laboratorios_agosto.pdf", { type: "application/pdf" });
  await userEvent.upload(within(hoja).getByTestId("elegir-archivos"), pdf);
  expect(within(hoja).getByLabelText("Nombre del documento laboratorios_agosto.pdf")).toHaveValue(
    "laboratorios agosto",
  );

  await userEvent.click(within(hoja).getByRole("button", { name: "Subir documento" }));

  await screen.findByText(/Todavía no ha subido documentos/);
  expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  const [envio] = pedidos.filter((p) => p.clave === "POST /api/v1/documentos");
  const formulario = envio.cuerpo as FormData;
  expect(formulario.get("nombre")).toBe("laboratorios agosto");
  expect(formulario.get("tipo")).toBe("historia_clinica");
  expect((formulario.get("archivo") as File).name).toBe("laboratorios_agosto.pdf");
  expect(envio.encabezados.get("X-Vitalia")).toBe("1");
});

test("rechaza antes de enviar lo que no es PDF, JPG o PNG", async () => {
  apiDeMentira({ "GET /api/v1/documentos": { cuerpo: { ia_autorizada: true, documentos: [] } } });
  pantalla();
  await userEvent.click(await screen.findByRole("button", { name: "Subir" }));

  // Sin filtrar por "accept": así llega también el que el navegador dejaría elegir igual.
  await userEvent
    .setup({ applyAccept: false })
    .upload(screen.getByTestId("elegir-archivos"), new File(["PK"], "examen.zip"));

  expect(screen.getByRole("alert")).toHaveTextContent("Solo se aceptan archivos PDF, JPG o PNG.");
  expect(screen.queryByRole("button", { name: /Subir documento/ })).not.toBeInTheDocument();
});

test("si el servidor rechaza el archivo, dice por qué y deja reintentar", async () => {
  apiDeMentira({
    "GET /api/v1/documentos": { cuerpo: { ia_autorizada: true, documentos: [] } },
    "POST /api/v1/documentos": {
      estado: 400,
      cuerpo: {
        codigo: "datos_invalidos",
        mensaje: "Revise los datos.",
        detalle: { archivo: "Solo se aceptan archivos PDF, JPG o PNG" },
      },
    },
  });
  pantalla();
  await userEvent.click(await screen.findByRole("button", { name: "Subir" }));

  await userEvent.upload(
    screen.getByTestId("elegir-archivos"),
    new File(["no es pdf"], "falso.pdf", { type: "application/pdf" }),
  );
  await userEvent.click(screen.getByRole("button", { name: "Subir documento" }));

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Solo se aceptan archivos PDF, JPG o PNG",
  );
  expect(screen.getByRole("button", { name: "Reintentar" })).toBeInTheDocument();
});
