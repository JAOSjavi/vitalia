# HU-047 — Cálculo del indicador de adherencia

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 2 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-38 |
| Jira | pendiente de cargar |

## Historia

> Como sistema, quiero calcular qué tanto cumple cada paciente su tratamiento, para que el médico y el paciente vean un dato objetivo.

## Criterios de aceptación

- **CA-1** · Dado un tratamiento activo, cuando se calcula el indicador, entonces corresponde a confirmaciones cumplidas sobre recordatorios cuya hora ya pasó, expresado en porcentaje.
- **CA-2** · Dado que hay recordatorios cuya hora aún no llega, cuando se calcula, entonces no se cuentan como incumplidos.
- **CA-3** · Dado que el paciente confirma una toma, cuando se registra, entonces el indicador se recalcula y queda disponible para el panel del profesional.
- **CA-4** · Dado que se consulta el indicador, cuando se muestra, entonces puede verse por tratamiento, por periodo (7, 30 días) y de forma global del paciente.

## Tareas y actividades

### T-047.1 Definición del indicador

- Documentar la fórmula y los casos borde
- Definir ventanas de cálculo
- Acordar el umbral de riesgo con el equipo clínico

### T-047.2 Servicio de cálculo

- Cálculo por tratamiento y periodo
- Recalcular al confirmar o al vencer un recordatorio
- Almacenar resultados para consulta rápida

### T-047.3 Pruebas

- Prueba de cálculo con y sin pendientes
- Prueba de recálculo por confirmación
- Prueba de periodos

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-044 Marcar un recordatorio como cumplido en la app](HU-044-marcar-un-recordatorio-como-cumplido-en-la-app.md)
- [HU-045 Confirmar la toma desde WhatsApp](HU-045-confirmar-la-toma-desde-whatsapp.md)

**Habilita** — no pueden construirse sin esta:

- [HU-048 Panel de adherencia del médico](HU-048-panel-de-adherencia-del-medico.md)
- [HU-049 Alerta automática por incumplimiento](HU-049-alerta-automatica-por-incumplimiento.md)
- [HU-050 Ver mi propia adherencia](HU-050-ver-mi-propia-adherencia.md)
- [HU-058 Reportes de operación](../E09-panel-administrativo-y-multi-clinica/HU-058-reportes-de-operacion.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
