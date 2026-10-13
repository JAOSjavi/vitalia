# Marco normativo

**Fase del ciclo de vida:** Planificación
**Versión:** 2.1 · 13 de octubre de 2026

> Este documento es una lectura técnica de las normas para convertirlas en requisitos. **No es un concepto jurídico.** Los puntos de la sección 5 deben confirmarse con un abogado de salud digital antes de salir a producción.

---

## 1. Quién responde por los datos

Según la Ley 1581 de 2012, el **consultorio** es el responsable del tratamiento: decide para qué se usan los datos de sus pacientes. Quien construya y opere el sistema por cuenta del consultorio es el **encargado**. Esa relación debe quedar en un contrato de encargo antes de cargar datos reales.

Los datos de salud son **datos sensibles**. Solo se pueden tratar con autorización explícita del titular, y nadie puede condicionar un servicio a que entregue más datos de los necesarios.

## 2. Normas que aplican a este alcance

| Norma | Qué exige | Cómo lo cubre el producto |
|---|---|---|
| **Ley 1581 de 2012** — protección de datos personales | Autorización previa, expresa e informada (art. 9) | HU-003: no hay cuenta sin autorización; se guarda versión, fecha y hora |
| | Tratamiento especial de datos sensibles (arts. 5 y 6) | HU-032: autorización aparte para usar IA sobre los documentos |
| | Atender consultas en 10 días hábiles y reclamos en 15 (arts. 14 y 15) | HU-029: el paciente ve y elimina sus documentos. HU-040: corrige sus datos. El canal de reclamos es un proceso del consultorio |
| | Medidas de seguridad para impedir acceso no autorizado | HU-027, HU-036, RNF-01 a RNF-05 |
| | Reglas para enviar datos a otro país (art. 26) | HU-033 y RNF-08: mínimo de datos y proveedor con acuerdo de tratamiento. Ver pregunta 2 |
| **Ley 23 de 1981** — ética médica | La historia clínica es reservada; un tercero solo la conoce con autorización del paciente o por mandato legal | HU-006, HU-036: solo el médico y el propio paciente acceden |
| **Resolución 1995 de 1999** y **Resolución 839 de 2017** — manejo y conservación de la historia clínica | Componentes y contenido mínimo de la historia; cada anotación con fecha, hora y autor; lo guardado no se modifica; conservación mínima de 15 años | La épica E9 lleva la historia clínica del consultorio con el contenido de la sección 4. Las atenciones cerradas (HU-044) y los tratamientos (HU-038) no se modifican ni se borran. Los documentos que sube el paciente son antecedentes, no la historia del consultorio |
| **Ley 2015 de 2020** — historia clínica electrónica interoperable | El titular es dueño de su historia; el prestador conserva la custodia en sus propios sistemas; el acceso de terceros requiere consentimiento | HU-037: trazabilidad de accesos. HU-032: consentimiento. HU-046: copia para el paciente |
| **Resolución 866 de 2021** — datos clínicos relevantes | Define 49 elementos de dato en cuatro grupos: identificación del usuario, contacto con el servicio, tecnologías en salud (procedimientos, medicamentos) y resultados (diagnósticos, incapacidades). Son de uso obligatorio para todos los prestadores | HU-041 y HU-043: los campos de la historia clínica siguen esos elementos. HU-035: el resumen del asistente se organiza con esos grupos como guía |
| **Resolución 1888 de 2025** — Resumen Digital de Atención (RDA) | Al terminar una consulta, el prestador genera y envía un resumen con los datos de la Resolución 866. El plazo para adecuar los sistemas fue de seis meses desde el 15 de octubre de 2025 | Los datos se guardan de forma que el resumen se pueda generar. **El envío no está en este alcance.** Ver pregunta 5 |

## 3. ISO/IEC 27001 como línea base de seguridad

La ISO/IEC 27001:2022 describe un sistema de gestión de seguridad de la información. **Certifica a una organización, no a un programa**, así que Vitalia no "se certifica". Lo que sí se hace es tomar los controles de su Anexo A como requisitos. La norma de la misma familia dedicada a privacidad es la ISO/IEC 27701.

