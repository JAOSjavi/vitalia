# HU-011 — Consultar mis citas pasadas y futuras

| Dato | Valor |
|---|---|
| Épica | E2 Gestión de citas |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-10 |
| Jira | SCRUM-27 |

## Historia

> Como paciente, quiero ver mis citas anteriores y las próximas, para saber cuándo me atendieron y qué tengo pendiente.

## Criterios de aceptación

- **CA-1** · Dado que abro «Mis citas», cuando carga la pantalla, entonces veo dos grupos: próximas (ascendente) y anteriores (descendente), cada una con fecha, hora, profesional, sede y estado.
- **CA-2** · Dado que toco una cita anterior atendida, cuando se abre el detalle, entonces accedo al plan de tratamiento y a los documentos generados en esa consulta.
- **CA-3** · Dado que no tengo citas registradas, cuando abro la pantalla, entonces veo un mensaje explicativo y un acceso directo a agendar.
- **CA-4** · Dado que otro paciente intenta consultar mis citas por el identificador, cuando hace la petición, entonces el sistema responde 403 sin exponer información.

## Tareas y actividades

### T-011.1 Endpoint de listado de citas

- Filtrar por identidad autenticada
- Ordenar y paginar por grupo
- Incluir datos del profesional y la sede

### T-011.2 Pantalla de historial

- Listas separadas de próximas y anteriores
- Estado visual por tipo de estado
- Estado vacío con acceso a agendar

### T-011.3 Detalle de cita

- Vincular plan de tratamiento y documentos
- Acciones disponibles según el estado

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-007 Agendar una cita desde la aplicación](HU-007-agendar-una-cita-desde-la-aplicacion.md)

**Habilita** — no pueden construirse sin esta:

- [HU-042 Consultar «mi próxima cita» por WhatsApp](../E03-agendamiento-y-atencion-por-whatsapp/HU-042-consultar-mi-proxima-cita-por-whatsapp.md)


---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
