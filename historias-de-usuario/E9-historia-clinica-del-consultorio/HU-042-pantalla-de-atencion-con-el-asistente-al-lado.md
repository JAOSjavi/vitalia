# HU-042 — Pantalla de atención con el asistente al lado

| Dato | Valor |
|---|---|
| Épica | E9 Historia clínica del consultorio |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-42 |
| Origen | Nueva (decisión D-24) |

## Historia

> Como médico, quiero abrir la atención de un paciente y ver a un lado el asistente con su resumen y en el centro el formulario de la historia clínica, para escribir la consulta sin cambiar de pantalla.

## Criterios de aceptación

- **CA-1** · Dada una cita de hoy o la ficha de un paciente, cuando elijo "Atender", entonces se abre la atención con la fecha y la hora de inicio y el formulario de la historia clínica en el centro.
- **CA-2** · Dado que el paciente autorizó el uso de IA y tiene documentos legibles, cuando se abre la atención, entonces a un lado aparece el resumen del paciente y puedo hacerle preguntas al asistente sin salir de la pantalla.
- **CA-3** · Dado que el paciente no autorizó el uso de IA o no tiene documentos legibles, cuando se abre la atención, entonces el lado del asistente lo explica y el formulario funciona igual.
- **CA-4** · Dado que el asistente responde, cuando leo su respuesta, entonces nada de lo que dice pasa al formulario por sí solo: lo que queda en la historia lo escribo yo.
- **CA-5** · Dado que estoy escribiendo, cuando cambio de sección o se cierra la pantalla, entonces lo escrito queda guardado como borrador y lo recupero al volver.
- **CA-6** · Dado un paciente con una atención abierta, cuando intento abrirle otra, entonces el sistema me lleva a la que ya está abierta.

## Tareas y actividades

### T-042.1 Servicio de atención

- Abrir una atención ligada a la cita o a la ficha
- Guardado del borrador
- Una sola atención abierta por paciente

### T-042.2 Pantalla

- Formulario en el centro y asistente a un lado
- Resumen y preguntas dentro de la misma pantalla
- Aviso de datos de identificación pendientes

### T-042.3 Pruebas

- Paciente con autorización de IA y sin ella
- Recuperación del borrador
- Intento de abrir dos atenciones

## Nota de diseño

El lado del asistente usa lo que ya existe en HU-034 y HU-035. Si esas historias todavía no están construidas, la pantalla funciona solo con el formulario. En celular el asistente pasa a una pestaña.

## Relación con otras historias

**Depende de:**

- [HU-021 Panel de inicio con la agenda del día](../E4-panel-del-medico/HU-021-agenda-del-dia.md)
- [HU-025 Ficha del paciente](../E4-panel-del-medico/HU-025-ficha-del-paciente.md)

**Habilita:**

- [HU-043 Registrar la consulta en la historia clínica](HU-043-registrar-la-consulta-en-la-historia-clinica.md)

---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
