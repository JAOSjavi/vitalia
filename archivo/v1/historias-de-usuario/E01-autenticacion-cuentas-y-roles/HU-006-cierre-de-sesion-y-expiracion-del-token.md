# HU-006 — Cierre de sesión y expiración del token

| Dato | Valor |
|---|---|
| Épica | E1 Autenticación, cuentas y roles |
| Fase | 1 |
| Rol | Paciente, Médico, Administrador |
| Prioridad | Should (MoSCoW) |
| Estimación | 2 puntos |
| Requisitos | RF-05, RF-06 |
| Jira | SCRUM-22 |

## Historia

> Como usuario, quiero cerrar mi sesión y que expire sola, para que nadie use mi cuenta si dejo el teléfono desatendido.

## Criterios de aceptación

- **CA-1** · Dado que pulso «Cerrar sesión», cuando se confirma, entonces el sistema invalida el token en el servidor y borra las credenciales locales.
- **CA-2** · Dado que mi token de acceso expiró, cuando la app hace una petición, entonces la renueva con el token de refresco sin pedirme credenciales de nuevo.
- **CA-3** · Dado que el token de refresco también expiró, cuando abro la aplicación, entonces el sistema me lleva a la pantalla de ingreso sin mostrar datos previos en pantalla.

## Tareas y actividades

### T-006.1 Invalidación de tokens

- Lista de tokens revocados con vigencia
- Endpoint POST /auth/logout
- Limpieza programada de registros vencidos

### T-006.2 Renovación transparente

- Interceptor de peticiones en el cliente
- Reintento tras renovar
- Redirección a ingreso si falla

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-002 Ingreso con contraseña](HU-002-ingreso-con-contrasena.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
