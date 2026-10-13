# Marco normativo

**Fase del ciclo de vida:** Planificación
**Versión:** 2.0 · 12 de octubre de 2026

> Este documento es una lectura técnica de las normas para convertirlas en requisitos. **No es un concepto jurídico.** Los puntos de la sección 4 deben confirmarse con un abogado de salud digital antes de salir a producción.

---

## 1. Quién responde por los datos

Según la Ley 1581 de 2012, el **consultorio** es el responsable del tratamiento: decide para qué se usan los datos de sus pacientes. Quien construya y opere el sistema por cuenta del consultorio es el **encargado**. Esa relación debe quedar en un contrato de encargo antes de cargar datos reales.

Los datos de salud son **datos sensibles**. Solo se pueden tratar con autorización explícita del titular, y nadie puede condicionar un servicio a que entregue más datos de los necesarios.

## 2. Normas que aplican a este alcance

| Norma | Qué exige | Cómo lo cubre el producto |
|---|---|---|
| **Ley 1581 de 2012** — protección de datos personales | Autorización previa, expresa e informada (art. 9) | HU-003: no hay cuenta sin autorización; se guarda versión, fecha y hora |
| | Tratamiento especial de datos sensibles (arts. 5 y 6) | HU-032: autorización aparte para usar IA sobre los documentos |
| | Atender consultas en 10 días hábiles y reclamos en 15 (arts. 14 y 15) | HU-029: el paciente ve y elimina sus documentos. El canal de reclamos es un proceso del consultorio |
| | Medidas de seguridad para impedir acceso no autorizado | HU-027, HU-036, RNF-01 a RNF-05 |
| | Reglas para enviar datos a otro país (art. 26) | HU-033 y RNF-08: mínimo de datos y proveedor con acuerdo de tratamiento. Ver pregunta 2 |
| **Ley 23 de 1981** — ética médica | La historia clínica es reservada; un tercero solo la conoce con autorización del paciente o por mandato legal | HU-006, HU-036: solo el médico y el propio paciente acceden |
| **Resolución 1995 de 1999** y **Resolución 839 de 2017** — manejo y conservación de la historia clínica | Integralidad, secuencialidad, disponibilidad y custodia de la historia que lleva el prestador; conservación mínima de 15 años | Aplica a la nota clínica del médico, que queda para después. Los documentos que sube el paciente son antecedentes, no la historia del consultorio |
| **Ley 2015 de 2020** — historia clínica electrónica interoperable | El titular es dueño de su historia; el prestador conserva la custodia en sus propios sistemas; el acceso de terceros requiere consentimiento | HU-037: trazabilidad de accesos. HU-032: consentimiento |
| **Resolución 866 de 2021** — datos clínicos relevantes | Define cuatro grupos de datos: identificación del usuario, contacto con el servicio, tecnologías en salud (procedimientos, medicamentos) y resultados (diagnósticos, incapacidades) | HU-035: el resumen del asistente se organiza con esos grupos como guía |

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

## 4. Preguntas para el abogado

| # | Pregunta | Por qué importa |
|---|---|---|
| 1 | ¿Qué texto exacto debe tener la autorización de tratamiento de datos y la autorización para usar IA? | HU-003 y HU-032 necesitan el texto definitivo |
| 2 | Si el proveedor de IA procesa los datos fuera de Colombia, ¿basta la autorización del paciente y un contrato, o hace falta algo más? | Define qué proveedor se puede usar (HU-033) |
| 3 | ¿El consultorio debe inscribir sus bases de datos en el Registro Nacional de Bases de Datos? | Trámite previo a operar |
| 4 | ¿Por cuánto tiempo deben conservarse la bitácora y los documentos que sube el paciente? | RNF-06 y la regla de eliminación de HU-029 |
| 5 | ¿La Resolución 1888 de 2025 obliga a un consultorio privado a reportar el Resumen Digital de Atención (RDA)? | Si aplica, entra al alcance junto con la nota clínica |
| 6 | ¿Un consultorio que solo atiende particulares debe reportar RIPS con la factura (Resolución 948 de 2026)? | Condiciona la factura electrónica cuando se retome |

## 5. Normas que aplican a lo que quedó para después

| Tema | Norma | Estado |
|---|---|---|
| Resumen Digital de Atención | Resolución 1888 de 2025, modificada por la 1799 de 2026. Aplica a prestadores públicos y privados; el plazo de seis meses corrió desde el 15 de octubre de 2025 | Por confirmar (pregunta 5) |
| RIPS y factura de salud | Resolución 948 de 2026, expedida el 14 de mayo de 2026, que derogó la 2275 de 2023 | Por confirmar (pregunta 6) |
| Actualización de la norma de historia clínica | Proyecto de resolución publicado por el Ministerio de Salud en julio de 2026 para reemplazar la Resolución 1995 de 1999 | En trámite; revisar antes de levantar la nota clínica |

## 6. Corrección frente a la versión anterior

El README de la versión anterior citaba un decreto de 2024 sobre la validez de la historia clínica exclusivamente digital. No se encontró ninguna fuente que lo confirme, así que se retiró de este marco.

## Fuentes

- [Ley 2015 de 2020 — Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=105472)
- [Resolución 866 de 2021](https://jurinfo.jep.gov.co/normograma/compilacion/docs/resolucion_minsaludps_0866_2021.htm)
- [Resolución 1888 de 2025](https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=190733&dt=S)
- [Resolución 948 de 2026 — resumen de Medifolios](https://medifolios.net/articulos/resolucion-2275.php)
- [Normatividad de interoperabilidad — Ministerio de Salud](https://www.minsalud.gov.co/ihce/Paginas/Normatividad.aspx)
