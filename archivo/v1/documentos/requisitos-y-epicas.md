# Vitalia Salud — Levantamiento de Requisitos y Épicas

**Proyecto:** Aplicación de salud para consultorios y clínicas en Colombia (citas, historia clínica, plan de tratamiento y adherencia)
**Documento:** 01 — Requisitos funcionales, no funcionales y épicas
**Versión:** 1.0 · 15 de septiembre de 2026
**Fuente:** *PROMPT MAESTRO — App de Salud (Citas, Historia Clínica y Adherencia al Tratamiento)*

---

## 1. Contexto y visión del producto

**Problema.** El software existente para consultorios (Alegra, Dentalink, Okvet, agendadores genéricos) resuelve la agenda y archiva documentos, pero abandona al paciente en el momento en que sale del consultorio. El resultado clínico depende de que el paciente recuerde, entienda y cumpla un plan de tratamiento que quedó escrito en un papel o enterrado en un PDF.

**Visión.** Cubrir el ciclo completo del paciente —agendar cita → consulta con historia clínica digital → plan de tratamiento claro → recordatorios activos por WhatsApp/SMS → seguimiento de adherencia— acompañando activamente al paciente después de la consulta.

**Diferencial.** No es un agendador con recordatorios: es un sistema de adherencia al tratamiento que además agenda. WhatsApp es canal de primera clase (no un extra), porque la población objetivo incluye adultos mayores y pacientes con baja alfabetización digital.

**Población objetivo.** Consultorios independientes y clínicas pequeñas/medianas en Colombia.

---

## 2. Alcance

### 2.1 Dentro del alcance

| # | Bloque | Fase |
|---|--------|------|
| 1 | Autenticación real con roles en base de datos | 1 |
| 2 | Agenda de citas con disponibilidad en tiempo real | 1 |
| 3 | Historia clínica digital con documentos y URLs firmadas | 1 |
| 4 | Plan de tratamiento (medicamentos + cuidados + próximos pasos) | 1 |
| 5 | Recordatorios de cita y de medicamento por WhatsApp/SMS | 1 |
| 6 | Agendamiento conversacional completo por WhatsApp | 2 |
| 7 | Confirmación de adherencia y panel para el médico | 2 |
| 8 | Alertas por incumplimiento de tratamiento | 2 |
| 9 | Multi-sede, panel administrativo y reportes | 3 |
| 10 | Cuidador/familiar con acceso limitado y consentimiento | 3 |
| 11 | Asistente de IA acotado y contenido educativo curado | 3 |
| 12 | Modo accesible avanzado y exportación a PDF | 3 |
| 13 | Interoperabilidad con el Resumen Digital de Atención (RDA) | 4 |

### 2.2 Fuera del alcance (versión 1.0)

- Facturación electrónica, RIPS y cobro a EPS.
- Telemedicina con video en vivo.
- Atención de urgencias o triage clínico automatizado.
- Ejecución de órdenes de laboratorio contra sistemas de terceros.
- Diagnóstico asistido por IA (la IA solo resume información ya registrada).
- Aplicación de escritorio nativa.

---

## 3. Actores del sistema

| Actor | Descripción | Acceso |
|-------|-------------|--------|
| **Paciente** | Usuario final. Agenda citas, consulta su historia y plan, recibe y confirma recordatorios. | Solo sus propios datos |
| **Médico** | Atiende citas, registra diagnóstico y plan de tratamiento, consulta historia clínica, ve adherencia. | Pacientes de las sedes donde atiende |
| **Cuidador / familiar** | Acompañante autorizado explícitamente por el paciente. | Solo recordatorios y plan de cuidado — **nunca** la historia clínica completa |
| **Administrador de clínica** | Gestiona doctores, horarios, sedes y consulta reportes. | Su clínica y sus sedes; sin acceso clínico |
| **Sistema** | Procesos automáticos: envío de recordatorios, cálculo de adherencia, detección de incumplimiento. | Según política de servicio |

---

## 4. Épicas

