# HU-021 — Panel de inicio con la agenda del día

| Dato | Valor |
|---|---|
| Épica | E4 Panel del médico |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-20 |
| Origen | HU-014 de la versión anterior, ajustada |

## Historia

> Como médico, quiero ver al entrar mis citas de hoy en orden, para saber a quién atiendo y en qué va el día.

## Criterios de aceptación

- **CA-1** · Dado que entro al panel, cuando carga, entonces veo las citas de hoy por hora, con paciente, tipo y estado.
- **CA-2** · Dada una cita de la lista, cuando la selecciono, entonces llego a la ficha de ese paciente.
- **CA-3** · Dado que no hay citas hoy, cuando entro, entonces veo el mensaje y cuál es la próxima cita agendada.
- **CA-4** · Dado que se crea, se mueve o se cancela una cita de hoy, cuando vuelvo al panel, entonces la lista ya refleja el cambio.

## Tareas y actividades

### T-021.1 Servicio de agenda del día

- Consulta de citas por fecha
- Datos mínimos del paciente en cada cita
- Actualización al volver al panel

### T-021.2 Pantalla del panel

- Lista por hora con el estado de cada cita
- Menú de navegación a calendario, pacientes y configuración
- Mensaje cuando no hay citas

## Relación con otras historias

**Depende de:**

- [HU-004 Ingreso con contraseña](../E1-cuentas-e-ingreso/HU-004-ingreso-con-contrasena.md)
- [HU-011 Cálculo de espacios libres sin choques](../E2-calendario-de-disponibilidad/HU-011-calculo-de-espacios-libres.md)

**Habilita:**

- [HU-017 Mover o cancelar una cita como médico](../E3-citas/HU-017-mover-o-cancelar-una-cita-como-medico.md)
- [HU-018 Registrar asistencia o inasistencia](../E3-citas/HU-018-registrar-asistencia.md)
- [HU-022 Vista de calendario semanal y mensual](HU-022-vista-de-calendario.md)
- [HU-026 Botón de cobro sin función](HU-026-boton-de-cobro-sin-funcion.md)

---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
