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
- **CA-2** · Dada una consulta sobre un paciente, cuando el servidor busca los fragmentos, entonces solo encuentra fragmentos de ese paciente, de sus documentos y de sus atenciones cerradas, y la petición al proveedor lleva solo esos. *(Ajustado por D-30.)*
- **CA-3** · Dado un paciente sin autorización vigente, cuando se intenta una consulta, entonces el servidor la bloquea antes de llamar al proveedor.
- **CA-4** · Dada una consulta o una vectorización, cuando se envía, entonces no incluye el nombre, el número de documento, el celular ni el correo del paciente. *(Ajustado por D-30.)*
- **CA-5** · Dado un paciente con más texto del que admite una petición, cuando pregunto, entonces se envían solo los fragmentos más cercanos a la pregunta, buscados por significado y por palabras, sin pasar del tope. *(Ajustado por D-30.)*
- **CA-6** · Dada cada consulta, cuando termina, entonces queda en la bitácora quién preguntó, sobre qué paciente y cuándo.
- **CA-7** · Dado un paciente cuya autorización vigente es la versión 1 del texto, cuando pregunto, entonces la búsqueda no incluye sus atenciones y lo veo indicado. *(Agregado por D-30.)*

## Tareas y actividades

### T-033.1 Servicio intermediario

- Clave del proveedor guardada solo en el servidor
- Validación del rol médico y de la autorización del paciente
- Límite de consultas por hora

### T-033.2 Búsqueda y armado del contexto

- Función de búsqueda por paciente: por significado con `pgvector` y por palabras en español, combinadas
- Retiro de los identificadores directos
- Fragmentos rotulados por documento y página o por atención

### T-033.3 Pruebas

- Consulta sobre un paciente sin autorización
- Intento de consulta con rol paciente
- Verificación de que la búsqueda no trae fragmentos de otro paciente
- Paciente con la autorización versión 1: sin atenciones

## Nota de diseño

El proveedor de la primera versión es Qwen, detrás de un adaptador que permite cambiarlo por configuración. Al modelo se le envían los fragmentos encontrados, no los archivos ni todo el historial (D-30). El detalle está en [diseño del asistente](../../diseno/04-asistente-ia.md).

## Relación con otras historias

**Depende de:**

- [HU-031 Lectura del documento para la IA](../E5-historias-clinicas-del-paciente/HU-031-lectura-del-documento-para-la-ia.md)
- [HU-032 Autorización del paciente para usar IA](HU-032-autorizacion-para-usar-ia.md)

**Habilita:**

- [HU-034 Preguntar al asistente sobre los documentos de un paciente](HU-034-preguntar-al-asistente.md)

---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
