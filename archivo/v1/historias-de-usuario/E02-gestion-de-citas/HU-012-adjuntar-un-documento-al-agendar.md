# HU-012 — Adjuntar un documento al agendar

| Dato | Valor |
|---|---|
| Épica | E2 Gestión de citas |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Should (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-11 |
| Jira | SCRUM-28 |

## Historia

> Como paciente, quiero adjuntar mi orden médica o un examen al agendar, para que el profesional la tenga antes de la consulta.

## Criterios de aceptación

- **CA-1** · Dado que selecciono un archivo PDF o imagen de hasta 10 MB, cuando confirmo, entonces el sistema lo carga, lo clasifica por tipo y lo vincula a la cita.
- **CA-2** · Dado que el archivo excede el tamaño o tiene una extensión no permitida, cuando intento cargarlo, entonces el sistema lo rechaza e indica los formatos y el tamaño admitidos.
- **CA-3** · Dado que el documento quedó cargado, cuando el profesional abre la cita, entonces puede visualizarlo mediante una URL firmada de vigencia limitada.
- **CA-4** · Dado que el documento está almacenado, cuando se intenta acceder a su ruta sin firma válida, entonces el almacenamiento niega el acceso.

## Tareas y actividades

### T-012.1 Servicio de carga de archivos

- Validar tipo y tamaño en el servidor
- Guardar en almacenamiento privado cifrado
- Registrar metadatos y vínculo con la cita

### T-012.2 Generación de URLs firmadas

- Emitir enlaces con vigencia corta
- Registrar cada emisión en auditoría
- Rechazar accesos sin firma

### T-012.3 Interfaz de carga

- Selector de archivo con vista previa
- Barra de progreso y manejo de errores
- Listado de adjuntos de la cita

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-007 Agendar una cita desde la aplicación](HU-007-agendar-una-cita-desde-la-aplicacion.md)
- [HU-036 Documentos servidos con URL firmada](../E11-seguridad-privacidad-y-cumplimiento/HU-036-documentos-servidos-con-url-firmada.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
