# HU-023 — Lista y búsqueda de pacientes

| Dato | Valor |
|---|---|
| Épica | E4 Panel del médico |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-22 |
| Origen | Nueva |

## Historia

> Como médico, quiero buscar a mis pacientes por nombre o documento, para llegar rápido a su ficha.

## Criterios de aceptación

- **CA-1** · Dado que escribo parte del nombre o del documento, cuando busco, entonces veo los pacientes que coinciden.
- **CA-2** · Dada la lista, cuando la abro sin buscar, entonces veo los pacientes en orden alfabético y por páginas.
- **CA-3** · Dado un resultado, cuando lo selecciono, entonces llego a la ficha del paciente.
- **CA-4** · Dado un usuario con rol paciente, cuando intenta abrir la lista, entonces el sistema le niega el acceso.

## Tareas y actividades

### T-023.1 Servicio de búsqueda

- Búsqueda por nombre y por documento
- Paginación
- Restricción al rol médico

### T-023.2 Pantalla de pacientes

- Buscador
- Lista con los datos básicos
- Acceso a la ficha

## Relación con otras historias

**Depende de:**

- [HU-006 Roles y permisos de médico y paciente](../E1-cuentas-e-ingreso/HU-006-roles-y-permisos.md)

**Habilita:**

- [HU-016 Crear una cita para un paciente](../E3-citas/HU-016-crear-una-cita-para-un-paciente.md)
- [HU-024 Registrar un paciente desde el panel](HU-024-registrar-un-paciente-desde-el-panel.md)
- [HU-025 Ficha del paciente](HU-025-ficha-del-paciente.md)

---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
