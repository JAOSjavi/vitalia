# HU-047 — Sugerencias para la historia con los documentos del paciente

| Dato | Valor |
|---|---|
| Épica | E9 Historia clínica del consultorio |
| Rol | Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-43 |
| Origen | Pedido del dueño el 10 de noviembre de 2026 (decisión D-36) |

## Historia

> Como médico, quiero que la atención me proponga los antecedentes y la enfermedad actual con lo que dicen los documentos del paciente, para no copiarlos a mano y ver de dónde sale cada dato.

## Criterios de aceptación

- **CA-1** · Dada una atención abierta de un paciente que autorizó la IA y tiene documentos leídos, cuando pido "Completar con los documentos", entonces debajo de los antecedentes personales, los antecedentes familiares, las alergias, los factores de riesgo y la enfermedad actual aparece lo que dicen los documentos, cada dato con el documento, la página y la frase de la que sale.
- **CA-2** · Dada una sugerencia, cuando el modelo no la respalda con una frase que esté tal cual en lo que se le envió, entonces no se muestra.
- **CA-3** · Dada una sugerencia, cuando la uso, entonces queda en el campo y se guarda en el borrador; si el campo ya tenía texto, se agrega al final y no lo reemplaza. Si la descarto, desaparece y el campo no cambia.
- **CA-4** · Dado un campo del que los documentos no dicen nada, cuando pido las sugerencias, entonces no se propone nada para ese campo: que los documentos no lo mencionen no es "no refiere".
- **CA-5** · Dado que el paciente no autorizó la IA, no tiene documentos leídos o el médico llegó al tope de consultas por hora, cuando pido las sugerencias, entonces no se envía nada al proveedor y la pantalla dice por qué.
- **CA-6** · Dado cualquier envío, entonces sale sin el nombre, el documento, el teléfono ni el correo del paciente, y la bitácora anota quién pidió sugerencias sobre quién y cuándo, sin el texto.
- **CA-7** · Nunca se sugieren diagnósticos, plan de manejo, fórmula, órdenes ni datos de identificación.

## Tareas y actividades

### T-047.1 Servidor

- Pedirle al modelo una respuesta en JSON (`ProveedorIA.responder_en_json`)
- Caso de uso `SugerirCampos`: las mismas comprobaciones del asistente, una búsqueda por campo y la comprobación de cada frase
- Ruta `POST /api/v1/atenciones/{id}/sugerencias`

### T-047.2 Pantalla

- Botón "Completar con los documentos" en la atención
- Sugerencia debajo de cada campo con su origen, Usar y Descartar

### T-047.3 Pruebas

- Frase comprobada y frase inventada
- Campo con texto: se agrega, no se reemplaza
- Sin autorización, sin documentos y atención cerrada: no se llama al modelo
- Nada del paciente sale hacia el modelo

## Nota de alcance

Usa el mismo modelo de respuestas del asistente (`qwen3.7-plus`) y la misma búsqueda (D-30). Solo lee los documentos que subió el paciente: las atenciones cerradas entran cuando exista la versión 2 de la autorización de IA. Sugerir diagnósticos o tratamientos contradice el texto que firmó el paciente ("no lo diagnostica ni recomienda tratamientos") y queda fuera hasta que el abogado revise un texto nuevo.

## Relación con otras historias

**Depende de:**

- [HU-043 Registrar la consulta en la historia clínica](HU-043-registrar-la-consulta-en-la-historia-clinica.md)
- [HU-034 Preguntar al asistente](../E6-asistente-de-ia/HU-034-preguntar-al-asistente.md)

---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
