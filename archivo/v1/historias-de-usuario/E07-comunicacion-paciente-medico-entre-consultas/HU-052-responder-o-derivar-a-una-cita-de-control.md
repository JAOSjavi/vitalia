# HU-052 — Responder o derivar a una cita de control

| Dato | Valor |
|---|---|
| Épica | E7 Comunicación paciente–médico entre consultas |
| Fase | 2 |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-42 |
| Jira | pendiente de cargar |

## Historia

> Como médico, quiero responder el reporte o convertirlo en un control, para resolverlo sin abrir un canal de atención permanente.

## Criterios de aceptación

- **CA-1** · Dado que tengo reportes pendientes, cuando abro la bandeja, entonces los veo ordenados por antigüedad con el nombre del paciente y un extracto.
- **CA-2** · Dado que respondo un reporte, cuando envío la respuesta, entonces el paciente la recibe en la app y por su canal preferido.
- **CA-3** · Dado que considero necesario verlo, cuando elijo «Derivar a control», entonces el sistema agenda o propone una cita y lo informa en la conversación.
- **CA-4** · Dado que respondí, cuando se cierra la atención, entonces la conversación queda marcada como respondida y registrada en la historia del paciente.

## Tareas y actividades

### T-052.1 Bandeja de reportes

- Listado con filtros por estado
- Orden por antigüedad
- Contador de pendientes

### T-052.2 Respuesta y notificación

- Envío de la respuesta
- Notificación por canal preferido
- Cambio de estado de la conversación

### T-052.3 Derivación a cita

- Acción que reutiliza el agendamiento
- Registro del vínculo entre reporte y cita
- Mensaje automático en el hilo

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-051 Reportar un síntoma o una duda](HU-051-reportar-un-sintoma-o-una-duda.md)

**Habilita** — no pueden construirse sin esta:

- [HU-054 Notificación de respuesta del médico](HU-054-notificacion-de-respuesta-del-medico.md)


---

[← Volver a E7](README.md) · [Mapa de relaciones](../RELACIONES.md)
