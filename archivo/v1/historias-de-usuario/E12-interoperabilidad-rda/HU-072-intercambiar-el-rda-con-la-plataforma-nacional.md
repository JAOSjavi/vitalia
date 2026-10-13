# HU-072 — Intercambiar el RDA con la plataforma nacional

| Dato | Valor |
|---|---|
| Épica | E12 Interoperabilidad (RDA) |
| Fase | 4 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 13 puntos |
| Requisitos | RF-60 |
| Jira | pendiente de cargar |

## Historia

> Como IPS, quiero enviar y consultar el RDA en la plataforma de interoperabilidad, para que la historia del paciente esté disponible donde se le atienda.

## Criterios de aceptación

- **CA-1** · Dado un RDA generado, cuando se envía a la plataforma, entonces el sistema registra el identificador de la transacción y su resultado.
- **CA-2** · Dado que el envío falla, cuando se agotan los reintentos, entonces queda en una bandeja de pendientes con el motivo del error, para reenvío manual.
- **CA-3** · Dado que el paciente autorizó la consulta, cuando el médico solicita su resumen desde la plataforma, entonces el sistema lo recupera y lo muestra identificando su origen externo.
- **CA-4** · Dado cualquier intercambio, cuando ocurre, entonces queda registrado en la bitácora de auditoría con el detalle de la operación.

## Tareas y actividades

Sin desglosar. Esta historia pertenece a una fase posterior y se refina antes de entrar a un sprint.

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-071 Generar el Resumen Digital de Atención (RDA)](HU-071-generar-el-resumen-digital-de-atencion-rda.md)
- [HU-074 Consentimiento para compartir el resumen con otras instituciones](HU-074-consentimiento-para-compartir-el-resumen-con-otras.md)

**Habilita** — no pueden construirse sin esta:

- [HU-073 Registro de eventos de interoperabilidad](HU-073-registro-de-eventos-de-interoperabilidad.md)


---

[← Volver a E12](README.md) · [Mapa de relaciones](../RELACIONES.md)
