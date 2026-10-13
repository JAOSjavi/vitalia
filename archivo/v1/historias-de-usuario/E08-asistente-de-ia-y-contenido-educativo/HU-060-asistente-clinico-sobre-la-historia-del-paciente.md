# HU-060 — Asistente clínico sobre la historia del paciente

| Dato | Valor |
|---|---|
| Épica | E8 Asistente de IA y contenido educativo |
| Fase | 3 |
| Rol | Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 13 puntos |
| Requisitos | RF-44 |
| Jira | pendiente de cargar |

## Historia

> Como médico, quiero preguntarle al asistente por los antecedentes del paciente, para no leer todo el expediente durante la consulta.

## Criterios de aceptación

- **CA-1** · Dado que el paciente autorizó el uso de IA, cuando pregunto por sus antecedentes, diagnósticos, alergias o evolución, entonces el asistente responde con base únicamente en la información registrada en su historia.
- **CA-2** · Dado que el asistente responde, cuando leo la respuesta, entonces indica de qué registros la obtuvo (fecha y tipo de documento).
- **CA-3** · Dado que la historia no contiene la información solicitada, cuando pregunto, entonces el asistente lo dice explícitamente en vez de inferir o completar.
- **CA-4** · Dado que uso el asistente, cuando se muestra la respuesta, entonces incluye la advertencia de que es una ayuda de lectura y no sustituye el criterio clínico.

## Tareas y actividades

Sin desglosar. Esta historia pertenece a una fase posterior y se refina antes de entrar a un sprint.

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-017 Consultar la historia clínica del paciente](../E04-historia-clinica-y-documentos/HU-017-consultar-la-historia-clinica-del-paciente.md)
- [HU-059 Consentimiento del paciente para el uso de IA](HU-059-consentimiento-del-paciente-para-el-uso-de-ia.md)
- [HU-061 Intermediación de la IA a través de backend propio](HU-061-intermediacion-de-la-ia-a-traves-de-backend-propio.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E8](README.md) · [Mapa de relaciones](../RELACIONES.md)
