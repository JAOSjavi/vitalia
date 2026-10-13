# HU-034 — Envío por SMS

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Should (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-35 |
| Jira | SCRUM-97 |

## Historia

> Como sistema, quiero poder enviar por SMS, para llegar a pacientes sin WhatsApp o cuando ese canal falla.

## Criterios de aceptación

- **CA-1** · Dado un recordatorio con canal SMS, cuando se despacha, entonces se envía por el proveedor configurado y se registra su estado.
- **CA-2** · Dado el límite de caracteres del SMS, cuando se compone el mensaje, entonces el contenido se ajusta sin perder la información esencial (qué, cuándo y dónde).
- **CA-3** · Dado que el envío falla, cuando se agotan los reintentos, entonces queda registrado como fallido con el motivo devuelto por el proveedor.

## Tareas y actividades

### T-034.1 Integración del proveedor de SMS

- Configurar credenciales en el backend
- Implementar envío y consulta de estado
- Manejar reintentos

### T-034.2 Composición de mensajes cortos

- Plantillas ajustadas a 160 caracteres
- Pruebas de truncamiento
- Verificación de caracteres especiales

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-032 Configurar canal preferido de aviso](HU-032-configurar-canal-preferido-de-aviso.md)

**Habilita** — no pueden construirse sin esta:

- [HU-046 Reintento por canal alterno](HU-046-reintento-por-canal-alterno.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
