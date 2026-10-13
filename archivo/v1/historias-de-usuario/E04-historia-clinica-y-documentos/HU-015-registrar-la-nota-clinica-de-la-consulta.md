# HU-015 — Registrar la nota clínica de la consulta

| Dato | Valor |
|---|---|
| Épica | E4 Historia clínica y documentos |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-23 |
| Jira | SCRUM-78 |

## Historia

> Como médico, quiero registrar motivo, hallazgos y diagnóstico durante la consulta, para dejar la historia clínica completa y válida en digital.

## Criterios de aceptación

- **CA-1** · Dado que atiendo una cita, cuando registro motivo, hallazgos y al menos un diagnóstico con código CIE-10 y guardo, entonces el sistema crea el documento de historia clínica vinculado a esa cita.
- **CA-2** · Dado que la nota fue guardada, cuando intento modificarla después del cierre, entonces el sistema conserva la versión original y registra la corrección como una adenda con autor y fecha.
- **CA-3** · Dado que busco un diagnóstico, cuando escribo parte del nombre, entonces el sistema sugiere códigos CIE-10 coincidentes y guarda el código junto con la descripción.
- **CA-4** · Dado que dejo campos obligatorios vacíos, cuando intento cerrar la consulta, entonces el sistema lo impide e indica qué falta.

## Tareas y actividades

### T-015.1 Modelo de nota clínica

- Tablas nota_clinica, diagnostico, adenda
- Vínculo con cita, paciente y profesional
- Política de inmutabilidad tras el cierre

### T-015.2 Catálogo CIE-10

- Cargar el catálogo de códigos
- Búsqueda por texto y por código
- Almacenar código y descripción en la nota

### T-015.3 Formulario de consulta

- Campos de motivo, hallazgos y diagnóstico
- Buscador de diagnósticos con sugerencias
- Guardado parcial y cierre de consulta

### T-015.4 Adendas

- Flujo de corrección posterior
- Visualización de versión original y adendas
- Registro en auditoría

### T-015.5 Pruebas

- Prueba de creación y vínculo con la cita
- Prueba de inmutabilidad
- Prueba de validación de obligatorios

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-013 Registrar asistencia o inasistencia](../E02-gestion-de-citas/HU-013-registrar-asistencia-o-inasistencia.md)

**Habilita** — no pueden construirse sin esta:

- [HU-017 Consultar la historia clínica del paciente](HU-017-consultar-la-historia-clinica-del-paciente.md)
- [HU-021 Registrar medicamentos del plan](../E05-plan-de-tratamiento-post-consulta/HU-021-registrar-medicamentos-del-plan.md)
- [HU-024 Registrar cuidados e instrucciones](../E05-plan-de-tratamiento-post-consulta/HU-024-registrar-cuidados-e-instrucciones.md)
- [HU-025 Registrar próximos pasos](../E05-plan-de-tratamiento-post-consulta/HU-025-registrar-proximos-pasos.md)
- [HU-062 Contenido educativo curado](../E08-asistente-de-ia-y-contenido-educativo/HU-062-contenido-educativo-curado.md)
- [HU-071 Generar el Resumen Digital de Atención (RDA)](../E12-interoperabilidad-rda/HU-071-generar-el-resumen-digital-de-atencion-rda.md)


---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
