# HU-029 — Ver y eliminar mis documentos

| Dato | Valor |
|---|---|
| Épica | E5 Historias clínicas del paciente |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-27 |
| Origen | HU-019 de la versión anterior, ajustada |

## Historia

> Como paciente, quiero ver lo que he subido y poder eliminarlo, para mantener el control de mi información.

## Criterios de aceptación

- **CA-1** · Dado que tengo documentos, cuando abro "Mis documentos", entonces los veo con nombre, fecha del documento y fecha de carga.
- **CA-2** · Dado un documento, cuando lo abro, entonces se muestra por medio de un enlace temporal.
- **CA-3** · Dado un documento, cuando lo elimino y confirmo, entonces deja de estar disponible para el médico y para el asistente.
- **CA-4** · Dado que soy paciente, cuando consulto, entonces solo veo mis propios documentos.

## Tareas y actividades

### T-029.1 Servicio de documentos del paciente

- Listar los documentos
- Abrir con enlace temporal
- Eliminar el archivo junto con su texto leído

### T-029.2 Pantalla "Mis documentos"

- Lista y mensaje cuando no hay documentos
- Confirmación antes de eliminar

## Relación con otras historias

**Depende de:**

- [HU-028 Subir mis historias clínicas](HU-028-subir-mis-historias-clinicas.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
