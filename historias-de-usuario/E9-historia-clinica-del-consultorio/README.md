# E9 — Historia clínica del consultorio

**Objetivo:** que el médico deje dentro del sistema la historia clínica de cada atención, con lo mínimo que exige la norma, mientras tiene a un lado el asistente con el resumen del paciente.

| Dato | Valor |
|---|---|
| Historias | 6 |
| Puntos | 27 |
| Requisitos | RF-41 a RF-46 y RNF-15 |

## Historias de esta épica

| ID | Historia | Rol | Prioridad | Puntos |
|---|---|---|---|---|
| HU-041 | [Datos de identificación de la historia clínica](HU-041-datos-de-identificacion-de-la-historia-clinica.md) | Paciente, Médico | Must | 3 |
| HU-042 | [Pantalla de atención con el asistente al lado](HU-042-pantalla-de-atencion-con-el-asistente-al-lado.md) | Médico | Must | 5 |
| HU-043 | [Registrar la consulta en la historia clínica](HU-043-registrar-la-consulta-en-la-historia-clinica.md) | Médico | Must | 8 |
| HU-044 | [Cerrar y firmar la atención](HU-044-cerrar-y-firmar-la-atencion.md) | Médico | Must | 5 |
| HU-045 | [Consultar la historia clínica de un paciente](HU-045-consultar-la-historia-clinica-de-un-paciente.md) | Médico | Must | 3 |
| HU-046 | [Copia de la historia clínica para el paciente](HU-046-copia-de-la-historia-clinica-para-el-paciente.md) | Médico | Should | 3 |

## Qué entra y qué no

| Entra | Queda para después |
|---|---|
| Los datos de identificación que pide la Resolución 1995 de 1999 | Los datos de la Resolución 866 que la 1995 no exige: nacionalidad, identidad de género, pertenencia étnica, discapacidad y zona |
| El registro de la consulta con el contenido mínimo y el diagnóstico en CIE-10 | Envío del Resumen Digital de Atención al Ministerio |
| Cierre con autor, fecha y hora; lo cerrado no se modifica | Firma digital certificada, si el abogado dice que hace falta |
| Notas aclaratorias para corregir | Consentimientos informados de procedimientos |
| Copia en PDF para el paciente | Que el paciente vea su historia clínica desde su cuenta |

> El contenido de cada campo y el artículo del que sale están en la sección 4 del [marco normativo](../../planificacion/03-marco-normativo.md). El asistente ayuda a leer los antecedentes, pero **no escribe la historia clínica**: lo que queda registrado lo escribe el médico.

---

[Alcance y flujo](../../planificacion/01-alcance-y-flujo.md) · [Requisitos](../../planificacion/02-requisitos.md) · [Mapa de relaciones](../RELACIONES.md)
