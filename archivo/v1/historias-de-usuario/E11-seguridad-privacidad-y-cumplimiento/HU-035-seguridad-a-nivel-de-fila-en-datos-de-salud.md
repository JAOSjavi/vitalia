# HU-035 — Seguridad a nivel de fila en datos de salud

| Dato | Valor |
|---|---|
| Épica | E11 Seguridad, privacidad y cumplimiento |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 13 puntos |
| Requisitos | RF-04 |
| Jira | SCRUM-98 |

## Historia

> Como responsable del sistema, quiero que la base de datos filtre por identidad autenticada, para que un usuario no pueda leer datos de otro ni aunque la aplicación tenga un error.

## Criterios de aceptación

- **CA-1** · Dado el conjunto de tablas con datos de salud, cuando se revisa su configuración, entonces todas tienen seguridad a nivel de fila habilitada y ninguna política usa una condición abierta (USING true).
- **CA-2** · Dado un usuario autenticado como paciente, cuando consulta directamente una tabla clínica, entonces solo obtiene las filas cuyo paciente corresponde a su identidad.
- **CA-3** · Dado un usuario autenticado como médico, cuando consulta datos clínicos, entonces solo obtiene los de pacientes con los que tiene relación de atención vigente.
- **CA-4** · Dado el conjunto de pruebas automatizadas, cuando se ejecuta la suite de seguridad, entonces incluye pruebas negativas que fallan si alguna política queda abierta.

## Tareas y actividades

### T-035.1 Inventario y clasificación de tablas

- Identificar tablas con datos de salud
- Clasificar por sensibilidad
- Definir la regla de acceso de cada una

### T-035.2 Implementación de políticas

- Habilitar seguridad a nivel de fila
- Escribir políticas por rol y operación
- Resolver la identidad desde el token

### T-035.3 Relación médico–paciente

- Modelar la relación de atención vigente
- Usarla en las políticas del rol médico
- Definir su caducidad

### T-035.4 Suite de pruebas de seguridad

- Pruebas negativas por rol y tabla
- Verificación automática de ausencia de USING true
- Integración en el flujo de despliegue

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-005 Roles y permisos resueltos en base de datos](../E01-autenticacion-cuentas-y-roles/HU-005-roles-y-permisos-resueltos-en-base-de-datos.md)

**Habilita** — no pueden construirse sin esta:

- [HU-057 Aislamiento de información entre sedes](../E09-panel-administrativo-y-multi-clinica/HU-057-aislamiento-de-informacion-entre-sedes.md)


---

[← Volver a E11](README.md) · [Mapa de relaciones](../RELACIONES.md)
