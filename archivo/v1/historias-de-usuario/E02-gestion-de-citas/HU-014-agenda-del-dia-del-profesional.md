# HU-014 — Agenda del día del profesional

| Dato | Valor |
|---|---|
| Épica | E2 Gestión de citas |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-07, RF-12 |
| Jira | SCRUM-30 |

## Historia

> Como médico, quiero ver mi agenda del día ordenada, para saber a quién atiendo, a qué hora y por qué motivo.

## Criterios de aceptación

- **CA-1** · Dado que ingreso al panel, cuando carga la agenda, entonces veo las citas del día en orden cronológico con hora, paciente, tipo de cita y estado.
- **CA-2** · Dado que atiendo en varias sedes, cuando selecciono una sede, entonces la agenda muestra únicamente las citas de esa sede.
- **CA-3** · Dado que toco una cita, cuando se abre, entonces accedo al resumen de historia clínica del paciente y a las acciones de la consulta.
- **CA-4** · Dado que un paciente tiene adherencia por debajo del umbral, cuando veo la agenda, entonces su cita aparece marcada con un distintivo de alerta.

## Tareas y actividades

### T-014.1 Endpoint de agenda diaria

- Filtrar por profesional, fecha y sede
- Incluir indicadores del paciente
- Restringir por identidad autenticada

### T-014.2 Vista de agenda en el panel

- Lista cronológica con estados
- Selector de sede y de fecha
- Distintivos de alerta

### T-014.3 Pruebas

- Prueba de aislamiento entre profesionales
- Prueba de filtro por sede
- Prueba de orden y estados

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-008 Verificación de disponibilidad en tiempo real](HU-008-verificacion-de-disponibilidad-en-tiempo-real.md)
- [HU-005 Roles y permisos resueltos en base de datos](../E01-autenticacion-cuentas-y-roles/HU-005-roles-y-permisos-resueltos-en-base-de-datos.md)

**Habilita** — no pueden construirse sin esta:

- [HU-013 Registrar asistencia o inasistencia](HU-013-registrar-asistencia-o-inasistencia.md)


---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