| Control del Anexo A | Tema | Dónde queda en el producto |
|---|---|---|
| A.5.15 y A.8.3 | Control y restricción de acceso | HU-006, HU-036 |
| A.5.17 y A.8.5 | Credenciales y autenticación segura | HU-004, HU-005, RNF-04 |
| A.5.23 | Seguridad al usar servicios en la nube | Decisión de Diseño: dónde se aloja y con qué proveedor |
| A.5.34 | Privacidad y protección de datos personales | HU-003, HU-032, RNF-07 |
| A.8.10 | Eliminación de información | HU-029: al eliminar un documento se elimina su texto |
| A.8.11 | Enmascaramiento de datos | HU-033: sin identificadores directos hacia la IA |
| A.8.13 | Copias de respaldo | RNF-12 |
| A.8.15 | Registro de eventos | HU-037 |
| A.8.24 | Uso de criptografía | HU-027, RNF-03, RNF-05 |

Los controles de personas y de instalaciones físicas del Anexo A son responsabilidad del consultorio y de quien opere el sistema; no son funciones del programa.

## 4. Contenido mínimo de la historia clínica

El dueño del proyecto decidió que la historia clínica del consultorio entra al alcance, con lo mínimo que exija la norma (D-24). La norma vigente es la Resolución 1995 de 1999. El contenido sale de tres fuentes:

| Fuente | Qué aporta |
|---|---|
| Resolución 1995 de 1999, arts. 8 a 11 | Los tres componentes de la historia: identificación del usuario, registro de cada atención y anexos. Lista los datos de identificación. Para el contenido de la atención remite a los datos mínimos de prestación de servicios y a lo generalmente aceptado en la práctica médica |
| Resolución 866 de 2021 | Los 49 elementos de dato, con sus listas de valores |
| Resolución 1888 de 2025, anexo técnico | Cuáles de esos elementos lleva el resumen de una consulta externa |

Las tablas que siguen son la base del formulario. **Las debe revisar un médico**, porque la norma deja el detalle clínico a la práctica aceptada, **y el abogado**.

### 4.1 Identificación del paciente

| Dato | De dónde sale | Dónde se pide |
|---|---|---|
| Nombres y apellidos completos | 1995, art. 9 · 866, dato 3 | Registro |
| Tipo y número de documento | 1995, art. 9 · 866, dato 2 | Registro |
| Fecha de nacimiento; la edad se calcula | 1995, art. 9 · 866, dato 4 | Registro |
| Teléfono | 1995, art. 9 | Registro |
| Correo | No lo pide la norma; se usa para avisos y para recuperar la contraseña | Registro |
| Sexo | 1995, art. 9 · 866, dato 5 | Datos de la historia clínica |
| Estado civil | 1995, art. 9 | Datos de la historia clínica |
| Ocupación | 1995, art. 9 · 866, dato 7 | Datos de la historia clínica |
| Dirección y municipio de residencia | 1995, art. 9 · 866, dato 12 | Datos de la historia clínica |
| Aseguradora y tipo de vinculación | 1995, art. 9 · 866, dato 15 | Datos de la historia clínica |
| Persona responsable: nombre, teléfono y parentesco, si aplica | 1995, art. 9 | Datos de la historia clínica |
| Acompañante: nombre y teléfono | 1995, art. 9 | En cada atención |

El registro se queda corto, como lo pidió el dueño del proyecto (D-21). Los demás datos se completan una sola vez, antes de cerrar la primera atención (HU-041).

La Resolución 866 pide además país de nacionalidad, identidad de género, pertenencia étnica, categoría de discapacidad y zona de residencia (datos 1, 6, 10, 13 y 14). La 1995 no los exige. Quedan previstos y se piden cuando se conecte el envío del resumen de atención.

### 4.2 Registro de cada atención

