# Historia clínica de medicina general: los campos y de dónde salen

**Fecha:** 3 de noviembre de 2026 · **Historias:** HU-041 a HU-045 · **Decisión:** D-33

El dueño del proyecto entregó como modelo una historia clínica real de **oftalmología** (primera vez, de una fundación oftalmológica). Este documento dice qué se tomó de ella, qué se cambió y qué se quitó para un **consultorio de medicina general**, y de qué norma sale cada campo. Del modelo solo se usó la estructura: ningún dato de la paciente entró al proyecto.

Las normas son las de la sección 4 del [marco normativo](../planificacion/03-marco-normativo.md):

- **Resolución 1995 de 1999**: identificación (art. 9), registro de cada atención (art. 10), fecha, hora y autor (art. 5), lo guardado no se modifica (art. 18).
- **Resolución 866 de 2021**: los elementos de dato de la atención, con sus listas.
- **Práctica médica aceptada**: a ella remite el art. 10 de la 1995 para el contenido clínico.

> **Lo debe revisar un médico** (supuesto S-17). El detalle clínico lo deja la norma a la práctica aceptada.

## 1. Qué se hizo con cada parte del modelo

| Parte del PDF de oftalmología | En medicina general | Por qué |
|---|---|---|
| Fecha de atención, fecha de elaboración, folio | Fecha y hora de inicio y de cierre; las pone el sistema | 1995, art. 5 |
| Historia clínica n.º = número de documento | Igual: la historia se identifica con el documento del paciente | 1995, art. 6 |
| Administradora y régimen ("NUEVA EPS SA-Contributivo") | **Aseguradora** y **tipo de vinculación** (contributivo, subsidiado, especial, particular) | 1995, art. 9 · 866 |
| Nombres, apellidos, fecha de nacimiento, edad, sexo | Iguales; la edad se calcula | 1995, art. 9 · 866 |
| Ocupación, nivel escolar, etnia | Iguales. Nivel escolar y pertenencia étnica no frenan el cierre | 1995 pide ocupación; 866 pide pertenencia étnica |
| Municipio y dirección | Iguales, más **zona** (urbana o rural) | 1995, art. 9 · 866 |
| Acompañante con parentesco y teléfono | Igual, en cada atención | 1995, art. 9 |
| — | **Estado civil** y **persona responsable** (nombre, teléfono, parentesco) | Los pide el art. 9 de la 1995 y el modelo no los trae |
| Sintomático de piel / respiratorio | Iguales, como sí o no en la revisión por sistemas | Tamizaje de tuberculosis y lepra que se hace en toda consulta |
| Motivo de la consulta | Igual | Práctica aceptada |
| Enfermedad actual | Igual | Práctica aceptada |
| — | **Antecedentes**: personales, familiares, alergias y factores de riesgo; admiten "No refiere" | 866, datos 47 y 48. El modelo no los separa |
| — | **Revisión por sistemas**; admite "Sin hallazgos" | Práctica aceptada |
| **Examen de especialidad**: agudeza visual, refracción, queratometría, balance muscular, presión intraocular, segmento anterior, fondo de ojo | **Se quita.** En su lugar: **signos vitales** (tensión arterial, frecuencias cardiaca y respiratoria, temperatura, saturación, peso, talla e índice de masa corporal calculado) y **examen físico** general en texto | Lo oftalmológico es propio de la especialidad. Los signos vitales son de práctica aceptada en medicina general y la 866 los menciona |
| Observaciones de bioseguridad | **Se quita** | Es un texto fijo del prestador, no un dato del paciente |
| Concepto | **Análisis**, opcional | Práctica aceptada |
| Diagnósticos con código, tipo (confirmado nuevo…), clase (principal) y sitio (bilateral) | Código **CIE-10** de la lista, tipo (impresión diagnóstica, confirmado nuevo, confirmado repetido) y **un principal**; los demás son relacionados. El **sitio se quita** | 866, datos 37 y 38. La lateralidad es propia de oftalmología |
| Plan de tratamiento con códigos CUPS y cantidad (ayudas diagnósticas, interconsultas) | **Plan de manejo** en texto, **fórmula** con medicamento, dosis, vía, frecuencia, días e indicaciones, **órdenes** en texto e **incapacidad** en días | 866, datos 24 a 31 y 45. Las órdenes van en texto libre (supuesto S-18) |
| Signos de alarma y estilos de vida | **Recomendaciones y signos de alarma**, opcional | Práctica aceptada |
| — | **Cómo termina la atención**: a casa o remitido, y a dónde | 866, datos 41 y 44 |
| Profesional, especialidad, registro médico y documento | **Firma** al cerrar: nombre, registro y documento del médico, con fecha y hora. Se confirma con su contraseña | 1995, arts. 5 y 18 |
| Aceptación de términos y tratamiento de datos | Ya está en el registro del paciente (autorización de datos) | Ley 1581 de 2012 |

## 2. Lo que hace falta para cerrar

**Identificación:** sexo, estado civil, ocupación, dirección, municipio y tipo de vinculación; la aseguradora, salvo que sea particular.

**Consulta:** tipo de consulta, finalidad, causa, motivo, enfermedad actual, los cuatro antecedentes, revisión por sistemas, los siete signos vitales menos la saturación, examen físico, diagnóstico principal, plan de manejo y cómo termina; si es remitido, a dónde.

Si falta algo, la atención no se cierra y el sistema dice qué falta.

## 3. Reglas que quedaron en el código

| Regla | Dónde |
|---|---|
| Una sola atención abierta por paciente | Índice `una_abierta_por_paciente` |
| Lo cerrado no cambia, ni siquiera para el dueño de las tablas | Disparador `atencion_cerrada_no_cambia`; la API no tiene permiso de borrar |
| Las correcciones son notas aclaratorias, con su fecha y su autor | Tabla `notas_aclaratorias`, solo inserción |
| Un signo vital imposible no se guarda y pide revisarlo | `dominio/historia_clinica.py` y la base con rangos |
| El paciente solo ve sus atenciones cerradas | Permiso por fila `propias_cerradas` |
| Cada consulta de la historia queda en la bitácora | `consulta_de_historia` |
| Al cerrar, la cita queda como atendida | `casos_de_uso/historia_clinica.py` |

## 4. Lo que queda pendiente

- **Catálogo CIE-10 completo.** Hoy hay 110 diagnósticos frecuentes de medicina general (`servidor/migraciones/textos/cie10-frecuentes.csv`), escritos a mano. Hay que cargar la tabla oficial de SISPRO y revisar los nombres contra ella.
- **Municipio** en texto libre: falta la lista de municipios del DANE (DIVIPOLA).
- **Copia en PDF para el paciente** (HU-046).
- **La fórmula como tratamiento del paciente** (E8, HU-038 y HU-039): hoy la fórmula queda dentro de la atención y el paciente la ve ahí.
- **Las atenciones cerradas en el asistente**: requiere la versión 2 del texto de autorización de IA, que debe revisar el abogado.
- **Firma**: hoy es la sesión más la contraseña del médico. La firma digital certificada es la pregunta 7 para el abogado.
