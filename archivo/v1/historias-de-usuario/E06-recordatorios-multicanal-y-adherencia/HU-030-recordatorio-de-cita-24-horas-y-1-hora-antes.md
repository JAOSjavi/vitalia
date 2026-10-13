# HU-030 — Recordatorio de cita 24 horas y 1 hora antes

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-33 |
| Jira | SCRUM-93 |

## Historia

> Como paciente, quiero que me recuerden mi cita el día anterior y una hora antes, para no olvidarla ni perder el cupo.

## Criterios de aceptación

- **CA-1** · Dado que tengo una cita confirmada, cuando faltan 24 horas, entonces recibo un recordatorio por mi canal preferido con fecha, hora, profesional y sede.
- **CA-2** · Dado que tengo una cita confirmada, cuando falta 1 hora, entonces recibo el segundo recordatorio.
- **CA-3** · Dado que la cita se cancela o se reagenda, cuando se procesa el cambio, entonces los recordatorios pendientes se cancelan o se reprograman según corresponda.
- **CA-4** · Dado que la cita se agenda con menos de 24 horas de anticipación, cuando se crea, entonces solo se programa el recordatorio de 1 hora antes.

## Tareas y actividades

### T-030.1 Reglas de programación por cita

- Programar avisos al crear la cita
- Manejar el caso de cita con poca anticipación
- Cancelar o reprogramar ante cambios

### T-030.2 Contenido del mensaje

- Plantilla con fecha, hora, profesional y sede
- Variantes por canal
- Revisión de longitud para SMS

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-007 Agendar una cita desde la aplicación](../E02-gestion-de-citas/HU-007-agendar-una-cita-desde-la-aplicacion.md)

**Habilita** — no pueden construirse sin esta:

- [HU-041 Confirmar asistencia el día anterior](../E03-agendamiento-y-atencion-por-whatsapp/HU-041-confirmar-asistencia-el-dia-anterior.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
