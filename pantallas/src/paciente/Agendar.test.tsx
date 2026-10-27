import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { diaIso, hora } from "../comunes/fechas";
import { Agendar } from "./Agendar";

const DIA = 86_400_000;
// Siempre en el futuro: la semana que viene, a las 9 y a las 9 y media de Colombia.
const dia = diaIso(new Date(Date.now() + 7 * DIA));
const nueve = `${dia}T09:00:00-05:00`;
const nueveYMedia = `${dia}T09:30:00-05:00`;
const diez = `${dia}T10:00:00-05:00`;

const TIPO = { id: "tipo-1", nombre: "Consulta general", duracion_minutos: 30, activo: true };

const AGENDA = {
  "GET /api/v1/tipos-cita": { cuerpo: [TIPO] },
  "GET /api/v1/consultorio/publico": {
    cuerpo: { nombre: "Consultorio", telefono: null, medico: "Dra. Camila Ríos" },
  },
  "GET /api/v1/disponibilidad?tipo_cita=tipo-1": {
    cuerpo: { tipo: TIPO, dias: [dia], dia, horas: [nueve, nueveYMedia] },
  },
};

async function elegirHasta(inicio: string) {
  await userEvent.click(await screen.findByRole("button", { name: /Consulta general/ }));
  await userEvent.click(await screen.findByRole("button", { name: hora(inicio) }));
  await userEvent.click(screen.getByRole("button", { name: "Continuar" }));
}

test("solo muestra las horas libres y agenda la elegida", async () => {
  const pedidos = apiDeMentira({ ...AGENDA, "POST /api/v1/citas": { estado: 201, cuerpo: { id: "c1" } } });
  mostrar("/paciente/agendar", { "/paciente/agendar": <Agendar /> });

  await userEvent.click(await screen.findByRole("button", { name: /Consulta general/ }));
  const manana = await screen.findByRole("group", { name: "Horas de la mañana" });
  expect(within(manana).getAllByRole("button").map((b) => b.textContent)).toEqual([
    hora(nueve),
    hora(nueveYMedia),
  ]);
  expect(screen.getByRole("button", { name: "Continuar" })).toBeDisabled();

  await userEvent.click(within(manana).getByRole("button", { name: hora(nueve) }));
  await userEvent.click(screen.getByRole("button", { name: "Continuar" }));
  await userEvent.click(screen.getByRole("button", { name: "Confirmar la cita" }));

  expect(await screen.findByTestId("ubicacion")).toHaveTextContent("/paciente/citas");
  expect(pedidos.find((p) => p.clave === "POST /api/v1/citas")?.cuerpo).toEqual({
    tipo_cita: "tipo-1",
    inicio: nueve,
    confirmar_repetida: false,
  });
});

test("si otro tomó el espacio, ofrece los más cercanos", async () => {
  const pedidos = apiDeMentira({
    ...AGENDA,
    "POST /api/v1/citas": {
      estado: 409,
      cuerpo: {
        codigo: "espacio_ocupado",
        mensaje: "Alguien tomó ese espacio mientras usted elegía. Estos son los más cercanos.",
        detalle: { alternativas: [diez] },
      },
    },
  });
  mostrar("/paciente/agendar", { "/paciente/agendar": <Agendar /> });

  await elegirHasta(nueve);
  await userEvent.click(screen.getByRole("button", { name: "Confirmar la cita" }));

  expect(await screen.findByRole("alert")).toHaveTextContent("Alguien tomó ese espacio");
  const cercanas = screen.getByRole("group", { name: "Horas cercanas" });
  await userEvent.click(within(cercanas).getByRole("button", { name: new RegExp(hora(diez)) }));
  await userEvent.click(screen.getByRole("button", { name: "Confirmar la cita" }));

  const intentos = pedidos.filter((p) => p.clave === "POST /api/v1/citas");
  expect(intentos.map((p) => (p.cuerpo as { inicio: string }).inicio)).toEqual([nueve, diez]);
  expect(screen.getByTestId("ubicacion")).toHaveTextContent("/paciente/agendar");
});
