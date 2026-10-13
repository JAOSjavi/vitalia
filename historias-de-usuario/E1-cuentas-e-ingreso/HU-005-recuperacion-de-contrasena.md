# HU-005 — Recuperación de contraseña

| Dato | Valor |
|---|---|
| Épica | E1 Cuentas e ingreso |
| Rol | Paciente, Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-04 |
| Origen | HU-004 de la versión anterior, ajustada |

## Historia

> Como usuario que olvidó su contraseña, quiero restablecerla desde mi correo, para volver a entrar sin ayuda.

## Criterios de aceptación

- **CA-1** · Dado que escribo mi número de documento, cuando pido recuperar la contraseña, entonces llega al correo que tengo registrado un enlace que sirve una sola vez y vence en 30 minutos. *(Ajustado el 13 de octubre.)*
- **CA-2** · Dado que el documento no está registrado, cuando pido recuperar, entonces veo el mismo mensaje que si existiera, y en ningún caso la pantalla muestra el correo.
- **CA-3** · Dado que abro un enlace vencido o ya usado, cuando intento cambiar la contraseña, entonces el sistema lo rechaza y me ofrece pedir uno nuevo.
- **CA-4** · Dado que cambio la contraseña, cuando termino, entonces todas mis sesiones abiertas se cierran.

## Tareas y actividades

### T-005.1 Enlaces de recuperación

- Generación del enlace de un solo uso
- Vencimiento a los 30 minutos
- Cierre de las sesiones abiertas al cambiar la contraseña

### T-005.2 Envío de correo

- Servicio de correo llamado desde el servidor
- Plantilla del mensaje
- Prueba de entrega

### T-005.3 Pantallas

- Solicitud de recuperación
- Definición de la nueva contraseña
- Mensaje de enlace vencido

## Relación con otras historias

**Depende de:**

- [HU-004 Ingreso con contraseña](HU-004-ingreso-con-contrasena.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
