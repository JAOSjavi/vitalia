import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { Calendario } from "./Calendario";

const hoy = new Date();
const aLas = (horas: number) =>
  new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate(), horas).toISOString();

function cita(id: string, paciente: string, horas: number, estado = "confirmada") {
  return {
    id,
    paciente_id: `p-${id}`,
    paciente,
    tipo_id: "t1",
    tipo: "Control",
    inicio: aLas(horas),
    fin: aLas(horas + 1),
    duracion_minutos: 30,
    estado,
    fuera_de_horario: false,
    motivo: null,
  };
}

test("el mes cuenta las citas de cada día y el día elegido las lista", async () => {
  apiDeMentira({
    "GET /api/v1/citas": {
      cuerpo: [
        cita("a", "Rosa Elena Duarte", 9, "atendida"),
        cita("b", "Carlos Muñoz", 10),
        cita("c", "Cancelada Antes", 11, "cancelada"),
      ],
    },
  });
  mostrar("/medico/calendario", { "/medico/calendario": <Calendario /> });

  // Las canceladas no cuentan.
  const dia = await screen.findByRole("button", { name: /, 2 citas$/ });
  expect(dia).toHaveAttribute("aria-pressed", "true");
  const panel = screen.getByRole("region", { name: "Día seleccionado" });
  expect(within(panel).getByText("Rosa Elena Duarte")).toBeVisible();
  expect(within(panel).getByText("Atendida")).toBeVisible();
  expect(within(panel).queryByText("Cancelada Antes")).toBeNull();
});

test("cambia a semana y a día, y agenda en el día elegido", async () => {
  apiDeMentira({ "GET /api/v1/citas": { cuerpo: [cita("a", "Rosa Elena Duarte", 9)] } });
  mostrar("/medico/calendario", { "/medico/calendario": <Calendario /> });

  await userEvent.click(await screen.findByRole("button", { name: "Semana" }));
  // La cita aparece en su columna de la semana y en el panel del día.
  expect(await screen.findAllByRole("link", { name: /Rosa Elena Duarte/ })).toHaveLength(2);

  await userEvent.click(screen.getByRole("button", { name: "Día" }));
  expect(screen.getByRole("button", { name: "Día anterior" })).toBeVisible();
  const mes = String(hoy.getMonth() + 1).padStart(2, "0");
  const dia = String(hoy.getDate()).padStart(2, "0");
  expect(screen.getByRole("link", { name: "Agendar en este día" })).toHaveAttribute(
    "href",
    `/medico/citas/nueva?dia=${hoy.getFullYear()}-${mes}-${dia}`,
  );
});
