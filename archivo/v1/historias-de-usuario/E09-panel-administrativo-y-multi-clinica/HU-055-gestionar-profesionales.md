# HU-055 — Gestionar profesionales

| Dato | Valor |
|---|---|
| Épica | E9 Panel administrativo y multi-clínica |
| Fase | 3 |
| Rol | Administrador |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-49 |
| Jira | pendiente de cargar |

## Historia

> Como administrador de la clínica, quiero registrar y administrar a los profesionales, para mantener la agenda al día cuando alguien entra o sale.

## Criterios de aceptación

- **CA-1** · Dado que registro un profesional con nombre, documento, especialidad y sedes donde atiende, cuando guardo, entonces queda habilitado para recibir citas en esas sedes.
- **CA-2** · Dado que desactivo a un profesional, cuando se guarda, entonces deja de aparecer en el agendamiento, pero sus citas y su historia clínica registrada se conservan.
- **CA-3** · Dado que un profesional tiene citas futuras, cuando intento desactivarlo, entonces el sistema advierte cuántas citas hay y exige decidir si se reasignan o se cancelan.
- **CA-4** · Dado que administro profesionales de mi clínica, cuando consulto la lista, entonces no veo profesionales de otras clínicas.

## Tareas y actividades

Sin desglosar. Esta historia pertenece a una fase posterior y se refina antes de entrar a un sprint.

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-005 Roles y permisos resueltos en base de datos](../E01-autenticacion-cuentas-y-roles/HU-005-roles-y-permisos-resueltos-en-base-de-datos.md)

**Habilita** — no pueden construirse sin esta:

- [HU-056 Gestionar horarios de atención](HU-056-gestionar-horarios-de-atencion.md)
- [HU-057 Aislamiento de información entre sedes](HU-057-aislamiento-de-informacion-entre-sedes.md)


---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
