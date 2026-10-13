# HU-048 — Panel de adherencia del médico

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 2 |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-39 |
| Jira | pendiente de cargar |

## Historia

> Como médico, quiero ver de un vistazo qué pacientes están cumpliendo su tratamiento, para intervenir a tiempo con los que no.

## Criterios de aceptación

- **CA-1** · Dado que abro el panel, cuando carga, entonces veo mis pacientes con tratamiento activo, su indicador de adherencia y su estado (en rango o en riesgo).
- **CA-2** · Dado que la lista se muestra, cuando se ordena por defecto, entonces aparecen primero los pacientes con menor adherencia.
- **CA-3** · Dado que un paciente está por debajo del umbral, cuando se muestra, entonces aparece distinguido visualmente y con la acción de contactarlo.
- **CA-4** · Dado que abro un paciente desde el panel, cuando se despliega, entonces veo el detalle de tomas cumplidas e incumplidas de su tratamiento.
- **CA-5** · Dado que consulto el panel, cuando se carga, entonces solo aparecen pacientes con los que tengo relación de atención vigente.

## Tareas y actividades

### T-048.1 Endpoint del panel

- Consultar pacientes activos del profesional
- Incluir indicador y umbral
- Ordenar y paginar

### T-048.2 Vista de panel

- Tabla con indicador visual de cumplimiento
- Distintivo de riesgo y acción de contacto
- Detalle por paciente

### T-048.3 Detalle de adherencia por paciente

- Serie de tomas cumplidas e incumplidas
- Filtro por periodo
- Acceso al plan vigente

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-047 Cálculo del indicador de adherencia](HU-047-calculo-del-indicador-de-adherencia.md)

**Habilita** — no pueden construirse sin esta:

- [HU-049 Alerta automática por incumplimiento](HU-049-alerta-automatica-por-incumplimiento.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
