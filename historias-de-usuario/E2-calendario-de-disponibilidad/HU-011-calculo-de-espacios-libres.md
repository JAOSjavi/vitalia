# HU-011 — Cálculo de espacios libres sin choques

| Dato | Valor |
|---|---|
| Épica | E2 Calendario de disponibilidad |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-11 |
| Origen | HU-008 de la versión anterior, ajustada |

## Historia

> Como sistema, quiero calcular los espacios libres y validarlos en el momento de confirmar, para que dos pacientes nunca queden en el mismo horario.

## Criterios de aceptación

- **CA-1** · Dados el horario, los bloqueos y las citas existentes, cuando se consulta un día, entonces solo se ofrecen los espacios libres con la duración del tipo de cita elegido.
- **CA-2** · Dado que dos personas confirman el mismo espacio a la vez, cuando se procesan las solicitudes, entonces se crea una sola cita y la otra recibe el aviso de espacio ocupado con alternativas.
- **CA-3** · Dado un espacio que ya pasó o que empieza en menos de una hora, cuando lo consulta un paciente, entonces no se le ofrece.
- **CA-4** · Dado un tipo de cita más largo que el tiempo que queda en una franja, cuando se calculan los espacios, entonces ese tramo no se ofrece.

## Tareas y actividades

### T-011.1 Motor de cálculo

- Generar los espacios a partir del horario
- Restar los bloqueos y las citas existentes
- Ajustar a la duración del tipo de cita

### T-011.2 Control de concurrencia

- Restricción que impide dos citas en la misma franja
- Confirmación dentro de una transacción
- Respuesta con alternativas cuando hay conflicto

### T-011.3 Pruebas

- Dos confirmaciones simultáneas
- Bloqueos y cambios de horario
- Tipos de cita con duraciones distintas

## Relación con otras historias

**Depende de:**

- [HU-008 Horario semanal de atención](HU-008-horario-semanal-de-atencion.md)
- [HU-009 Bloqueos y ausencias](HU-009-bloqueos-y-ausencias.md)
- [HU-010 Tipos de cita y duración](HU-010-tipos-de-cita-y-duracion.md)

**Habilita:**

- [HU-012 Agendar una cita como paciente](../E3-citas/HU-012-agendar-una-cita-como-paciente.md)
- [HU-016 Crear una cita para un paciente](../E3-citas/HU-016-crear-una-cita-para-un-paciente.md)
- [HU-017 Mover o cancelar una cita como médico](../E3-citas/HU-017-mover-o-cancelar-una-cita-como-medico.md)
- [HU-021 Panel de inicio con la agenda del día](../E4-panel-del-medico/HU-021-agenda-del-dia.md)

---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
