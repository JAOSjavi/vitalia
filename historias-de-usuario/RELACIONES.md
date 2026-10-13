# Relación entre historias de usuario

Cada historia declara de cuáles **depende** (no puede construirse antes) y a cuáles **habilita**. Este orden es técnico, no de prioridad.

## Orden de construcción

| Etapa | Qué se construye | Historias |
|---|---|---|
| 1. Cimientos | Roles, permisos por fila, bitácora y almacenamiento privado | HU-006, HU-036, HU-037, HU-027 |
| 2. Identidad | Cuenta del médico, registro del paciente, autorización, ingreso | HU-001, HU-002, HU-003, HU-004, HU-005, HU-007 |
| 3. Calendario | Horario, tipos de cita, bloqueos y cálculo de espacios | HU-008, HU-010, HU-009, HU-011 |
| 4. Citas y panel | Agenda, pacientes, citas de ambas partes | HU-012, HU-013, HU-020, HU-014, HU-015, HU-021, HU-023, HU-024, HU-016, HU-017, HU-022, HU-025, HU-018, HU-019, HU-026 |
| 5. Documentos | Carga, visor y lectura | HU-028, HU-029, HU-030, HU-031 |
| 6. Asistente | Autorización, aislamiento, preguntas y resumen | HU-032, HU-033, HU-034, HU-035 |
| 7. Tratamientos | Registro por el médico y consulta del paciente | HU-038, HU-039 |

Las etapas 4 y 5 pueden avanzar en paralelo: los documentos solo necesitan el ingreso y el almacenamiento. La etapa 7 solo necesita la ficha del paciente, así que puede adelantarse a la 5 y la 6.

## Las que más desbloquean

| Historia | Habilita a |
|---|---|
| **HU-006** Roles y permisos de médico y paciente | 6 historias: HU-001, HU-002, HU-023, HU-027, HU-036, HU-037 |
| **HU-004** Ingreso con contraseña | 5 historias: HU-005, HU-007, HU-012, HU-021, HU-028 |
| **HU-011** Cálculo de espacios libres sin choques | 4 historias: HU-012, HU-016, HU-017, HU-021 |
| **HU-012** Agendar una cita como paciente | 4 historias: HU-013, HU-014, HU-015, HU-019 |
| **HU-021** Panel de inicio con la agenda del día | 4 historias: HU-017, HU-018, HU-022, HU-026 |
| **HU-001** Configuración inicial del consultorio | 3 historias: HU-004, HU-008, HU-010 |
| **HU-023** Lista y búsqueda de pacientes | 3 historias: HU-016, HU-024, HU-025 |
| **HU-025** Ficha del paciente | 3 historias: HU-030, HU-034, HU-038 |
| **HU-028** Subir mis historias clínicas | 3 historias: HU-029, HU-030, HU-031 |

## Cadena completa

