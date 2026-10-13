# HU-041 — Datos de identificación de la historia clínica

| Dato | Valor |
|---|---|
| Épica | E9 Historia clínica del consultorio |
| Rol | Paciente, Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-41 |
| Origen | Nueva (decisión D-24) |

## Historia

> Como médico, quiero que la historia clínica de cada paciente tenga los datos de identificación que exige la norma, para abrirla correctamente en su primera atención.

## Criterios de aceptación

- **CA-1** · Dado un paciente, cuando él mismo desde su perfil o el médico desde la ficha completa sexo, estado civil, ocupación, dirección, municipio de residencia, aseguradora y tipo de vinculación, entonces esos datos quedan guardados.
- **CA-2** · Dado un paciente al que le faltan esos datos, cuando el médico abre una atención, entonces el sistema los muestra como pendientes y permite llenarlos ahí mismo.
- **CA-3** · Dado que faltan datos obligatorios de identificación, cuando el médico intenta cerrar la atención, entonces el sistema no la cierra y dice cuáles faltan.
- **CA-4** · Dado un paciente particular, sin aseguradora, cuando se llena ese dato, entonces se puede marcar "particular".
- **CA-5** · Dado un paciente que tiene una persona responsable, cuando se registran su nombre, su teléfono y su parentesco, entonces quedan en la historia.

## Tareas y actividades

### T-041.1 Modelo

- Campos de identificación de la historia clínica
- Listas de valores: sexo, estado civil, municipio y tipo de vinculación
- Regla de datos obligatorios para cerrar una atención

### T-041.2 Formularios

- Sección en el perfil del paciente
- Sección en la ficha y en la pantalla de atención
- Aviso de datos pendientes

### T-041.3 Pruebas

- Cierre con datos faltantes
- Paciente particular
- Persona responsable

## Nota de alcance

Los datos salen del artículo 9 de la Resolución 1995 de 1999. El registro de la cuenta se queda corto (decisión D-21); estos datos se completan una sola vez. El acompañante se anota en cada atención (HU-043).

## Relación con otras historias

**Depende de:**

- [HU-025 Ficha del paciente](../E4-panel-del-medico/HU-025-ficha-del-paciente.md)

**Habilita:**

- [HU-044 Cerrar y firmar la atención](HU-044-cerrar-y-firmar-la-atencion.md)

---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
