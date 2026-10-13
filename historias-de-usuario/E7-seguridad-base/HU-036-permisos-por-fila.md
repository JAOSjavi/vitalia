# HU-036 — Permisos por fila en la base de datos

| Dato | Valor |
|---|---|
| Épica | E7 Seguridad base |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-36 |
| Origen | HU-035 de la versión anterior, ajustada |

## Historia

> Como responsable del sistema, quiero que la base de datos misma filtre lo que cada usuario puede ver, para que un error en la aplicación no exponga datos ajenos.

## Criterios de aceptación

- **CA-1** · Dado un paciente autenticado, cuando consulta cualquier tabla con datos de salud, entonces la base solo devuelve sus propias filas.
- **CA-2** · Dado el médico autenticado, cuando consulta, entonces ve los pacientes, las citas y los documentos del consultorio.
- **CA-3** · Dada una operación de la aplicación que olvida filtrar por usuario, cuando la ejecuta un paciente, entonces la base igual no devuelve filas ajenas.
- **CA-4** · Dadas las políticas de la base, cuando se ejecutan las pruebas del despliegue, entonces el despliegue falla si alguna tabla con datos de salud quedó sin política o con una política abierta.

## Tareas y actividades

### T-036.1 Políticas

- Política por tabla para el paciente y para el médico
- Identidad autenticada disponible dentro de la base
- Inventario de las tablas con datos de salud

### T-036.2 Pruebas negativas

- Paciente intentando leer datos de otro paciente
- Tabla sin política
- Bloqueo del despliegue cuando una prueba falla

## Relación con otras historias

**Depende de:**

- [HU-006 Roles y permisos de médico y paciente](../E1-cuentas-e-ingreso/HU-006-roles-y-permisos.md)

**Habilita:**

- Ninguna la tiene como requisito previo. Debe estar lista antes de cargar datos reales.

---

[← Volver a E7](README.md) · [Mapa de relaciones](../RELACIONES.md)
