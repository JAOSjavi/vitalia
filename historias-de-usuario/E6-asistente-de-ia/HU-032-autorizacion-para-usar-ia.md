# HU-032 — Autorización del paciente para usar IA

| Dato | Valor |
|---|---|
| Épica | E6 Asistente de IA |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-31 |
| Origen | HU-059 de la versión anterior, ajustada |

## Historia

> Como paciente, quiero decidir si el médico puede usar un asistente de inteligencia artificial sobre mis documentos, para tener control de un uso que no es el habitual.

## Criterios de aceptación

- **CA-1** · Dado que estoy creando mi cuenta, cuando se abre la ventana de tratamiento de datos, entonces el uso de inteligencia artificial aparece resaltado y explicado en lenguaje simple, y lo autorizo o no con una casilla aparte que no viene marcada. *(Ajustado en Diseño.)*
- **CA-2** · Dado que acepto, cuando se guarda, entonces quedan la versión del texto, la fecha y la hora.
- **CA-3** · Dado que rechazo o no respondo, cuando el médico abre mi ficha, entonces el asistente aparece deshabilitado y mis documentos siguen disponibles en el visor.
- **CA-4** · Dado que ya acepté, cuando retiro la autorización desde mi perfil, entonces el asistente deja de estar disponible de inmediato y se borran los fragmentos que se habían hecho con mis documentos y mis atenciones. *(Ajustado por D-30.)*
- **CA-5** · Dado que tengo fotos o escaneados "sin leer", cuando acepto la autorización, entonces esos documentos entran a lectura. *(Agregado en Diseño.)*
- **CA-6** · Dado que acepto, cuando se guarda, entonces mis documentos legibles entran a indexación, y también mis atenciones cerradas si la versión del texto que acepté las menciona. *(Agregado por D-30.)*
- **CA-7** · Dado el texto de la autorización, cuando lo leo, entonces explica que el asistente consulta mis documentos y las atenciones del consultorio, y que para buscar en ellos su texto se envía al proveedor sin mis datos de identificación. Es la versión 2 del texto. *(Agregado por D-30.)*

## Tareas y actividades

### T-032.1 Registro de la autorización

- Texto de la autorización y sus versiones
- Aceptación, rechazo y retiro, con fecha y hora
- Consulta del estado vigente

### T-032.2 Pantallas

- Casilla aparte dentro de la ventana del registro
- Opción para retirarla en el perfil
- Texto explicativo en lenguaje simple

## Relación con otras historias

**Depende de:**

- [HU-003 Autorización de tratamiento de datos](../E1-cuentas-e-ingreso/HU-003-autorizacion-de-tratamiento-de-datos.md)

**Habilita:**

- [HU-033 IA solo desde el servidor y aislada por paciente](HU-033-ia-desde-el-servidor-y-aislada-por-paciente.md)

---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