| Dato | De dónde sale | Para cerrar la atención |
|---|---|---|
| Fecha y hora de inicio y de fin | 1995, art. 5 · 866, datos 17 y 43 | Lo pone el sistema |
| Médico que atiende, con su documento y su registro profesional | 1995, arts. 5 y 18 · 866, dato 49 | Lo pone el sistema |
| Tipo de consulta (primera vez o control) y finalidad | Datos mínimos de prestación de servicios, a los que remite el art. 10 de la 1995. La lista vigente está en el anexo de la Resolución 948 de 2026 y falta confirmarla | Obligatorio |
| Causa que motiva la atención | 866, dato 21 | Obligatorio, de una lista |
| Motivo de consulta | Práctica médica aceptada (1995, art. 10) | Obligatorio |
| Enfermedad actual | Práctica médica aceptada | Obligatorio |
| Antecedentes: personales, familiares con su parentesco, alergias con su tipo, y factores de riesgo | 866, datos 47 y 48 | Obligatorio; admite "no refiere" |
| Revisión por sistemas | Práctica médica aceptada | Obligatorio; admite "sin hallazgos" |
| Signos vitales: tensión arterial, frecuencia cardiaca, frecuencia respiratoria, temperatura, peso y talla | Práctica médica aceptada · 866, dato 39 | Obligatorio |
| Examen físico | Práctica médica aceptada | Obligatorio |
| Diagnóstico principal, con código CIE-10 y su tipo: impresión diagnóstica, confirmado nuevo o confirmado repetido | 866, dato 37 | Obligatorio |
| Diagnósticos relacionados | 866, dato 38 | Opcional |
| Plan de manejo | Práctica médica aceptada | Obligatorio |
| Fórmula: medicamento, dosis, vía, frecuencia y duración | 866, datos 24 a 31 | Si el médico formula |
| Órdenes de exámenes o procedimientos | 866, dato 24 | Si el médico ordena |
| Incapacidad, en días | 866, dato 45 | Si el médico la da |
| Cómo termina la atención: a casa, remitido, y a dónde | 866, datos 41 y 44 | Obligatorio, de una lista |

La fórmula es el tratamiento de la épica E8. A ese tratamiento le falta hoy la **vía de administración**, que la Resolución 866 sí pide (dato 29); se agrega en Diseño.

### 4.3 Anexos

El artículo 11 de la Resolución 1995 llama anexos a los soportes de la atención, como el consentimiento informado. En este alcance el sistema guarda la autorización de datos y la de inteligencia artificial. Los consentimientos de procedimientos no entran en la primera versión. Ver pregunta 8.

### 4.4 Reglas del registro

| Regla | Norma | Cómo queda en el producto |
|---|---|---|
| La historia se abre en la primera atención y se identifica con el número de documento del paciente | 1995, art. 6 | HU-041 |
| Cada anotación lleva fecha, hora y autor | 1995, art. 5 | HU-044: los pone el sistema al cerrar |
| Lo guardado no se puede modificar | 1995, art. 18 | HU-044: una atención cerrada no cambia. Las correcciones son notas aclaratorias que se suman, con su propia fecha y autor |
| El autor queda identificado por un medio que reemplaza la firma y el sello | 1995, art. 18 | La sesión del médico más su nombre y registro profesional en cada atención. Ver pregunta 7 |
| Los registros van en orden cronológico | 1995, art. 3 | HU-045 |
| Sin espacios en blanco y sin siglas | 1995, art. 5 | El formulario no deja cerrar con campos obligatorios vacíos. Evitar siglas queda a cargo del médico |
| La historia es reservada | Ley 23 de 1981 · 1995, art. 1 | Solo el médico y el paciente. Cada acceso queda en la bitácora |
| Se conserva 15 años como mínimo | 839 de 2017 | No existe operación de borrado. RNF-15 |

### 4.5 Lo que puede cambiar

El Ministerio de Salud publicó el 22 de julio de 2026 un proyecto de resolución, "Por la cual se establecen las disposiciones aplicables a la historia clínica y sus modalidades". **Al 13 de octubre de 2026 no se encontró expedida.**

| Tema | Qué dice el proyecto | Fuente |
|---|---|---|
| Normas que deroga | La Resolución 1995 de 1999 y la 839 de 2017, completas | Memoria justificativa del Ministerio |
| A quién aplica | A todos los prestadores, personas naturales incluidas, y también a "los proveedores y operadores de sistemas de información en salud" | Memoria justificativa |
| Plazo | 18 meses para implementar la historia clínica electrónica | Memoria justificativa |
| Historia electrónica | Autenticación, firma digital certificada, trazabilidad de cambios, cifrado, respaldo periódico e interoperabilidad | Prensa; falta leer el articulado |
| Derechos del paciente | Copia electrónica gratuita, saber quién consultó su información y corregir datos inexactos | Prensa; falta leer el articulado |

El diseño ya apunta en esa dirección: bitácora de accesos (HU-037), copia para el paciente (HU-046) y corrección de datos (HU-040). La firma es el punto abierto.

