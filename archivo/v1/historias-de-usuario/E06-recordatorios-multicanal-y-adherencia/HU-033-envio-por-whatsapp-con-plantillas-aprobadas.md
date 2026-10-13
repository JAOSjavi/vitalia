# HU-033 — Envío por WhatsApp con plantillas aprobadas

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 13 puntos |
| Requisitos | RF-18, RF-32 |
| Jira | SCRUM-96 |

## Historia

> Como sistema, quiero enviar los recordatorios por la API oficial de WhatsApp, para llegar al canal que el paciente sí revisa, cumpliendo las reglas de Meta.

## Criterios de aceptación

- **CA-1** · Dado un recordatorio con canal WhatsApp, cuando se despacha, entonces se envía mediante la API oficial de WhatsApp Business Cloud usando una plantilla previamente aprobada por Meta.
- **CA-2** · Dado que se envía el mensaje, cuando la API responde, entonces el sistema registra el identificador del mensaje y su estado (enviado, entregado, leído, fallido).
- **CA-3** · Dado que el envío falla, cuando se agotan los reintentos configurados, entonces el recordatorio se marca como fallido y queda habilitado el respaldo por otro canal.
- **CA-4** · Dado el código del cliente, cuando se revisa, entonces ninguna credencial de WhatsApp está presente en él: todo envío sale del backend.

## Tareas y actividades

### T-033.1 Cuenta y plantillas de WhatsApp

- Configurar la cuenta de WhatsApp Business
- Redactar y someter plantillas a aprobación
- Versionar plantillas por tipo de mensaje

### T-033.2 Servicio de envío en backend

- Cliente de la API oficial con credenciales del servidor
- Cola de envío con reintentos
- Registro de identificadores de mensaje

### T-033.3 Webhook de estados

- Endpoint de recepción de estados
- Validación de firma del webhook
- Actualización del estado del recordatorio

### T-033.4 Pruebas

- Prueba con número de pruebas de Meta
- Prueba de fallo y reintento
- Revisión de que no haya credenciales en el cliente

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-032 Configurar canal preferido de aviso](HU-032-configurar-canal-preferido-de-aviso.md)

**Habilita** — no pueden construirse sin esta:

- [HU-043 Cumplimiento de plantillas y ventana de 24 horas](../E03-agendamiento-y-atencion-por-whatsapp/HU-043-cumplimiento-de-plantillas-y-ventana-de-24-horas.md)
- [HU-038 Agendar una cita por WhatsApp](../E03-agendamiento-y-atencion-por-whatsapp/HU-038-agendar-una-cita-por-whatsapp.md)
- [HU-040 Cancelar o reagendar respondiendo el mensaje](../E03-agendamiento-y-atencion-por-whatsapp/HU-040-cancelar-o-reagendar-respondiendo-el-mensaje.md)
- [HU-041 Confirmar asistencia el día anterior](../E03-agendamiento-y-atencion-por-whatsapp/HU-041-confirmar-asistencia-el-dia-anterior.md)
- [HU-042 Consultar «mi próxima cita» por WhatsApp](../E03-agendamiento-y-atencion-por-whatsapp/HU-042-consultar-mi-proxima-cita-por-whatsapp.md)
- [HU-045 Confirmar la toma desde WhatsApp](HU-045-confirmar-la-toma-desde-whatsapp.md)
- [HU-046 Reintento por canal alterno](HU-046-reintento-por-canal-alterno.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
