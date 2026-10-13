# HU-018 — Registrar asistencia o inasistencia

| Dato | Valor |
|---|---|
| Épica | E3 Citas |
| Rol | Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 2 puntos |
| Requisitos | RF-17 |
| Origen | HU-013 de la versión anterior, ajustada |

## Historia

> Como médico, quiero marcar si el paciente asistió, para tener el registro real de mi consulta.

## Criterios de aceptación

- **CA-1** · Dada una cita de hoy, cuando la marco como atendida, entonces su estado cambia y queda la hora del registro.
- **CA-2** · Dada una cita cuya hora ya pasó, cuando la marco como "no asistió", entonces queda en ese estado y aparece así en el historial del paciente.
- **CA-3** · Dado que marqué un estado por error, cuando lo corrijo el mismo día, entonces el sistema lo permite y registra la corrección.

## Tareas y actividades

### T-018.1 Estados de asistencia

- Cambios de estado permitidos
- Corrección dentro del mismo día
- Registro en la bitácora

### T-018.2 Acción en la agenda

- Botones "atendida" y "no asistió"
- Indicador visual del estado

## Relación con otras historias

**Depende de:**

- [HU-021 Panel de inicio con la agenda del día](../E4-panel-del-medico/HU-021-agenda-del-dia.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
