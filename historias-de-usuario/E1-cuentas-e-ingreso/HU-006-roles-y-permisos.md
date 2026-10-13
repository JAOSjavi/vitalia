# HU-006 — Roles y permisos de médico y paciente

| Dato | Valor |
|---|---|
| Épica | E1 Cuentas e ingreso |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-07 |
| Origen | HU-005 de la versión anterior, ajustada |

## Historia

> Como responsable del sistema, quiero que los roles de médico y paciente vivan en la base de datos, para que nadie tenga privilegios escritos en el código.

## Criterios de aceptación

- **CA-1** · Dado el código fuente, cuando se revisa, entonces no existe ningún usuario ni credencial privilegiada escrita en él.
- **CA-2** · Dado un usuario con rol paciente, cuando llama una operación reservada al médico, entonces el sistema responde con acceso denegado y registra el intento.
- **CA-3** · Dado un usuario sin rol asignado, cuando intenta cualquier operación, entonces el sistema le niega el acceso.
- **CA-4** · Dada la matriz de permisos, cuando se agrega una operación nueva, entonces queda denegada para todos hasta que se le asigne un rol.

## Tareas y actividades

### T-006.1 Modelo de roles

- Tablas de rol y de asignación por usuario
- Cargar los roles médico y paciente
- Matriz de permisos por operación

### T-006.2 Control de autorización

- Resolver el rol en cada petición
- Validar el permiso de la operación
- Responder acceso denegado y registrar el intento

### T-006.3 Pruebas

- Matriz de pruebas de rol por operación
- Prueba de escalamiento de privilegios
- Prueba de denegación por defecto

## Relación con otras historias

**Depende de:**

- Ninguna. Es punto de partida.

**Habilita:**

- [HU-001 Configuración inicial del consultorio](HU-001-configuracion-inicial-del-consultorio.md)
- [HU-002 Registro de paciente](HU-002-registro-de-paciente.md)
- [HU-023 Lista y búsqueda de pacientes](../E4-panel-del-medico/HU-023-lista-y-busqueda-de-pacientes.md)
- [HU-027 Almacenamiento privado con enlace temporal](../E5-historias-clinicas-del-paciente/HU-027-almacenamiento-privado-con-enlace-temporal.md)
- [HU-036 Permisos por fila en la base de datos](../E7-seguridad-base/HU-036-permisos-por-fila.md)
- [HU-037 Bitácora de auditoría](../E7-seguridad-base/HU-037-bitacora-de-auditoria.md)

---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
