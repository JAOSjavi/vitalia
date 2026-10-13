# HU-054 — Notificación de respuesta del médico

| Dato | Valor |
|---|---|
| Épica | E7 Comunicación paciente–médico entre consultas |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Should (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-42 |
| Jira | pendiente de cargar |

## Historia

> Como paciente, quiero enterarme cuando mi médico responde, para no tener que revisar la aplicación a cada rato.

## Criterios de aceptación

- **CA-1** · Dado que el médico responde mi reporte, cuando se envía la respuesta, entonces recibo un aviso por mi canal preferido indicando que tengo respuesta.
- **CA-2** · Dado que recibo el aviso, cuando lo abro, entonces me lleva directamente a la conversación correspondiente.
- **CA-3** · Dado que el aviso viaja por WhatsApp o SMS, cuando se compone, entonces no incluye contenido clínico: solo informa que hay una respuesta disponible.

## Tareas y actividades

### T-054.1 Evento de respuesta

- Emitir evento al responder
- Componer aviso sin contenido clínico
- Enviar por canal preferido

### T-054.2 Enlace profundo a la conversación

- Definir el enlace por conversación
- Manejar el caso de sesión cerrada

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-052 Responder o derivar a una cita de control](HU-052-responder-o-derivar-a-una-cita-de-control.md)
- [HU-032 Configurar canal preferido de aviso](../E06-recordatorios-multicanal-y-adherencia/HU-032-configurar-canal-preferido-de-aviso.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E7](README.md) · [Mapa de relaciones](../RELACIONES.md)
