import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { Bloqueos } from "./Bloqueos";

const CITA = {
  id: "c1",
  paciente_id: "p1",
  paciente: "Rosa Elena Duarte",
  tipo_id: "t1",
  tipo: "Control",
  inicio: "2031-09-08T15:00:00-05:00",
  fin: "2031-09-08T15:20:00-05:00",
  duracion_minutos: 20,
  estado: "confirmada",
  fuera_de_horario: false,
  motivo: null,
};

test("si el bloqueo tapa citas las muestra con mover y cancelar", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/bloqueos": { cuerpo: [] },
    "POST /api/v1/bloqueos": {
      estado: 409,
      cuerpo: {
        codigo: "bloqueo_con_citas",
        mensaje: "Ese tiempo tiene citas agendadas.",
        detalle: { citas: [CITA] },
      },
    },
    "POST /api/v1/citas/c1/cancelar": { estado: 204 },
  });
  mostrar("/medico/bloqueos?dia=2031-09-08", { "/medico/bloqueos": <Bloqueos /> });

  await userEvent.type(await screen.findByLabelText("Motivo"), "Congreso médico");
  await userEvent.click(screen.getByRole("button", { name: "Guardar el bloqueo" }));

  expect(await screen.findByText("Rosa Elena Duarte")).toBeVisible();
  expect(pedidos.find((p) => p.clave === "POST /api/v1/bloqueos")?.cuerpo).toEqual({
    inicio: "2031-09-08T00:00:00-05:00",
    fin: "2031-09-09T00:00:00-05:00",
    motivo: "Congreso médico",
  });
  expect(screen.getByRole("link", { name: /Mover/ })).toHaveAttribute(
    "href",
    "/medico/citas/c1/mover",
  );

  await userEvent.click(screen.getByRole("button", { name: /Cancelar/ }));

  expect(pedidos.find((p) => p.clave === "POST /api/v1/citas/c1/cancelar")?.cuerpo).toEqual({
    motivo: "Congreso médico",
  });
  expect(screen.queryByText("Rosa Elena Duarte")).toBeNull();
});

test("un bloqueo por horas manda esas horas y se lista para eliminarlo", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/bloqueos": {
      cuerpo: [
        {
          id: "b1",
          inicio: "2031-09-08T14:00:00-05:00",
          fin: "2031-09-08T17:00:00-05:00",
          motivo: "Vacuna",
        },
      ],
    },
    "POST /api/v1/bloqueos": { estado: 201, cuerpo: { id: "b2" } },
    "DELETE /api/v1/bloqueos/b1": { estado: 204 },
  });
  mostrar("/medico/bloqueos?dia=2031-09-08", { "/medico/bloqueos": <Bloqueos /> });

  await userEvent.click(await screen.findByLabelText("Todo el día"));
  await userEvent.type(screen.getByLabelText("Motivo"), "Junta");
  await userEvent.click(screen.getByRole("button", { name: "Guardar el bloqueo" }));

  expect(await screen.findByText(/El bloqueo quedó guardado/)).toBeVisible();
  expect(pedidos.find((p) => p.clave === "POST /api/v1/bloqueos")?.cuerpo).toMatchObject({
    inicio: "2031-09-08T08:00:00-05:00",
    fin: "2031-09-08T12:00:00-05:00",
  });

  await userEvent.click(screen.getByRole("button", { name: "Eliminar el bloqueo: Vacuna" }));
  await userEvent.click(screen.getByRole("button", { name: "Sí, eliminar" }));
  expect(pedidos.some((p) => p.clave === "DELETE /api/v1/bloqueos/b1")).toBe(true);
});
