# HU-026 — Botón de cobro sin función

| Dato | Valor |
|---|---|
| Épica | E4 Panel del médico |
| Rol | Médico |
| Prioridad | Could (MoSCoW) |
| Estimación | 1 punto |
| Requisitos | RF-25 |
| Origen | Nueva |

## Historia

> Como médico, quiero ver en mi panel dónde quedará el cobro de la consulta, para saber que esa función viene después.

## Criterios de aceptación

- **CA-1** · Dado que estoy en el panel, cuando reviso el menú, entonces veo un botón "Cobro".
- **CA-2** · Dado que selecciono el botón, cuando se abre, entonces veo un aviso de que la función aún no está disponible, y no se guarda ni se envía nada.
- **CA-3** · Dado un usuario con rol paciente, cuando usa la aplicación, entonces no ve ese botón.

## Tareas y actividades

### T-026.1 Botón en el panel

- Entrada "Cobro" en el menú del médico
- Pantalla con el aviso de función no disponible

## Nota de alcance

**Reemplazada el 10 de noviembre de 2026 por D-35.** El botón Cobro ya no es un aviso: lista las citas atendidas de los últimos 30 días y emite la factura electrónica con Factus en su ambiente de pruebas. Ver [decisiones y supuestos](../../planificacion/04-decisiones-y-supuestos.md). Los criterios CA-1 y CA-3 se mantienen; CA-2 cambia: al cobrar se emite la factura y se guarda su número y su CUFE.

## Relación con otras historias

**Depende de:**

- [HU-021 Panel de inicio con la agenda del día](HU-021-agenda-del-dia.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
