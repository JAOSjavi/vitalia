import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { apiDeMentira, mostrar } from "../ayudas-de-prueba";
import { Ficha } from "./Ficha";

// Los identificadores crecen con el tiempo: "0001-a" se subió antes que "0002-b".
const PRIMERO = "0001-a";
const SEGUNDO = "0002-b";

function documento(id: string, nombre: string, fecha: string) {
  return {
    id,
    nombre,
    fecha_documento: fecha,
    tipo: "historia_clinica",
    formato: "pdf",
    tamano: 40_000,
    estado_lectura: "legible",
    paginas: 3,
    subido_en: "2026-10-27T15:00:00Z",
  };
}

function ficha(iaAutorizada: boolean) {
  return {
    paciente: {
      id: "p1",
      nombres: "Hernando",
      apellidos: "Castaño Ríos",
      tipo_documento: "CC",
      numero_documento: "79482615",
      fecha_nacimiento: "1968-03-14",
      telefono: "3104827713",
      correo: "paciente1@ejemplo.test",
      activo: true,
    },
    ia_autorizada: iaAutorizada,
    citas: [],
    // El servidor las manda de la más reciente a la más antigua.
    documentos: [
      documento(SEGUNDO, "Control de mayo", "2026-05-14"),
      documento(PRIMERO, "Control de febrero", "2026-02-12"),
    ],
  };
}

function lineas(...eventos: object[]) {
  return eventos.map((e) => JSON.stringify(e)).join("\n") + "\n";
}

function origen(pagina: number, frase: string, verificado: boolean) {
  return {
    etiqueta: "D1",
    documento_id: PRIMERO,
    documento: "Control de febrero",
    pagina,
    frase,
    verificado,
  };
}

const RESPUESTA = lineas(
  { tipo: "texto", texto: 'El LDL fue 168 mg/dL [D1, pág. 3: "Colesterol LDL: 168 mg/dL"]' },
  { tipo: "texto", texto: ' y toma losartán [D1, pág. 1: "losartán 100 mg"].' },
  {
    tipo: "fin",
    origenes: [
      origen(3, "Colesterol LDL: 168 mg/dL", true),
      origen(1, "losartán 100 mg", false),
    ],
    consultado: [
      {
        documento_id: PRIMERO,
        documento: "Control de febrero",
        fecha_documento: "2026-02-12",
        paginas: [1, 3],
      },
    ],
    aviso: "El asistente es un apoyo.",
  },
);

function pantalla() {
  return mostrar("/medico/pacientes/p1", { "/medico/pacientes/:paciente": <Ficha /> });
}

test("la ficha muestra los datos y los documentos con su etiqueta en orden de subida", async () => {
  apiDeMentira({ "GET /api/v1/pacientes/p1": { cuerpo: ficha(true) } });
  pantalla();

  expect(await screen.findByRole("heading", { name: "Hernando Castaño Ríos" })).toBeInTheDocument();
  expect(screen.getByText(/\d+ años/)).toBeInTheDocument();
  expect(screen.getByText("CC 79 482 615")).toBeInTheDocument();
  expect(screen.getByText("Cuenta activa")).toBeInTheDocument();
  const ruta = screen.getByRole("navigation", { name: "Ruta" });
  expect(within(ruta).getByRole("link", { name: "Pacientes" })).toHaveAttribute("href", "/medico/pacientes");

  const documentos = screen.getByRole("region", { name: "Documentos que subió" });
  const filas = within(documentos).getAllByText(/^D\d$/).map((e) => e.parentElement);
  expect(filas[0]).toHaveTextContent("D1Control de febrero12 feb 2026 · 3 pág.");
  expect(filas[1]).toHaveTextContent("D2Control de mayo14 may 2026 · 3 pág.");
  expect(within(documentos).getByRole("link", { name: "Ver Control de febrero" })).toHaveAttribute(
    "href",
    `/api/v1/documentos/${PRIMERO}/archivo`,
  );
  expect(screen.getByRole("link", { name: "Agendar cita" })).toHaveAttribute(
    "href",
    "/medico/citas/nueva?paciente=p1&nombre=Hernando%20Casta%C3%B1o%20R%C3%ADos",
  );
});

test("el asistente responde con cada cita como un botón que abre el documento en esa página", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/pacientes/p1": { cuerpo: ficha(true) },
    "POST /api/v1/pacientes/p1/asistente/preguntas": { texto: RESPUESTA },
  });
  pantalla();

  await userEvent.type(await screen.findByLabelText("Su pregunta"), "¿Cómo va el LDL?{Enter}");

  const verificada = await screen.findByRole("link", { name: "D1 · pág. 3" });
  expect(verificada).toHaveAttribute("href", `/api/v1/documentos/${PRIMERO}/archivo#page=3`);
  expect(screen.getByRole("link", { name: "D1 · pág. 1, frase sin verificar" })).toBeInTheDocument();
  expect(screen.getByText(/El LDL fue 168 mg\/dL/)).toHaveTextContent(
    "El LDL fue 168 mg/dL D1 · pág. 3 y toma losartán D1 · pág. 1.",
  );
  expect(screen.getByText("Consultó: D1 (págs. 1, 3)")).toBeInTheDocument();
  expect(pedidos.find((p) => p.clave.startsWith("POST"))?.cuerpo).toEqual({
    pregunta: "¿Cómo va el LDL?",
    conversacion: [],
  });
});

test("la segunda pregunta lleva la conversación anterior", async () => {
  const pedidos = apiDeMentira({
    "GET /api/v1/pacientes/p1": { cuerpo: ficha(true) },
    "POST /api/v1/pacientes/p1/asistente/preguntas": { texto: RESPUESTA },
  });
  pantalla();

  await userEvent.click(await screen.findByRole("button", { name: "¿Tiene alergias?" }));
  await screen.findByRole("link", { name: "D1 · pág. 3" });
  await userEvent.type(screen.getByLabelText("Su pregunta"), "¿Y antes?{Enter}");
  await screen.findAllByText(/Consultó:/);

  const ultimo = pedidos.filter((p) => p.clave.startsWith("POST")).at(-1);
  expect(ultimo?.cuerpo).toMatchObject({
    pregunta: "¿Y antes?",
    conversacion: [
      { autor: "medico", texto: "¿Tiene alergias?" },
      { autor: "asistente", texto: expect.stringContaining("El LDL fue 168") },
    ],
  });
});

test("si el proveedor falla, avisa sin perder la ficha", async () => {
  apiDeMentira({
    "GET /api/v1/pacientes/p1": { cuerpo: ficha(true) },
    "POST /api/v1/pacientes/p1/asistente/preguntas": {
      texto: lineas({
        tipo: "error",
        codigo: "proveedor_no_disponible",
        mensaje: "El asistente no está disponible en este momento.",
      }),
    },
  });
  pantalla();

  await userEvent.type(await screen.findByLabelText("Su pregunta"), "¿Alergias?{Enter}");

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "El asistente no está disponible en este momento.",
  );
  expect(screen.getByRole("heading", { name: "Hernando Castaño Ríos" })).toBeInTheDocument();
});

test("sin autorización de IA el asistente queda deshabilitado con la explicación", async () => {
  apiDeMentira({ "GET /api/v1/pacientes/p1": { cuerpo: ficha(false) } });
  pantalla();

  expect(await screen.findByText("Sin autorización")).toBeInTheDocument();
  expect(screen.getByText(/no ha autorizado el uso de inteligencia artificial/)).toBeInTheDocument();
  expect(screen.queryByLabelText("Su pregunta")).not.toBeInTheDocument();
});
