import { screen } from "@testing-library/react";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { atencion, FORMULARIO } from "../historia-de-prueba";
import { MiHistoria } from "./MiHistoria";

function pantalla(ruta = "/paciente/historia") {
  return mostrar(ruta, {
    "/paciente/historia": <MiHistoria />,
    "/paciente/historia/:atencion": <MiHistoria />,
  });
}

test("el paciente ve sus atenciones con el diagnóstico, la fórmula y la firma", async () => {
  apiDeMentira({
    "GET /api/v1/mi-historia": {
      cuerpo: [atencion({ notas: [{ texto: "La talla es 170 cm.", fecha: "2026-08-21T15:00:00Z", firma_nombre: "Camila Ríos", firma_registro: null }] })],
    },
    "GET /api/v1/historia-clinica/formulario": { cuerpo: FORMULARIO },
  });
  pantalla("/paciente/historia/a1");

  expect(await screen.findByRole("link", { name: /Hipertensión esencial \(primaria\)/ })).toHaveAttribute(
    "aria-current",
    "page",
  );
  expect(screen.getByText("Control de hipertensión arterial.")).toBeInTheDocument();
  expect(screen.getByText("128/82 mmHg")).toBeInTheDocument();
  expect(screen.getByText("36,5 °C")).toBeInTheDocument();
  expect(screen.getByText("Losartán 50 mg")).toBeInTheDocument();
  expect(screen.getByText(/1 tableta · vía oral · cada 12 horas · 90 días/)).toBeInTheDocument();
  expect(screen.getByText(/Firmada por/)).toHaveTextContent("Camila Ríos · Registro RM 79-4521");
  expect(screen.getByText("La talla es 170 cm.")).toBeInTheDocument();
});

test("sin atenciones cerradas lo dice", async () => {
  apiDeMentira({
    "GET /api/v1/mi-historia": { cuerpo: [] },
    "GET /api/v1/historia-clinica/formulario": { cuerpo: FORMULARIO },
  });
  pantalla();

  expect(await screen.findByText(/Todavía no tiene atenciones cerradas/)).toBeInTheDocument();
});
