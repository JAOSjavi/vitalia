# HU-059 — Consentimiento del paciente para el uso de IA

| Dato | Valor |
|---|---|
| Épica | E8 Asistente de IA y contenido educativo |
| Fase | 3 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-46 |
| Jira | pendiente de cargar |

## Historia

> Como paciente, quiero decidir si autorizo que se use inteligencia artificial sobre mi historia clínica, para mantener el control sobre mis datos sensibles.

## Criterios de aceptación

- **CA-1** · Dado que la clínica tiene habilitado el asistente, cuando se me solicita la autorización, entonces el texto explica en lenguaje claro qué información se procesa y con qué finalidad.
- **CA-2** · Dado que no otorgo la autorización, cuando el médico intenta usar el asistente sobre mi historia, entonces el sistema lo bloquea e informa que falta el consentimiento.
- **CA-3** · Dado que otorgué la autorización, cuando decido revocarla desde mi perfil, entonces surte efecto de inmediato y queda registrada la revocación.
- **CA-4** · Dado que otorgo o revoco, cuando se registra, entonces queda constancia con fecha, hora y versión del texto de consentimiento.

## Tareas y actividades

Sin desglosar. Esta historia pertenece a una fase posterior y se refina antes de entrar a un sprint.

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-037 Aceptación de la política de tratamiento de datos](../E11-seguridad-privacidad-y-cumplimiento/HU-037-aceptacion-de-la-politica-de-tratamiento-de-datos.md)

**Habilita** — no pueden construirse sin esta:

- [HU-061 Intermediación de la IA a través de backend propio](HU-061-intermediacion-de-la-ia-a-traves-de-backend-propio.md)
- [HU-060 Asistente clínico sobre la historia del paciente](HU-060-asistente-clinico-sobre-la-historia-del-paciente.md)


---

[← Volver a E8](README.md) · [Mapa de relaciones](../RELACIONES.md)
