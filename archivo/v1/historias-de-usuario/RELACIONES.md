# Relación entre historias de usuario

Cada historia declara de qué otras **depende** (no puede construirse antes) y a cuáles **habilita**.
Este orden es técnico, no de prioridad: una historia Must puede depender de una Should.

## Cimientos — no dependen de nada

Son las que se pueden empezar el primer día, y casi todo lo demás cuelga de ellas.

- **HU-001** Registro de paciente *(E1)*
- **HU-005** Roles y permisos resueltos en base de datos *(E1)*
- **HU-008** Verificación de disponibilidad en tiempo real *(E2)*
- **HU-022** Catálogo de medicamentos *(E5)*
- **HU-036** Documentos servidos con URL firmada *(E11)*
- **HU-063** Modo accesible *(E10)*

## Las que más desbloquean

| Historia | Habilita a |
|---|---|
| **HU-033** Envío por WhatsApp con plantillas aprobadas | 7 historias: HU-043, HU-038, HU-040, HU-041, HU-042, HU-045, HU-046 |
| **HU-015** Registrar la nota clínica de la consulta | 6 historias: HU-017, HU-021, HU-024, HU-025, HU-062, HU-071 |
| **HU-001** Registro de paciente | 5 historias: HU-002, HU-003, HU-004, HU-037, HU-032 |
| **HU-008** Verificación de disponibilidad en tiempo real | 5 historias: HU-007, HU-009, HU-014, HU-038, HU-056 |
| **HU-007** Agendar una cita desde la aplicación | 5 historias: HU-009, HU-010, HU-011, HU-012, HU-030 |
| **HU-005** Roles y permisos resueltos en base de datos | 5 historias: HU-014, HU-017, HU-020, HU-035, HU-055 |
| **HU-027** Ver «Mi plan de tratamiento» | 5 historias: HU-028, HU-051, HU-064, HU-065, HU-068 |
| **HU-036** Documentos servidos con URL firmada | 4 historias: HU-012, HU-016, HU-018, HU-019 |

## Cadena completa

