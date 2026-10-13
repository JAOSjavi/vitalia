# HU-042 — Consultar «mi próxima cita» por WhatsApp

| Dato | Valor |
|---|---|
| Épica | E3 Agendamiento y atención por WhatsApp |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Should (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-17 |
| Jira | pendiente de cargar |

## Historia

> Como paciente, quiero preguntar por mi próxima cita por WhatsApp, para confirmar la fecha sin entrar a la aplicación.

## Criterios de aceptación

- **CA-1** · Dado que escribo una consulta sobre mi próxima cita, cuando el asistente la reconoce, entonces responde con fecha, hora, profesional, sede y consultorio.
- **CA-2** · Dado que no tengo citas próximas, cuando consulto, entonces el asistente lo informa y me ofrece agendar una.
- **CA-3** · Dado que tengo varias citas próximas, cuando consulto, entonces responde con la más cercana e indica cuántas otras tengo programadas.
- **CA-4** · Dado que el número no corresponde a un paciente registrado, cuando consulta, entonces el asistente no entrega información y ofrece el registro.

## Tareas y actividades

### T-042.1 Reconocimiento de la intención

- Lista de frases y variantes frecuentes
- Asociar la intención a la consulta
- Respuesta de respaldo ante duda

### T-042.2 Consulta y respuesta

- Buscar la próxima cita del paciente
- Componer la respuesta con los datos completos
- Manejar los casos sin citas y múltiples citas

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-011 Consultar mis citas pasadas y futuras](../E02-gestion-de-citas/HU-011-consultar-mis-citas-pasadas-y-futuras.md)
- [HU-033 Envío por WhatsApp con plantillas aprobadas](../E06-recordatorios-multicanal-y-adherencia/HU-033-envio-por-whatsapp-con-plantillas-aprobadas.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
