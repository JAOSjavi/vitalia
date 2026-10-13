# HU-015 — Cancelar mi cita

| Dato | Valor |
|---|---|
| Épica | E3 Citas |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-14 |
| Origen | HU-010 de la versión anterior, ajustada |

## Historia

> Como paciente, quiero cancelar una cita a la que no voy a ir, para liberar el espacio.

## Criterios de aceptación

- **CA-1** · Dado que faltan más de 24 horas, cuando cancelo y confirmo, entonces la cita queda cancelada y el espacio vuelve a ofrecerse.
- **CA-2** · Dado que faltan menos de 24 horas, cuando intento cancelar, entonces el sistema no lo permite y me muestra el teléfono del consultorio.
- **CA-3** · Dado que cancelo, cuando se guarda, entonces la cita sigue apareciendo en mi historial como cancelada, con la fecha de cancelación.

## Tareas y actividades

### T-015.1 Servicio de cancelación

- Regla de anticipación (supuesto: 24 horas)
- Liberación del espacio
- Registro de quién canceló y cuándo

### T-015.2 Pantalla de cancelación

- Confirmación explícita antes de cancelar
- Mensaje cuando la anticipación ya venció

## Relación con otras historias

**Depende de:**

- [HU-012 Agendar una cita como paciente](HU-012-agendar-una-cita-como-paciente.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
