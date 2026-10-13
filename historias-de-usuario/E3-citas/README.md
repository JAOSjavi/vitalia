# E3 — Citas

**Objetivo:** que el paciente y el médico puedan crear, consultar, mover y cancelar citas, cada uno desde su lado.

| Dato | Valor |
|---|---|
| Historias | 9 |
| Puntos | 32 |
| Requisitos | RF-12 a RF-19 |

## Historias de esta épica

| ID | Historia | Rol | Prioridad | Puntos |
|---|---|---|---|---|
| HU-012 | [Agendar una cita como paciente](HU-012-agendar-una-cita-como-paciente.md) | Paciente | Must | 5 |
| HU-013 | [Consultar mis citas](HU-013-consultar-mis-citas.md) | Paciente | Must | 3 |
| HU-014 | [Mover mi cita](HU-014-mover-mi-cita.md) | Paciente | Must | 5 |
| HU-015 | [Cancelar mi cita](HU-015-cancelar-mi-cita.md) | Paciente | Must | 3 |
| HU-016 | [Crear una cita para un paciente](HU-016-crear-una-cita-para-un-paciente.md) | Médico | Must | 5 |
| HU-017 | [Mover o cancelar una cita como médico](HU-017-mover-o-cancelar-una-cita-como-medico.md) | Médico | Must | 3 |
| HU-018 | [Registrar asistencia o inasistencia](HU-018-registrar-asistencia.md) | Médico | Should | 2 |
| HU-019 | [Aviso por correo de cambios en la cita](HU-019-aviso-por-correo-de-cambios-en-la-cita.md) | Paciente | Should | 3 |
| HU-020 | [Inicio del paciente](HU-020-inicio-del-paciente.md) | Paciente | Must | 3 |

## Operaciones sobre la cita, por rol

| Operación | Paciente | Médico |
|---|---|---|
| Crear | HU-012 | HU-016 |
| Consultar | HU-013, HU-020 | HU-021, HU-022 (épica E4) |
| Mover | HU-014 | HU-017 |
| Cancelar | HU-015 | HU-017 |

---

[Alcance y flujo](../../planificacion/01-alcance-y-flujo.md) · [Requisitos](../../planificacion/02-requisitos.md) · [Mapa de relaciones](../RELACIONES.md)
