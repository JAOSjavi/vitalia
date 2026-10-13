# HU-043 — Cumplimiento de plantillas y ventana de 24 horas

| Dato | Valor |
|---|---|
| Épica | E3 Agendamiento y atención por WhatsApp |
| Fase | 2 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-18 |
| Jira | pendiente de cargar |

## Historia

> Como responsable del producto, quiero respetar las reglas de Meta en todo mensaje saliente, para no arriesgar el bloqueo de la línea de la clínica.

## Criterios de aceptación

- **CA-1** · Dado un mensaje proactivo (fuera de la ventana de 24 horas), cuando se envía, entonces usa obligatoriamente una plantilla aprobada.
- **CA-2** · Dado que el paciente escribió hace menos de 24 horas, cuando respondemos, entonces el sistema permite mensaje libre y lo registra como respuesta dentro de la ventana.
- **CA-3** · Dado que se intenta enviar texto libre fuera de la ventana, cuando se procesa, entonces el sistema lo bloquea antes de llamar a la API y registra el intento.
- **CA-4** · Dado que Meta rechaza o suspende una plantilla, cuando ocurre, entonces el sistema marca esa plantilla como inutilizable y alerta al administrador.

## Tareas y actividades

### T-043.1 Control de la ventana de conversación

- Registrar el último mensaje entrante por número
- Calcular la vigencia de la ventana
- Seleccionar plantilla o texto libre según corresponda

### T-043.2 Gestión del catálogo de plantillas

- Registro local de plantillas y su estado
- Sincronizar el estado con Meta
- Alertar al administrador ante rechazos

### T-043.3 Pruebas de cumplimiento

- Prueba de bloqueo fuera de la ventana
- Prueba de uso correcto de plantillas
- Prueba de plantilla inhabilitada

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-033 Envío por WhatsApp con plantillas aprobadas](../E06-recordatorios-multicanal-y-adherencia/HU-033-envio-por-whatsapp-con-plantillas-aprobadas.md)

**Habilita** — no pueden construirse sin esta:

- [HU-038 Agendar una cita por WhatsApp](HU-038-agendar-una-cita-por-whatsapp.md)


---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
