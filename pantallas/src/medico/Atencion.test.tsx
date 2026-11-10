import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { atencion, FORMULARIO } from "../historia-de-prueba";
import { Atencion } from "./Atencion";

const FICHA = {
  paciente: {
    id: "p1",
    nombres: "Hernando",
    apellidos: "Castaño Ríos",
    tipo_documento: "CC",
    numero_documento: "79482615",
    fecha_nacimiento: "1968-03-14",
    telefono: "3104827713",
    correo: null,
    activo: true,
  },
  ia_autorizada: false,
  citas: [],
  documentos: [],
};

function abierta() {
  return {
    atencion: atencion({
      estado: "abierta",
      fin: null,
      firma: null,
      datos: { motivo: null, temperatura: null },
      diagnosticos: [],
      medicamentos: [],
    }),
    identificacion: { sexo: null, ocupacion: null },
    faltantes: { identificacion: ["Sexo", "Ocupación"], atencion: ["Motivo de consulta"] },
  };
}

function pantalla() {
  return mostrar("/medico/atenciones/a1", { "/medico/atenciones/:atencion": <Atencion /> });
}

test("guarda el borrador al salir de un campo y avisa la identificación pendiente", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/atenciones/a1": { cuerpo: abierta() },
    "GET /api/v1/pacientes/p1": { cuerpo: FICHA },
    "GET /api/v1/historia-clinica/formulario": { cuerpo: FORMULARIO },
    "PATCH /api/v1/atenciones/a1": { cuerpo: { guardada_en: "2026-11-03T15:00:00Z" } },
  });
  pantalla();

  expect(await screen.findByText(/le faltan datos de identificación/)).toHaveTextContent(
    "sexo, ocupación",
  );
  await userEvent.type(screen.getByRole("textbox", { name: /^Motivo de consulta/ }), "Dolor de rodilla.");
  await userEvent.tab();

  const guardado = pedidos.find((p) => p.clave === "PATCH /api/v1/atenciones/a1");
  expect(guardado?.cuerpo).toEqual({ datos: { motivo: "Dolor de rodilla." } });
});

test("al firmar con datos pendientes dice cuáles faltan y no cierra", async () => {
  apiDeMentira({
    "GET /api/v1/atenciones/a1": { cuerpo: abierta() },
    "GET /api/v1/pacientes/p1": { cuerpo: FICHA },
    "GET /api/v1/historia-clinica/formulario": { cuerpo: FORMULARIO },
    "POST /api/v1/atenciones/a1/cierre": {
      estado: 422,
      cuerpo: {
        codigo: "faltan_datos",
        mensaje: "Faltan datos para cerrar la atención.",
        detalle: { identificacion: ["Sexo"], atencion: ["Motivo de consulta"] },
      },
    },
  });
  pantalla();

  await userEvent.click(await screen.findByRole("button", { name: "Cerrar y firmar" }));
  const ventana = screen.getByRole("dialog");
  await userEvent.type(within(ventana).getByLabelText("Su contraseña"), "consultorio2026");
  await userEvent.click(within(ventana).getByRole("button", { name: "Cerrar y firmar" }));

  expect(await within(ventana).findByText(/Faltan datos para cerrar/)).toBeInTheDocument();
  expect(within(ventana).getByText("Motivo de consulta.", { exact: false })).toBeInTheDocument();
});

test("la incapacidad se pregunta primero y, si se da, pide los días antes de cerrar", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/atenciones/a1": { cuerpo: abierta() },
    "GET /api/v1/pacientes/p1": { cuerpo: FICHA },
    "GET /api/v1/historia-clinica/formulario": { cuerpo: FORMULARIO },
    "PATCH /api/v1/atenciones/a1": { cuerpo: { guardada_en: "2026-11-03T15:00:00Z" } },
  });
  pantalla();

  const pregunta = await screen.findByRole("radiogroup", { name: "¿El paciente requiere incapacidad?" });
  expect(screen.queryByRole("textbox", { name: /Días de incapacidad/ })).not.toBeInTheDocument();
  const listo = screen.getByRole("status", { name: "Lo que falta para cerrar" });
  expect(within(listo).queryByText("Días de incapacidad")).not.toBeInTheDocument();

  await userEvent.click(within(pregunta).getByRole("radio", { name: "Sí" }));
  expect(screen.getByRole("textbox", { name: /Días de incapacidad/ })).toBeInTheDocument();
  expect(within(listo).getByRole("link", { name: "Días de incapacidad" })).toHaveAttribute(
    "href",
    "#campo-incapacidad_dias",
  );

  await userEvent.click(within(pregunta).getByRole("radio", { name: "No" }));
  const guardado = pedidos.filter((p) => p.clave === "PATCH /api/v1/atenciones/a1").pop();
  expect(guardado?.cuerpo).toEqual({ datos: { incapacidad_dias: 0 } });
});

