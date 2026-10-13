# HU-050 — Ver mi propia adherencia

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Should (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-38 |
| Jira | pendiente de cargar |

## Historia

> Como paciente, quiero ver cómo voy cumpliendo mi tratamiento, para saber si lo estoy haciendo bien.

## Criterios de aceptación

- **CA-1** · Dado que abro mis recordatorios, cuando carga la pantalla, entonces veo mi porcentaje de adherencia del mes con una barra de progreso.
- **CA-2** · Dado que veo el indicador, cuando lo leo, entonces el texto aclara que mi médico también lo ve.
- **CA-3** · Dado que mi adherencia baja del umbral, cuando se muestra, entonces aparece un mensaje de apoyo, sin lenguaje culpabilizador.

## Tareas y actividades

### T-050.1 Endpoint del indicador del paciente

- Devolver adherencia del periodo
- Filtrar por identidad autenticada

### T-050.2 Componente visual

- Barra de progreso y porcentaje
- Mensajes por rango de cumplimiento
- Revisión del tono de los textos

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-047 Cálculo del indicador de adherencia](HU-047-calculo-del-indicador-de-adherencia.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
