# HU-035 — Resumen del paciente con un clic

| Dato | Valor |
|---|---|
| Épica | E6 Asistente de IA |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-33, RF-34 |
| Origen | Nueva |

## Historia

> Como médico, quiero un resumen de los procedimientos, los tratamientos y el estado actual del paciente, para ponerme al día en un minuto antes de atenderlo.

## Criterios de aceptación

- **CA-1** · Dado un paciente con documentos indexados o atenciones cerradas y autorización vigente, cuando pido el resumen, entonces recibo las secciones de diagnósticos, procedimientos, tratamientos y medicamentos, alergias y estado más reciente, cada una en orden de fecha.
- **CA-2** · Dado cada punto del resumen, cuando lo leo, entonces indica el documento y la página, o la atención, de origen. *(Ajustado por D-30.)*
- **CA-3** · Dada una sección sin información en los documentos ni en las atenciones, cuando se muestra, entonces dice "no aparece en los documentos ni en las atenciones". *(Ajustado por D-30.)*
- **CA-4** · Dado que el paciente sube o elimina un documento, o se cierra una atención, cuando vuelvo a la ficha, entonces el resumen anterior aparece como desactualizado y puedo generarlo de nuevo.
- **CA-5** · Dados documentos con datos que se contradicen, cuando se genera el resumen, entonces muestra ambos datos con su origen.

## Tareas y actividades

### T-035.1 Servicio de resumen

- Resumen por documento al indexarlo, y resumen del paciente con esos resúmenes y los datos de sus atenciones, sin búsqueda, para que quede completo
- Estructura fija por secciones
- Orden por fecha y origen de cada punto
- Guardar el resumen con la fecha en que se generó

### T-035.2 Presentación

- Botón de resumen en la ficha
- Marca de resumen desactualizado
- Enlaces al visor

### T-035.3 Pruebas

- Paciente con diez documentos
- Secciones sin información
- Datos contradictorios entre documentos

## Nota de diseño

Las secciones del resumen siguen como guía los grupos de datos clínicos relevantes de la Resolución 866 de 2021. Ver [marco normativo](../../planificacion/03-marco-normativo.md).

## Relación con otras historias

**Depende de:**

- [HU-034 Preguntar al asistente sobre los documentos de un paciente](HU-034-preguntar-al-asistente.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
