# HU-028 — Subir mis historias clínicas

| Dato | Valor |
|---|---|
| Épica | E5 Historias clínicas del paciente |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-26 |
| Origen | HU-016 de la versión anterior, ajustada: ahora quien sube es el paciente |

## Historia

> Como paciente, quiero subir las historias clínicas y los exámenes que tengo de otras atenciones, para que el médico conozca mis antecedentes.

## Criterios de aceptación

- **CA-1** · Dado que elijo un archivo PDF, JPG o PNG de hasta 20 MB, cuando lo subo con su nombre y la fecha del documento, entonces queda guardado y aparece en mi lista.
- **CA-2** · Dado un archivo de otro formato o de más de 20 MB, cuando intento subirlo, entonces el sistema lo rechaza y me dice por qué.
- **CA-3** · Dado que subo varios archivos a la vez, cuando termina la carga, entonces veo cuáles se guardaron y cuáles fallaron.
- **CA-4** · Dado que uso el celular, cuando elijo subir, entonces puedo tomar una foto del documento con la cámara.
- **CA-5** · Dado que la conexión se cae durante la carga, cuando vuelve, entonces puedo reintentar sin que queden archivos a medias.

## Tareas y actividades

### T-028.1 Servicio de carga

- Validación de formato y de tamaño
- Guardado en el almacenamiento privado
- Datos del documento: nombre, fecha y tipo

### T-028.2 Pantalla de carga

- Selección de uno o varios archivos
- Toma de foto desde el celular
- Avance y resultado por archivo

### T-028.3 Pruebas

- Formatos y tamaños no permitidos
- Carga de varios archivos
- Corte de conexión durante la carga

## Relación con otras historias

**Depende de:**

- [HU-004 Ingreso con contraseña](../E1-cuentas-e-ingreso/HU-004-ingreso-con-contrasena.md)
- [HU-027 Almacenamiento privado con enlace temporal](HU-027-almacenamiento-privado-con-enlace-temporal.md)

**Habilita:**

- [HU-029 Ver y eliminar mis documentos](HU-029-ver-y-eliminar-mis-documentos.md)
- [HU-030 Consultar los documentos del paciente en un visor](HU-030-visor-de-documentos-del-paciente.md)
- [HU-031 Lectura del documento para la IA](HU-031-lectura-del-documento-para-la-ia.md)

---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
