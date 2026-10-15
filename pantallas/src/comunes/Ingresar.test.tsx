import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { Ingresar } from "./Ingresar";

const PUBLICO = { cuerpo: { nombre: "Consultorio Dra. Camila Ríos", telefono: null, medico: null } };

async function ingresarCon(documento: string, contrasena: string) {
  await userEvent.type(screen.getByLabelText("Documento"), documento);
  await userEvent.type(screen.getByLabelText("Contraseña"), contrasena);
  await userEvent.click(screen.getByRole("button", { name: /Ingresar/ }));
}

test("ingresa con documento y contraseña y va al inicio de su rol", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/consultorio/publico": PUBLICO,
    "POST /api/v1/sesion": { cuerpo: { rol: "medico", vence: "2026-10-14T20:00:00Z" } },
  });
  mostrar("/ingresar", { "/ingresar": <Ingresar /> });

  expect(await screen.findByText("Consultorio Dra. Camila Ríos · Medicina general")).toBeVisible();
  await ingresarCon("52.345.678", "consultorio2026");

  expect(await screen.findByTestId("ubicacion")).toHaveTextContent("/medico");
  const ingreso = pedidos.find((p) => p.clave === "POST /api/v1/sesion");
  expect(ingreso?.cuerpo).toEqual({
    tipo_documento: "CC",
    numero_documento: "52.345.678",
    contrasena: "consultorio2026",
  });
  expect(ingreso?.encabezados.get("X-Vitalia")).toBe("1");
});

test("si falla, no dice si fue el documento o la contraseña", async () => {
  apiDeMentira({
    "GET /api/v1/consultorio/publico": PUBLICO,
    "POST /api/v1/sesion": {
      estado: 401,
      cuerpo: {
        codigo: "credenciales_invalidas",
        mensaje: "El documento o la contraseña no coinciden.",
      },
    },
  });
  mostrar("/ingresar", { "/ingresar": <Ingresar /> });

  await ingresarCon("41652318", "otra2026x");

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "El documento o la contraseña no coinciden.",
  );
  expect(screen.getByTestId("ubicacion")).toHaveTextContent("/ingresar");
});

test("la contraseña se puede mostrar mientras se escribe", async () => {
  apiDeMentira({ "GET /api/v1/consultorio/publico": PUBLICO });
  mostrar("/ingresar", { "/ingresar": <Ingresar /> });

  const contrasena = screen.getByLabelText("Contraseña");
  expect(contrasena).toHaveAttribute("type", "password");
  await userEvent.click(screen.getByRole("button", { name: "Mostrar la contraseña" }));

  expect(contrasena).toHaveAttribute("type", "text");
});
