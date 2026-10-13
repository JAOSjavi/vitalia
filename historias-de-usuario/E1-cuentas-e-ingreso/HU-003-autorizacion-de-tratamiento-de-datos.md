# HU-003 — Autorización de tratamiento de datos

| Dato | Valor |
|---|---|
| Épica | E1 Cuentas e ingreso |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-02 |
| Origen | HU-037 de la versión anterior, ajustada |

## Historia

> Como paciente, quiero conocer y aceptar cómo se usarán mis datos de salud antes de crear mi cuenta, para decidir con información.

## Criterios de aceptación

- **CA-1** · Dado que estoy en el registro, cuando llego al paso final, entonces se abre una ventana con los puntos más importantes de la política de tratamiento de datos (quién es el responsable, para qué se usan, el uso de inteligencia artificial sobre mis documentos y mis derechos), con acceso al texto completo, y no puedo crear la cuenta sin aceptarla. *(Ajustado en Diseño.)*
- **CA-2** · Dado que acepto, cuando se crea mi cuenta, entonces el sistema guarda la versión del texto, la fecha y la hora de mi aceptación.
- **CA-3** · Dado que el texto de la autorización cambia, cuando ingreso de nuevo, entonces el sistema me pide aceptar la nueva versión antes de seguir.
- **CA-4** · Dado que quiero revisar lo que acepté, cuando entro a mi perfil, entonces puedo leer la versión vigente y la fecha en que la acepté.

## Tareas y actividades

### T-003.1 Registro de aceptaciones

- Tabla de versiones del texto
- Tabla de aceptaciones por paciente
- Consulta de la versión vigente

### T-003.2 Paso de aceptación

- Ventana con los puntos clave, el texto completo y la casilla de aceptación
- Bloqueo del registro sin aceptación
- Solicitud de nueva aceptación cuando cambia la versión

## Relación con otras historias

**Depende de:**

- [HU-002 Registro de paciente](HU-002-registro-de-paciente.md)

**Habilita:**

- [HU-024 Registrar un paciente desde el panel](../E4-panel-del-medico/HU-024-registrar-un-paciente-desde-el-panel.md)
- [HU-032 Autorización del paciente para usar IA](../E6-asistente-de-ia/HU-032-autorizacion-para-usar-ia.md)

---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
