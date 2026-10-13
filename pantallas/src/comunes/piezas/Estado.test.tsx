import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";

import { Estado } from "./Estado";

test("el nombre del estado va escrito y el punto no se anuncia", () => {
  render(<Estado tono="verde">Atendida</Estado>);

  const nombre = screen.getByText("Atendida");
  expect(nombre).toBeVisible();
  expect(nombre.querySelector(".estado__punto--verde")).toHaveAttribute("aria-hidden", "true");
});
