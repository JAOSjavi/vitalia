# HU-045 — Consultar la historia clínica de un paciente

| Dato | Valor |
|---|---|
| Épica | E9 Historia clínica del consultorio |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-45 |
| Origen | Nueva (decisión D-24). Retoma HU-017 de la versión anterior |

## Historia

> Como médico, quiero ver las atenciones anteriores de un paciente en orden, para conocer cómo ha evolucionado antes de atenderlo.

## Criterios de aceptación

- **CA-1** · Dada la ficha de un paciente, cuando abro su historia clínica, entonces veo sus atenciones cerradas en orden de fecha, cada una con fecha, diagnóstico principal y médico.
- **CA-2** · Dada una atención de la lista, cuando la abro, entonces la veo completa, con sus notas aclaratorias, y sin opción de editarla.
- **CA-3** · Dado que abro la historia o una atención, cuando se muestra, entonces el acceso queda en la bitácora.
- **CA-4** · Dado un usuario con rol paciente, cuando intenta abrir la historia clínica de otro paciente, entonces el sistema le niega el acceso.

## Tareas y actividades

### T-045.1 Consulta

- Lista de atenciones de un paciente
- Vista de una atención con sus notas aclaratorias
- Registro del acceso en la bitácora

### T-045.2 Pruebas

- Orden cronológico
- Acceso denegado a otro paciente

## Relación con otras historias

**Depende de:**

- [HU-044 Cerrar y firmar la atención](HU-044-cerrar-y-firmar-la-atencion.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
