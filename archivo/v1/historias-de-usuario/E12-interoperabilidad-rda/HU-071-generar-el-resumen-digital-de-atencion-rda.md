# HU-071 — Generar el Resumen Digital de Atención (RDA)

| Dato | Valor |
|---|---|
| Épica | E12 Interoperabilidad (RDA) |
| Fase | 4 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 13 puntos |
| Requisitos | RF-59 |
| Jira | pendiente de cargar |

## Historia

> Como IPS, quiero generar el RDA por cada atención, para cumplir la normativa de interoperabilidad de historia clínica.

## Criterios de aceptación

- **CA-1** · Dado que se cierra una consulta, cuando se genera el RDA, entonces contiene los datos exigidos por la normativa vigente en el formato definido.
- **CA-2** · Dado que faltan datos obligatorios para el RDA, cuando el médico intenta cerrar la consulta, entonces el sistema indica qué falta antes de permitir el cierre.
- **CA-3** · Dado que el RDA se genera, cuando se guarda, entonces queda vinculado a la atención y disponible para consulta y reenvío.
- **CA-4** · Dado que la normativa cambia de versión de formato, cuando se actualiza la configuración, entonces los RDA nuevos usan la versión vigente sin alterar los ya emitidos.

## Tareas y actividades

Sin desglosar. Esta historia pertenece a una fase posterior y se refina antes de entrar a un sprint.

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-015 Registrar la nota clínica de la consulta](../E04-historia-clinica-y-documentos/HU-015-registrar-la-nota-clinica-de-la-consulta.md)

**Habilita** — no pueden construirse sin esta:

- [HU-072 Intercambiar el RDA con la plataforma nacional](HU-072-intercambiar-el-rda-con-la-plataforma-nacional.md)


---

[← Volver a E12](README.md) · [Mapa de relaciones](../RELACIONES.md)
