# HU-024 — Registrar cuidados e instrucciones

| Dato | Valor |
|---|---|
| Épica | E5 Plan de tratamiento post-consulta |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-27 |
| Jira | SCRUM-87 |

## Historia

> Como médico, quiero registrar los cuidados con su horario y material de apoyo, para que el paciente sepa exactamente qué hacer en casa.

## Criterios de aceptación

- **CA-1** · Dado que escribo una instrucción de cuidado con su frecuencia o fecha específica, cuando guardo, entonces queda en el plan y genera sus recordatorios correspondientes.
- **CA-2** · Dado que adjunto una imagen o un video corto de apoyo, cuando guardo, entonces el paciente puede verlo desde su plan.
- **CA-3** · Dado que el cuidado tiene fecha de finalización, cuando esa fecha pasa, entonces el sistema deja de enviar sus recordatorios.
- **CA-4** · Dado que redacto la instrucción, cuando la guardo, entonces el sistema la muestra al paciente en lenguaje simple, sin abreviaturas clínicas obligatorias.

## Tareas y actividades

### T-024.1 Modelo de cuidados

- Tabla plan_cuidado con frecuencia y vigencia
- Vínculo con material de apoyo
- Estados de vigencia

### T-024.2 Material de apoyo

- Carga de imagen o video corto
- Límite de tamaño y duración
- Servido con URL firmada

### T-024.3 Formulario de cuidados

- Campos de instrucción, frecuencia y vigencia
- Adjuntar material
- Vista previa de cómo lo verá el paciente

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-015 Registrar la nota clínica de la consulta](../E04-historia-clinica-y-documentos/HU-015-registrar-la-nota-clinica-de-la-consulta.md)

**Habilita** — no pueden construirse sin esta:

- [HU-027 Ver «Mi plan de tratamiento»](HU-027-ver-mi-plan-de-tratamiento.md)
- [HU-031 Recordatorio de cuidados en fecha específica](../E06-recordatorios-multicanal-y-adherencia/HU-031-recordatorio-de-cuidados-en-fecha-especifica.md)


---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
