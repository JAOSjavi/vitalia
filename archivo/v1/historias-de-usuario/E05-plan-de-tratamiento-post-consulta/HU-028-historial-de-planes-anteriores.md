# HU-028 — Historial de planes anteriores

| Dato | Valor |
|---|---|
| Épica | E5 Plan de tratamiento post-consulta |
| Fase | 1 |
| Rol | Paciente, Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-31 |
| Jira | SCRUM-91 |

## Historia

> Como paciente o médico, quiero consultar los planes de consultas anteriores, para comparar el tratamiento actual con los previos.

## Criterios de aceptación

- **CA-1** · Dado que abro el historial, cuando carga, entonces veo los planes anteriores con fecha, profesional y estado, del más reciente al más antiguo.
- **CA-2** · Dado que abro un plan anterior, cuando se despliega, entonces muestra su contenido tal como estuvo vigente, sin mezclarse con el plan actual.
- **CA-3** · Dado que soy médico, cuando consulto el historial de planes de un paciente que atiendo, entonces el acceso queda registrado en la bitácora de auditoría.

## Tareas y actividades

### T-028.1 Endpoint de historial de planes

- Listar planes finalizados por paciente
- Preservar el contenido histórico
- Registrar el acceso cuando es profesional

### T-028.2 Vista de historial

- Lista cronológica inversa
- Detalle de solo lectura
- Distintivo de plan vigente

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-027 Ver «Mi plan de tratamiento»](HU-027-ver-mi-plan-de-tratamiento.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
