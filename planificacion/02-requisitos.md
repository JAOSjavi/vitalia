# Requisitos

**Fase del ciclo de vida:** Planificación
**Versión:** 2.0 · 12 de octubre de 2026

Cada requisito funcional (RF) indica la historia que lo desarrolla. Cada requisito no funcional (RNF) indica de qué norma o necesidad sale.

---

## 1. Requisitos funcionales

### E1 — Cuentas e ingreso

| ID | El sistema debe… | Historia |
|---|---|---|
| RF-01 | Permitir que un paciente cree su cuenta con nombre, documento, fecha de nacimiento, celular, correo y una contraseña propia | HU-002 |
| RF-02 | Registrar la autorización de tratamiento de datos personales y de salud al crear la cuenta, con versión del texto, fecha y hora | HU-003 |
| RF-03 | Autenticar con correo y contraseña. El documento de identidad nunca sirve como clave | HU-004 |
| RF-04 | Permitir recuperar la contraseña con un enlace de un solo uso enviado al correo | HU-005 |
| RF-05 | Permitir cerrar la sesión y cerrarla sola por inactividad | HU-007 |
| RF-06 | Permitir que el médico cree su cuenta en la puesta en marcha y registre los datos del consultorio | HU-001 |
| RF-07 | Guardar los roles de médico y paciente en la base de datos y resolver los permisos desde ahí | HU-006 |

### E2 — Calendario de disponibilidad

| ID | El sistema debe… | Historia |
|---|---|---|
| RF-08 | Permitir al médico definir su horario semanal de atención por franjas | HU-008 |
| RF-09 | Permitir al médico bloquear días u horas en que no atiende | HU-009 |
| RF-10 | Permitir al médico definir tipos de cita con nombre y duración | HU-010 |
| RF-11 | Calcular los espacios libres a partir del horario, los bloqueos y las citas, e impedir dos citas en el mismo espacio | HU-011 |

### E3 — Citas

| ID | El sistema debe… | Historia |
|---|---|---|
| RF-12 | Permitir al paciente agendar una cita eligiendo tipo, día y un espacio libre | HU-012 |
| RF-13 | Mostrar al paciente sus citas próximas y pasadas con su estado | HU-013 |
| RF-14 | Permitir al paciente mover o cancelar su cita dentro de la anticipación mínima | HU-014, HU-015 |
| RF-15 | Permitir al médico crear una cita a nombre de un paciente | HU-016 |
| RF-16 | Permitir al médico mover o cancelar cualquier cita futura, con motivo | HU-017 |
| RF-17 | Permitir al médico registrar si el paciente asistió | HU-018 |
| RF-18 | Avisar por correo al paciente cuando una cita se crea, se mueve o se cancela | HU-019 |
| RF-19 | Mostrar al paciente, al entrar, su próxima cita y los accesos principales | HU-020 |

### E4 — Panel del médico

| ID | El sistema debe… | Historia |
|---|---|---|
| RF-20 | Mostrar al médico, al entrar, sus citas del día en orden | HU-021 |
| RF-21 | Mostrar la agenda en vista semanal y mensual con citas, bloqueos y tiempo libre | HU-022 |
| RF-22 | Permitir al médico listar y buscar pacientes por nombre o documento | HU-023 |
| RF-23 | Permitir al médico registrar un paciente, que luego activa su propia cuenta | HU-024 |
| RF-24 | Reunir en una ficha los datos, las citas y los documentos de un paciente | HU-025 |
| RF-25 | Mostrar un botón de cobro en el panel, sin función por ahora | HU-026 |

### E5 — Historias clínicas del paciente

| ID | El sistema debe… | Historia |
|---|---|---|
| RF-26 | Permitir al paciente subir historias clínicas y exámenes en PDF, JPG o PNG | HU-028 |
| RF-27 | Permitir al paciente ver y eliminar los documentos que subió | HU-029 |
| RF-28 | Permitir al médico leer los documentos del paciente en un visor, sin descargarlos | HU-030 |
| RF-29 | Guardar los documentos en almacenamiento privado y entregarlos solo con enlace firmado temporal | HU-027 |
| RF-30 | Leer el texto de cada documento al subirlo e indicar si quedó legible | HU-031 |

### E6 — Asistente de IA

| ID | El sistema debe… | Historia |
|---|---|---|
| RF-31 | Exigir la autorización expresa y revocable del paciente antes de usar IA sobre sus documentos | HU-032 |
| RF-32 | Permitir al médico hacer preguntas en lenguaje natural sobre los documentos de un paciente | HU-034 |
| RF-33 | Generar un resumen de diagnósticos, procedimientos, tratamientos, alergias y estado actual del paciente | HU-035 |
| RF-34 | Indicar en cada respuesta el documento y la página de origen, y decir cuándo un dato no aparece | HU-034, HU-035 |
| RF-35 | Hacer toda consulta a la IA desde el servidor y solo con los documentos del paciente consultado | HU-033 |