test("una atención cerrada se ve de solo lectura con la nota aclaratoria", async () => {
  apiDeMentira({
    "GET /api/v1/atenciones/a1": {
      cuerpo: { atencion: atencion(), identificacion: {}, faltantes: { identificacion: [], atencion: [] } },
    },
    "GET /api/v1/pacientes/p1": { cuerpo: FICHA },
    "GET /api/v1/historia-clinica/formulario": { cuerpo: FORMULARIO },
  });
  pantalla();

  expect(await screen.findByText(/Firmada por/)).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Cerrar y firmar" })).not.toBeInTheDocument();
  expect(screen.getByRole("heading", { name: "Agregar una nota aclaratoria" })).toBeInTheDocument();
});

test("propone lo que dicen los documentos y solo lo guarda al usarlo, sin borrar lo escrito", async () => {
  const consulta = abierta();
  Object.assign(consulta.atencion.datos, { antecedentes_personales: "Hipertensión." });
  const pedidos = apiDeMentira({
    "GET /api/v1/atenciones/a1": { cuerpo: consulta },
    "GET /api/v1/pacientes/p1": {
      cuerpo: { ...FICHA, ia_autorizada: true, documentos: [{ id: "d1", nombre: "Control" }] },
    },
    "GET /api/v1/historia-clinica/formulario": { cuerpo: FORMULARIO },
    "PATCH /api/v1/atenciones/a1": { cuerpo: { guardada_en: "2026-11-10T15:00:00Z" } },
    "POST /api/v1/atenciones/a1/sugerencias": {
      cuerpo: {
        sugerencias: [
          {
            campo: "antecedentes_personales",
            valor: "Dislipidemia en manejo con atorvastatina.",
            origenes: [
              { etiqueta: "D1", documento_id: "d1", documento: "Control", pagina: 1, frase: "atorvastatina 20 mg" },
            ],
          },
          {
            campo: "alergias",
            valor: "Ibuprofeno: angioedema.",
            origenes: [
              { etiqueta: "D1", documento_id: "d1", documento: "Control", pagina: 1, frase: "ibuprofeno con angioedema" },
            ],
          },
        ],
        consultado: [],
        aviso: "El asistente es un apoyo.",
      },
    },
  });
  pantalla();

  await userEvent.click(await screen.findByRole("button", { name: "Completar con los documentos" }));
  expect(await screen.findByText("Ibuprofeno: angioedema.")).toBeInTheDocument();
  expect(screen.getByText("Hay 2 sugerencias", { exact: false })).toBeInTheDocument();
  // Nada se guarda solo por pedirlas.
  expect(pedidos.some((p) => p.clave === "PATCH /api/v1/atenciones/a1")).toBe(false);

  await userEvent.click(screen.getByRole("button", { name: "Agregar al texto" }));
  await userEvent.click(screen.getByRole("button", { name: "Descartar" }));

  const guardados = pedidos.filter((p) => p.clave === "PATCH /api/v1/atenciones/a1");
  expect(guardados.map((p) => p.cuerpo)).toEqual([
    { datos: { antecedentes_personales: "Hipertensión.\nDislipidemia en manejo con atorvastatina." } },
  ]);
  expect(screen.getByRole("textbox", { name: /^Alergias/ })).toHaveValue("");
  expect(screen.queryByText("Ibuprofeno: angioedema.")).not.toBeInTheDocument();
});
