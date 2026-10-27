import { describe, expect, it } from "vitest";

import { festivosDe } from "./festivos";

describe("festivos de Colombia", () => {
  it("corre al lunes los que lo exigen y calcula los de Pascua", () => {
    const f2026 = festivosDe(2026);
    // Los del tablero del calendario.
    expect(f2026.get("2026-10-12")).toBe("Día de la Raza");
    expect(f2026.get("2026-11-02")).toBe("Todos los Santos");
    expect(f2026.get("2026-11-16")).toBe("Independencia de Cartagena");
    expect(f2026.get("2026-12-08")).toBe("Inmaculada Concepción");
    // Pascua de 2026 es el 5 de abril.
    expect(f2026.get("2026-04-02")).toBe("Jueves Santo");
    expect(f2026.get("2026-04-03")).toBe("Viernes Santo");
    expect(f2026.size).toBe(18);
  });
});