### E7 — Seguridad base

| ID | El sistema debe… | Historia |
|---|---|---|
| RF-36 | Limitar en la base de datos lo que cada usuario puede leer y escribir | HU-036 |
| RF-37 | Registrar en una bitácora los accesos a fichas y documentos, las consultas a la IA y los cambios de citas | HU-037 |

### E8 — Tratamientos

| ID | El sistema debe… | Historia |
|---|---|---|
| RF-38 | Permitir al médico registrar el tratamiento de un paciente: motivo, medicamentos con dosis, frecuencia, duración y forma de tomarlos, e indicaciones | HU-038 |
| RF-39 | Mostrar al paciente su último tratamiento y los anteriores, con la forma de tomar cada medicamento | HU-039 |

---

## 2. Requisitos no funcionales

| ID | Requisito | De dónde sale |
|---|---|---|
| RNF-01 | Toda tabla con datos de salud tiene una política de acceso por usuario en la base de datos. Ninguna queda abierta | Ley 1581 (seguridad); ISO 27001 A.5.15 y A.8.3 |
| RNF-02 | Ninguna clave de un proveedor externo viaja en el navegador. La IA y el correo se llaman desde el servidor | ISO 27001 A.5.17 y A.8.24 |
| RNF-03 | Los documentos se guardan cifrados y se entregan con enlace firmado de máximo 15 minutos | Ley 1581 (seguridad); ISO 27001 A.8.24 |
| RNF-04 | Las contraseñas se guardan con un algoritmo de hash resistente (argon2 o bcrypt) y sal única | ISO 27001 A.8.5 |
| RNF-05 | Todo el tráfico viaja por TLS 1.2 o superior | ISO 27001 A.8.24 |
| RNF-06 | La bitácora es de solo inserción y se conserva por el término legal aplicable | Resolución 1995 de 1999; ISO 27001 A.8.15 |
| RNF-07 | El tratamiento de datos cumple la Ley 1581: autorización previa, expresa e informada; finalidad declarada; atención de consultas y reclamos; eliminación a solicitud del titular | Ley 1581 de 2012 |
| RNF-08 | A la IA se envía solo lo necesario para responder, sin número de documento, celular ni correo del paciente, y con un proveedor que tenga acuerdo de tratamiento de datos | Ley 1581 (datos sensibles y envío al exterior); ISO 27001 A.5.34 y A.8.11 |
| RNF-09 | El asistente solo resume lo que está en los documentos. No diagnostica ni recomienda tratamiento | Seguridad del paciente |
| RNF-10 | Las pantallas de consulta responden en menos de 2 segundos con conexión móvil 4G. El asistente muestra la respuesta a medida que la escribe | Experiencia de uso |
| RNF-11 | La interfaz cumple WCAG 2.1 nivel AA en contraste, tamaño de los botones y texto ampliable | Pacientes adultos mayores |
| RNF-12 | Hay respaldo diario de la base de datos y de los documentos, con una restauración probada cada trimestre | ISO 27001 A.8.13 |
| RNF-13 | La disponibilidad mensual es de 99,5 % en horario de atención | Operación del consultorio |
| RNF-14 | La aplicación funciona en navegadores actuales y en celulares Android de gama baja | Población objetivo |

---

## 3. Trazabilidad

| Épica | Requisitos funcionales | Historias |
|---|---|---|
| E1 | RF-01 a RF-07 | HU-001 a HU-007 |
| E2 | RF-08 a RF-11 | HU-008 a HU-011 |
| E3 | RF-12 a RF-19 | HU-012 a HU-020 |
| E4 | RF-20 a RF-25 | HU-021 a HU-026 |
| E5 | RF-26 a RF-30 | HU-027 a HU-031 |
| E6 | RF-31 a RF-35 | HU-032 a HU-035 |
| E7 | RF-36 y RF-37 | HU-036 y HU-037 |
| E8 | RF-38 y RF-39 | HU-038 y HU-039 |

Los requisitos no funcionales aplican a todas las épicas. Los que tienen historia propia son RNF-01 (HU-036), RNF-03 (HU-027), RNF-06 (HU-037) y RNF-08 (HU-033).

## 4. Glosario

| Término | Significado |
|---|---|
| Espacio libre | Tramo de la agenda que se puede ofrecer para una cita |
| Bloqueo | Tiempo que el médico marca como no disponible |
| Enlace firmado | Dirección temporal que da acceso a un archivo por unos minutos |
| Documento legible | Documento del que el sistema pudo leer el texto |
| Bitácora | Registro de quién hizo qué y cuándo; no se puede modificar |
| MoSCoW | Escala de prioridad: Must (obligatorio), Should (debería), Could (podría) |