| ID | Épica | Objetivo de negocio | Fase |
|----|-------|---------------------|------|
| **E1** | Autenticación, cuentas y roles | Que cada quien entre con identidad propia y vea únicamente lo que le corresponde. | 1 |
| **E2** | Gestión de citas | Eliminar choques de horario y dar autonomía al paciente para agendar, mover y cancelar. | 1 |
| **E3** | Agendamiento y atención por WhatsApp | Que el paciente resuelva su cita sin descargar la app ni recordar contraseñas. | 2 |
| **E4** | Historia clínica y documentos | Historia clínica exclusivamente digital, trazable y con documentos protegidos. | 1 |
| **E5** | Plan de tratamiento post-consulta | Que el paciente entienda qué debe hacer, cuándo y hasta cuándo. **Núcleo diferencial.** | 1 |
| **E6** | Recordatorios multicanal y adherencia | Convertir el plan en acciones recordadas, confirmadas y medidas. **Núcleo diferencial.** | 1-2 |
| **E7** | Comunicación paciente–médico entre consultas | Resolver dudas de seguimiento sin saturar la agenda ni simular urgencias. | 2 |
| **E8** | Asistente de IA y contenido educativo | Ahorrar tiempo de lectura al médico y educar al paciente, sin exponer datos sensibles. | 3 |
| **E9** | Panel administrativo y multi-clínica | Operar varias sedes y medir el desempeño del consultorio. | 3 |
| **E10** | Accesibilidad y experiencia | Que un adulto mayor pueda usar el producto sin ayuda. | 3 |
| **E11** | Seguridad, privacidad y cumplimiento | Tratar la historia clínica como el dato sensible que es, según la ley colombiana. **Transversal.** | 1-4 |
| **E12** | Interoperabilidad (RDA) | Habilitar el producto para IPS formales. | 4 |

---

## 5. Requisitos funcionales

Nomenclatura: `RF-##` · Cada requisito indica la(s) épica(s) de la que se deriva y la fase en que se implementa.

### E1 — Autenticación, cuentas y roles

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-01** | El sistema debe permitir el registro de un paciente con nombre, documento, celular y correo, exigiendo contraseña propia. | E1 | 1 |
| **RF-02** | El sistema debe autenticar mediante contraseña o código de un solo uso (OTP) enviado al celular. **Queda prohibido** usar cédula y/o EPS como único factor de autenticación. | E1, E11 | 1 |
| **RF-03** | El sistema debe permitir la recuperación de contraseña por un canal verificado, con enlace o código de vigencia limitada. | E1 | 1 |
| **RF-04** | El sistema debe almacenar los roles (paciente, médico, administrador, cuidador) en base de datos y resolver los permisos a partir de ellos, sin usuarios privilegiados escritos en el código. | E1, E11 | 1 |
| **RF-05** | El sistema debe emitir tokens de sesión (JWT) con expiración y renovación, sin almacenar datos personales en texto plano en el dispositivo. | E1, E11 | 1 |
| **RF-06** | El sistema debe permitir cerrar sesión e invalidar el token en el servidor. | E1 | 1 |

### E2 — Gestión de citas

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-07** | El sistema debe permitir agendar una cita seleccionando tipo de cita, profesional, sede, fecha y hora. | E2 | 1 |
| **RF-08** | El sistema debe verificar la disponibilidad del profesional en tiempo real antes de confirmar, impidiendo dos citas en el mismo espacio. | E2 | 1 |
| **RF-09** | El sistema debe permitir editar y cancelar citas dentro de las reglas de anticipación definidas por la clínica. | E2 | 1 |
| **RF-10** | El sistema debe mostrar al paciente el historial de citas pasadas y futuras con su estado. | E2 | 1 |
| **RF-11** | El sistema debe permitir adjuntar documentos (orden médica, examen) al momento de agendar. | E2, E4 | 1 |
| **RF-12** | El sistema debe registrar la asistencia o inasistencia de cada cita. | E2, E9 | 1 |

### E3 — Agendamiento y atención por WhatsApp

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-13** | El sistema debe ofrecer un flujo conversacional por WhatsApp para agendar: tipo de cita → profesional → horario disponible → confirmación. | E3 | 2 |
| **RF-14** | El sistema debe registrar a un paciente nuevo desde WhatsApp con los datos mínimos cuando no exista en la base. | E3 | 2 |
| **RF-15** | El sistema debe permitir cancelar o reagendar respondiendo al mensaje de confirmación. | E3 | 2 |
| **RF-16** | El sistema debe solicitar confirmación de asistencia el día anterior por el mismo canal. | E3, E6 | 2 |
| **RF-17** | El sistema debe responder la consulta «mi próxima cita» por WhatsApp sin requerir ingreso a la app. | E3 | 2 |
| **RF-18** | El sistema debe usar exclusivamente plantillas pre-aprobadas por Meta para todo mensaje proactivo, y operar sobre la API oficial de WhatsApp Business Cloud o un BSP certificado. | E3, E11 | 2 |