| Historia | Épica | Depende de | Habilita a |
|---|---|---|---|
| **HU-001** Configuración inicial del consultorio | E1 | HU-006 | HU-004, HU-008, HU-010 |
| **HU-002** Registro de paciente | E1 | HU-006 | HU-003, HU-004 |
| **HU-003** Autorización de tratamiento de datos | E1 | HU-002 | HU-024, HU-032 |
| **HU-004** Ingreso con contraseña | E1 | HU-001, HU-002 | HU-005, HU-007, HU-012, HU-021, HU-028 |
| **HU-005** Recuperación de contraseña | E1 | HU-004 | — |
| **HU-006** Roles y permisos de médico y paciente | E1 | — | HU-001, HU-002, HU-023, HU-027, HU-036, HU-037 |
| **HU-007** Cierre de sesión y expiración | E1 | HU-004 | — |
| **HU-008** Horario semanal de atención | E2 | HU-001 | HU-009, HU-011 |
| **HU-009** Bloqueos y ausencias | E2 | HU-008 | HU-011, HU-022 |
| **HU-010** Tipos de cita y duración | E2 | HU-001 | HU-011 |
| **HU-011** Cálculo de espacios libres sin choques | E2 | HU-008, HU-009, HU-010 | HU-012, HU-016, HU-017, HU-021 |
| **HU-012** Agendar una cita como paciente | E3 | HU-004, HU-011 | HU-013, HU-014, HU-015, HU-019 |
| **HU-013** Consultar mis citas | E3 | HU-012 | HU-020 |
| **HU-014** Mover mi cita | E3 | HU-012 | — |
| **HU-015** Cancelar mi cita | E3 | HU-012 | — |
| **HU-016** Crear una cita para un paciente | E3 | HU-011, HU-023 | — |
| **HU-017** Mover o cancelar una cita como médico | E3 | HU-011, HU-021 | — |
| **HU-018** Registrar asistencia o inasistencia | E3 | HU-021 | — |
| **HU-019** Aviso por correo de cambios en la cita | E3 | HU-012 | — |
| **HU-020** Inicio del paciente | E3 | HU-013 | — |
| **HU-021** Panel de inicio con la agenda del día | E4 | HU-004, HU-011 | HU-017, HU-018, HU-022, HU-026 |
| **HU-022** Vista de calendario semanal y mensual | E4 | HU-009, HU-021 | — |
| **HU-023** Lista y búsqueda de pacientes | E4 | HU-006 | HU-016, HU-024, HU-025 |
| **HU-024** Registrar un paciente desde el panel | E4 | HU-003, HU-023 | — |
| **HU-025** Ficha del paciente | E4 | HU-023 | HU-030, HU-034, HU-038 |
| **HU-026** Botón de cobro sin función | E4 | HU-021 | — |
| **HU-027** Almacenamiento privado con enlace temporal | E5 | HU-006 | HU-028 |
| **HU-028** Subir mis historias clínicas | E5 | HU-004, HU-027 | HU-029, HU-030, HU-031 |
| **HU-029** Ver y eliminar mis documentos | E5 | HU-028 | — |
| **HU-030** Consultar los documentos del paciente en un visor | E5 | HU-025, HU-028 | — |
| **HU-031** Lectura del documento para la IA | E5 | HU-028 | HU-033 |
| **HU-032** Autorización del paciente para usar IA | E6 | HU-003 | HU-033 |
| **HU-033** IA solo desde el servidor y aislada por paciente | E6 | HU-031, HU-032 | HU-034 |
| **HU-034** Preguntar al asistente sobre los documentos de un paciente | E6 | HU-025, HU-033 | HU-035 |
| **HU-035** Resumen del paciente con un clic | E6 | HU-034 | — |
| **HU-036** Permisos por fila en la base de datos | E7 | HU-006 | — |
| **HU-037** Bitácora de auditoría | E7 | HU-006 | — |
| **HU-038** Registrar el tratamiento de un paciente | E8 | HU-025 | HU-039 |
| **HU-039** Ver mis tratamientos | E8 | HU-038 | — |

## Cadenas críticas

**1. El paciente consigue una cita**

```
HU-006 roles → HU-001 consultorio → HU-008 horario + HU-010 tipos de cita
       → HU-011 espacios libres → HU-012 agendar
```

**2. El médico atiende con su panel**

```
HU-004 ingreso → HU-021 agenda del día → HU-023 pacientes → HU-025 ficha
```

**3. El asistente responde sobre los antecedentes**

```
HU-027 almacenamiento → HU-028 subir → HU-031 lectura
       → HU-032 autorización → HU-033 aislamiento → HU-034 preguntar → HU-035 resumen
```

La tercera cadena es la más larga y la de mayor incertidumbre técnica: la calidad de la lectura (HU-031) condiciona todo lo que sigue. Conviene probarla temprano, con documentos inventados o anonimizados que se parezcan a los reales.

---

[Alcance y flujo](../planificacion/01-alcance-y-flujo.md) · [Requisitos](../planificacion/02-requisitos.md)
