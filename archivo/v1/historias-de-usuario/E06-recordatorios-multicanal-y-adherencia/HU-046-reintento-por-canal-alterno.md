# HU-046 — Reintento por canal alterno

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 2 |
| Rol | Sistema |
| Prioridad | Should (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-36 |
| Jira | pendiente de cargar |

## Historia

> Como sistema, quiero intentar por otro canal cuando el primero falla, para que el recordatorio llegue de todas formas.

## Criterios de aceptación

- **CA-1** · Dado que el envío por WhatsApp falla o no se entrega en el plazo definido, cuando se evalúa, entonces el sistema reintenta por SMS.
- **CA-2** · Dado que el reintento también falla, cuando se agotan los canales configurados, entonces el recordatorio se marca como no entregado y queda visible en el panel del profesional.
- **CA-3** · Dado que el mensaje sí se entregó por el canal principal, cuando se evalúa, entonces no se envía por ningún canal adicional (sin mensajes duplicados).
- **CA-4** · Dado que ocurre un reintento, cuando se ejecuta, entonces queda registrado el canal usado, el motivo del fallo anterior y el resultado.

## Tareas y actividades

### T-046.1 Política de escalamiento de canales

- Definir el orden y los plazos de espera
- Configurar por tipo de recordatorio
- Evitar duplicados por confirmación de entrega

### T-046.2 Proceso de reintento

- Evaluar estados de entrega pendientes
- Despachar por el canal siguiente
- Registrar la trazabilidad del intento

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-033 Envío por WhatsApp con plantillas aprobadas](HU-033-envio-por-whatsapp-con-plantillas-aprobadas.md)
- [HU-034 Envío por SMS](HU-034-envio-por-sms.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
