# HU-043 — Registrar la consulta en la historia clínica

| Dato | Valor |
|---|---|
| Épica | E9 Historia clínica del consultorio |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 8 puntos |
| Requisitos | RF-43 |
| Origen | Nueva (decisión D-24). Retoma HU-015 de la versión anterior |

## Historia

> Como médico, quiero registrar la consulta con el contenido mínimo que exige la norma, para dejar constancia completa de la atención.

## Criterios de aceptación

- **CA-1** · Dado que estoy en una atención abierta, cuando lleno el tipo de consulta, la causa que motiva la atención, el motivo de consulta, la enfermedad actual, los antecedentes, la revisión por sistemas, los signos vitales, el examen físico, el diagnóstico principal y el plan de manejo, entonces quedan guardados en la atención.
- **CA-2** · Dado el diagnóstico, cuando busco por nombre o por código, entonces elijo uno de la lista CIE-10 y marco si es impresión diagnóstica, confirmado nuevo o confirmado repetido; y puedo sumar diagnósticos relacionados.
- **CA-3** · Dado un antecedente o una parte de la revisión por sistemas sin nada que anotar, cuando lo marco como "no refiere" o "sin hallazgos", entonces queda escrito así y no en blanco.
- **CA-4** · Dados los signos vitales, cuando escribo un valor imposible, entonces el sistema me pide revisarlo; y con el peso y la talla calcula el índice de masa corporal.
- **CA-5** · Dado que el paciente ya tiene atenciones cerradas, cuando abro una nueva, entonces los antecedentes de la última aparecen para confirmarlos o cambiarlos; el resto de la consulta empieza vacío.
- **CA-6** · Dado que formulo medicamentos, ordeno exámenes o doy una incapacidad, cuando los registro, entonces quedan en la atención, y la fórmula queda además como tratamiento del paciente.
- **CA-7** · Dado que termino la consulta, cuando indico cómo termina (a casa, o remitido y a dónde) y, si vino acompañado, el nombre y el teléfono del acompañante, entonces quedan registrados.

## Tareas y actividades

### T-043.1 Modelo de la atención

- Tabla de atenciones y de sus diagnósticos
- Carga de la lista CIE-10
- Listas de tipo de consulta, causa, tipo de diagnóstico y destino

### T-043.2 Formulario

- Secciones de la consulta
- Buscador de diagnósticos
- Validación de signos vitales y cálculo del índice de masa corporal

### T-043.3 Vínculo con el tratamiento

- Fórmula registrada como tratamiento del paciente
- Órdenes e incapacidad dentro de la atención
- Antecedentes traídos de la atención anterior

### T-043.4 Pruebas

- Registro completo
- Campos marcados como "no refiere"
- Diagnóstico por nombre y por código

## Nota de alcance

Los campos y la norma de la que sale cada uno están en la sección 4.2 del [marco normativo](../../planificacion/03-marco-normativo.md). El detalle clínico (qué antecedentes, qué sistemas, qué signos) lo debe validar un médico (supuesto S-17). Los medicamentos y las órdenes van en texto libre (supuesto S-18).

## Relación con otras historias

**Depende de:**

- [HU-038 Registrar el tratamiento de un paciente](../E8-tratamientos/HU-038-registrar-el-tratamiento-de-un-paciente.md)
- [HU-042 Pantalla de atención con el asistente al lado](HU-042-pantalla-de-atencion-con-el-asistente-al-lado.md)

**Habilita:**

- [HU-044 Cerrar y firmar la atención](HU-044-cerrar-y-firmar-la-atencion.md)

---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
