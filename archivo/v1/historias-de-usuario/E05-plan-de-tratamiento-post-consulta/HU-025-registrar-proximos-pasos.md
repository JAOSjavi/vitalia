# HU-025 — Registrar próximos pasos

| Dato | Valor |
|---|---|
| Épica | E5 Plan de tratamiento post-consulta |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-28 |
| Jira | SCRUM-88 |

## Historia

> Como médico, quiero dejar registrados los próximos pasos del paciente, para que no se pierda el control ni el examen pendiente.

## Criterios de aceptación

- **CA-1** · Dado que registro un próximo paso (control, examen, remisión) con su fecha objetivo, cuando guardo, entonces aparece en el plan del paciente.
- **CA-2** · Dado que el próximo paso es un control, cuando se guarda, entonces el sistema ofrece al paciente agendarlo directamente desde su plan.
- **CA-3** · Dado que se acerca la fecha objetivo, cuando falta el plazo configurado, entonces el sistema envía un recordatorio del paso pendiente.
- **CA-4** · Dado que el paso se cumple, cuando se registra la cita o el documento correspondiente, entonces el paso se marca como cumplido.

## Tareas y actividades

### T-025.1 Modelo de próximos pasos

- Tabla plan_proximo_paso con tipo y fecha objetivo
- Estados: pendiente, cumplido, vencido
- Vínculo con cita o documento que lo cumple

### T-025.2 Acción de agendar desde el plan

- Botón de agendar control
- Prefijar tipo de cita y profesional
- Marcar el paso al confirmar

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-015 Registrar la nota clínica de la consulta](../E04-historia-clinica-y-documentos/HU-015-registrar-la-nota-clinica-de-la-consulta.md)

**Habilita** — no pueden construirse sin esta:

- [HU-027 Ver «Mi plan de tratamiento»](HU-027-ver-mi-plan-de-tratamiento.md)


---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