## 5. Preguntas para el abogado

| # | Pregunta | Por qué importa |
|---|---|---|
| 1 | ¿Qué texto exacto debe tener la autorización de tratamiento de datos y la autorización para usar IA? | HU-003 y HU-032 necesitan el texto definitivo |
| 2 | El alojamiento (Render, en Estados Unidos) y el proveedor de IA (Qwen, en Singapur o Estados Unidos) procesan los datos fuera de Colombia. ¿Basta la autorización del paciente y un contrato con cada uno, o hace falta algo más? | Condiciona el uso de datos reales (HU-027, HU-033). Ahora incluye la historia clínica del consultorio, no solo los documentos del paciente |
| 3 | ¿El consultorio debe inscribir sus bases de datos en el Registro Nacional de Bases de Datos? | Trámite previo a operar |
| 4 | ¿Por cuánto tiempo deben conservarse la bitácora y los documentos que sube el paciente? | RNF-06 y la regla de eliminación de HU-029 |
| 5 | Con la historia clínica dentro del sistema, ¿desde cuándo debe el consultorio enviar el Resumen Digital de Atención de cada consulta (Resolución 1888 de 2025)? | Si ya es exigible, el envío hay que construirlo antes de atender pacientes reales. Hoy no está en el alcance |
| 6 | ¿Un consultorio que solo atiende particulares debe reportar RIPS con la factura (Resolución 948 de 2026)? | Condiciona la factura electrónica cuando se retome |
| 7 | ¿El ingreso del médico con su usuario y contraseña basta como firma de la historia clínica electrónica, o hace falta firma digital certificada? | HU-044. El proyecto de resolución de 2026 menciona firma digital certificada |
| 8 | ¿Qué consentimientos informados necesita una consulta de medicina general, y deben quedar dentro del sistema? | Sección 4.3 |

Para enviar el Resumen Digital de Atención el consultorio necesita además su código de habilitación como prestador. Es un dato del consultorio real, que todavía no existe (S-11).

## 6. Normas que aplican a lo que quedó para después

| Tema | Norma | Estado |
|---|---|---|
| Envío del Resumen Digital de Atención | Resolución 1888 de 2025, modificada por la 1799 de 2026. Aplica a prestadores públicos y privados | Por confirmar (pregunta 5) |
| RIPS y factura de salud | Resolución 948 de 2026, expedida el 14 de mayo de 2026, que derogó la 2275 de 2023. Sus anexos técnicos se publican aparte | Por confirmar (pregunta 6) |

## 7. Corrección frente a la versión anterior

El README de la versión anterior citaba un decreto de 2024 sobre la validez de la historia clínica exclusivamente digital. No se encontró ninguna fuente que lo confirme, así que se retiró de este marco.

## Fuentes

- [Resolución 1995 de 1999 — Supersalud](https://normograma.supersalud.gov.co/compilacion/docs/resolucion_minsalud_r1995_99.htm)
- [Ley 2015 de 2020 — Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=105472)
- [Resolución 866 de 2021 — Supersalud](https://normograma.supersalud.gov.co/compilacion/docs/resolucion_minsaludps_0866_2021.htm)
- [Resolución 866 de 2021 — JEP](https://jurinfo.jep.gov.co/normograma/compilacion/docs/resolucion_minsaludps_0866_2021.htm)
- [Resolución 1888 de 2025](https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=190733&dt=S)
- [Resolución 1888 de 2025 — anexo técnico](https://normograma.com/documentospdf/PDF/R_MSPS_1888_2025_ANEXO.pdf)
- [Proyecto de resolución de historia clínica — memoria justificativa del 22 de julio de 2026](https://www.minsalud.gov.co/Normativa/anexosproyectos/ANEXO2MEMJUSTIFICATIVAHISTORIA%20CLINICA%2022%20JUL%2026_20260722151201.pdf)
- [Proyecto de resolución de historia clínica — La FM](https://www.lafm.com.co/sociedad/historia-clinica-salud-cambios-resolucion-ministerio-salud-criticas-gobierno-pacientes-privacidad-405964)
- [Resolución 948 de 2026 — resumen de Medifolios](https://medifolios.net/articulos/resolucion-2275.php)
- [Normatividad de interoperabilidad — Ministerio de Salud](https://www.minsalud.gov.co/ihce/Paginas/Normatividad.aspx)
