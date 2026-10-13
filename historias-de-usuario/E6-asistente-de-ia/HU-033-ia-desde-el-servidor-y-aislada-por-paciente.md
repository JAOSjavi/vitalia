# HU-033 — IA solo desde el servidor y aislada por paciente

| Dato | Valor |
|---|---|
| Épica | E6 Asistente de IA |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-35 |
| Origen | HU-061 de la versión anterior, ajustada |

## Historia

> Como responsable del sistema, quiero que toda consulta a la IA salga del servidor y lleve solo los documentos de un paciente, para que no se mezclen historias ni se expongan claves.

## Criterios de aceptación

- **CA-1** · Dado el código que corre en el navegador, cuando se revisa, entonces no contiene la clave del proveedor de IA ni llamadas directas a él.
- **CA-2** · Dada una consulta sobre un paciente, cuando el servidor arma la petición, entonces incluye únicamente el texto de los documentos legibles de ese paciente.
- **CA-3** · Dado un paciente sin autorización vigente, cuando se intenta una consulta, entonces el servidor la bloquea antes de llamar al proveedor.
- **CA-4** · Dada una consulta, cuando se envía, entonces no incluye el número de documento, el celular ni el correo del paciente.
- **CA-5** · Dado que el volumen de documentos supera lo que admite una sola petición, cuando se arma el contexto, entonces se usan los resúmenes por documento y el médico ve el aviso.
- **CA-6** · Dada cada consulta, cuando termina, entonces queda en la bitácora quién preguntó, sobre qué paciente y cuándo.

## Tareas y actividades

### T-033.1 Servicio intermediario

- Clave del proveedor guardada solo en el servidor
- Validación del rol médico y de la autorización del paciente
- Límite de consultas por hora

### T-033.2 Armado del contexto

- Selección de los documentos del paciente consultado
- Retiro de los identificadores directos
- Uso de resúmenes por documento cuando el volumen crece

### T-033.3 Pruebas

- Consulta sobre un paciente sin autorización
- Intento de consulta con rol paciente
- Verificación de que no se mezclan documentos de pacientes distintos

## Nota de diseño

Como referencia de la investigación: una petición a un modelo actual admite hasta unas 600 páginas de PDF o 32 MB. El proveedor es una decisión abierta (A-04 en [decisiones y supuestos](../../planificacion/04-decisiones-y-supuestos.md)).

## Relación con otras historias

**Depende de:**

- [HU-031 Lectura del documento para la IA](../E5-historias-clinicas-del-paciente/HU-031-lectura-del-documento-para-la-ia.md)
- [HU-032 Autorización del paciente para usar IA](HU-032-autorizacion-para-usar-ia.md)

**Habilita:**

- [HU-034 Preguntar al asistente sobre los documentos de un paciente](HU-034-preguntar-al-asistente.md)

---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
