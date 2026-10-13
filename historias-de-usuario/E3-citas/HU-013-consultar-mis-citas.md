# HU-013 — Consultar mis citas

| Dato | Valor |
|---|---|
| Épica | E3 Citas |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-13 |
| Origen | HU-011 de la versión anterior, ajustada |

## Historia

> Como paciente, quiero ver mis citas próximas y pasadas, para saber cuándo debo ir y qué ya ocurrió.

## Criterios de aceptación

- **CA-1** · Dado que tengo citas, cuando abro "Mis citas", entonces veo primero las próximas en orden de fecha y luego las pasadas.
- **CA-2** · Dada cada cita, cuando la veo en la lista, entonces muestra fecha, hora, tipo y estado (confirmada, cancelada, atendida o no asistió).
- **CA-3** · Dado que no tengo citas, cuando abro la sección, entonces veo un mensaje y el acceso para agendar.
- **CA-4** · Dado que soy paciente, cuando consulto, entonces solo veo mis propias citas.

## Tareas y actividades

### T-013.1 Consulta de citas

- Servicio de citas del paciente
- Orden y paginación
- Filtro por estado

### T-013.2 Pantalla "Mis citas"

- Lista de próximas y pasadas
- Mensaje cuando no hay citas
- Acceso al detalle de cada cita

## Relación con otras historias

**Depende de:**

- [HU-012 Agendar una cita como paciente](HU-012-agendar-una-cita-como-paciente.md)

**Habilita:**

- [HU-020 Inicio del paciente](HU-020-inicio-del-paciente.md)

---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
