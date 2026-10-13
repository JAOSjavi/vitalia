# HU-018 — Visor de PDF integrado

| Dato | Valor |
|---|---|
| Épica | E4 Historia clínica y documentos |
| Fase | 1 |
| Rol | Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-22 |
| Jira | SCRUM-81 |

## Historia

> Como médico, quiero abrir los documentos dentro del sistema, para revisarlos sin descargar archivos clínicos al computador.

## Criterios de aceptación

- **CA-1** · Dado que selecciono un documento PDF, cuando se abre, entonces se muestra en el visor integrado con navegación de páginas y acercamiento.
- **CA-2** · Dado que abro el visor, cuando se carga el archivo, entonces se usa una URL firmada con vigencia máxima de 15 minutos.
- **CA-3** · Dado que expiró el enlace, cuando intento seguir navegando el documento, entonces el sistema solicita recargarlo y emite una nueva firma.
- **CA-4** · Dado que el documento es una imagen, cuando lo abro, entonces se muestra en el mismo visor con acercamiento.

## Tareas y actividades

### T-018.1 Componente visor

- Integrar biblioteca de render de PDF
- Controles de página y acercamiento
- Soporte de imágenes

### T-018.2 Manejo de URLs firmadas

- Solicitar firma al abrir
- Renovar al expirar
- Evitar almacenamiento en caché local del archivo

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-016 Cargar documentos clínicos del paciente](HU-016-cargar-documentos-clinicos-del-paciente.md)
- [HU-036 Documentos servidos con URL firmada](../E11-seguridad-privacidad-y-cumplimiento/HU-036-documentos-servidos-con-url-firmada.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
