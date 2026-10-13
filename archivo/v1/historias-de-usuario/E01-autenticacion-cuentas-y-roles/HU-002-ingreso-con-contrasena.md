# HU-002 — Ingreso con contraseña

| Dato | Valor |
|---|---|
| Épica | E1 Autenticación, cuentas y roles |
| Fase | 1 |
| Rol | Paciente, Médico, Administrador |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-02, RF-05 |
| Jira | SCRUM-18 |

## Historia

> Como usuario registrado, quiero ingresar con mi celular y contraseña para entrar a mi cuenta de forma segura.

## Criterios de aceptación

- **CA-1** · Dado que ingreso credenciales correctas, cuando pulso «Ingresar», entonces el sistema me autentica, emite un token con expiración y me lleva a la pantalla de inicio de mi rol.
- **CA-2** · Dado que ingreso credenciales incorrectas, cuando pulso «Ingresar», entonces el sistema muestra un mensaje genérico («usuario o contraseña incorrectos») que no revela cuál de los dos falló.
- **CA-3** · Dado que fallo 5 intentos seguidos, cuando intento de nuevo, entonces el sistema bloquea temporalmente el acceso por 15 minutos e informa el tiempo restante.
- **CA-4** · Dado que el sistema autentica correctamente, cuando se emite el token, entonces no se almacena ningún dato personal en texto plano en el dispositivo.

## Tareas y actividades

### T-002.1 Endpoint POST /auth/login

- Verificar hash de contraseña
- Emitir JWT de acceso y token de renovación
- Registrar el intento en la bitácora

### T-002.2 Control de intentos fallidos

- Contar intentos por celular e IP
- Aplicar bloqueo temporal progresivo
- Limpiar el contador tras un ingreso exitoso

### T-002.3 Pantalla de ingreso

- Maquetar formulario y estado de carga
- Mostrar mensajes de error y de bloqueo
- Guardar el token en almacenamiento seguro del dispositivo

### T-002.4 Pruebas

- Prueba de credenciales válidas e inválidas
- Prueba del bloqueo por intentos
- Revisión de que el token no contenga datos sensibles

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-001 Registro de paciente](HU-001-registro-de-paciente.md)

**Habilita** — no pueden construirse sin esta:

- [HU-004 Recuperación de contraseña](HU-004-recuperacion-de-contrasena.md)
- [HU-006 Cierre de sesión y expiración del token](HU-006-cierre-de-sesion-y-expiracion-del-token.md)
- [HU-007 Agendar una cita desde la aplicación](../E02-gestion-de-citas/HU-007-agendar-una-cita-desde-la-aplicacion.md)


---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
