# HU-041 — Confirmar asistencia el día anterior

| Dato | Valor |
|---|---|
| Épica | E3 Agendamiento y atención por WhatsApp |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-16 |
| Jira | pendiente de cargar |

## Historia

> Como clínica, quiero que el paciente confirme su asistencia el día anterior, para liberar a tiempo los cupos que no se van a usar.

## Criterios de aceptación

- **CA-1** · Dado que falta un día para la cita, cuando se envía el recordatorio, entonces incluye las opciones «Confirmo» y «No podré asistir».
- **CA-2** · Dado que el paciente confirma, cuando se procesa la respuesta, entonces la cita queda marcada como confirmada y visible así en la agenda del profesional.
- **CA-3** · Dado que responde que no podrá asistir, cuando se procesa, entonces la cita se cancela, el espacio se libera y se le ofrece reagendar.
- **CA-4** · Dado que no responde, cuando llega la hora de la cita, entonces permanece como «sin confirmar» y así aparece en la agenda.

## Tareas y actividades

### T-041.1 Plantilla de confirmación de asistencia

- Redactar y aprobar la plantilla
- Programar el envío a 24 horas
- Vincular respuestas con la cita

### T-041.2 Estados de confirmación

- Agregar estado confirmada_por_paciente
- Reflejarlo en la agenda del profesional
- Contabilizar la tasa de confirmación

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-030 Recordatorio de cita 24 horas y 1 hora antes](../E06-recordatorios-multicanal-y-adherencia/HU-030-recordatorio-de-cita-24-horas-y-1-hora-antes.md)
- [HU-033 Envío por WhatsApp con plantillas aprobadas](../E06-recordatorios-multicanal-y-adherencia/HU-033-envio-por-whatsapp-con-plantillas-aprobadas.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
