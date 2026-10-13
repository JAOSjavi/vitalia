# HU-021 — Registrar medicamentos del plan

| Dato | Valor |
|---|---|
| Épica | E5 Plan de tratamiento post-consulta |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-24 |
| Jira | SCRUM-84 |

## Historia

> Como médico, quiero registrar los medicamentos con dosis, frecuencia y duración al cerrar la consulta, para que el paciente reciba recordatorios exactos.

## Criterios de aceptación

- **CA-1** · Dado que selecciono un medicamento del catálogo e indico dosis, frecuencia y duración, cuando guardo, entonces queda incorporado al plan vigente del paciente.
- **CA-2** · Dado que registré la frecuencia, cuando se guarda el medicamento, entonces el sistema calcula los horarios de toma y los deja listos para programar recordatorios.
- **CA-3** · Dado que intento guardar sin dosis, sin frecuencia o sin duración, cuando envío el formulario, entonces el sistema lo impide e indica el campo faltante.
- **CA-4** · Dado que agrego varios medicamentos, cuando cierro la consulta, entonces todos quedan en el mismo plan asociado a esa cita.

## Tareas y actividades

### T-021.1 Modelo de plan y medicamentos

- Tablas plan_tratamiento, plan_medicamento
- Vínculo con cita, paciente y profesional
- Estados del plan: activo, finalizado, suspendido

### T-021.2 Cálculo de horarios de toma

- Traducir frecuencia a horarios concretos
- Permitir ajuste manual del horario inicial
- Generar la serie hasta la fecha de fin

### T-021.3 Formulario de prescripción

- Buscador de medicamento
- Campos de dosis, frecuencia y duración
- Lista editable de medicamentos del plan

### T-021.4 Pruebas

- Prueba de cálculo de horarios por frecuencia
- Prueba de validaciones
- Prueba de plan con varios medicamentos

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-022 Catálogo de medicamentos](HU-022-catalogo-de-medicamentos.md)
- [HU-015 Registrar la nota clínica de la consulta](../E04-historia-clinica-y-documentos/HU-015-registrar-la-nota-clinica-de-la-consulta.md)

**Habilita** — no pueden construirse sin esta:

- [HU-023 Aviso de interacciones básicas](HU-023-aviso-de-interacciones-basicas.md)
- [HU-026 Fecha de fin automática del tratamiento](HU-026-fecha-de-fin-automatica-del-tratamiento.md)
- [HU-027 Ver «Mi plan de tratamiento»](HU-027-ver-mi-plan-de-tratamiento.md)
- [HU-029 Programación automática de recordatorios de medicamento](../E06-recordatorios-multicanal-y-adherencia/HU-029-programacion-automatica-de-recordatorios-de-medica.md)


---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
