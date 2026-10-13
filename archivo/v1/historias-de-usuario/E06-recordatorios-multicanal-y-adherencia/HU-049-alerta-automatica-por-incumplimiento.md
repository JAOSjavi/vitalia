# HU-049 — Alerta automática por incumplimiento

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 2 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-40 |
| Jira | pendiente de cargar |

## Historia

> Como médico, quiero que el sistema me avise cuando un paciente deja de confirmar, para actuar antes de que el tratamiento fracase.

## Criterios de aceptación

- **CA-1** · Dado un paciente que no confirma durante los días configurados, cuando se evalúa el incumplimiento, entonces el sistema genera una alerta dirigida a su médico tratante.
- **CA-2** · Dado que el tratamiento está marcado como crítico o post-operatorio, cuando se evalúa, entonces el umbral de días es menor y la alerta se marca con prioridad alta.
- **CA-3** · Dado que el paciente tiene un cuidador autorizado, cuando se genera la alerta, entonces también se le notifica, sin incluir información clínica más allá del plan de cuidado.
- **CA-4** · Dado que el paciente retoma las confirmaciones, cuando se evalúa nuevamente, entonces la alerta se cierra automáticamente y queda registrada en el historial.
- **CA-5** · Dado que se genera una alerta, cuando el médico la revisa, entonces puede marcarla como gestionada dejando una nota.

## Tareas y actividades

### T-049.1 Reglas de incumplimiento

- Parametrizar umbrales por tipo de tratamiento
- Definir prioridad y criterios de cierre
- Documentar el criterio clínico aplicado

### T-049.2 Proceso de evaluación

- Tarea programada diaria
- Generar, actualizar y cerrar alertas
- Evitar alertas duplicadas

### T-049.3 Notificación a médico y cuidador

- Notificación en el panel y por canal preferido
- Contenido limitado para el cuidador
- Registro del envío

### T-049.4 Gestión de la alerta

- Vista de alertas activas
- Acción de marcar como gestionada con nota
- Historial de alertas por paciente

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-047 Cálculo del indicador de adherencia](HU-047-calculo-del-indicador-de-adherencia.md)
- [HU-048 Panel de adherencia del médico](HU-048-panel-de-adherencia-del-medico.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
