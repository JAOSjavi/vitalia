# HU-051 — Reportar un síntoma o una duda

| Dato | Valor |
|---|---|
| Épica | E7 Comunicación paciente–médico entre consultas |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-41 |
| Jira | pendiente de cargar |

## Historia

> Como paciente en tratamiento, quiero contarle a mi médico algo que me pasó, para saber si debo preocuparme o esperar al control.

## Criterios de aceptación

- **CA-1** · Dado que abro «Mensajes», cuando escribo y envío un reporte, entonces queda asociado a mi médico tratante y a mi tratamiento vigente.
- **CA-2** · Dado que envío el reporte, cuando se registra, entonces veo el tiempo de respuesta esperado que la clínica configuró.
- **CA-3** · Dado que escribo el mensaje, cuando está en pantalla, entonces el aviso de que el canal no atiende urgencias permanece visible todo el tiempo.
- **CA-4** · Dado que ya tengo un reporte abierto sin responder, cuando envío otro, entonces el sistema lo agrupa en la misma conversación.

## Tareas y actividades

### T-051.1 Modelo de conversación clínica

- Tablas conversacion y mensaje
- Vínculo con paciente, profesional y tratamiento
- Estados: abierta, respondida, cerrada

### T-051.2 Pantalla de mensajes del paciente

- Hilo de conversación
- Composición y envío
- Aviso permanente de no urgencias

### T-051.3 Reglas de enrutamiento

- Determinar el médico tratante
- Agrupar reportes abiertos
- Configurar el tiempo de respuesta por clínica

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-027 Ver «Mi plan de tratamiento»](../E05-plan-de-tratamiento-post-consulta/HU-027-ver-mi-plan-de-tratamiento.md)

**Habilita** — no pueden construirse sin esta:

- [HU-052 Responder o derivar a una cita de control](HU-052-responder-o-derivar-a-una-cita-de-control.md)
- [HU-053 Aviso explícito de que el canal no es para urgencias](HU-053-aviso-explicito-de-que-el-canal-no-es-para-urgenci.md)


---

[← Volver a E7](README.md) · [Mapa de relaciones](../RELACIONES.md)
