# HU-029 — Programación automática de recordatorios de medicamento

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-32 |
| Jira | SCRUM-92 |

## Historia

> Como sistema, quiero programar los recordatorios de cada toma a partir del plan, para que el paciente reciba el aviso a la hora correcta sin que nadie lo configure.

## Criterios de aceptación

- **CA-1** · Dado que se guarda un medicamento con frecuencia y duración, cuando se confirma el plan, entonces el sistema genera la serie completa de recordatorios hasta la fecha de fin.
- **CA-2** · Dado que llega la hora programada, cuando el proceso se ejecuta, entonces el recordatorio se envía dentro de una ventana de ±5 minutos.
- **CA-3** · Dado que el médico modifica o suspende el medicamento, cuando guarda el cambio, entonces el sistema cancela los recordatorios pendientes y regenera los que correspondan.
- **CA-4** · Dado que el tratamiento llegó a su fecha de fin, cuando se evalúa, entonces no se envía ningún recordatorio adicional de ese ítem.

## Tareas y actividades

### T-029.1 Modelo de recordatorios

- Tabla recordatorio con tipo, destino, hora y estado
- Índices por fecha de ejecución
- Estados: programado, enviado, fallido, cancelado

### T-029.2 Generador de series

- Expandir frecuencia en ocurrencias
- Respetar zona horaria del paciente
- Regenerar ante cambios del plan

### T-029.3 Ejecutor programado

- Tarea que consulta pendientes por minuto
- Despachar al canal correspondiente
- Reintento y marcado de estado

### T-029.4 Pruebas

- Prueba de generación por frecuencia
- Prueba de cancelación por cambio de plan
- Prueba de ventana de entrega

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-021 Registrar medicamentos del plan](../E05-plan-de-tratamiento-post-consulta/HU-021-registrar-medicamentos-del-plan.md)
- [HU-026 Fecha de fin automática del tratamiento](../E05-plan-de-tratamiento-post-consulta/HU-026-fecha-de-fin-automatica-del-tratamiento.md)

**Habilita** — no pueden construirse sin esta:

- [HU-044 Marcar un recordatorio como cumplido en la app](HU-044-marcar-un-recordatorio-como-cumplido-en-la-app.md)
- [HU-045 Confirmar la toma desde WhatsApp](HU-045-confirmar-la-toma-desde-whatsapp.md)
- [HU-068 Vista del cuidador](../E11-seguridad-privacidad-y-cumplimiento/HU-068-vista-del-cuidador.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
