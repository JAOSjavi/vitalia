# HU-025 — Ficha del paciente

| Dato | Valor |
|---|---|
| Épica | E4 Panel del médico |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-24 |
| Origen | HU-017 de la versión anterior, ajustada |

## Historia

> Como médico, quiero ver en una sola pantalla los datos, las citas y los documentos de un paciente, para prepararme antes de atenderlo.

## Criterios de aceptación

- **CA-1** · Dado que abro la ficha, cuando carga, entonces veo los datos de identificación y contacto, las citas pasadas y futuras, la lista de documentos que el paciente subió y los tratamientos registrados.
- **CA-2** · Dada la ficha, cuando la veo, entonces tengo los accesos para agendarle una cita, abrir un documento, registrar un tratamiento y preguntar al asistente.
- **CA-3** · Dado que el paciente no ha autorizado el uso de IA, cuando veo la ficha, entonces el acceso al asistente aparece deshabilitado con la explicación.
- **CA-4** · Dado que abro la ficha, cuando se carga, entonces el acceso queda en la bitácora.

## Tareas y actividades

### T-025.1 Servicio de ficha

- Reunir datos, citas y documentos del paciente
- Estado de la autorización de IA
- Registro del acceso en la bitácora

### T-025.2 Pantalla de ficha

- Secciones de datos, citas y documentos
- Accesos a las acciones
- Mensaje cuando el paciente no ha subido documentos

## Relación con otras historias

**Depende de:**

- [HU-023 Lista y búsqueda de pacientes](HU-023-lista-y-busqueda-de-pacientes.md)

**Habilita:**

- [HU-030 Consultar los documentos del paciente en un visor](../E5-historias-clinicas-del-paciente/HU-030-visor-de-documentos-del-paciente.md)
- [HU-034 Preguntar al asistente sobre los documentos de un paciente](../E6-asistente-de-ia/HU-034-preguntar-al-asistente.md)
- [HU-038 Registrar el tratamiento de un paciente](../E8-tratamientos/HU-038-registrar-el-tratamiento-de-un-paciente.md)
- [HU-040 Corregir los datos de un paciente](../E1-cuentas-e-ingreso/HU-040-corregir-los-datos-de-un-paciente.md)
- [HU-041 Datos de identificación de la historia clínica](../E9-historia-clinica-del-consultorio/HU-041-datos-de-identificacion-de-la-historia-clinica.md)
- [HU-042 Pantalla de atención con el asistente al lado](../E9-historia-clinica-del-consultorio/HU-042-pantalla-de-atencion-con-el-asistente-al-lado.md)

---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
