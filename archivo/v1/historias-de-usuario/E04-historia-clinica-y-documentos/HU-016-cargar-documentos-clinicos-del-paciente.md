# HU-016 — Cargar documentos clínicos del paciente

| Dato | Valor |
|---|---|
| Épica | E4 Historia clínica y documentos |
| Fase | 1 |
| Rol | Médico, Administrador |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-19 |
| Jira | SCRUM-79 |

## Historia

> Como profesional, quiero cargar exámenes, recetas e imágenes al expediente, para tener todo el historial del paciente en un solo lugar.

## Criterios de aceptación

- **CA-1** · Dado que cargo un archivo, cuando selecciono su tipo (historia clínica, examen, receta, imagen diagnóstica) y confirmo, entonces queda asociado al paciente con fecha, tipo y autor.
- **CA-2** · Dado que el documento corresponde a una consulta, cuando lo cargo desde esa cita, entonces queda vinculado también a la cita.
- **CA-3** · Dado que consulto el expediente, cuando filtro por tipo de documento, entonces la lista muestra solo los documentos de ese tipo, ordenados del más reciente al más antiguo.
- **CA-4** · Dado que el archivo se almacena, cuando se guarda, entonces queda cifrado y sin ruta pública accesible.

## Tareas y actividades

### T-016.1 Modelo de documentos

- Tabla documento con tipo, paciente, cita y autor
- Restricciones por tipo permitido
- Índices para consulta por paciente y tipo

### T-016.2 Carga desde el panel

- Selector con tipo obligatorio
- Validación de formato y tamaño
- Confirmación y listado actualizado

### T-016.3 Listado y filtros

- Filtro por tipo y por rango de fechas
- Orden cronológico inverso
- Paginación

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-036 Documentos servidos con URL firmada](../E11-seguridad-privacidad-y-cumplimiento/HU-036-documentos-servidos-con-url-firmada.md)

**Habilita** — no pueden construirse sin esta:

- [HU-018 Visor de PDF integrado](HU-018-visor-de-pdf-integrado.md)
- [HU-019 Ver mis documentos como paciente](HU-019-ver-mis-documentos-como-paciente.md)


---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
