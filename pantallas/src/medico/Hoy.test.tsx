import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { Hoy } from "./Hoy";

const HORA = 3_600_000;
const inicio = Date.now() + HORA;

const CITA = {
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

test("cancelar como médico exige el motivo", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/agenda/hoy": {
      cuerpo: { dia: "2026-10-26", citas: [CITA], proxima: CITA, pendientes: [] },
    },
    "POST /api/v1/citas/c1/cancelar": {
      estado: 400,
      cuerpo: {
        codigo: "datos_invalidos",
        mensaje: "Revise los datos.",
        detalle: { motivo: "Escriba el motivo de la cancelación" },
      },
    },
  });
  mostrar("/medico/hoy", { "/medico/hoy": <Hoy /> });

  await userEvent.click(
    await screen.findByRole("button", { name: "Cancelar la cita de Rosa Elena Duarte" }),
  );
  await userEvent.click(screen.getByRole("button", { name: "Cancelar la cita" }));

  expect(await screen.findByRole("alert")).toHaveTextContent("Escriba el motivo de la cancelación");
  expect(pedidos.find((p) => p.clave === "POST /api/v1/citas/c1/cancelar")?.cuerpo).toEqual({
    motivo: null,
  });
});

test("avisa lo que falta configurar con enlace a cada parte", async () => {
  apiDeMentira({
    "GET /api/v1/agenda/hoy": {
      cuerpo: { dia: "2026-10-26", citas: [], proxima: null, pendientes: ["horario", "consultorio"] },
    },
  });
  mostrar("/medico/hoy", { "/medico/hoy": <Hoy /> });

  expect(await screen.findByRole("link", { name: "el horario de atención" })).toHaveAttribute(
    "href",
    "/medico/configuracion",
  );
  expect(screen.getByRole("link", { name: "los datos del consultorio" })).toHaveAttribute(
    "href",
    "/medico/consultorio",
  );
  expect(screen.getByText(/los pacientes no pueden agendar/)).toBeVisible();
});

test("la que sigue tiene su tarjeta y se marca como atendida", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/agenda/hoy": {
      cuerpo: {
        dia: "2026-10-26",
        citas: [CITA],
        proxima: null,
        pendientes: [],
        sigue: { cita_id: "c1", edad: 68, documentos: 4, legibles: 3, ia_autorizada: true },
      },
    },
    "POST /api/v1/citas/c1/asistencia": { estado: 204 },
  });
  mostrar("/medico/hoy", { "/medico/hoy": <Hoy /> });

  const tarjeta = await screen.findByRole("region", { name: "La cita que sigue" });
  expect(tarjeta).toHaveTextContent("Consulta general · 30 min · 68 años");
  expect(tarjeta).toHaveTextContent("4 documentos subidos, 3 legibles");
  expect(screen.getByRole("link", { name: /Abrir la ficha/ })).toHaveAttribute(
    "href",
    "/medico/pacientes/p1",
  );
  // Todavía no es la hora: "no asistió" espera a que pase.
  expect(
    screen.getByRole("button", { name: "Marcar que Rosa Elena Duarte no asistió" }),
  ).toBeDisabled();

  await userEvent.click(screen.getByRole("button", { name: "Atendida" }));

  expect(pedidos.find((p) => p.clave === "POST /api/v1/citas/c1/asistencia")?.cuerpo).toEqual({
    estado: "atendida",
  });
});
