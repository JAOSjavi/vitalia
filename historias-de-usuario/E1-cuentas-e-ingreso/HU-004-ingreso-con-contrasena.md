# HU-004 — Ingreso con contraseña

| Dato | Valor |
|---|---|
| Épica | E1 Cuentas e ingreso |
| Rol | Paciente, Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-03 |
| Origen | HU-002 de la versión anterior, ajustada |

## Historia

> Como usuario registrado, quiero ingresar con mi correo y mi contraseña, para llegar a mi información de forma segura.

## Criterios de aceptación

- **CA-1** · Dado que escribo mi correo y mi contraseña correctos, cuando ingreso, entonces el sistema abre mi sesión y me lleva al inicio que corresponde a mi rol.
- **CA-2** · Dado que la contraseña es incorrecta, cuando intento ingresar, entonces el mensaje no dice si falló el correo o la contraseña.
- **CA-3** · Dados cinco intentos fallidos seguidos, cuando intento de nuevo, entonces el sistema bloquea el ingreso por 15 minutos y me ofrece recuperar la contraseña.
- **CA-4** · Dada cualquier pantalla de ingreso, cuando se revisa, entonces en ningún caso el documento de identidad sirve como clave.

## Tareas y actividades

### T-004.1 Servicio de autenticación

- Verificación de la contraseña contra el hash guardado
- Apertura de la sesión con expiración
- Bloqueo temporal por intentos fallidos

### T-004.2 Pantalla de ingreso

- Formulario y mensajes de error
- Paso al inicio según el rol
- Enlace a la recuperación de contraseña

## Relación con otras historias

**Depende de:**

- [HU-001 Configuración inicial del consultorio](HU-001-configuracion-inicial-del-consultorio.md)
- [HU-002 Registro de paciente](HU-002-registro-de-paciente.md)

**Habilita:**

- [HU-005 Recuperación de contraseña](HU-005-recuperacion-de-contrasena.md)
- [HU-007 Cierre de sesión y expiración](HU-007-cierre-de-sesion-y-expiracion.md)
- [HU-012 Agendar una cita como paciente](../E3-citas/HU-012-agendar-una-cita-como-paciente.md)
- [HU-021 Panel de inicio con la agenda del día](../E4-panel-del-medico/HU-021-agenda-del-dia.md)
- [HU-028 Subir mis historias clínicas](../E5-historias-clinicas-del-paciente/HU-028-subir-mis-historias-clinicas.md)

---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
