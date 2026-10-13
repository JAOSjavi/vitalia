# HU-040 — Cancelar o reagendar respondiendo el mensaje

| Dato | Valor |
|---|---|
| Épica | E3 Agendamiento y atención por WhatsApp |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-15 |
| Jira | pendiente de cargar |

## Historia

> Como paciente, quiero cancelar o mover mi cita respondiendo el mismo mensaje de confirmación, para resolverlo en dos toques.

## Criterios de aceptación

- **CA-1** · Dado que recibo el mensaje de confirmación con botones, cuando pulso «Reagendar», entonces el asistente me ofrece los horarios disponibles del mismo profesional.
- **CA-2** · Dado que pulso «Cancelar», cuando confirmo la acción, entonces la cita queda cancelada, el espacio se libera y los recordatorios pendientes se anulan.
- **CA-3** · Dado que la regla de anticipación de la clínica no permite el cambio, cuando lo intento, entonces el asistente lo explica e indica cómo comunicarse con el consultorio.
- **CA-4** · Dado que completo la acción, cuando termina, entonces recibo la confirmación escrita del nuevo estado de la cita.

## Tareas y actividades

### T-040.1 Plantillas con botones de acción

- Diseñar plantilla de confirmación con respuestas rápidas
- Someter a aprobación de Meta
- Vincular cada botón con su acción

### T-040.2 Procesamiento de la respuesta

- Identificar la cita del contexto
- Invocar los servicios de cancelar y reagendar
- Validar la regla de anticipación

### T-040.3 Pruebas

- Prueba de reagendar desde el botón
- Prueba de cancelar y liberar espacio
- Prueba de bloqueo por anticipación

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-033 Envío por WhatsApp con plantillas aprobadas](../E06-recordatorios-multicanal-y-adherencia/HU-033-envio-por-whatsapp-con-plantillas-aprobadas.md)
- [HU-009 Reagendar una cita](../E02-gestion-de-citas/HU-009-reagendar-una-cita.md)
- [HU-010 Cancelar una cita](../E02-gestion-de-citas/HU-010-cancelar-una-cita.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