| Historia | Depende de | Habilita a |
|---|---|---|
| **HU-001** Registro de paciente | — | HU-002, HU-003, HU-004, HU-037, HU-032 |
| **HU-002** Ingreso con contraseña | HU-001 | HU-004, HU-006, HU-007 |
| **HU-003** Ingreso con código por SMS (OTP) | HU-001 | — |
| **HU-004** Recuperación de contraseña | HU-001, HU-002 | — |
| **HU-005** Roles y permisos resueltos en base de datos | — | HU-014, HU-017, HU-020, HU-035, HU-055 |
| **HU-006** Cierre de sesión y expiración del token | HU-002 | — |
| **HU-007** Agendar una cita desde la aplicación | HU-002, HU-008 | HU-009, HU-010, HU-011, HU-012, HU-030 |
| **HU-008** Verificación de disponibilidad en tiempo real | — | HU-007, HU-009, HU-014, HU-038, HU-056 |
| **HU-009** Reagendar una cita | HU-007, HU-008 | HU-040 |
| **HU-010** Cancelar una cita | HU-007 | HU-040 |
| **HU-011** Consultar mis citas pasadas y futuras | HU-007 | HU-042 |
| **HU-012** Adjuntar un documento al agendar | HU-007, HU-036 | — |
| **HU-013** Registrar asistencia o inasistencia | HU-014 | HU-015, HU-058, HU-066 |
| **HU-014** Agenda del día del profesional | HU-008, HU-005 | HU-013 |
| **HU-015** Registrar la nota clínica de la consulta | HU-013 | HU-017, HU-021, HU-024, HU-025, HU-062, HU-071 |
| **HU-016** Cargar documentos clínicos del paciente | HU-036 | HU-018, HU-019 |
| **HU-017** Consultar la historia clínica del paciente | HU-015, HU-005 | HU-060 |
| **HU-018** Visor de PDF integrado | HU-016, HU-036 | — |
| **HU-019** Ver mis documentos como paciente | HU-016, HU-036 | — |
| **HU-020** Bitácora de auditoría de accesos | HU-005 | HU-070 |
| **HU-021** Registrar medicamentos del plan | HU-022, HU-015 | HU-023, HU-026, HU-027, HU-029 |
| **HU-022** Catálogo de medicamentos | — | HU-021, HU-023 |
| **HU-023** Aviso de interacciones básicas | HU-021, HU-022 | — |
| **HU-024** Registrar cuidados e instrucciones | HU-015 | HU-027, HU-031 |
| **HU-025** Registrar próximos pasos | HU-015 | HU-027 |
| **HU-026** Fecha de fin automática del tratamiento | HU-021 | HU-029 |
| **HU-027** Ver «Mi plan de tratamiento» | HU-021, HU-024, HU-025 | HU-028, HU-051, HU-064, HU-065, HU-068 |
| **HU-028** Historial de planes anteriores | HU-027 | — |
| **HU-029** Programación automática de recordatorios de medicamento | HU-021, HU-026 | HU-044, HU-045, HU-068 |
| **HU-030** Recordatorio de cita 24 horas y 1 hora antes | HU-007 | HU-041 |
| **HU-031** Recordatorio de cuidados en fecha específica | HU-024 | — |
| **HU-032** Configurar canal preferido de aviso | HU-001 | HU-033, HU-034, HU-054 |
| **HU-033** Envío por WhatsApp con plantillas aprobadas | HU-032 | HU-043, HU-038, HU-040, HU-041, HU-042, HU-045, HU-046 |
| **HU-034** Envío por SMS | HU-032 | HU-046 |
| **HU-035** Seguridad a nivel de fila en datos de salud | HU-005 | HU-057 |
| **HU-036** Documentos servidos con URL firmada | — | HU-012, HU-016, HU-018, HU-019 |
| **HU-037** Aceptación de la política de tratamiento de datos | HU-001 | HU-039, HU-059, HU-067, HU-074 |
| **HU-038** Agendar una cita por WhatsApp | HU-008, HU-033, HU-043 | HU-039 |
| **HU-039** Registrar paciente nuevo desde WhatsApp | HU-038, HU-037 | — |
| **HU-040** Cancelar o reagendar respondiendo el mensaje | HU-033, HU-009, HU-010 | — |
| **HU-041** Confirmar asistencia el día anterior | HU-030, HU-033 | — |
| **HU-042** Consultar «mi próxima cita» por WhatsApp | HU-011, HU-033 | — |
| **HU-043** Cumplimiento de plantillas y ventana de 24 horas | HU-033 | HU-038 |
| **HU-044** Marcar un recordatorio como cumplido en la app | HU-029 | HU-047 |
| **HU-045** Confirmar la toma desde WhatsApp | HU-029, HU-033 | HU-047 |
| **HU-046** Reintento por canal alterno | HU-033, HU-034 | — |
| **HU-047** Cálculo del indicador de adherencia | HU-044, HU-045 | HU-048, HU-049, HU-050, HU-058 |
| **HU-048** Panel de adherencia del médico | HU-047 | HU-049 |
| **HU-049** Alerta automática por incumplimiento | HU-047, HU-048 | — |
| **HU-050** Ver mi propia adherencia | HU-047 | — |
| **HU-051** Reportar un síntoma o una duda | HU-027 | HU-052, HU-053 |
| **HU-052** Responder o derivar a una cita de control | HU-051 | HU-054 |
| **HU-053** Aviso explícito de que el canal no es para urgencias | HU-051 | — |
| **HU-054** Notificación de respuesta del médico | HU-052, HU-032 | — |
| **HU-055** Gestionar profesionales | HU-005 | HU-056, HU-057 |
| **HU-056** Gestionar horarios de atención | HU-055, HU-008 | — |
| **HU-057** Aislamiento de información entre sedes | HU-055, HU-035 | — |
| **HU-058** Reportes de operación | HU-013, HU-047 | — |
| **HU-059** Consentimiento del paciente para el uso de IA | HU-037 | HU-061, HU-060 |
| **HU-060** Asistente clínico sobre la historia del paciente | HU-017, HU-059, HU-061 | — |
| **HU-061** Intermediación de la IA a través de backend propio | HU-059 | HU-060 |
| **HU-062** Contenido educativo curado | HU-015 | — |
| **HU-063** Modo accesible | — | — |
| **HU-064** Lectura en voz alta | HU-027 | — |
| **HU-065** Exportar el plan de tratamiento en PDF | HU-027 | — |
| **HU-066** Encuesta de satisfacción post-consulta | HU-013 | — |
| **HU-067** Autorizar a un cuidador | HU-037 | HU-068, HU-069 |
| **HU-068** Vista del cuidador | HU-067, HU-027, HU-029 | — |
| **HU-069** Revocar el acceso de un cuidador | HU-067 | — |
| **HU-070** Consultar quién ha accedido a mi historia clínica | HU-020 | — |
| **HU-071** Generar el Resumen Digital de Atención (RDA) | HU-015 | HU-072 |
| **HU-072** Intercambiar el RDA con la plataforma nacional | HU-071, HU-074 | HU-073 |
| **HU-073** Registro de eventos de interoperabilidad | HU-072 | — |
| **HU-074** Consentimiento para compartir el resumen con otras instituciones | HU-037 | HU-072 |

## Cadenas críticas del producto

Tres recorridos donde el orden importa de verdad:

**1. El paciente consigue una cita**

```
HU-001 registro → HU-002 ingreso → HU-008 disponibilidad → HU-007 agendar → HU-030 recordatorio
```

**2. El tratamiento llega al paciente** (el diferencial del producto)

```
HU-013 asistencia → HU-015 nota clínica → HU-022 catálogo → HU-021 medicamentos
       → HU-026 fecha de fin → HU-029 recordatorios → HU-027 «Mi plan»
```

**3. La adherencia se vuelve medible** (lo que se vende)

```
HU-029 recordatorios → HU-044/HU-045 confirmar → HU-047 indicador
       → HU-048 panel del médico → HU-049 alerta por incumplimiento
```

La tercera cadena es la que justifica el producto frente a un agendador común, y toda ella vive en la Fase 2: hasta que HU-047 exista, la adherencia no se puede demostrar con datos.