### E4 — Historia clínica y documentos

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-19** | El sistema debe permitir asociar múltiples documentos a un paciente, clasificados por tipo (historia clínica, examen, receta, imagen diagnóstica). | E4 | 1 |
| **RF-20** | El sistema debe vincular cada cita con el documento clínico que se genere en ella. | E4 | 1 |
| **RF-21** | El sistema debe servir todo documento médico mediante URL firmada de vigencia temporal; ningún documento puede quedar en almacenamiento público. | E4, E11 | 1 |
| **RF-22** | El sistema debe ofrecer un visor de PDF integrado para el médico, sin descargar el archivo al dispositivo. | E4 | 1 |
| **RF-23** | El sistema debe permitir al médico registrar la nota clínica de la consulta (motivo, hallazgos, diagnóstico con código CIE-10). | E4 | 1 |

### E5 — Plan de tratamiento post-consulta

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-24** | El sistema debe permitir al médico registrar, al cerrar la cita, los medicamentos del plan con nombre, dosis, frecuencia y duración. | E5 | 1 |
| **RF-25** | El sistema debe ofrecer un catálogo de medicamentos (nombre genérico y presentación) en lugar de texto libre. | E5 | 1 |
| **RF-26** | El sistema debe advertir al médico sobre interacciones básicas cuando el paciente ya tenga otro medicamento activo. | E5 | 1 |
| **RF-27** | El sistema debe permitir registrar cuidados e instrucciones de procedimiento en texto, con imagen o video corto opcional. | E5 | 1 |
| **RF-28** | El sistema debe permitir registrar próximos pasos (próxima cita, examen pendiente). | E5 | 1 |
| **RF-29** | El sistema debe calcular automáticamente la fecha de fin del tratamiento a partir de la duración indicada, para dejar de enviar recordatorios al terminar. | E5, E6 | 1 |
| **RF-30** | El sistema debe mostrar al paciente su plan vigente en una sección propia y legible, no como un archivo adjunto. | E5 | 1 |
| **RF-31** | El sistema debe conservar el historial de planes de tratamiento de consultas anteriores. | E5 | 1 |

### E6 — Recordatorios multicanal y adherencia

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-32** | El sistema debe generar y enviar recordatorios de toma de medicamento según el horario y la frecuencia del plan. | E6 | 1 |
| **RF-33** | El sistema debe enviar recordatorio de cita 24 horas y 1 hora antes. | E6 | 1 |
| **RF-34** | El sistema debe enviar recordatorios de cuidados puntuales en fechas específicas (ej. cambio de vendaje). | E6 | 1 |
| **RF-35** | El sistema debe permitir al paciente configurar su canal preferido (WhatsApp, SMS, notificación push o combinación). | E6 | 1 |
| **RF-36** | El sistema debe reintentar el envío por un canal alterno cuando el canal principal falle. | E6 | 2 |
| **RF-37** | El sistema debe permitir al paciente marcar cada recordatorio como cumplido desde la app o desde el mismo mensaje. | E6 | 2 |
| **RF-38** | El sistema debe calcular un indicador de adherencia por paciente y por tratamiento. | E6 | 2 |
| **RF-39** | El sistema debe ofrecer al médico un panel con la adherencia de sus pacientes activos. | E6 | 2 |
| **RF-40** | El sistema debe alertar automáticamente al médico —y al cuidador autorizado— cuando un paciente no confirme adherencia durante el número de días configurado, con prioridad en tratamientos críticos o post-operatorios. | E6, E11 | 2 |

### E7 — Comunicación paciente–médico entre consultas

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-41** | El sistema debe ofrecer un canal para que el paciente reporte síntomas o dudas de seguimiento. | E7 | 2 |
| **RF-42** | El sistema debe permitir al médico responder el reporte o derivarlo a una cita de control. | E7 | 2 |
| **RF-43** | El sistema debe advertir de forma explícita y permanente en la interfaz que el canal no atiende urgencias, indicando a dónde acudir. | E7, E11 | 2 |

