# Contrato de la API

**Fase del ciclo de vida:** Diseño
**Versión:** 1.2 · 26 de octubre de 2026

La API es el único punto de entrada al sistema. Este documento dice qué operaciones existen, quién puede usarlas y qué historia las pide. Los campos exactos de cada petición se fijan al diseñar cada historia.

La versión 1.1 incorpora las decisiones D-20 a D-24: ingreso con documento, corrección de datos e historia clínica del consultorio.

---

## 1. Convenciones

| Tema | Regla |
|---|---|
| Dirección base | `/api/v1` |
| Formato | JSON, salvo la carga de archivos (formulario con archivo), la respuesta del asistente (texto por partes) y la copia de la historia clínica (PDF) |
| Sesión | Cookie segura que la página no puede leer. Toda operación que modifica algo exige además un encabezado propio de la aplicación, para evitar peticiones desde otros sitios |
| Fechas | Con hora y zona, en formato ISO 8601 |
| Listas | Paginadas: `pagina` y `tamano`; la respuesta trae el total |
| Errores | Siempre con la misma forma: `codigo`, `mensaje` para mostrar y `detalle` opcional |

**Códigos de respuesta**

| Código | Cuándo |
|---|---|
| 200, 201 | Todo bien |
| 400 | Datos inválidos; el `detalle` dice qué campo |
| 401 | No hay sesión o ya venció |
| 403 | La sesión existe, pero el rol no tiene permiso. Queda en la bitácora |
| 404 | No existe, o no es suyo. No se distingue, para no revelar que existe |
| 409 | Choque: el espacio ya está ocupado, el documento ya existe, la cita ya fue atendida, la atención ya está cerrada |
| 422 | La regla de negocio lo impide: faltan menos de 24 horas, falta la autorización, faltan campos obligatorios para cerrar la atención |
| 429 | Demasiados intentos |

## 2. Operaciones

Roles: **P** paciente, **M** médico, **—** sin sesión.

### Cuentas e ingreso (E1)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Crear la cuenta del médico con el enlace de puesta en marcha | `POST /puesta-en-marcha` | — | HU-001 |
| Registrarse como paciente | `POST /cuentas/registro` | — | HU-002 |
| Activar una cuenta creada por el médico | `POST /cuentas/activacion` | — | HU-002, HU-024 |
| Ingresar con tipo y número de documento y contraseña | `POST /sesion` | — | HU-004 |
| Cerrar sesión | `DELETE /sesion` | P, M | HU-007 |
| Ver mi usuario, mi rol y qué me falta por aceptar o por llenar | `GET /yo` | P, M | HU-004, HU-003, HU-041 |
| Cambiar mi teléfono, mi correo y mis datos de la historia clínica | `PATCH /yo` | P | HU-040, HU-041 |
| Pedir recuperación de contraseña con el documento | `POST /cuentas/recuperacion` | — | HU-005 |
| Definir la contraseña nueva | `POST /cuentas/recuperacion/confirmar` | — | HU-005 |
| Leer el texto vigente de una autorización | `GET /autorizaciones/texto?tipo=` | —, P | HU-003, HU-032 |
| Aceptar, rechazar o retirar una autorización | `POST /yo/autorizaciones` | P | HU-003, HU-032 |
| Ver mis autorizaciones | `GET /yo/autorizaciones` | P | HU-003, HU-032 |

Reglas del ingreso y de la recuperación:

- El ingreso y la recuperación responden igual exista o no la cuenta. La recuperación nunca muestra el correo: solo dice que, si la cuenta existe, se envió un enlace al correo registrado.
- Cinco fallos seguidos desde un mismo equipo bloquean el ingreso a esa cuenta **desde ese equipo** por 15 minutos. El dueño de la cuenta puede seguir entrando desde el suyo.
- Cambiar el correo exige la contraseña y envía un aviso al correo anterior.

### Consultorio y calendario (E1, E2)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Ver los datos públicos del consultorio | `GET /consultorio` | P, M | HU-001 |
| Editar los datos del consultorio | `PUT /consultorio` | M | HU-001 |
| Ver qué falta por configurar | `GET /consultorio/pendientes` | M | HU-001 |
| Ver y guardar el horario semanal | `GET`, `PUT /horario` | M | HU-008 |
| Listar, crear y eliminar bloqueos | `GET`, `POST /bloqueos`, `DELETE /bloqueos/{id}` | M | HU-009 |
| Listar tipos de cita | `GET /tipos-cita` | P, M | HU-010 |
| Crear, editar, activar y desactivar tipos de cita | `POST /tipos-cita`, `PATCH /tipos-cita/{id}` | M | HU-010 |
| Consultar los próximos días con espacio y las horas libres de un día | `GET /disponibilidad?tipo_cita=&fecha=` | P, M | HU-011, HU-012 |

