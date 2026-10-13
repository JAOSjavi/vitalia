# E6 — Asistente de IA

**Objetivo:** que el médico se ponga al día con los antecedentes de un paciente en minutos, sin exponer la información de nadie y sin que la IA opine sobre lo que no está escrito.

| Dato | Valor |
|---|---|
| Historias | 4 |
| Puntos | 24 |
| Requisitos | RF-31 a RF-35 |

## Historias de esta épica

| ID | Historia | Rol | Prioridad | Puntos |
|---|---|---|---|---|
| HU-032 | [Autorización del paciente para usar IA](HU-032-autorizacion-para-usar-ia.md) | Paciente | Must | 3 |
| HU-033 | [IA solo desde el servidor y aislada por paciente](HU-033-ia-desde-el-servidor-y-aislada-por-paciente.md) | Sistema | Must | 8 |
| HU-034 | [Preguntar al asistente sobre los documentos de un paciente](HU-034-preguntar-al-asistente.md) | Médico | Must | 8 |
| HU-035 | [Resumen del paciente con un clic](HU-035-resumen-del-paciente.md) | Médico | Must | 5 |

## Reglas que no se negocian

1. **Sin autorización del paciente no hay asistente.** El médico igual puede leer los documentos en el visor.
2. **Cada consulta lleva solo los documentos de un paciente.** El modelo no guarda memoria entre consultas; el servidor arma el contexto cada vez.
3. **La clave del proveedor nunca está en el navegador.**
4. **Cada dato de la respuesta dice de qué documento y de qué página salió.** Si no aparece, el asistente lo dice.
5. **El asistente resume; no diagnostica ni recomienda tratamiento.**

---

[Alcance y flujo](../../planificacion/01-alcance-y-flujo.md) · [Requisitos](../../planificacion/02-requisitos.md) · [Mapa de relaciones](../RELACIONES.md)
