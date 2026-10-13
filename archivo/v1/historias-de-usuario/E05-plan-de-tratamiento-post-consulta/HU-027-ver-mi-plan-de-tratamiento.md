# HU-027 — Ver «Mi plan de tratamiento»

| Dato | Valor |
|---|---|
| Épica | E5 Plan de tratamiento post-consulta |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-30 |
| Jira | SCRUM-90 |

## Historia

> Como paciente, quiero ver mi tratamiento en una pantalla clara, para entender qué debo tomar y qué cuidados seguir sin descifrar un PDF.

## Criterios de aceptación

- **CA-1** · Dado que tengo un plan activo, cuando abro «Mi plan», entonces veo tres secciones: medicamentos, cuidados y próximos pasos, con la fecha hasta la que está vigente.
- **CA-2** · Dado que veo un medicamento, cuando leo su tarjeta, entonces muestra nombre, presentación, dosis, frecuencia y los horarios concretos de toma.
- **CA-3** · Dado que no tengo un plan activo, cuando abro la pantalla, entonces veo un mensaje explicativo y el acceso a mis planes anteriores.
- **CA-4** · Dado que la información se muestra, cuando la leo, entonces está redactada en lenguaje claro y con tamaño de texto legible según el modo accesible.

## Tareas y actividades

### T-027.1 Endpoint del plan vigente

- Componer medicamentos, cuidados y pasos
- Filtrar por identidad autenticada
- Incluir vigencia y estado

### T-027.2 Pantalla «Mi plan»

- Secciones con jerarquía visual clara
- Tarjetas de medicamento con horarios
- Estado vacío con acceso al historial

### T-027.3 Pruebas de comprensión

- Revisión de lenguaje con usuario final
- Verificación de legibilidad y contraste

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-021 Registrar medicamentos del plan](HU-021-registrar-medicamentos-del-plan.md)
- [HU-024 Registrar cuidados e instrucciones](HU-024-registrar-cuidados-e-instrucciones.md)
- [HU-025 Registrar próximos pasos](HU-025-registrar-proximos-pasos.md)

**Habilita** — no pueden construirse sin esta:

- [HU-028 Historial de planes anteriores](HU-028-historial-de-planes-anteriores.md)
- [HU-051 Reportar un síntoma o una duda](../E07-comunicacion-paciente-medico-entre-consultas/HU-051-reportar-un-sintoma-o-una-duda.md)
- [HU-064 Lectura en voz alta](../E10-accesibilidad-y-experiencia/HU-064-lectura-en-voz-alta.md)
- [HU-065 Exportar el plan de tratamiento en PDF](../E10-accesibilidad-y-experiencia/HU-065-exportar-el-plan-de-tratamiento-en-pdf.md)
- [HU-068 Vista del cuidador](../E11-seguridad-privacidad-y-cumplimiento/HU-068-vista-del-cuidador.md)


---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