### E8 — Asistente de IA y contenido educativo

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-44** | El sistema debe ofrecer al médico un chat que responda sobre la historia clínica del paciente (diagnósticos, tratamientos, alergias, antecedentes). | E8 | 3 |
| **RF-45** | Toda llamada al proveedor de IA debe pasar por un backend propio que controle qué se envía, registre el acceso y custodie la clave de API. **Queda prohibido** invocar la IA desde el cliente. | E8, E11 | 3 |
| **RF-46** | El sistema debe exigir consentimiento explícito del paciente antes de usar IA sobre su historia clínica. | E8, E11 | 3 |
| **RF-47** | El sistema debe mostrar al paciente contenido educativo verificado y curado por condición (hipertensión, diabetes, etc.), sin generarlo libremente con IA en el momento. | E8 | 3 |

### E9 — Panel administrativo y multi-clínica

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-48** | El sistema debe permitir que un médico atienda en varias sedes, mostrando a cada sede únicamente sus propias citas. | E9 | 3 |
| **RF-49** | El sistema debe permitir al administrador gestionar profesionales, horarios y sedes. | E9 | 3 |
| **RF-50** | El sistema debe generar reportes de citas por semana y por mes, adherencia promedio y tipos de cita más frecuentes. | E9 | 3 |

### E10 — Accesibilidad y experiencia

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-51** | El sistema debe ofrecer un modo accesible con texto ampliado y alto contraste. | E10 | 3 |
| **RF-52** | El sistema debe permitir la lectura en voz alta del plan de tratamiento y los recordatorios. | E10 | 3 |
| **RF-53** | El sistema debe permitir exportar el plan de tratamiento en PDF para pacientes sin teléfono inteligente. | E10 | 3 |
| **RF-54** | El sistema debe aplicar una encuesta breve de satisfacción después de la consulta. | E10, E9 | 3 |

### E11 — Seguridad, privacidad y cumplimiento

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-55** | El sistema debe permitir al paciente otorgar y revocar el consentimiento de acceso a un cuidador, delimitando qué puede ver. | E11 | 3 |
| **RF-56** | El sistema debe registrar en bitácora de auditoría quién accede o modifica una historia clínica y en qué momento. | E11 | 1 |
| **RF-57** | El sistema debe permitir al paciente consultar quién ha accedido a su historia clínica. | E11 | 3 |
| **RF-58** | El sistema debe registrar la aceptación de la política de tratamiento de datos personales en el momento del registro. | E11 | 1 |

### E12 — Interoperabilidad

| ID | Requisito | Épica | Fase |
|----|-----------|-------|------|
| **RF-59** | El sistema debe generar el Resumen Digital de Atención (RDA) por evento de atención en el formato exigido. | E12 | 4 |
| **RF-60** | El sistema debe intercambiar el RDA con la plataforma de interoperabilidad, registrando el resultado de cada envío. | E12 | 4 |

---

## 6. Requisitos no funcionales

Estos requisitos son **innegociables**: se derivan de fallas concretas de una versión anterior mal implementada.