Guardar el horario o crear un bloqueo que afecta citas existentes responde con la lista de citas afectadas. El bloqueo no se guarda hasta que esas citas se muevan o se cancelen (HU-009, CA-2).

### Citas (E3)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Crear una cita | `POST /citas` | P, M | HU-012, HU-016 |
| Listar citas | `GET /citas?desde=&hasta=&estado=` | P, M | HU-013 |
| Ver una cita con su historial de cambios | `GET /citas/{id}` | P, M | HU-013 |
| Mover una cita | `POST /citas/{id}/mover` | P, M | HU-014, HU-017 |
| Cancelar una cita | `POST /citas/{id}/cancelar` | P, M | HU-015, HU-017 |
| Marcar asistencia o inasistencia | `POST /citas/{id}/asistencia` | M | HU-018 |
| Inicio del paciente | `GET /yo/inicio` | P | HU-020 |

Diferencias por rol sobre la misma ruta:

| Regla | Paciente | Médico |
|---|---|---|
| Para quién crea | Solo para sí mismo | Para cualquier paciente |
| Qué citas lista | Solo las suyas | Todas |
| Anticipación de 24 horas para mover o cancelar | Aplica | No aplica |
| Motivo al cancelar | Opcional | Obligatorio |
| Horario por fuera de las franjas | No permitido | Permitido con advertencia |

**Aviso que no llegó.** Cuando el correo de una cita falla, la cita trae la marca "aviso no entregado" en la agenda, en el calendario y en su detalle. Así lo ve el médico sin una pantalla aparte (HU-019, CA-3).

### Panel del médico (E4)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Agenda de hoy, con las atenciones que siguen abiertas | `GET /agenda/hoy` | M | HU-021, HU-044 |
| Calendario con citas, bloqueos y tiempo libre | `GET /calendario?desde=&hasta=` | M | HU-022 |
| Buscar y listar pacientes | `GET /pacientes?buscar=` | M | HU-023 |
| Registrar un paciente | `POST /pacientes` | M | HU-024 |
| Ficha del paciente | `GET /pacientes/{id}` | M | HU-025 |
| Corregir los datos de un paciente | `PATCH /pacientes/{id}` | M | HU-040, HU-041 |

El botón de cobro (HU-026) no tiene operación en la API. Al registrar un paciente el correo es opcional: si lo tiene, recibe el enlace de activación; si no, queda sin cuenta activa hasta que el médico le agregue uno (S-22).

### Documentos (E5)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Subir un documento | `POST /documentos` | P | HU-028 |
| Listar mis documentos | `GET /documentos` | P | HU-029 |
| Listar los documentos de un paciente | `GET /pacientes/{id}/documentos` | M | HU-025, HU-030 |
| Pedir el enlace temporal para abrir un documento | `POST /documentos/{id}/enlace` | P, M | HU-027, HU-029, HU-030 |
| Eliminar un documento | `DELETE /documentos/{id}` | P | HU-029 |

El enlace temporal dura máximo 15 minutos. El visor pide uno nuevo cuando el anterior está por vencer (HU-030, CA-4). Subir dos veces el mismo archivo responde 409 con el documento que ya existe; así reintentar una carga no deja copias (HU-028, CA-5).

### Asistente de IA (E6)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Hacer una pregunta sobre los documentos y las atenciones de un paciente | `POST /pacientes/{id}/asistente/preguntas` | M | HU-034, HU-042 |
| Generar el resumen del paciente | `POST /pacientes/{id}/resumen` | M | HU-035 |
| Ver el último resumen y si está desactualizado | `GET /pacientes/{id}/resumen` | M | HU-035, HU-042 |

Antes de llamar al proveedor de IA, estas operaciones verifican, en este orden: rol médico, autorización de IA vigente del paciente, que tenga al menos un fragmento indexado y el tope de consultas por hora. Si algo falla, responden 422 o 429 y **no** se llama al proveedor (HU-033, CA-3).

