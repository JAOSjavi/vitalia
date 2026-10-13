# HU-003 — Ingreso con código por SMS (OTP)

| Dato | Valor |
|---|---|
| Épica | E1 Autenticación, cuentas y roles |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-02 |
| Jira | SCRUM-19 |

## Historia

> Como paciente que olvida contraseñas, quiero entrar con un código que me llega al celular para no quedarme por fuera de la aplicación.

## Criterios de aceptación

- **CA-1** · Dado que elijo «Ingresar con código», cuando escribo mi celular registrado, entonces el sistema envía un código de 6 dígitos y muestra la pantalla para digitarlo.
- **CA-2** · Dado que recibí el código, cuando lo ingreso dentro de los 5 minutos de vigencia, entonces el sistema me autentica e invalida el código usado.
- **CA-3** · Dado que el código expiró o es incorrecto, cuando lo envío, entonces el sistema lo rechaza y permite solicitar uno nuevo después de 60 segundos.
- **CA-4** · Dado que el celular no está registrado, cuando solicito el código, entonces el sistema muestra el mismo mensaje de «código enviado» sin confirmar si el número existe.

## Tareas y actividades

### T-003.1 Servicio de generación y validación de OTP

- Generar código aleatorio y guardarlo hasheado con vigencia
- Validar, marcar como usado e invalidar los anteriores
- Limitar solicitudes por número y por hora

### T-003.2 Integrar el proveedor de SMS

- Configurar credenciales en el backend
- Implementar el envío con reintento
- Registrar el resultado del envío

### T-003.3 Pantallas de solicitud y digitación

- Campo de celular con formato colombiano
- Casillas de 6 dígitos con avance automático
- Contador regresivo para reenviar

### T-003.4 Pruebas

- Prueba de vigencia y un solo uso
- Prueba de límite de solicitudes
- Prueba con número no registrado

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-001 Registro de paciente](HU-001-registro-de-paciente.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
