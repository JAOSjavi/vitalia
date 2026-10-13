# HU-022 — Vista de calendario semanal y mensual

| Dato | Valor |
|---|---|
| Épica | E4 Panel del médico |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-21 |
| Origen | Nueva |

## Historia

> Como médico, quiero ver mi agenda por semana y por mes, para planear mis días y detectar huecos.

## Criterios de aceptación

- **CA-1** · Dado que abro el calendario, cuando elijo semana o mes, entonces veo las citas, los bloqueos y el tiempo libre de ese periodo.
- **CA-2** · Dado un espacio libre, cuando lo selecciono, entonces se abre el formulario para crear una cita o un bloqueo en ese horario.
- **CA-3** · Dada una cita en el calendario, cuando la selecciono, entonces veo su detalle y las acciones de mover, cancelar y abrir la ficha del paciente.
- **CA-4** · Dado que uso un celular, cuando abro el calendario, entonces la vista se adapta a un día o a una lista sin perder información.

## Tareas y actividades

### T-022.1 Servicio de calendario

- Consulta de citas y bloqueos por rango de fechas
- Cálculo del tiempo libre
- Rendimiento con un mes completo

### T-022.2 Componente de calendario

- Vista semanal y vista mensual
- Acciones sobre espacios libres y sobre citas
- Adaptación a celular

## Relación con otras historias

**Depende de:**

- [HU-009 Bloqueos y ausencias](../E2-calendario-de-disponibilidad/HU-009-bloqueos-y-ausencias.md)
- [HU-021 Panel de inicio con la agenda del día](HU-021-agenda-del-dia.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
