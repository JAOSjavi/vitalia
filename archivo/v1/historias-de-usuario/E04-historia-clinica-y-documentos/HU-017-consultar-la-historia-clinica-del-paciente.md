# HU-017 — Consultar la historia clínica del paciente

| Dato | Valor |
|---|---|
| Épica | E4 Historia clínica y documentos |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-19, RF-20 |
| Jira | SCRUM-80 |

## Historia

> Como médico, quiero consultar la historia del paciente antes y durante la consulta, para decidir con la información completa.

## Criterios de aceptación

- **CA-1** · Dado que abro el expediente de un paciente que atiendo, cuando carga, entonces veo el resumen con diagnósticos activos, alergias, antecedentes y la fecha de la última consulta.
- **CA-2** · Dado que consulto el expediente, cuando se muestra, entonces aparece la línea de tiempo de consultas con su nota clínica y sus documentos.
- **CA-3** · Dado que el paciente no está bajo mi atención en ninguna sede, cuando intento abrir su expediente, entonces el sistema niega el acceso y registra el intento.
- **CA-4** · Dado que abro cualquier historia clínica, cuando se despliega la información, entonces el sistema registra en auditoría mi identidad, el paciente consultado y la fecha y hora.

## Tareas y actividades

### T-017.1 Endpoint de expediente

- Componer resumen clínico del paciente
- Aplicar la regla de relación médico-paciente
- Registrar el acceso en auditoría

### T-017.2 Vista de expediente

- Tarjeta de resumen clínico
- Línea de tiempo de consultas
- Acceso a documentos por consulta

### T-017.3 Pruebas de acceso

- Prueba de acceso permitido y denegado
- Verificación del registro de auditoría

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-015 Registrar la nota clínica de la consulta](HU-015-registrar-la-nota-clinica-de-la-consulta.md)
- [HU-005 Roles y permisos resueltos en base de datos](../E01-autenticacion-cuentas-y-roles/HU-005-roles-y-permisos-resueltos-en-base-de-datos.md)

**Habilita** — no pueden construirse sin esta:

- [HU-060 Asistente clínico sobre la historia del paciente](../E08-asistente-de-ia-y-contenido-educativo/HU-060-asistente-clinico-sobre-la-historia-del-paciente.md)


---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
