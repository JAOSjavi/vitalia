# HU-026 — Fecha de fin automática del tratamiento

| Dato | Valor |
|---|---|
| Épica | E5 Plan de tratamiento post-consulta |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-29 |
| Jira | SCRUM-89 |

## Historia

> Como sistema, quiero calcular cuándo termina cada tratamiento, para dejar de enviar recordatorios cuando ya no corresponden.

## Criterios de aceptación

- **CA-1** · Dado un medicamento con duración de N días, cuando se guarda, entonces el sistema calcula la fecha de fin como fecha de inicio más N días y la muestra en el plan.
- **CA-2** · Dado que llega la fecha de fin, cuando el proceso se ejecuta, entonces el sistema deja de programar recordatorios de ese ítem y lo marca como finalizado.
- **CA-3** · Dado que todos los ítems del plan finalizaron, cuando se evalúa el plan, entonces pasa a estado finalizado y el paciente ve el aviso de tratamiento terminado.
- **CA-4** · Dado que el médico extiende la duración, cuando guarda el cambio, entonces el sistema recalcula la fecha de fin y reactiva los recordatorios.

## Tareas y actividades

### T-026.1 Cálculo de vigencia

- Calcular fecha de fin por ítem
- Recalcular ante cambios
- Exponer la vigencia en el plan

### T-026.2 Proceso de cierre

- Tarea programada diaria
- Marcar ítems y planes finalizados
- Cancelar recordatorios pendientes

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-021 Registrar medicamentos del plan](HU-021-registrar-medicamentos-del-plan.md)

**Habilita** — no pueden construirse sin esta:

- [HU-029 Programación automática de recordatorios de medicamento](../E06-recordatorios-multicanal-y-adherencia/HU-029-programacion-automatica-de-recordatorios-de-medica.md)


---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
