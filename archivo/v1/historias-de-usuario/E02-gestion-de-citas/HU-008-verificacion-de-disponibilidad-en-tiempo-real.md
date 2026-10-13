# HU-008 — Verificación de disponibilidad en tiempo real

| Dato | Valor |
|---|---|
| Épica | E2 Gestión de citas |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-08 |
| Jira | SCRUM-24 |

## Historia

> Como sistema, quiero validar la disponibilidad en el momento de confirmar, para que dos pacientes nunca queden en el mismo horario.

## Criterios de aceptación

- **CA-1** · Dado un horario ya ocupado, cuando se consulta la disponibilidad, entonces el sistema no lo ofrece como seleccionable.
- **CA-2** · Dado que dos pacientes confirman el mismo horario simultáneamente, cuando se procesan las solicitudes, entonces solo una cita se crea y la otra recibe un aviso de horario ya tomado con opciones alternativas.
- **CA-3** · Dado el horario de atención y los bloqueos del profesional (vacaciones, bloqueos manuales), cuando se calcula la disponibilidad, entonces esos espacios no aparecen como libres.
- **CA-4** · Dado el tipo de cita seleccionado, cuando se calculan los espacios, entonces la duración del espacio corresponde a la duración configurada para ese tipo.

## Tareas y actividades

### T-008.1 Motor de cálculo de disponibilidad

- Generar espacios desde el horario del profesional
- Restar citas existentes y bloqueos
- Ajustar la duración por tipo de cita

### T-008.2 Control de concurrencia

- Restricción de unicidad por profesional y franja
- Transacción con bloqueo al confirmar
- Manejo del conflicto con alternativas sugeridas

### T-008.3 Gestión de horarios y bloqueos

- Modelo de horario semanal por profesional y sede
- Registro de bloqueos y ausencias
- Pantalla básica de administración

### T-008.4 Pruebas de concurrencia

- Prueba de dos confirmaciones simultáneas
- Prueba de bloqueos y ausencias
- Prueba de duraciones distintas

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- Ninguna. Es punto de partida.

**Habilita** — no pueden construirse sin esta:

- [HU-007 Agendar una cita desde la aplicación](HU-007-agendar-una-cita-desde-la-aplicacion.md)
- [HU-009 Reagendar una cita](HU-009-reagendar-una-cita.md)
- [HU-014 Agenda del día del profesional](HU-014-agenda-del-dia-del-profesional.md)
- [HU-038 Agendar una cita por WhatsApp](../E03-agendamiento-y-atencion-por-whatsapp/HU-038-agendar-una-cita-por-whatsapp.md)
- [HU-056 Gestionar horarios de atención](../E09-panel-administrativo-y-multi-clinica/HU-056-gestionar-horarios-de-atencion.md)


---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
