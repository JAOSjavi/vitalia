import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";

import { conEnfasis, Markdown } from "./Markdown";

const tal = (texto: string, clave: string) => conEnfasis(texto, clave);

test("la respuesta del asistente muestra listas, negrita y títulos", () => {
  const { container } = render(
    <Markdown
      texto={"### Medicamentos\n- **Losartán 50 mg** cada 12 horas\n- Amlodipino *en la mañana*\n\nNada más."}
      enLinea={tal}
    />,
  );

  expect(screen.getByRole("heading", { level: 4, name: "Medicamentos" })).toBeVisible();
  expect(screen.getAllByRole("listitem")).toHaveLength(2);
  expect(screen.getByText("Losartán 50 mg").tagName).toBe("STRONG");
  expect(screen.getByText("en la mañana").tagName).toBe("EM");
  expect(container.querySelectorAll("p")).toHaveLength(1);
});

test("lo que escriba el modelo como HTML se muestra como texto, sin ejecutarse", () => {
  const { container } = render(<Markdown texto={'<img src=x onerror="alert(1)">'} enLinea={tal} />);

  expect(container.querySelector("img")).toBeNull();
  expect(screen.getByText('<img src=x onerror="alert(1)">')).toBeVisible();
});
