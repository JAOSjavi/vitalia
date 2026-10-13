# HU-038 — Registrar el tratamiento de un paciente

| Dato | Valor |
|---|---|
| Épica | E8 Tratamientos |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-38 |
| Origen | HU-021 y HU-024 de la versión anterior, simplificadas |

## Historia

> Como médico, quiero registrar el tratamiento que le indico a un paciente, para que lo tenga por escrito y sepa cómo tomar cada medicamento.

## Criterios de aceptación

- **CA-1** · Dado que estoy en la ficha de un paciente, cuando registro el motivo y al menos un medicamento con nombre, dosis, frecuencia, duración en días y cómo tomarlo, entonces el tratamiento queda guardado con mi nombre y la fecha.
- **CA-2** · Dado que falta el motivo o algún dato de un medicamento, cuando intento guardar, entonces el sistema no guarda y me dice qué falta.
- **CA-3** · Dado un tratamiento guardado, cuando lo consulto, entonces no puedo modificarlo ni borrarlo; si algo cambia, registro uno nuevo.
- **CA-4** · Dado que guardo el tratamiento, cuando termina, entonces el paciente lo ve de inmediato en "Mis tratamientos" y el registro queda en la bitácora.
- **CA-5** · Dada la duración de cada medicamento, cuando se guarda, entonces el sistema calcula hasta qué fecha va el tratamiento y lo muestra como vigente o terminado.

## Tareas y actividades

### T-038.1 Modelo y servicio

- Tablas de tratamientos y de sus medicamentos
- Regla de no modificar ni borrar un tratamiento guardado
- Cálculo de la fecha de fin y del estado

### T-038.2 Formulario en la ficha

- Motivo, medicamentos e indicaciones generales
- Aviso de los datos que faltan
- Lista de los tratamientos del paciente en la ficha

### T-038.3 Pruebas

- Guardado completo
- Datos faltantes
- Intento de modificar un tratamiento guardado

## Nota de alcance

Los medicamentos se escriben en texto libre. No hay catálogo, aviso de interacciones ni recordatorios; eso quedó para después.

## Relación con otras historias

**Depende de:**

- [HU-025 Ficha del paciente](../E4-panel-del-medico/HU-025-ficha-del-paciente.md)

**Habilita:**

- [HU-039 Ver mis tratamientos](HU-039-ver-mis-tratamientos.md)
- [HU-043 Registrar la consulta en la historia clínica](../E9-historia-clinica-del-consultorio/HU-043-registrar-la-consulta-en-la-historia-clinica.md)

---

[← Volver a E8](README.md) · [Mapa de relaciones](../RELACIONES.md)
