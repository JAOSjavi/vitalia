# HU-013 — Registrar asistencia o inasistencia

| Dato | Valor |
|---|---|
| Épica | E2 Gestión de citas |
| Fase | 1 |
| Rol | Médico, Administrador |
| Prioridad | Should (MoSCoW) |
| Estimación | 2 puntos |
| Requisitos | RF-12 |
| Jira | SCRUM-29 |

## Historia

> Como profesional o administrador, quiero marcar si el paciente asistió, para medir la inasistencia y depurar la agenda.

## Criterios de aceptación

- **CA-1** · Dado que la hora de la cita ya pasó, cuando abro la agenda, entonces puedo marcarla como atendida o no asistió.
- **CA-2** · Dado que marco una cita como atendida, cuando se guarda, entonces el sistema habilita el registro de la nota clínica y del plan de tratamiento.
- **CA-3** · Dado que marco no asistió, cuando se guarda, entonces el sistema lo contabiliza en el indicador de inasistencia de la sede.
- **CA-4** · Dado que una cita ya fue marcada, cuando se intenta cambiar el estado, entonces queda registro del cambio con autor y fecha.

## Tareas y actividades

### T-013.1 Endpoint de cambio de estado

- Validar transiciones permitidas
- Registrar autor y fecha
- Emitir evento para indicadores

### T-013.2 Controles en la agenda

- Acciones rápidas por cita
- Confirmación visual del estado
- Acceso directo a registrar la consulta

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-014 Agenda del día del profesional](HU-014-agenda-del-dia-del-profesional.md)

**Habilita** — no pueden construirse sin esta:

- [HU-015 Registrar la nota clínica de la consulta](../E04-historia-clinica-y-documentos/HU-015-registrar-la-nota-clinica-de-la-consulta.md)
- [HU-058 Reportes de operación](../E09-panel-administrativo-y-multi-clinica/HU-058-reportes-de-operacion.md)
- [HU-066 Encuesta de satisfacción post-consulta](../E10-accesibilidad-y-experiencia/HU-066-encuesta-de-satisfaccion-post-consulta.md)


---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
