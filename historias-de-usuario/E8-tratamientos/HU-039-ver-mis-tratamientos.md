# HU-039 — Ver mis tratamientos

| Dato | Valor |
|---|---|
| Épica | E8 Tratamientos |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-39 |
| Origen | HU-027 y HU-028 de la versión anterior, simplificadas |

## Historia

> Como paciente, quiero ver el último tratamiento que me indicó el médico y los anteriores, para saber qué debo tomar y cómo.

## Criterios de aceptación

- **CA-1** · Dado que tengo tratamientos, cuando abro "Mis tratamientos", entonces veo primero el último, con el motivo, la fecha, quién lo indicó y si está vigente o terminado.
- **CA-2** · Dado cada medicamento, cuando lo veo, entonces muestra nombre, dosis, frecuencia, duración y, resaltado, cómo tomarlo.
- **CA-3** · Dado que tengo tratamientos anteriores, cuando los consulto, entonces aparecen en orden de fecha y puedo abrir el detalle de cada uno.
- **CA-4** · Dado que no tengo tratamientos, cuando abro la sección, entonces veo un mensaje que lo explica.
- **CA-5** · Dado que soy paciente, cuando consulto, entonces solo veo mis propios tratamientos.

## Tareas y actividades

### T-039.1 Consulta de tratamientos

- Servicio de tratamientos del paciente
- Orden por fecha y estado vigente o terminado
- Restricción a los tratamientos propios

### T-039.2 Pantalla "Mis tratamientos"

- Último tratamiento completo
- Lista de anteriores con su detalle
- Tarjeta del tratamiento vigente en el inicio

## Relación con otras historias

**Depende de:**

- [HU-038 Registrar el tratamiento de un paciente](HU-038-registrar-el-tratamiento-de-un-paciente.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E8](README.md) · [Mapa de relaciones](../RELACIONES.md)
