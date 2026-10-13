# HU-045 — Confirmar la toma desde WhatsApp

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-37 |
| Jira | pendiente de cargar |

## Historia

> Como paciente, quiero confirmar la toma respondiendo el mensaje, para no tener que abrir la aplicación.

## Criterios de aceptación

- **CA-1** · Dado que recibo el recordatorio de medicamento, cuando llega, entonces incluye las opciones «Ya la tomé» y «Posponer 15 minutos».
- **CA-2** · Dado que respondo «Ya la tomé», cuando se procesa, entonces la confirmación queda registrada igual que si la hubiera marcado en la app.
- **CA-3** · Dado que respondo «Posponer», cuando se procesa, entonces el sistema reenvía el recordatorio 15 minutos después, máximo dos veces.
- **CA-4** · Dado que respondo mucho después de la hora, cuando se registra, entonces queda como cumplida con retraso, con la hora real de la respuesta.

## Tareas y actividades

### T-045.1 Plantilla de recordatorio con acciones

- Redactar y aprobar la plantilla con botones
- Incluir nombre del medicamento y hora
- Vincular la respuesta con el recordatorio

### T-045.2 Procesamiento de la confirmación

- Asociar la respuesta al recordatorio correcto
- Registrar confirmación idempotente
- Implementar el aplazamiento con límite

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-029 Programación automática de recordatorios de medicamento](HU-029-programacion-automatica-de-recordatorios-de-medica.md)
- [HU-033 Envío por WhatsApp con plantillas aprobadas](HU-033-envio-por-whatsapp-con-plantillas-aprobadas.md)

**Habilita** — no pueden construirse sin esta:

- [HU-047 Cálculo del indicador de adherencia](HU-047-calculo-del-indicador-de-adherencia.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
