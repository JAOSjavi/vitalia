# HU-010 — Cancelar una cita

| Dato | Valor |
|---|---|
| Épica | E2 Gestión de citas |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-09 |
| Jira | SCRUM-26 |

## Historia

> Como paciente, quiero cancelar una cita a la que no podré asistir, para liberar el espacio y no quedar como inasistente.

## Criterios de aceptación

- **CA-1** · Dado que confirmo la cancelación dentro del plazo permitido, cuando se procesa, entonces la cita pasa a estado cancelada y su horario vuelve a estar disponible.
- **CA-2** · Dado que la cita fue cancelada, cuando se completa la operación, entonces el sistema cancela todos sus recordatorios pendientes.
- **CA-3** · Dado que intento cancelar, cuando se muestra la confirmación, entonces el sistema pide ratificar la acción e indica la política de cancelación de la clínica.
- **CA-4** · Dado que la cita quedó cancelada, cuando el profesional consulta su agenda, entonces el espacio aparece libre y marcado como liberado por cancelación.

## Tareas y actividades

### T-010.1 Endpoint de cancelación

- Validar estado y plazo
- Cambiar estado y liberar el espacio
- Registrar motivo y autor

### T-010.2 Limpieza de recordatorios

- Cancelar los avisos programados
- Confirmar la cancelación al paciente

### T-010.3 Interfaz de cancelación

- Diálogo de confirmación con la política
- Selección opcional de motivo
- Estado visible en el historial

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-007 Agendar una cita desde la aplicación](HU-007-agendar-una-cita-desde-la-aplicacion.md)

**Habilita** — no pueden construirse sin esta:

- [HU-040 Cancelar o reagendar respondiendo el mensaje](../E03-agendamiento-y-atencion-por-whatsapp/HU-040-cancelar-o-reagendar-respondiendo-el-mensaje.md)


---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
