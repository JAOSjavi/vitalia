# HU-034 — Preguntar al asistente sobre los documentos de un paciente

| Dato | Valor |
|---|---|
| Épica | E6 Asistente de IA |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-32, RF-34 |
| Origen | HU-060 de la versión anterior, ajustada |

## Historia

> Como médico, quiero hacerle preguntas al asistente sobre lo que el paciente subió, para encontrar un dato sin leer todos los documentos.

## Criterios de aceptación

- **CA-1** · Dado un paciente con documentos legibles y autorización vigente, cuando escribo una pregunta, entonces recibo una respuesta basada solo en esos documentos.
- **CA-2** · Dada una respuesta, cuando la leo, entonces cada dato indica el documento y la página de donde salió, y puedo abrirlo en el visor en esa página.
- **CA-3** · Dado que la información no está en los documentos, cuando pregunto por ella, entonces el asistente responde que no aparece, sin suponer.
- **CA-4** · Dado que pregunto qué diagnóstico tiene el paciente o qué tratamiento darle, cuando el asistente responde, entonces aclara que solo resume lo registrado y no emite una recomendación clínica.
- **CA-5** · Dado que hago una segunda pregunta, cuando la envío, entonces el asistente tiene en cuenta la conversación de esa sesión.
- **CA-6** · Dada toda respuesta, cuando se muestra, entonces incluye el aviso de que es un apoyo y no reemplaza la lectura del documento.

## Tareas y actividades

### T-034.1 Servicio de preguntas

- Instrucciones del asistente: solo lo registrado y siempre con el origen
- Respuesta con documento y página por cada dato
- Conversación dentro de la sesión

### T-034.2 Pantalla del asistente

- Caja de pregunta y respuesta que aparece a medida que se escribe
- Enlaces al visor en la página citada
- Aviso permanente de que es un apoyo

### T-034.3 Pruebas

- Conjunto de preguntas con respuesta conocida
- Preguntas cuya respuesta no está en los documentos
- Peticiones de diagnóstico o de tratamiento

## Ejemplo

> **Médico:** ¿Qué procedimientos le han hecho en los últimos dos años?
>
> **Asistente:** Según los documentos: colecistectomía por laparoscopia en marzo de 2025 *(Epicrisis Clínica del Norte, pág. 2)* y endoscopia digestiva alta en agosto de 2025 *(Informe de endoscopia, pág. 1)*. No aparece ningún otro procedimiento en los documentos.

## Relación con otras historias

**Depende de:**

- [HU-025 Ficha del paciente](../E4-panel-del-medico/HU-025-ficha-del-paciente.md)
- [HU-033 IA solo desde el servidor y aislada por paciente](HU-033-ia-desde-el-servidor-y-aislada-por-paciente.md)

**Habilita:**

- [HU-035 Resumen del paciente con un clic](HU-035-resumen-del-paciente.md)

---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
