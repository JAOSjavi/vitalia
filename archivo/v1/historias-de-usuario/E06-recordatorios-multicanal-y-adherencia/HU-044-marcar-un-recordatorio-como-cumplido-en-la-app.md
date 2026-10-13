# HU-044 — Marcar un recordatorio como cumplido en la app

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-37 |
| Jira | pendiente de cargar |

## Historia

> Como paciente, quiero marcar que ya tomé el medicamento, para llevar el control y que mi médico sepa cómo voy.

## Criterios de aceptación

- **CA-1** · Dado que veo un recordatorio pendiente del día, cuando pulso «Marcar», entonces queda como cumplido con la hora real de la confirmación.
- **CA-2** · Dado que marqué un recordatorio, cuando se registra, entonces el indicador de adherencia se actualiza inmediatamente en pantalla.
- **CA-3** · Dado que un recordatorio ya fue marcado, cuando intento marcarlo de nuevo, entonces el sistema no duplica el registro.
- **CA-4** · Dado que marco una toma después de su hora programada, cuando se registra, entonces se guarda como cumplida con retraso y se distingue de las cumplidas a tiempo.

## Tareas y actividades

### T-044.1 Modelo de confirmaciones

- Tabla confirmacion_adherencia
- Restricción de unicidad por recordatorio
- Registro de hora programada y hora real

### T-044.2 Endpoint de confirmación

- Validar propiedad del recordatorio
- Registrar confirmación idempotente
- Recalcular el indicador

### T-044.3 Pantalla de recordatorios

- Lista del día con estado
- Acción de marcar con respuesta inmediata
- Indicador de adherencia visible

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-029 Programación automática de recordatorios de medicamento](HU-029-programacion-automatica-de-recordatorios-de-medica.md)

**Habilita** — no pueden construirse sin esta:

- [HU-047 Cálculo del indicador de adherencia](HU-047-calculo-del-indicador-de-adherencia.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