| ID | Requisito | Categoría |
|----|-----------|-----------|
| **RNF-01** | Seguridad a nivel de fila real: cada usuario accede únicamente a sus propios datos mediante políticas de base de datos filtradas por la identidad autenticada. **Ninguna tabla con datos de salud puede tener políticas abiertas (`USING true`).** | Seguridad |
| **RNF-02** | Ninguna clave de API de terceros puede viajar dentro del cliente (app móvil o web). Todo llamado externo (IA, WhatsApp, SMS) pasa por backend propio. | Seguridad |
| **RNF-03** | Todo documento médico se almacena cifrado y se sirve con URL firmada de vigencia corta. Prohibido el almacenamiento público. | Seguridad |
| **RNF-04** | Las contraseñas se almacenan con algoritmo de hash resistente (bcrypt/argon2) y sal única. | Seguridad |
| **RNF-05** | Todo el tráfico viaja sobre TLS 1.2 o superior. | Seguridad |
| **RNF-06** | La bitácora de auditoría es de solo anexado y conserva los registros por el término legal aplicable. | Trazabilidad |
| **RNF-07** | Cumplimiento de la **Ley 1581 de 2012** (Habeas Data) para el tratamiento de datos sensibles de salud. | Normativo |
| **RNF-08** | Cumplimiento de la **Ley 2015 de 2020** y la **Resolución 1888 de 2025**: historia clínica electrónica interoperable, RDA, control de accesos y trazabilidad. | Normativo |
| **RNF-09** | Cumplimiento del **Decreto 580 de 2024**: validez de la historia clínica exclusivamente digital. | Normativo |
| **RNF-10** | Consentimiento explícito y revocable del paciente para acceso de cuidador y para uso de IA sobre su historia. | Normativo |
| **RNF-11** | Integración de WhatsApp exclusivamente mediante la API oficial de Meta o un BSP certificado (Twilio, 360dialog). Prohibidas las librerías no oficiales y los números personales. | Normativo / Técnico |
| **RNF-12** | Las pantallas de consulta responden en menos de 2 segundos con conectividad móvil típica (4G). | Rendimiento |
| **RNF-13** | Los recordatorios se entregan dentro de una ventana de ±5 minutos respecto de la hora programada. | Rendimiento |
| **RNF-14** | Disponibilidad mensual objetivo del 99.5% en horario de atención. | Disponibilidad |
| **RNF-15** | Interfaz conforme a WCAG 2.1 nivel AA en contraste, tamaño de objetivo táctil y navegación. | Accesibilidad |
| **RNF-16** | Respaldo diario de la base de datos con restauración probada al menos una vez por trimestre. | Continuidad |

> **Nota de validación jurídica.** Las referencias normativas provienen del brief del proyecto. Antes de la salida a producción deben verificarse su vigencia y alcance con asesoría jurídica especializada en salud digital.

---

## 7. Restricciones y supuestos

**Restricciones**
- El envío de mensajes proactivos por WhatsApp está sujeto a la aprobación de plantillas por Meta y tiene costo por conversación.
- La ventana de servicio al cliente de WhatsApp (24 horas) condiciona qué mensajes pueden enviarse libremente.
- La app debe funcionar con conectividad intermitente y en gama baja de dispositivos Android.

**Supuestos**
- La clínica cuenta con una línea de WhatsApp Business propia y verificada.
- Los profesionales registran el plan de tratamiento dentro de la consulta, no después.
- El catálogo de medicamentos se alimenta de una fuente de referencia (INVIMA o equivalente) y se mantiene actualizado.

---

## 8. Trazabilidad Épica → Requisito

| Épica | Requisitos funcionales | Fase |
|-------|------------------------|------|
| E1 | RF-01 … RF-06 | 1 |
| E2 | RF-07 … RF-12 | 1 |
| E3 | RF-13 … RF-18 | 2 |
| E4 | RF-19 … RF-23, RF-11 | 1 |
| E5 | RF-24 … RF-31 | 1 |
| E6 | RF-32 … RF-40, RF-16, RF-29 | 1-2 |
| E7 | RF-41 … RF-43 | 2 |
| E8 | RF-44 … RF-47 | 3 |
| E9 | RF-48 … RF-50, RF-12, RF-54 | 3 |
| E10 | RF-51 … RF-54 | 3 |
| E11 | RF-55 … RF-58, RF-02, RF-04, RF-21, RF-45, RF-46 | 1-4 |
| E12 | RF-59, RF-60 | 4 |

---

## 9. Glosario

| Término | Definición |
|---------|------------|
| **Adherencia** | Grado en que el paciente cumple el tratamiento indicado; en el producto se mide como confirmaciones cumplidas sobre recordatorios enviados. |
| **BSP** | *Business Solution Provider*: proveedor certificado por Meta para operar WhatsApp Business API. |
| **CIE-10** | Clasificación Internacional de Enfermedades, décima revisión. |
| **RDA** | Resumen Digital de Atención, definido por la normativa colombiana de interoperabilidad de historia clínica. |
| **RLS** | *Row Level Security*: seguridad a nivel de fila en la base de datos. |
| **URL firmada** | Enlace temporal con firma criptográfica que autoriza el acceso a un archivo por tiempo limitado. |
| **Ventana de 24h** | Periodo posterior al último mensaje del usuario durante el cual WhatsApp permite responder con mensajes libres. |
