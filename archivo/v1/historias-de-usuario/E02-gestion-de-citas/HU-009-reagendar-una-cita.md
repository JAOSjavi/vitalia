# HU-009 — Reagendar una cita

| Dato | Valor |
|---|---|
| Épica | E2 Gestión de citas |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-09 |
| Jira | SCRUM-25 |

## Historia

> Como paciente, quiero mover mi cita a otro horario, para ajustarla cuando me cambian los planes.

## Criterios de aceptación

- **CA-1** · Dado que mi cita está dentro del plazo permitido para cambios, cuando elijo un nuevo horario disponible y confirmo, entonces el sistema libera el horario anterior y reserva el nuevo.
- **CA-2** · Dado que reagendé, cuando se confirma el cambio, entonces el sistema cancela los recordatorios anteriores, programa los nuevos y me envía la confirmación.
- **CA-3** · Dado que faltan menos horas que el mínimo configurado por la clínica, cuando intento reagendar, entonces el sistema lo impide y me indica comunicarme con el consultorio.
- **CA-4** · Dado que reagendé, cuando consulto el historial de la cita, entonces queda registro del horario anterior, el nuevo y quién hizo el cambio.

## Tareas y actividades

### T-009.1 Endpoint de reagendamiento

- Validar la regla de anticipación
- Liberar y reservar en una sola transacción
- Registrar la trazabilidad del cambio

### T-009.2 Reprogramar recordatorios

- Cancelar los avisos pendientes
- Programar los nuevos
- Enviar la confirmación al canal preferido

### T-009.3 Interfaz de reagendamiento

- Acceso desde el detalle de la cita
- Selector de nuevo horario
- Aviso claro cuando la regla lo impide

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-007 Agendar una cita desde la aplicación](HU-007-agendar-una-cita-desde-la-aplicacion.md)
- [HU-008 Verificación de disponibilidad en tiempo real](HU-008-verificacion-de-disponibilidad-en-tiempo-real.md)

**Habilita** — no pueden construirse sin esta:

- [HU-040 Cancelar o reagendar respondiendo el mensaje](../E03-agendamiento-y-atencion-por-whatsapp/HU-040-cancelar-o-reagendar-respondiendo-el-mensaje.md)


---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
