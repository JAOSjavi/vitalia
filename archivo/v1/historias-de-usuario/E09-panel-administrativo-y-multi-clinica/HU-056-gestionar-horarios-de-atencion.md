# HU-056 — Gestionar horarios de atención

| Dato | Valor |
|---|---|
| Épica | E9 Panel administrativo y multi-clínica |
| Fase | 3 |
| Rol | Administrador |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-49 |
| Jira | pendiente de cargar |

## Historia

> Como administrador, quiero definir los horarios y las ausencias de cada profesional, para que el sistema solo ofrezca espacios reales.

## Criterios de aceptación

- **CA-1** · Dado que defino el horario semanal de un profesional por sede, cuando guardo, entonces el motor de disponibilidad genera los espacios según ese horario.
- **CA-2** · Dado que registro una ausencia (vacaciones, incapacidad), cuando guardo, entonces esos días dejan de ofrecerse para agendar.
- **CA-3** · Dado que la ausencia se cruza con citas ya agendadas, cuando la registro, entonces el sistema las lista y exige reagendarlas o cancelarlas antes de confirmar.
- **CA-4** · Dado que un profesional atiende en dos sedes el mismo día, cuando se calculan los espacios, entonces el sistema impide traslapes entre sedes.

## Tareas y actividades

Sin desglosar. Esta historia pertenece a una fase posterior y se refina antes de entrar a un sprint.

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-055 Gestionar profesionales](HU-055-gestionar-profesionales.md)
- [HU-008 Verificación de disponibilidad en tiempo real](../E02-gestion-de-citas/HU-008-verificacion-de-disponibilidad-en-tiempo-real.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
