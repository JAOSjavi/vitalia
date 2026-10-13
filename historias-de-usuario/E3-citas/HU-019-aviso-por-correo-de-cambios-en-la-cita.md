# HU-019 — Aviso por correo de cambios en la cita

| Dato | Valor |
|---|---|
| Épica | E3 Citas |
| Rol | Paciente |
| Prioridad | Should (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-18 |
| Origen | Nueva |

## Historia

> Como paciente, quiero recibir un correo cuando mi cita se crea, se mueve o se cancela, para enterarme aunque no abra la aplicación.

## Criterios de aceptación

- **CA-1** · Dado que se crea una cita a mi nombre, cuando se confirma, entonces recibo un correo con fecha, hora, tipo y dirección del consultorio.
- **CA-2** · Dado que el médico o yo movemos o cancelamos la cita, cuando se guarda, entonces recibo un correo con el cambio y, si lo hay, el motivo.
- **CA-3** · Dado que el correo no se puede entregar, cuando falla el envío, entonces la cita se mantiene y el fallo queda registrado para que el médico lo vea.
- **CA-4** · Dado el contenido del correo, cuando se revisa, entonces no incluye información clínica.

## Tareas y actividades

### T-019.1 Envío de avisos

- Evento de cita creada, movida o cancelada
- Plantillas de correo
- Reintento y registro de fallos

### T-019.2 Pruebas

- Los tres tipos de aviso
- Correo que rebota
- Revisión de que el contenido no trae datos clínicos

## Relación con otras historias

**Depende de:**

- [HU-012 Agendar una cita como paciente](HU-012-agendar-una-cita-como-paciente.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