La respuesta a una pregunta llega por partes, para que el texto aparezca mientras se escribe. Al final llegan dos listas: los orígenes citados, cada uno con documento y página o con la atención, y la frase citada; y lo consultado, es decir, los documentos, páginas y atenciones de los fragmentos que encontró la búsqueda (D-30).

La pantalla de atención usa estas mismas operaciones. No hay ninguna que escriba en la historia clínica con lo que responde el asistente (HU-042, CA-4).

### Historia clínica del consultorio (E9)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Abrir una atención, desde una cita o desde la ficha | `POST /pacientes/{id}/atenciones` | M | HU-042 |
| Ver una atención | `GET /atenciones/{id}` | M | HU-042, HU-045 |
| Guardar el borrador de una atención abierta | `PATCH /atenciones/{id}` | M | HU-042, HU-043 |
| Cerrar y firmar la atención, con la contraseña del médico | `POST /atenciones/{id}/cierre` | M | HU-044 |
| Agregar una nota aclaratoria a una atención cerrada | `POST /atenciones/{id}/notas` | M | HU-044 |
| Listar las atenciones cerradas de un paciente | `GET /pacientes/{id}/atenciones` | M | HU-045 |
| Generar la copia de la historia clínica en PDF | `POST /pacientes/{id}/historia-clinica/copia` | M | HU-046 |
| Buscar diagnósticos por nombre o por código | `GET /cie10?buscar=` | M | HU-043 |
| Buscar municipios | `GET /municipios?buscar=` | P, M | HU-041 |
| Leer una lista de valores | `GET /listas/{lista}` | P, M | HU-041, HU-043 |

Reglas de la atención:

- Si el paciente ya tiene una atención abierta, abrir otra devuelve la que está abierta (HU-042, CA-6).
- El borrador se guarda por secciones: la pantalla envía solo lo que cambió.
- El cierre revisa, en este orden: la contraseña del médico, los datos de identificación del paciente y los campos obligatorios de la consulta. Si falta algo responde 422 con la lista de lo que falta y **no** cierra (HU-041, CA-3; HU-044, CA-2).
- Al cerrar, la cita queda como atendida y la fórmula, si la hay, queda como tratamiento del paciente, todo en la misma transacción.
- Una atención cerrada no admite `PATCH`: responde 409. No existe operación para borrarla.

### Tratamientos (E8)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Registrar un tratamiento | `POST /pacientes/{id}/tratamientos` | M | HU-038 |
| Listar los tratamientos de un paciente | `GET /pacientes/{id}/tratamientos` | M | HU-038, HU-025 |
| Ver mis tratamientos | `GET /yo/tratamientos` | P | HU-039, HU-020 |

No existe operación para modificar ni borrar un tratamiento. Cada medicamento lleva nombre, dosis, vía, frecuencia, duración y forma de tomarlo.

### Bitácora (E7)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Consultar la bitácora por paciente y fecha | `GET /bitacora?paciente=&desde=&hasta=` | M | HU-037 |

## 3. Matriz de permisos

Es la que se carga en la tabla `rol_permiso` (HU-006). Todo lo que no aparece queda denegado.

| Grupo de operaciones | Paciente | Médico |
|---|---|---|
| Mi cuenta, mis autorizaciones | Sí | Sí (solo cuenta) |
| Cambiar mi teléfono, mi correo y mis datos de la historia clínica | Sí | — |
| Configuración del consultorio, horario, bloqueos, tipos de cita | Solo leer lo necesario para agendar | Sí |
| Citas propias | Sí | — |
| Citas de cualquier paciente, asistencia | No | Sí |
| Agenda, calendario, pacientes, ficha | No | Sí |
| Corregir los datos de cualquier paciente | No | Sí |
| Subir y eliminar documentos | Sí, los propios | No |
| Leer documentos | Los propios | Todos |
| Asistente y resumen | No | Sí |
| Atenciones, notas aclaratorias, historial y copia de la historia clínica | No | Sí |
| Diagnósticos CIE-10 | No | Sí |
| Municipios y listas de valores | Sí | Sí |
| Registrar tratamientos | No | Sí |
| Leer tratamientos | Los propios | Todos |
| Bitácora | No | Sí |

## 4. Trazabilidad

Las 46 historias tienen operación, salvo las cuatro que no la necesitan: HU-006 y HU-036 (permisos, dentro del servidor y de la base), HU-026 (botón sin función) y HU-031 (lectura en segundo plano). HU-019 no tiene operación propia: sus avisos salen de las operaciones de citas.
