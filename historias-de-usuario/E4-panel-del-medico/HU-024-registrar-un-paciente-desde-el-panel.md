# HU-024 — Registrar un paciente desde el panel

| Dato | Valor |
|---|---|
| Épica | E4 Panel del médico |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-23 |
| Origen | Nueva |

## Historia

> Como médico, quiero registrar a un paciente que no usa la aplicación, para poder agendarlo y llevar su información.

## Criterios de aceptación

- **CA-1** · Dado que ingreso nombres, apellidos, tipo y número de documento, fecha de nacimiento, teléfono y, si lo tiene, correo, cuando guardo, entonces el paciente queda creado y puedo agendarle una cita.
- **CA-2** · Dado que el paciente tiene correo, cuando lo registro, entonces recibe un enlace para activar su cuenta y definir su contraseña.
- **CA-3** · Dado que el paciente activa su cuenta, cuando ingresa por primera vez, entonces debe aceptar la autorización de tratamiento de datos antes de continuar.
- **CA-4** · Dado que el documento ya existe, cuando intento registrarlo, entonces el sistema me muestra el paciente existente.

## Tareas y actividades

### T-024.1 Registro por el médico

- Crear el paciente sin contraseña
- Detección de pacientes repetidos
- Envío del enlace de activación

### T-024.2 Formulario en el panel

- Campos y validaciones
- Aviso de paciente existente
- Paso siguiente a agendar la cita

## Relación con otras historias

**Depende de:**

- [HU-003 Autorización de tratamiento de datos](../E1-cuentas-e-ingreso/HU-003-autorizacion-de-tratamiento-de-datos.md)
- [HU-023 Lista y búsqueda de pacientes](HU-023-lista-y-busqueda-de-pacientes.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
