# HU-004 — Recuperación de contraseña

| Dato | Valor |
|---|---|
| Épica | E1 Autenticación, cuentas y roles |
| Fase | 1 |
| Rol | Paciente, Médico, Administrador |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-03 |
| Jira | SCRUM-20 |

## Historia

> Como usuario que olvidó su contraseña, quiero restablecerla por un canal verificado para recuperar el acceso sin llamar a la clínica.

## Criterios de aceptación

- **CA-1** · Dado que solicito recuperación con mi celular registrado, cuando confirmo, entonces el sistema envía un enlace o código de un solo uso con vigencia de 15 minutos.
- **CA-2** · Dado que abro el enlace vigente, cuando defino una contraseña que cumple la política, entonces el sistema la actualiza, invalida el enlace y cierra todas las sesiones abiertas.
- **CA-3** · Dado que el enlace ya fue usado o expiró, cuando intento abrirlo, entonces el sistema lo rechaza y ofrece solicitar uno nuevo.
- **CA-4** · Dado que se cambió la contraseña, cuando se completa la operación, entonces el sistema notifica el cambio al canal verificado del usuario.

## Tareas y actividades

### T-004.1 Flujo de restablecimiento en backend

- Endpoint de solicitud con token de un solo uso
- Endpoint de confirmación con validación de política
- Invalidar sesiones activas al cambiar

### T-004.2 Pantallas de recuperación

- Formulario de solicitud
- Formulario de nueva contraseña con indicador de fortaleza
- Pantalla de confirmación

### T-004.3 Notificación del cambio

- Plantilla de aviso por SMS o WhatsApp
- Enviar tras el cambio exitoso
- Registrar el evento en auditoría

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-001 Registro de paciente](HU-001-registro-de-paciente.md)
- [HU-002 Ingreso con contraseña](HU-002-ingreso-con-contrasena.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
