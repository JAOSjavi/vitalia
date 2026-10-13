# HU-017 — Mover o cancelar una cita como médico

| Dato | Valor |
|---|---|
| Épica | E3 Citas |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-16 |
| Origen | Nueva |

## Historia

> Como médico, quiero mover o cancelar cualquier cita de mi agenda, para reorganizarme cuando surge un imprevisto.

## Criterios de aceptación

- **CA-1** · Dada una cita futura, cuando la muevo a otro espacio, entonces queda en el nuevo horario sin la restricción de 24 horas que aplica al paciente.
- **CA-2** · Dada una cita futura, cuando la cancelo, entonces debo escribir un motivo y el espacio se libera.
- **CA-3** · Dado que muevo o cancelo una cita, cuando se guarda, entonces el paciente ve el cambio en "Mis citas" con el motivo.
- **CA-4** · Dada una cita ya atendida, cuando intento moverla o cancelarla, entonces el sistema no lo permite.

## Tareas y actividades

### T-017.1 Servicio de cambios del médico

- Mover sin regla de anticipación
- Cancelar con motivo obligatorio
- Impedir cambios en citas atendidas

### T-017.2 Acciones en la agenda

- Mover desde la agenda
- Cancelar con motivo
- Actualizar la vista después del cambio

## Relación con otras historias

**Depende de:**

- [HU-011 Cálculo de espacios libres sin choques](../E2-calendario-de-disponibilidad/HU-011-calculo-de-espacios-libres.md)
- [HU-021 Panel de inicio con la agenda del día](../E4-panel-del-medico/HU-021-agenda-del-dia.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
