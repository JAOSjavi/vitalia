# HU-001 — Registro de paciente

| Dato | Valor |
|---|---|
| Épica | E1 Autenticación, cuentas y roles |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-01, RF-58 |
| Jira | SCRUM-17 |

## Historia

> Como paciente nuevo, quiero crear mi cuenta con mi celular y una contraseña propia para acceder a la aplicación sin depender de la recepción de la clínica.

## Criterios de aceptación

- **CA-1** · Dado que ingreso nombre, documento, celular, correo y una contraseña válida, cuando confirmo el registro, entonces el sistema crea mi cuenta con rol paciente y me lleva a la pantalla de inicio autenticado.
- **CA-2** · Dado que escribo una contraseña de menos de 8 caracteres o sin al menos un número, cuando intento continuar, entonces el sistema bloquea el envío y explica en texto claro qué le falta a la contraseña.
- **CA-3** · Dado que el celular o el documento ya están registrados, cuando envío el formulario, entonces el sistema informa que la cuenta ya existe y ofrece ir a recuperar contraseña, sin revelar datos del titular.
- **CA-4** · Dado que no he marcado la aceptación de la política de tratamiento de datos, cuando intento registrarme, entonces el sistema impide continuar; al aceptarla, registra fecha, hora y versión del documento aceptado.

## Tareas y actividades

### T-001.1 Modelar la entidad usuario y paciente

- Definir tablas, llaves y restricciones de unicidad (documento, celular)
- Crear la migración inicial
- Sembrar catálogo de tipos de documento

### T-001.2 Construir el endpoint POST /auth/registro

- Validar el esquema de entrada en el servidor
- Hashear la contraseña con argon2
- Devolver token de sesión y perfil

### T-001.3 Construir la pantalla de registro

- Maquetar el formulario con validación en línea
- Mostrar mensajes de error específicos por campo
- Enlazar la política de datos y su casilla de aceptación

### T-001.4 Registrar el consentimiento de datos

- Versionar el texto de la política
- Guardar aceptación con fecha, hora y versión
- Exponer la constancia en el perfil del paciente

### T-001.5 Pruebas

- Pruebas unitarias de validación de contraseña
- Prueba de integración de duplicados
- Prueba de extremo a extremo del registro exitoso

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- Ninguna. Es punto de partida.

**Habilita** — no pueden construirse sin esta:

- [HU-002 Ingreso con contraseña](HU-002-ingreso-con-contrasena.md)
- [HU-003 Ingreso con código por SMS (OTP)](HU-003-ingreso-con-codigo-por-sms-otp.md)
- [HU-004 Recuperación de contraseña](HU-004-recuperacion-de-contrasena.md)
- [HU-037 Aceptación de la política de tratamiento de datos](../E11-seguridad-privacidad-y-cumplimiento/HU-037-aceptacion-de-la-politica-de-tratamiento-de-datos.md)
- [HU-032 Configurar canal preferido de aviso](../E06-recordatorios-multicanal-y-adherencia/HU-032-configurar-canal-preferido-de-aviso.md)


---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
