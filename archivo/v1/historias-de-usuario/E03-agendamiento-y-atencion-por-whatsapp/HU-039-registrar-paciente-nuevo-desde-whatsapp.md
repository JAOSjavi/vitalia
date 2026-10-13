# HU-039 — Registrar paciente nuevo desde WhatsApp

| Dato | Valor |
|---|---|
| Épica | E3 Agendamiento y atención por WhatsApp |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-14 |
| Jira | pendiente de cargar |

## Historia

> Como paciente que nunca ha ido a la clínica, quiero quedar registrado durante la misma conversación, para agendar sin un trámite previo.

## Criterios de aceptación

- **CA-1** · Dado que escribo desde un número no registrado, cuando pido una cita, entonces el asistente solicita los datos mínimos: nombre completo, tipo y número de documento, y fecha de nacimiento.
- **CA-2** · Dado que entrego los datos, cuando se validan, entonces el sistema crea el paciente asociado a ese número y continúa con el agendamiento.
- **CA-3** · Dado que el documento ya existe con otro número de celular, cuando se detecta, entonces el asistente no revela datos del titular y deriva el caso a la clínica para verificación.
- **CA-4** · Dado que se crea el registro, cuando se completa, entonces el asistente informa el tratamiento de datos y registra la autorización obtenida por este canal.

## Tareas y actividades

### T-039.1 Flujo de captura de datos

- Solicitar y validar campo por campo
- Reintentar ante formato inválido
- Confirmar los datos antes de crear

### T-039.2 Creación de paciente desde el canal

- Crear el registro con origen «WhatsApp»
- Vincular el número verificado
- Marcar la cuenta como sin contraseña definida

### T-039.3 Consentimiento por el canal

- Texto resumido y enlace a la política
- Registrar aceptación con fecha y canal
- Rechazar el registro si no acepta

### T-039.4 Manejo de duplicados

- Detectar documento existente
- Respuesta que no revela información
- Notificación a la clínica para verificación

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-038 Agendar una cita por WhatsApp](HU-038-agendar-una-cita-por-whatsapp.md)
- [HU-037 Aceptación de la política de tratamiento de datos](../E11-seguridad-privacidad-y-cumplimiento/HU-037-aceptacion-de-la-politica-de-tratamiento-de-datos.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
