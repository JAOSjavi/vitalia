# HU-009 — Bloqueos y ausencias

| Dato | Valor |
|---|---|
| Épica | E2 Calendario de disponibilidad |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-09 |
| Origen | HU-056 de la versión anterior, ajustada |

## Historia

> Como médico, quiero bloquear los días u horas en que no voy a atender, para que nadie agende en ellos.

## Criterios de aceptación

- **CA-1** · Dado que registro un bloqueo con fecha, hora de inicio, hora de fin y motivo, cuando guardo, entonces ese tiempo deja de ofrecerse.
- **CA-2** · Dado que el bloqueo se cruza con citas ya agendadas, cuando lo registro, entonces el sistema las lista y me exige moverlas o cancelarlas antes de confirmar.
- **CA-3** · Dado un bloqueo futuro, cuando lo elimino, entonces ese tiempo vuelve a ofrecerse.
- **CA-4** · Dado un bloqueo de varios días, cuando lo registro, entonces aplica a cada día del rango.

## Tareas y actividades

### T-009.1 Modelo de bloqueos

- Tabla de bloqueos con rango de tiempo y motivo
- Detección de citas en conflicto
- Eliminación de bloqueos futuros

### T-009.2 Pantalla de bloqueos

- Formulario de bloqueo
- Lista de citas afectadas con las acciones de mover y cancelar
- Lista de bloqueos vigentes

## Relación con otras historias

**Depende de:**

- [HU-008 Horario semanal de atención](HU-008-horario-semanal-de-atencion.md)

**Habilita:**

- [HU-011 Cálculo de espacios libres sin choques](HU-011-calculo-de-espacios-libres.md)
- [HU-022 Vista de calendario semanal y mensual](../E4-panel-del-medico/HU-022-vista-de-calendario.md)

---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
