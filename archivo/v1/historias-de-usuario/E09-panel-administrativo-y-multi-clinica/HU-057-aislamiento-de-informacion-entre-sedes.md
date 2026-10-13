# HU-057 — Aislamiento de información entre sedes

| Dato | Valor |
|---|---|
| Épica | E9 Panel administrativo y multi-clínica |
| Fase | 3 |
| Rol | Administrador, Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-48 |
| Jira | pendiente de cargar |

## Historia

> Como clínica con varias sedes, quiero que cada sede vea solo lo suyo, para mantener la operación ordenada y la información acotada.

## Criterios de aceptación

- **CA-1** · Dado que consulto la agenda desde una sede, cuando carga, entonces solo aparecen las citas de esa sede.
- **CA-2** · Dado un médico que atiende en varias sedes, cuando cambia de sede en el panel, entonces la información se actualiza a la sede seleccionada.
- **CA-3** · Dado un administrador de una sede, cuando intenta consultar datos de otra sede, entonces el sistema niega el acceso y registra el intento.
- **CA-4** · Dado un paciente atendido en dos sedes de la misma clínica, cuando su médico consulta la historia clínica, entonces ve el expediente completo, sin fragmentarlo por sede.

## Tareas y actividades

Sin desglosar. Esta historia pertenece a una fase posterior y se refina antes de entrar a un sprint.

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-055 Gestionar profesionales](HU-055-gestionar-profesionales.md)
- [HU-035 Seguridad a nivel de fila en datos de salud](../E11-seguridad-privacidad-y-cumplimiento/HU-035-seguridad-a-nivel-de-fila-en-datos-de-salud.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
