# HU-023 — Aviso de interacciones básicas

| Dato | Valor |
|---|---|
| Épica | E5 Plan de tratamiento post-consulta |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-26 |
| Jira | SCRUM-86 |

## Historia

> Como médico, quiero que el sistema me avise si el nuevo medicamento choca con uno activo, para revisar antes de confirmar la prescripción.

## Criterios de aceptación

- **CA-1** · Dado que el paciente tiene un medicamento activo, cuando agrego otro con interacción conocida, entonces el sistema muestra una advertencia con el par de medicamentos y el nivel de severidad.
- **CA-2** · Dado que aparece la advertencia, cuando decido continuar, entonces el sistema me permite confirmar de forma explícita y registra esa decisión en la historia.
- **CA-3** · Dado que no existe interacción registrada entre los medicamentos, cuando guardo, entonces el sistema indica que no se detectaron conflictos con los medicamentos activos.
- **CA-4** · Dado que la advertencia se muestra, cuando la leo, entonces el texto aclara que es una verificación de apoyo y no sustituye el criterio clínico.

## Tareas y actividades

### T-023.1 Base de interacciones

- Definir fuente y modelo de pares de interacción
- Cargar severidades
- Procedimiento de actualización

### T-023.2 Servicio de verificación

- Consultar medicamentos activos del paciente
- Evaluar pares e informar severidad
- Responder en línea al agregar

### T-023.3 Interfaz de advertencia

- Componente de alerta con severidad
- Confirmación explícita para continuar
- Registro de la decisión

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-021 Registrar medicamentos del plan](HU-021-registrar-medicamentos-del-plan.md)
- [HU-022 Catálogo de medicamentos](HU-022-catalogo-de-medicamentos.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
