# HU-038 — Agendar una cita por WhatsApp

| Dato | Valor |
|---|---|
| Épica | E3 Agendamiento y atención por WhatsApp |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 13 puntos |
| Requisitos | RF-13 |
| Jira | pendiente de cargar |

## Historia

> Como paciente que no usa aplicaciones, quiero agendar mi cita conversando por WhatsApp, para no tener que descargar nada ni recordar una contraseña.

## Criterios de aceptación

- **CA-1** · Dado que escribo al número de la clínica pidiendo una cita, cuando el asistente responde, entonces me guía en el orden: tipo de cita → profesional → horario disponible → confirmación.
- **CA-2** · Dado que llego al paso de horarios, cuando el asistente me los ofrece, entonces solo aparecen espacios realmente disponibles, validados contra la agenda en ese momento.
- **CA-3** · Dado que confirmo un horario, cuando el sistema lo procesa, entonces crea la cita, me envía el resumen con fecha, hora, profesional y sede, y programa los recordatorios.
- **CA-4** · Dado que escribo algo que el asistente no entiende, cuando ocurre dos veces seguidas, entonces ofrece el contacto humano de la clínica sin dejar la conversación sin salida.
- **CA-5** · Dado que abandono la conversación a mitad del flujo, cuando vuelvo a escribir dentro de las 24 horas, entonces el asistente retoma desde el punto donde quedé.

## Tareas y actividades

### T-038.1 Máquina de estados de la conversación

- Definir estados y transiciones del flujo
- Persistir el estado por número de teléfono
- Caducar conversaciones inactivas

### T-038.2 Webhook de mensajes entrantes

- Endpoint receptor con validación de firma
- Enrutar el mensaje al estado correspondiente
- Responder dentro del tiempo exigido por Meta

### T-038.3 Interpretación de respuestas

- Reconocer selección por número y por texto
- Normalizar variantes comunes
- Manejar respuestas no reconocidas

### T-038.4 Reutilizar el motor de disponibilidad

- Consumir el servicio de disponibilidad de HU-008
- Presentar como lista de botones o numerada
- Confirmar de forma transaccional

### T-038.5 Pruebas

- Guion de conversación completo
- Prueba de horario tomado durante la conversación
- Prueba de reanudación y de abandono

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-008 Verificación de disponibilidad en tiempo real](../E02-gestion-de-citas/HU-008-verificacion-de-disponibilidad-en-tiempo-real.md)
- [HU-033 Envío por WhatsApp con plantillas aprobadas](../E06-recordatorios-multicanal-y-adherencia/HU-033-envio-por-whatsapp-con-plantillas-aprobadas.md)
- [HU-043 Cumplimiento de plantillas y ventana de 24 horas](HU-043-cumplimiento-de-plantillas-y-ventana-de-24-horas.md)

**Habilita** — no pueden construirse sin esta:

- [HU-039 Registrar paciente nuevo desde WhatsApp](HU-039-registrar-paciente-nuevo-desde-whatsapp.md)


---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
