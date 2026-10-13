# HU-030 — Consultar los documentos del paciente en un visor

| Dato | Valor |
|---|---|
| Épica | E5 Historias clínicas del paciente |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-28 |
| Origen | HU-018 de la versión anterior, ajustada |

## Historia

> Como médico, quiero abrir los documentos del paciente dentro del sistema, para leerlos sin descargarlos a mi equipo.

## Criterios de aceptación

- **CA-1** · Dado un documento PDF o una imagen, cuando lo abro desde la ficha, entonces se muestra en un visor dentro de la aplicación, con zoom y paso de página.
- **CA-2** · Dado el visor, cuando lo uso, entonces no ofrece la opción de descargar el archivo.
- **CA-3** · Dado que abro un documento, cuando se muestra, entonces el acceso queda en la bitácora con mi usuario, el paciente y la hora.
- **CA-4** · Dado que el enlace temporal vence mientras leo, cuando paso de página, entonces el visor lo renueva sin perder el lugar.

## Tareas y actividades

### T-030.1 Visor

- Visor de PDF y de imagen
- Zoom y paso de página
- Sin opción de descarga

### T-030.2 Integración

- Abrir con enlace temporal
- Renovación del enlace mientras se lee
- Registro del acceso en la bitácora

## Relación con otras historias

**Depende de:**

- [HU-025 Ficha del paciente](../E4-panel-del-medico/HU-025-ficha-del-paciente.md)
- [HU-028 Subir mis historias clínicas](HU-028-subir-mis-historias-clinicas.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
