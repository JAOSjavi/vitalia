# HU-005 — Roles y permisos resueltos en base de datos

| Dato | Valor |
|---|---|
| Épica | E1 Autenticación, cuentas y roles |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-04 |
| Jira | SCRUM-21 |

## Historia

> Como responsable del sistema, quiero que los roles y permisos vivan en la base de datos, para que ningún usuario privilegiado quede escrito en el código.

## Criterios de aceptación

- **CA-1** · Dado el modelo de datos, cuando se revisa el código fuente, entonces no existe ningún identificador de «superusuario» ni credencial fija escrita en él.
- **CA-2** · Dado un usuario con rol paciente, cuando invoca un endpoint reservado a médico o administrador, entonces el sistema responde 403 y registra el intento.
- **CA-3** · Dado que un administrador cambia el rol de un usuario, cuando se guarda el cambio, entonces aplica en la siguiente petición y queda registrado en auditoría con autor y fecha.
- **CA-4** · Dado un usuario sin rol asignado, cuando intenta cualquier operación, entonces el sistema le niega el acceso por defecto (denegación implícita).

## Tareas y actividades

### T-005.1 Modelo de roles y permisos

- Tablas rol, permiso, rol_permiso, usuario_rol
- Sembrar los cuatro roles del producto
- Definir la matriz de permisos por endpoint

### T-005.2 Middleware de autorización

- Resolver roles desde el token y la base
- Validar permiso por operación
- Responder 403 y registrar el intento

### T-005.3 Pruebas de control de acceso

- Matriz de pruebas rol × endpoint
- Prueba de escalamiento de privilegios
- Prueba de denegación por defecto

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- Ninguna. Es punto de partida.

**Habilita** — no pueden construirse sin esta:

- [HU-014 Agenda del día del profesional](../E02-gestion-de-citas/HU-014-agenda-del-dia-del-profesional.md)
- [HU-017 Consultar la historia clínica del paciente](../E04-historia-clinica-y-documentos/HU-017-consultar-la-historia-clinica-del-paciente.md)
- [HU-020 Bitácora de auditoría de accesos](../E11-seguridad-privacidad-y-cumplimiento/HU-020-bitacora-de-auditoria-de-accesos.md)
- [HU-035 Seguridad a nivel de fila en datos de salud](../E11-seguridad-privacidad-y-cumplimiento/HU-035-seguridad-a-nivel-de-fila-en-datos-de-salud.md)
- [HU-055 Gestionar profesionales](../E09-panel-administrativo-y-multi-clinica/HU-055-gestionar-profesionales.md)


---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
