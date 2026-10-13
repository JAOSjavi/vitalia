# HU-008 — Horario semanal de atención

| Dato | Valor |
|---|---|
| Épica | E2 Calendario de disponibilidad |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-08 |
| Origen | HU-056 de la versión anterior, ajustada |

## Historia

> Como médico, quiero definir en qué días y horas atiendo, para que solo se ofrezcan espacios reales.

## Criterios de aceptación

- **CA-1** · Dado que defino una o varias franjas por día de la semana, cuando guardo, entonces el calendario ofrece espacios solo dentro de esas franjas.
- **CA-2** · Dado que una franja termina antes de empezar o se cruza con otra del mismo día, cuando intento guardar, entonces el sistema lo impide y señala cuál.
- **CA-3** · Dado que cambio el horario y hay citas futuras por fuera del nuevo horario, cuando guardo, entonces el sistema me las lista y las conserva hasta que yo las mueva o las cancele.
- **CA-4** · Dado un día sin franjas, cuando un paciente busca espacio ese día, entonces no se le ofrece ninguno.

## Tareas y actividades

### T-008.1 Modelo de horario

- Tabla de franjas por día de la semana
- Validación de cruces entre franjas
- Fecha a partir de la cual rige un cambio

### T-008.2 Pantalla de horario

- Editor semanal de franjas
- Aviso de las citas afectadas por el cambio
- Guardado con confirmación

## Relación con otras historias

**Depende de:**

- [HU-001 Configuración inicial del consultorio](../E1-cuentas-e-ingreso/HU-001-configuracion-inicial-del-consultorio.md)

**Habilita:**

- [HU-009 Bloqueos y ausencias](HU-009-bloqueos-y-ausencias.md)
- [HU-011 Cálculo de espacios libres sin choques](HU-011-calculo-de-espacios-libres.md)

---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
