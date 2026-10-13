# HU-020 — Bitácora de auditoría de accesos

| Dato | Valor |
|---|---|
| Épica | E11 Seguridad, privacidad y cumplimiento |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-56 |
| Jira | SCRUM-83 |

## Historia

> Como responsable de cumplimiento, quiero que quede registro de cada acceso a una historia clínica, para responder ante una auditoría o un reclamo.

## Criterios de aceptación

- **CA-1** · Dado que alguien consulta, crea o modifica información clínica, cuando ocurre la operación, entonces el sistema registra actor, rol, paciente afectado, acción, fecha y hora, y origen de la petición.
- **CA-2** · Dado un registro de auditoría creado, cuando se intenta modificar o eliminar por cualquier vía de la aplicación, entonces la operación es rechazada (bitácora de solo anexado).
- **CA-3** · Dado que se consulta la bitácora, cuando se filtra por paciente o por rango de fechas, entonces devuelve los eventos correspondientes ordenados cronológicamente.
- **CA-4** · Dado que falla el registro en la bitácora, cuando se procesa una operación clínica, entonces la operación no se da por exitosa y se reporta el error.

## Tareas y actividades

### T-020.1 Modelo de bitácora

- Tabla auditoria de solo anexado
- Revocar permisos de actualización y borrado
- Índices por paciente y por fecha

### T-020.2 Instrumentación de operaciones clínicas

- Interceptor en endpoints clínicos
- Registro dentro de la transacción
- Manejo de fallo del registro

### T-020.3 Consulta de la bitácora

- Endpoint con filtros
- Vista para el administrador
- Exportación para auditoría

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-005 Roles y permisos resueltos en base de datos](../E01-autenticacion-cuentas-y-roles/HU-005-roles-y-permisos-resueltos-en-base-de-datos.md)

**Habilita** — no pueden construirse sin esta:

- [HU-070 Consultar quién ha accedido a mi historia clínica](HU-070-consultar-quien-ha-accedido-a-mi-historia-clinica.md)


---

[← Volver a E11](README.md) · [Mapa de relaciones](../RELACIONES.md)
