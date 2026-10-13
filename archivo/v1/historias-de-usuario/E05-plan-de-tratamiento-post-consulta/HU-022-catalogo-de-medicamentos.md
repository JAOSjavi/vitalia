# HU-022 — Catálogo de medicamentos

| Dato | Valor |
|---|---|
| Épica | E5 Plan de tratamiento post-consulta |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-25 |
| Jira | SCRUM-85 |

## Historia

> Como médico, quiero elegir el medicamento de un catálogo y no escribirlo a mano, para evitar errores de nombre y habilitar la revisión de interacciones.

## Criterios de aceptación

- **CA-1** · Dado que escribo al menos tres letras, cuando busco, entonces el sistema sugiere medicamentos por nombre genérico y presentación.
- **CA-2** · Dado que selecciono un medicamento, cuando se agrega al plan, entonces se guarda su identificador del catálogo, no solo el texto.
- **CA-3** · Dado que el medicamento no está en el catálogo, cuando lo requiero, entonces el sistema permite registrarlo como excepción marcada para revisión, sin bloquear la consulta.
- **CA-4** · Dado que el catálogo se actualiza, cuando se carga una nueva versión, entonces los planes existentes conservan la referencia con la que fueron creados.

## Tareas y actividades

### T-022.1 Carga del catálogo

- Definir la fuente de referencia y su formato
- Proceso de importación y actualización
- Versionado del catálogo

### T-022.2 Servicio de búsqueda

- Búsqueda por nombre genérico y comercial
- Orden por relevancia
- Límite de resultados

### T-022.3 Excepciones controladas

- Registro de medicamento fuera de catálogo
- Marca para revisión posterior
- Reporte de excepciones

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- Ninguna. Es punto de partida.

**Habilita** — no pueden construirse sin esta:

- [HU-021 Registrar medicamentos del plan](HU-021-registrar-medicamentos-del-plan.md)
- [HU-023 Aviso de interacciones básicas](HU-023-aviso-de-interacciones-basicas.md)


---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
