# HU-061 — Intermediación de la IA a través de backend propio

| Dato | Valor |
|---|---|
| Épica | E8 Asistente de IA y contenido educativo |
| Fase | 3 |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-45 |
| Jira | pendiente de cargar |

## Historia

> Como responsable de seguridad, quiero que la historia clínica nunca salga del cliente hacia un tercero, para no exponer datos sensibles ni credenciales.

## Criterios de aceptación

- **CA-1** · Dado el código del cliente, cuando se revisa, entonces no contiene ninguna credencial del proveedor de IA ni llamadas directas a su API.
- **CA-2** · Dado que el médico hace una consulta al asistente, cuando se procesa, entonces pasa por el backend, que decide qué fragmentos se envían y registra el acceso.
- **CA-3** · Dado que se envía información al proveedor, cuando se compone la solicitud, entonces se excluyen los identificadores directos del paciente que no sean necesarios para responder.
- **CA-4** · Dado que se realiza cualquier consulta al asistente, cuando ocurre, entonces queda registrada en la bitácora de auditoría con médico, paciente, fecha y hora.

## Tareas y actividades

Sin desglosar. Esta historia pertenece a una fase posterior y se refina antes de entrar a un sprint.

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-059 Consentimiento del paciente para el uso de IA](HU-059-consentimiento-del-paciente-para-el-uso-de-ia.md)

**Habilita** — no pueden construirse sin esta:

- [HU-060 Asistente clínico sobre la historia del paciente](HU-060-asistente-clinico-sobre-la-historia-del-paciente.md)


---

[← Volver a E8](README.md) · [Mapa de relaciones](../RELACIONES.md)
