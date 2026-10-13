# HU-001 — Configuración inicial del consultorio

| Dato | Valor |
|---|---|
| Épica | E1 Cuentas e ingreso |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-06 |
| Origen | Nueva |

## Historia

> Como médico, quiero dejar configurados mi cuenta y mi consultorio la primera vez que entro, para empezar a recibir pacientes sin depender de nadie.

## Criterios de aceptación

- **CA-1** · Dado que el sistema se acaba de instalar, cuando abro el enlace de puesta en marcha, entonces creo mi cuenta de médico con correo y contraseña propia, y ese enlace deja de servir.
- **CA-2** · Dado que ya tengo cuenta, cuando registro el nombre del consultorio, la dirección, el teléfono, mi nombre y mi registro profesional, entonces esos datos quedan guardados y aparecen en lo que ve el paciente.
- **CA-3** · Dado que ya existe una cuenta de médico, cuando alguien intenta crear otra por el enlace de puesta en marcha, entonces el sistema lo rechaza.
- **CA-4** · Dado que no he definido horario ni tipos de cita, cuando entro al panel, entonces veo la lista de lo que falta por configurar y los pacientes todavía no pueden agendar.

## Tareas y actividades

### T-001.1 Puesta en marcha

- Enlace de un solo uso para crear la cuenta del médico
- Validación de la contraseña
- Bloqueo de una segunda cuenta de médico

### T-001.2 Datos del consultorio

- Modelo de datos del consultorio
- Formulario de edición
- Mostrar los datos en las pantallas del paciente

### T-001.3 Lista de pendientes de configuración

- Detectar si faltan el horario o los tipos de cita
- Mostrar el aviso en el panel
- Impedir que se agende mientras falten

## Relación con otras historias

**Depende de:**

- [HU-006 Roles y permisos de médico y paciente](HU-006-roles-y-permisos.md)

**Habilita:**

- [HU-004 Ingreso con contraseña](HU-004-ingreso-con-contrasena.md)
- [HU-008 Horario semanal de atención](../E2-calendario-de-disponibilidad/HU-008-horario-semanal-de-atencion.md)
- [HU-010 Tipos de cita y duración](../E2-calendario-de-disponibilidad/HU-010-tipos-de-cita-y-duracion.md)

---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
