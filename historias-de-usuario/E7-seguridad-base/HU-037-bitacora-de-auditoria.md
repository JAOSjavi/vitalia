# HU-037 — Bitácora de auditoría

| Dato | Valor |
|---|---|
| Épica | E7 Seguridad base |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-37 |
| Origen | HU-020 de la versión anterior, ajustada |

## Historia

> Como responsable del sistema, quiero un registro de quién accedió a qué y cuándo, para poder responder un reclamo y cumplir la norma.

## Criterios de aceptación

- **CA-1** · Dado que alguien abre una ficha o un documento, hace una consulta al asistente, o crea, mueve o cancela una cita, cuando ocurre, entonces queda un registro con usuario, rol, paciente afectado, acción, fecha y hora.
- **CA-2** · Dada la bitácora, cuando la aplicación intenta modificar o borrar un registro, entonces la base lo rechaza.
- **CA-3** · Dado que el registro en la bitácora falla, cuando se ejecuta una operación sobre datos clínicos, entonces la operación no se da por exitosa.
- **CA-4** · Dado el médico, cuando consulta la bitácora, entonces puede filtrarla por paciente y por fecha.

## Tareas y actividades

### T-037.1 Tabla de bitácora

- Estructura del registro
- Permisos de solo inserción
- Tiempo de conservación

### T-037.2 Registro desde los servicios

- Registro dentro de la misma transacción de la operación
- Acciones cubiertas: fichas, documentos, asistente y citas
- Consulta filtrada para el médico

### T-037.3 Pruebas

- Intento de modificar la bitácora
- Fallo del registro
- Cobertura de todas las acciones

## Relación con otras historias

**Depende de:**

- [HU-006 Roles y permisos de médico y paciente](../E1-cuentas-e-ingreso/HU-006-roles-y-permisos.md)

**Habilita:**

- Ninguna la tiene como requisito previo. La usan todas las historias que tocan datos clínicos.

---

[← Volver a E7](README.md) · [Mapa de relaciones](../RELACIONES.md)
