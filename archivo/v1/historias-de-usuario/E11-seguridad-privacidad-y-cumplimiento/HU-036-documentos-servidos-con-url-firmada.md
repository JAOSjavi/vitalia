# HU-036 — Documentos servidos con URL firmada

| Dato | Valor |
|---|---|
| Épica | E11 Seguridad, privacidad y cumplimiento |
| Fase | 1 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-21 |
| Jira | SCRUM-99 |

## Historia

> Como responsable de cumplimiento, quiero que ningún documento clínico sea accesible por una URL pública, para evitar la exposición de información sensible.

## Criterios de aceptación

- **CA-1** · Dado un documento almacenado, cuando se intenta acceder a su ruta sin firma válida, entonces el almacenamiento responde con acceso denegado.
- **CA-2** · Dado que un usuario autorizado solicita abrir un documento, cuando el backend valida sus permisos, entonces emite una URL firmada con vigencia máxima de 15 minutos.
- **CA-3** · Dado que una URL firmada expiró, cuando se usa nuevamente, entonces el acceso es rechazado.
- **CA-4** · Dado que se emite una URL firmada, cuando ocurre la emisión, entonces queda registrada en la bitácora de auditoría con el solicitante y el documento.

## Tareas y actividades

### T-036.1 Configuración del almacenamiento privado

- Deshabilitar el acceso público del bucket
- Habilitar cifrado en reposo
- Definir políticas de acceso del servicio

### T-036.2 Servicio de firma

- Endpoint que valida permisos y firma
- Vigencia corta configurable
- Registro en auditoría

### T-036.3 Pruebas de exposición

- Intento de acceso directo sin firma
- Prueba de expiración
- Revisión de configuración del bucket

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- Ninguna. Es punto de partida.

**Habilita** — no pueden construirse sin esta:

- [HU-012 Adjuntar un documento al agendar](../E02-gestion-de-citas/HU-012-adjuntar-un-documento-al-agendar.md)
- [HU-016 Cargar documentos clínicos del paciente](../E04-historia-clinica-y-documentos/HU-016-cargar-documentos-clinicos-del-paciente.md)
- [HU-018 Visor de PDF integrado](../E04-historia-clinica-y-documentos/HU-018-visor-de-pdf-integrado.md)
- [HU-019 Ver mis documentos como paciente](../E04-historia-clinica-y-documentos/HU-019-ver-mis-documentos-como-paciente.md)


---

[← Volver a E11](README.md) · [Mapa de relaciones](../RELACIONES.md)
