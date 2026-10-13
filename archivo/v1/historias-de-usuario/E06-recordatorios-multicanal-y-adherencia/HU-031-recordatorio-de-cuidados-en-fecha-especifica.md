# HU-031 — Recordatorio de cuidados en fecha específica

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Should (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-34 |
| Jira | SCRUM-94 |

## Historia

> Como paciente en recuperación, quiero que me recuerden los cuidados puntuales, para cumplir con la curación o el control indicado el día exacto.

## Criterios de aceptación

- **CA-1** · Dado un cuidado con fecha y hora definidas, cuando llega el momento, entonces recibo el recordatorio con la instrucción completa.
- **CA-2** · Dado un cuidado con frecuencia diaria, cuando se guarda, entonces se generan los recordatorios de todos los días de vigencia.
- **CA-3** · Dado que el cuidado tiene material de apoyo, cuando recibo el recordatorio en la app, entonces incluye el acceso a la imagen o video.

## Tareas y actividades

### T-031.1 Recordatorios de cuidado

- Generar ocurrencias por fecha o frecuencia
- Incluir instrucción en el contenido
- Vincular material de apoyo

### T-031.2 Pruebas

- Prueba de cuidado puntual y recurrente
- Prueba de fin de vigencia

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-024 Registrar cuidados e instrucciones](../E05-plan-de-tratamiento-post-consulta/HU-024-registrar-cuidados-e-instrucciones.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
