import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import CrearCuenta from "./CrearCuenta";

const TEXTOS = {
  "GET /api/v1/autorizaciones/texto?tipo=datos": {
    cuerpo: {
      id: "texto-datos-1",
      tipo: "datos",
      version: 1,
      vigente_desde: "2026-10-01T00:00:00Z",
      contenido: "Política completa.",
      puntos: [
        { titulo: "Quién responde", texto: "Consultorio Dra. Camila Ríos.", resaltado: false },
        { titulo: "Inteligencia artificial", texto: "Solo si lo autoriza.", resaltado: true },
      ],
    },
  },
  "GET /api/v1/autorizaciones/texto?tipo=ia": {
    cuerpo: {
      id: "texto-ia-1",
      tipo: "ia",
      version: 1,
      vigente_desde: "2026-10-01T00:00:00Z",
      contenido: "Autorización de IA.",
      puntos: [],
    },
  },
};

async function llenarHastaLaHoja(contrasena = "girasol2026") {
  await userEvent.type(screen.getByLabelText("Nombres"), "Rosa Elena");
  await userEvent.type(screen.getByLabelText("Apellidos"), "Duarte");
  await userEvent.type(screen.getByLabelText("Documento"), "41652318");
  await userEvent.type(screen.getByLabelText("Fecha de nacimiento"), "1958-03-02");
  await userEvent.type(screen.getByLabelText("Celular"), "318 555 0116");
  await userEvent.type(screen.getByLabelText("Correo"), "rosa@ejemplo.co");
  await userEvent.click(screen.getByRole("button", { name: "Continuar" }));
  await userEvent.type(await screen.findByLabelText("Cree su contraseña"), contrasena);
  await userEvent.click(screen.getByRole("button", { name: "Continuar" }));
}

test("la contraseña dice qué le falta antes de seguir", async () => {
  apiDeMentira(TEXTOS);
  mostrar("/crear-cuenta", { "/crear-cuenta": <CrearCuenta /> });

  await llenarHastaLaHoja("corta");

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Debe tener al menos 8 caracteres. Debe incluir al menos un número",
  );
  expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
});

test("sin aceptar el tratamiento de datos no se crea la cuenta", async () => {
  const pedidos = apiDeMentira(TEXTOS);
  mostrar("/crear-cuenta", { "/crear-cuenta": <CrearCuenta /> });

  await llenarHastaLaHoja();
  const hoja = await screen.findByRole("dialog", { name: "Tratamiento de sus datos" });
  expect(within(hoja).getByText(/Solo si lo autoriza/)).toBeVisible();
  await userEvent.click(within(hoja).getByRole("button", { name: "Aceptar y crear cuenta" }));

  expect(await within(hoja).findByRole("alert")).toHaveTextContent(
    "Para crear la cuenta debe autorizar el tratamiento de sus datos.",
  );
  expect(pedidos.some((p) => p.clave === "POST /api/v1/cuentas/registro")).toBe(false);
});

test("la casilla de IA va aparte y sin marcar no se autoriza", async () => {
  const pedidos = apiDeMentira({
    ...TEXTOS,
    "POST /api/v1/cuentas/registro": {
      estado: 201,
      cuerpo: { rol: "paciente", vence: "2026-10-14T20:00:00Z" },
    },
  });
  mostrar("/crear-cuenta", { "/crear-cuenta": <CrearCuenta /> });

  await llenarHastaLaHoja();
  const hoja = await screen.findByRole("dialog");
  const ia = within(hoja).getByLabelText(/analicen con inteligencia artificial/);
  expect(ia).not.toBeChecked();
  await userEvent.click(within(hoja).getByLabelText(/tratamiento de mis datos/));
  await userEvent.click(within(hoja).getByRole("button", { name: "Aceptar y crear cuenta" }));

  expect(await screen.findByTestId("ubicacion")).toHaveTextContent("/paciente");
  const registro = pedidos.find((p) => p.clave === "POST /api/v1/cuentas/registro");
  expect(registro?.cuerpo).toMatchObject({
    numero_documento: "41652318",
    texto_datos: "texto-datos-1",
    texto_ia: null,
  });
});
