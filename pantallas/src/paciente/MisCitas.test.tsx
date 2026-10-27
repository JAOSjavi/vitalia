import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { MisCitas } from "./MisCitas";

const HORA = 3_600_000;

function citaEn(horas: number) {
  const inicio = Date.now() + horas * HORA;
  return {
    id: "c1",
    paciente_id: "p1",
    paciente: "Rosa Elena Duarte",
    tipo_id: "tipo-1",
    tipo: "Consulta general",
    inicio: new Date(inicio).toISOString(),
    fin: new Date(inicio + HORA / 2).toISOString(),
    duracion_minutos: 30,
    estado: "confirmada",
    fuera_de_horario: false,
    motivo: null,
  };
}

function api(horas: number) {
  return apiDeMentira({
    "GET /api/v1/citas": { cuerpo: [citaEn(horas)] },
    "GET /api/v1/yo/inicio": {
      cuerpo: {
        proxima: null,
        puede_cambiarla: true,
        anticipacion_horas: 24,
        telefono: "601 555 0100",
        direccion: null,
      },
    },
    "POST /api/v1/citas/c1/cancelar": { estado: 204 },
  });
}

test("cancelar pide confirmación antes de liberar el espacio", async () => {
  const pedidos = api(5 * 24);
  mostrar("/paciente/citas", { "/paciente/citas": <MisCitas /> });

  await userEvent.click(await screen.findByRole("button", { name: "Cancelar" }));
  expect(screen.getByRole("alert")).toHaveTextContent("El espacio quedará libre para otra persona.");
  expect(pedidos.some((p) => p.clave === "POST /api/v1/citas/c1/cancelar")).toBe(false);

  await userEvent.click(screen.getByRole("button", { name: "Sí, cancelar" }));

  await screen.findAllByRole("button", { name: "Cancelar" });
  expect(pedidos.find((p) => p.clave === "POST /api/v1/citas/c1/cancelar")?.cuerpo).toEqual({
    motivo: null,
  });
});

test("con menos de 24 horas no deja mover ni cancelar y muestra el teléfono", async () => {
  api(3);
  mostrar("/paciente/citas", { "/paciente/citas": <MisCitas /> });

  expect(await screen.findByText(/Faltan menos de 24 horas/)).toBeVisible();
  expect(screen.getByRole("link", { name: "601 555 0100" })).toHaveAttribute("href", "tel:6015550100");
  expect(screen.queryByRole("button", { name: "Cancelar" })).not.toBeInTheDocument();
  expect(screen.queryByRole("link", { name: "Mover" })).not.toBeInTheDocument();
});
