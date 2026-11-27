# HU-031 — Lectura del documento para la IA

| Dato | Valor |
|---|---|
| Épica | E5 Historias clínicas del paciente |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-30 |
| Origen | Nueva |

## Historia

> Como sistema, quiero leer el contenido de cada documento al subirlo, para que el asistente pueda responder sobre él y el médico sepa si quedó legible.

## Criterios de aceptación

- **CA-1** · Dado un PDF que trae texto, cuando se sube, entonces el sistema guarda su texto página por página.
- **CA-2** · Dado un PDF escaneado o una foto, cuando se sube, entonces el sistema reconoce el texto y lo guarda página por página.
- **CA-3** · Dado un documento que no se pudo leer, cuando termina el proceso, entonces queda marcado como "no legible" y tanto el paciente como el médico lo ven así.
- **CA-4** · Dado que la lectura tarda, cuando el paciente sube el archivo, entonces la carga no se queda esperando y el documento aparece como "en proceso".
- **CA-5** · Dado que el paciente elimina el documento, cuando se elimina, entonces también se eliminan su texto y sus fragmentos. *(Ajustado por D-30.)*
- **CA-6** · Dado un PDF escaneado o una foto de un paciente que no ha autorizado el uso de IA, cuando se sube, entonces no se envía a ningún proveedor externo y queda como "sin leer" hasta que el paciente autorice. *(Agregado en Diseño.)*
- **CA-7** · Dado un documento legible de un paciente que autorizó el uso de IA, cuando termina la lectura, entonces queda partido en fragmentos de una sola página, sin los identificadores del paciente, con su vector, y disponible para el asistente. *(Agregado por D-30.)*
- **CA-8** · Dado un documento legible de un paciente que no ha autorizado el uso de IA, cuando termina la lectura, entonces no se indexa ni se envía nada al proveedor, aunque sea un PDF con texto. *(Agregado por D-30.)*

## Tareas y actividades

### T-031.1 Extracción de texto

- Texto de los PDF, por página
- Reconocimiento de texto en escaneados y fotos
- Medida de qué tan legible quedó

### T-031.2 Proceso en segundo plano

- Cola de documentos por leer
- Estados: sin leer, en proceso, legible y no legible
- Reintento cuando falla

### T-031.3 Indexación

- Partir cada página en fragmentos, sin cruzar de página
- Retiro de identificadores y vectorización
- Tabla de fragmentos con `pgvector` y su permiso por fila

### T-031.4 Pruebas

- PDF con texto
- Foto de buena calidad y foto de mala calidad
- Documento escrito a mano
- Paciente sin autorización: no se indexa

## Nota de diseño

Los PDF con texto se leen dentro del servidor. Las fotos y los escaneados los lee un modelo de visión del proveedor de IA, por eso dependen de la autorización del paciente. El detalle está en [diseño del asistente](../../diseno/04-asistente-ia.md). La letra manuscrita es el caso más difícil.

## Relación con otras historias

**Depende de:**

- [HU-028 Subir mis historias clínicas](HU-028-subir-mis-historias-clinicas.md)

**Habilita:**

- [HU-033 IA solo desde el servidor y aislada por paciente](../E6-asistente-de-ia/HU-033-ia-desde-el-servidor-y-aislada-por-paciente.md)

---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
