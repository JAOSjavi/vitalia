# HU-007 — Agendar una cita desde la aplicación

| Dato | Valor |
|---|---|
| Épica | E2 Gestión de citas |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-07 |
| Jira | SCRUM-23 |

## Historia

> Como paciente, quiero agendar mi cita eligiendo tipo, profesional y horario, para no tener que llamar al consultorio.

## Criterios de aceptación

- **CA-1** · Dado que selecciono tipo de cita, profesional, sede y un horario disponible, cuando confirmo, entonces el sistema crea la cita en estado confirmada y muestra el resumen con fecha, hora, profesional y sede.
- **CA-2** · Dado que el sistema creó la cita, cuando termina el proceso, entonces programa los recordatorios de 24 horas y 1 hora antes.
- **CA-3** · Dado que no completo un paso obligatorio, cuando intento avanzar, entonces el sistema impide continuar e indica qué falta.
- **CA-4** · Dado que la cita quedó creada, cuando consulto «Mis citas», entonces aparece en la lista de próximas citas con su estado.

## Tareas y actividades

### T-007.1 Modelo de cita y tipos de cita

- Tablas cita, tipo_cita con duración asociada
- Estados: solicitada, confirmada, atendida, cancelada, no asistió
- Migración y datos de referencia

### T-007.2 Endpoints de agendamiento

- GET /disponibilidad por profesional y fecha
- POST /citas con validación transaccional
- Respuesta con el detalle de la cita creada

### T-007.3 Asistente de agendamiento en la app

- Paso 1: tipo de cita
- Paso 2: profesional, fecha y horario
- Paso 3: confirmación y resumen

### T-007.4 Encadenar la programación de recordatorios

- Publicar el evento cita_creada
- Programar los avisos de 24 h y 1 h
- Registrar la programación

### T-007.5 Pruebas

- Prueba del flujo completo
- Prueba de campos obligatorios
- Prueba de que se programan los recordatorios

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-002 Ingreso con contraseña](../E01-autenticacion-cuentas-y-roles/HU-002-ingreso-con-contrasena.md)
- [HU-008 Verificación de disponibilidad en tiempo real](HU-008-verificacion-de-disponibilidad-en-tiempo-real.md)

**Habilita** — no pueden construirse sin esta:

- [HU-009 Reagendar una cita](HU-009-reagendar-una-cita.md)
- [HU-010 Cancelar una cita](HU-010-cancelar-una-cita.md)
- [HU-011 Consultar mis citas pasadas y futuras](HU-011-consultar-mis-citas-pasadas-y-futuras.md)
- [HU-012 Adjuntar un documento al agendar](HU-012-adjuntar-un-documento-al-agendar.md)
- [HU-030 Recordatorio de cita 24 horas y 1 hora antes](../E06-recordatorios-multicanal-y-adherencia/HU-030-recordatorio-de-cita-24-horas-y-1-hora-antes.md)


---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
