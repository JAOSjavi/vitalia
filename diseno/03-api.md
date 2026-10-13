# Contrato de la API

**Fase del ciclo de vida:** Diseño
**Versión:** 1.0 · 12 de octubre de 2026

La API es el único punto de entrada al sistema. Este documento dice qué operaciones existen, quién puede usarlas y qué historia las pide. Los campos exactos de cada petición se fijan al diseñar cada historia.

---

## 1. Convenciones

| Tema | Regla |
|---|---|
| Dirección base | `/api/v1` |
| Formato | JSON, salvo la carga de archivos (formulario con archivo) y la respuesta del asistente (texto por partes) |
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
| 409 | Choque: el espacio ya está ocupado, el documento ya existe, la cita ya fue atendida |
| 422 | La regla de negocio lo impide: faltan menos de 24 horas, falta la autorización |
| 429 | Demasiados intentos |

## 2. Operaciones

Roles: **P** paciente, **M** médico, **—** sin sesión.

### Cuentas e ingreso (E1)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Crear la cuenta del médico con el enlace de puesta en marcha | `POST /puesta-en-marcha` | — | HU-001 |
| Registrarse como paciente | `POST /cuentas/registro` | — | HU-002 |
| Activar una cuenta creada por el médico | `POST /cuentas/activacion` | — | HU-002, HU-024 |
| Ingresar | `POST /sesion` | — | HU-004 |
| Cerrar sesión | `DELETE /sesion` | P, M | HU-007 |
| Ver mi usuario, mi rol y qué me falta por aceptar | `GET /yo` | P, M | HU-004, HU-003 |
| Pedir recuperación de contraseña | `POST /cuentas/recuperacion` | — | HU-005 |
| Definir la contraseña nueva | `POST /cuentas/recuperacion/confirmar` | — | HU-005 |
| Leer el texto vigente de una autorización | `GET /autorizaciones/texto?tipo=` | —, P | HU-003, HU-032 |
| Aceptar, rechazar o retirar una autorización | `POST /yo/autorizaciones` | P | HU-003, HU-032 |
| Ver mis autorizaciones | `GET /yo/autorizaciones` | P | HU-003, HU-032 |

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

### Panel del médico (E4)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Agenda de hoy | `GET /agenda/hoy` | M | HU-021 |
| Calendario con citas, bloqueos y tiempo libre | `GET /calendario?desde=&hasta=` | M | HU-022 |
| Buscar y listar pacientes | `GET /pacientes?buscar=` | M | HU-023 |
| Registrar un paciente | `POST /pacientes` | M | HU-024 |
| Ficha del paciente | `GET /pacientes/{id}` | M | HU-025 |

El botón de cobro (HU-026) no tiene operación en la API.

### Documentos (E5)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Subir un documento | `POST /documentos` | P | HU-028 |
| Listar mis documentos | `GET /documentos` | P | HU-029 |
| Listar los documentos de un paciente | `GET /pacientes/{id}/documentos` | M | HU-025, HU-030 |
| Pedir el enlace temporal para abrir un documento | `POST /documentos/{id}/enlace` | P, M | HU-027, HU-029, HU-030 |
| Eliminar un documento | `DELETE /documentos/{id}` | P | HU-029 |

El enlace temporal dura máximo 15 minutos. El visor pide uno nuevo cuando el anterior está por vencer (HU-030, CA-4).

### Asistente de IA (E6)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Hacer una pregunta sobre los documentos de un paciente | `POST /pacientes/{id}/asistente/preguntas` | M | HU-034 |
| Generar el resumen del paciente | `POST /pacientes/{id}/resumen` | M | HU-035 |
| Ver el último resumen y si está desactualizado | `GET /pacientes/{id}/resumen` | M | HU-035 |

Antes de llamar al proveedor de IA, estas operaciones verifican, en este orden: rol médico, autorización de IA vigente del paciente, que haya al menos un documento legible y el tope de consultas por hora. Si algo falla, responden 422 o 429 y **no** se llama al proveedor (HU-033, CA-3).

La respuesta a una pregunta llega por partes, para que el texto aparezca mientras se escribe. Al final llega la lista de orígenes, cada uno con documento, página y el fragmento citado.

### Tratamientos (E8)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Registrar un tratamiento | `POST /pacientes/{id}/tratamientos` | M | HU-038 |
| Listar los tratamientos de un paciente | `GET /pacientes/{id}/tratamientos` | M | HU-038, HU-025 |
| Ver mis tratamientos | `GET /yo/tratamientos` | P | HU-039, HU-020 |

No existe operación para modificar ni borrar un tratamiento.

### Bitácora (E7)

| Operación | Ruta | Rol | Historia |
|---|---|---|---|
| Consultar la bitácora por paciente y fecha | `GET /bitacora?paciente=&desde=&hasta=` | M | HU-037 |

## 3. Matriz de permisos

Es la que se carga en la tabla `rol_permiso` (HU-006). Todo lo que no aparece queda denegado.

| Grupo de operaciones | Paciente | Médico |
|---|---|---|
| Mi cuenta, mis autorizaciones | Sí | Sí (solo cuenta) |
| Configuración del consultorio, horario, bloqueos, tipos de cita | Solo leer lo necesario para agendar | Sí |
| Citas propias | Sí | — |
| Citas de cualquier paciente, asistencia | No | Sí |
| Agenda, calendario, pacientes, ficha | No | Sí |
| Subir y eliminar documentos | Sí, los propios | No |
| Leer documentos | Los propios | Todos |
| Asistente y resumen | No | Sí |
| Registrar tratamientos | No | Sí |
| Leer tratamientos | Los propios | Todos |
| Bitácora | No | Sí |
