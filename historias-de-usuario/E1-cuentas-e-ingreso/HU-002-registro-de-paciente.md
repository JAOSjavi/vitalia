# HU-002 — Registro de paciente

| Dato | Valor |
|---|---|
| Épica | E1 Cuentas e ingreso |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-01 |
| Origen | HU-001 de la versión anterior, ajustada |

## Historia

> Como paciente nuevo, quiero crear mi cuenta con mis datos y una contraseña propia, para agendar y subir mis documentos sin llamar al consultorio.

## Criterios de aceptación

- **CA-1** · Dado que ingreso nombre, tipo y número de documento, fecha de nacimiento, celular, correo y una contraseña válida, cuando confirmo, entonces el sistema crea mi cuenta con rol paciente y me lleva al inicio.
- **CA-2** · Dado que la contraseña tiene menos de 8 caracteres o no incluye un número, cuando intento continuar, entonces el sistema no envía el formulario y explica qué le falta.
- **CA-3** · Dado que el correo o el documento ya están registrados, cuando intento registrarme, entonces el sistema me avisa y me ofrece ingresar o recuperar la contraseña, sin mostrar datos de la otra cuenta.
- **CA-4** · Dado que el médico ya me había registrado, cuando abro el enlace de activación que recibí, entonces solo defino mi contraseña y mis datos ya aparecen cargados.

## Tareas y actividades

### T-002.1 Modelo y servicio de registro

- Tablas de pacientes y de cuentas
- Validación de que el correo y el documento no se repitan
- Guardar la contraseña con hash y sal

### T-002.2 Pantalla de registro

- Formulario con validación mientras se escribe
- Mensajes de error en lenguaje claro
- Paso al inicio del paciente al terminar

### T-002.3 Activación de una cuenta creada por el médico

- Enlace de activación con vigencia
- Pantalla para definir la contraseña
- Prueba del recorrido completo

## Relación con otras historias

**Depende de:**

- [HU-006 Roles y permisos de médico y paciente](HU-006-roles-y-permisos.md)

**Habilita:**

- [HU-003 Autorización de tratamiento de datos](HU-003-autorizacion-de-tratamiento-de-datos.md)
- [HU-004 Ingreso con contraseña](HU-004-ingreso-con-contrasena.md)

---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
