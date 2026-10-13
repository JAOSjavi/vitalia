# HU-014 — Mover mi cita

| Dato | Valor |
|---|---|
| Épica | E3 Citas |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-14 |
| Origen | HU-009 de la versión anterior, ajustada |

## Historia

> Como paciente, quiero cambiar mi cita a otro espacio libre, para no perderla cuando no puedo asistir.

## Criterios de aceptación

- **CA-1** · Dado que faltan más de 24 horas para mi cita, cuando elijo otro espacio libre y confirmo, entonces la cita queda en el nuevo horario y el anterior se libera.
- **CA-2** · Dado que faltan menos de 24 horas, cuando intento moverla, entonces el sistema no lo permite y me muestra el teléfono del consultorio.
- **CA-3** · Dado que el nuevo espacio se ocupa mientras confirmo, cuando el sistema lo detecta, entonces mi cita original se conserva sin cambios.
- **CA-4** · Dado que muevo la cita, cuando se guarda, entonces queda registrado quién la movió y cuándo.

## Tareas y actividades

### T-014.1 Servicio de cambio de cita

- Regla de anticipación configurable (supuesto: 24 horas)
- Cambio de horario y liberación del anterior en una sola transacción
- Registro del cambio

### T-014.2 Pantalla de cambio

- Selección del nuevo espacio
- Mensaje cuando la anticipación ya venció
- Confirmación del cambio

## Relación con otras historias

**Depende de:**

- [HU-012 Agendar una cita como paciente](HU-012-agendar-una-cita-como-paciente.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
