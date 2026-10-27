# Estado del proyecto y etapas del Desarrollo

**Fecha:** 26 de octubre de 2026
**Para qué sirve este archivo:** retomar el trabajo sin releer toda la conversación. Léalo primero.

---

## 1. Qué es Vitalia

Sistema a la medida para **un consultorio médico general privado en Colombia**. Dos usuarios: el **médico**, que hace todo lo del consultorio, y el **paciente**. No se vende a otros consultorios.

Lo que cubre el alcance: cuentas, calendario de disponibilidad, citas de ambos lados, panel del médico, historias clínicas que sube el paciente, asistente de IA sobre esos documentos, tratamientos y la historia clínica que el consultorio lleva de cada atención.

## 2. En qué va

| Fase | Estado | Detalle |
|---|---|---|
| **1. Planificación** | Hecha | Alcance, requisitos, marco normativo, 46 historias en 9 épicas con 212 criterios, 110 tareas y 200 puntos |
| **2. Diseño** | Cerrada en documentos | Arquitectura limpia, modelo de datos con permisos por fila, API, asistente, pantallas, diagramas, base visual, herramientas y entrega |
| **3. Desarrollo** | **En curso** | Bloques 1 (registro e ingreso) y 2 (citas) construidos, probados contra PostgreSQL 18 en Docker y unidos a `master`. Bloque 3 en curso: subir, leer, indexar con Qwen, buscar y preguntar al asistente ya funcionan en el servidor; las respuestas con Qwen esperan la verificación de la cuenta en Alibaba. Ya tienen pantalla, según el lienzo: Mis documentos del paciente (subir, ver y eliminar) y la ficha del médico con el asistente. Siguen el resumen, los tratamientos y el enlace firmado con R2. Falta crear los servicios en la nube y correrlo contra Render. Ver la sección 4 y [estado_desarrollo.md](estado_desarrollo.md) |
| **4. Pruebas** | Sin iniciar | — |
| **5. Despliegue** | Sin iniciar | — |

Planificación y Diseño están confirmados en git y son consistentes entre sí: el 13 de octubre se cruzaron las 46 historias contra requisitos, mapa de relaciones, modelo de datos, API y pantallas, y las 33 tablas contra sus permisos. Si se cambia una historia, una tabla o una operación, hay que volver a cruzar.

**Decisiones que definen el producto**

| Tema | Cómo quedó |
|---|---|
| Tecnología | Python con FastAPI, PostgreSQL en Render, React con Vite y TypeScript, archivos en Cloudflare R2 y Qwen como modelo de IA detrás de un adaptador intercambiable |
| Asistente | Búsqueda de fragmentos (RAG) en los documentos del paciente y en sus atenciones cerradas, siempre de un solo paciente, con `pgvector` en la misma base (D-30) |
| Servicios | En la nube desde el primer día, sin instalar nada en el computador (D-27) |
| Código | Arquitectura limpia: dominio, casos de uso, adaptadores y entrada. Rápido, midiendo antes de optimizar (D-19) |
| Ingreso | Tipo y número de documento más contraseña. El documento identifica; nunca hace de contraseña (D-20) |
| Cuentas | Solo adultos. Registro con nombres, apellidos, fecha de nacimiento, correo, documento y teléfono (D-21, D-22) |
| Historia clínica | Dentro del sistema, con lo mínimo de la Resolución 1995 de 1999. Al atender, el asistente va a un lado y el formulario en el centro. Lo cerrado no se modifica (D-24) |
| Aspecto | El lienzo es la base visual. Estados en caja blanca redondeada con sombra y un punto de color; tarjetas y botones con sombra; nada que se vea genérico (D-18, D-25) |
| Iconos | Phosphor Icons (D-26). Los que se ven en el lienzo son provisionales |

## 3. Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Alcance y flujo principal | [planificacion/01-alcance-y-flujo.md](planificacion/01-alcance-y-flujo.md) |
| 46 requisitos funcionales y 15 no funcionales | [planificacion/02-requisitos.md](planificacion/02-requisitos.md) |
| Leyes, contenido mínimo de la historia clínica y ocho preguntas para el abogado | [planificacion/03-marco-normativo.md](planificacion/03-marco-normativo.md) |
| Decisiones (D-01 a D-30), supuestos (S-01 a S-23) y decisiones de diseño (A-01 a A-15) | [planificacion/04-decisiones-y-supuestos.md](planificacion/04-decisiones-y-supuestos.md) |
| Reglas del tablero Kanban | [planificacion/05-kanban.md](planificacion/05-kanban.md) |
| 46 historias en 9 épicas, con criterios y tareas | [historias-de-usuario/](historias-de-usuario/) |
| Orden de construcción y dependencias | [historias-de-usuario/RELACIONES.md](historias-de-usuario/RELACIONES.md) |
| Tecnología, capas del código y reglas de rendimiento | [diseno/01-arquitectura.md](diseno/01-arquitectura.md) |
| Tablas, diagrama entidad-relación y permisos por fila | [diseno/02-modelo-de-datos.md](diseno/02-modelo-de-datos.md) |
| Operaciones de la API | [diseno/03-api.md](diseno/03-api.md) |
| Decisiones del asistente de IA | [diseno/04-asistente-ia.md](diseno/04-asistente-ia.md) |
| Inventario de pantallas | [diseno/05-pantallas.md](diseno/05-pantallas.md) |
| Diagramas de contexto, contenedores, componentes, despliegue, secuencias y estados | [diseno/06-diagramas-de-arquitectura.md](diseno/06-diagramas-de-arquitectura.md) |
| Cómo se construye el asistente, paso a paso | [diseno/07-como-se-construye-el-asistente.md](diseno/07-como-se-construye-el-asistente.md) |
| Colores, letra, sombras y piezas aprobados | [diseno/08-base-visual.md](diseno/08-base-visual.md) |
| Herramientas, servicios, ramas, pruebas y despliegue | [diseno/09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md) |
| Código del servidor: capas, migraciones y pruebas | `servidor/` |
| Código de las pantallas | `pantallas/` |
| Pruebas automáticas de GitHub | `.github/workflows/pruebas.yml` |
| Versión anterior del proyecto (solo consulta) | `archivo/v1/` |

**Fuera del repositorio**

| Qué | Enlace |
|---|---|
| Lienzo de diseño (aspecto, base visual aprobada) | https://claude.ai/artifact/R6WLHr5eAt7FQztseugqQY |
| Prototipo navegable (comportamiento) | https://claude.ai/artifact/4MN2vq99tcrQBzUWDJ4pEy |

El código del prototipo está en [diseno/prototipo/index.html](diseno/prototipo/index.html) y la fuente de las once pantallas del lienzo en [diseno/lienzo/](diseno/lienzo/). El lienzo solo se ve dibujado en el artefacto. Si el dueño del proyecto lo edita a mano, la copia del repositorio queda atrás: hay que volver a traerla.

Existe un tercer artefacto, "Vitalia Salud", de agosto: es el demo comercial de la versión anterior, con otra paleta y otro alcance, y no es referencia.

## 4. Etapas del Desarrollo

El 13 de octubre el dueño del proyecto cambió el arranque (D-27 y D-28): los servicios se montan en la nube desde el primer día y se construye por historias, sin pantalla de verificación del sistema. Las pruebas de concepto de la arquitectura ya no son una etapa aparte: cada duda se despeja dentro del paso o del bloque que la toca.

### Paso 0 · Servicios y clave

Lo hace el dueño del proyecto. Ninguna clave pasa por el chat ni entra al repositorio: todas van a `servidor/.env`, cuyas variables están en `servidor/.env.example`.

| Qué | Dónde | Estado |
|---|---|---|
| Repositorio privado | GitHub. Al crearlo, la rama `master` pasa a llamarse `main` | Pendiente |
| PostgreSQL 18 | Render, región Virginia, plan gratuito. Base `vitalia_dev`, usuario `vitalia_migraciones` | Pendiente |
| Archivos | Cloudflare R2, espacio `vitalia-dev`, con una clave limitada a ese espacio | Pendiente |
| Clave de la IA | Alibaba Cloud Model Studio, región Singapur | Pendiente |

El paso a paso de cada uno está en la sección 3 de [herramientas y entrega](diseno/09-herramientas-y-entrega.md). El plan gratuito de la base **vence a los 30 días de creada**: antes de esa fecha hay que pasarla al plan pago.

### Paso 1 · Esqueleto y conexión

| Qué | Estado |
|---|---|
| `servidor/` con las cuatro capas, migraciones, regla de dependencia entre capas y pruebas | Hecho |
| `pantallas/` con las variables de la base visual, sus piezas y la carga separada por zona | Hecho |
| Pruebas automáticas en cada cambio | Escritas. Corren cuando exista el repositorio remoto |
| Conectar a Render, leer los privilegios del usuario dueño y crear `vitalia_api` sin privilegios | Pendiente del paso 0. **Despeja la duda 3 de la arquitectura** |
| Guardar, leer y borrar un archivo en R2; abrirlo con enlace firmado y comprobar que sin firma se rechaza | Pendiente del paso 0 |
| Una llamada mínima a cada modelo de Qwen | Pendiente del paso 0 |

### Bloques de construcción

Cada historia sigue las capas de la [arquitectura](diseno/01-arquitectura.md), con una rama por historia. Toda tabla nace con su permiso por fila en la misma migración.

| Bloque | Qué se construye | Historias |
|---|---|---|
| **1 · Registro e ingreso** | Roles, permisos por fila, bitácora, cuenta del médico, registro del paciente con sus autorizaciones, ingreso y cierre de sesión | HU-006, HU-036, HU-037, HU-001, HU-002, HU-003, HU-004, HU-007 y la casilla de IA de HU-032 |
| **2 · Citas** | Horario, tipos de cita y espacios libres; el paciente agenda, consulta, mueve y cancela; el médico ve su día, busca pacientes y crea, mueve y cancela | HU-008, HU-010, HU-011, HU-012 a HU-017, HU-020, HU-021, HU-023 |
| **3 · Documentos y resumen con IA** | Almacenamiento privado, subir y listar documentos, lectura por página, indexación en fragmentos, autorización de IA, búsqueda aislada por paciente, ficha, resumen, preguntas y visor. Las atenciones entran a la búsqueda cuando exista E9 | HU-027 a HU-035, HU-025 |
| **Después** | Recuperación de contraseña; bloqueos, asistencia, avisos por correo y calendario; registro y corrección de pacientes desde el panel; cobro; tratamientos; historia clínica del consultorio | HU-005, HU-009, HU-018, HU-019, HU-022, HU-024, HU-026, HU-040, HU-038, HU-039, HU-041 a HU-046 |

**Bloque 1: hecho el 14 de octubre, en la rama `bloque-1-registro-e-ingreso`**

| Qué | Cómo quedó |
|---|---|
| Servidor | Tres migraciones: cuentas, roles, matriz de permisos, bitácora, sesiones, intentos, enlaces y autorizaciones, todas con permisos por fila forzados. Lo que pasa sin sesión va por funciones de la base. 65 pruebas en verde contra PostgreSQL 18.4, una por criterio de aceptación; las migraciones se aplican, se deshacen y se vuelven a aplicar |
| Pantallas | Ingresar (P-01), Crear mi cuenta en tres pasos con la hoja del tratamiento de datos (P-02), cuenta del médico con el enlace de puesta en marcha (P-13), datos del consultorio (M-11), inicio mínimo del paciente y el marco de cada zona. 7 pruebas en verde; carga inicial de 95 KB comprimida |
| Recorrido a la vista | Puesta en marcha, datos del consultorio, registro de un paciente con la hoja de datos, inicio del paciente con los datos del consultorio, un paciente que intenta entrar al panel del médico vuelve a su zona, y al salir el botón de atrás no muestra información |
| Enlace de la cuenta del médico | `uv run python -m vitalia.principal puesta-en-marcha` en `servidor/`. Sirve una vez y vence en 24 horas |
| Textos de autorización | Borradores de la versión 1 en `servidor/migraciones/textos/`, para que los revise el abogado |

**Bloque 2: hecho el 26 de octubre, en la rama `bloque-2-citas`**

| Qué | Cómo quedó |
|---|---|
| Servidor | Horario semanal, tipos de cita, espacios libres calculados en el dominio, citas de los dos lados y agenda de hoy con lo que falta configurar. Dos citas no pueden ocupar el mismo tiempo: lo impide la base. 105 pruebas en verde contra PostgreSQL 18 en Docker |
| Pantallas | Paciente: inicio con la próxima cita (P-04), agendar (P-05) y mis citas (P-06). Médico: hoy (M-01), pacientes (M-04), nueva cita o mover (M-03) y configuración (M-08, M-10). 13 pruebas en verde |
| Recorrido a la vista | De punta a punta contra la API y la base de Docker; el detalle está en la sección 4 de [estado_desarrollo.md](estado_desarrollo.md) |

**Lo que cada bloque deja para después**

| Bloque | Qué queda por fuera | Por qué |
|---|---|---|
| 1 | Consulta filtrada de la bitácora (HU-037, CA-4) | Su pantalla no hace falta para ingresar |
| 1 | Activación de una cuenta creada por el médico (HU-002, CA-4) | Depende de HU-024 |
| 1 | Aceptar una versión nueva del texto y verlo en el perfil (HU-003, CA-3 y CA-4) | Van con la pantalla de perfil |
| 1 | Lista de lo que falta por configurar (HU-001, CA-4) | Va con el horario y los tipos de cita, en el bloque 2 |
| 1 | Enlace "Olvidé mi contraseña" en la pantalla de ingreso | Llega con HU-005, que necesita el servicio de correo. No se dejó un enlace sin destino |
| 2 | Bloqueos en el cálculo de espacios | HU-009 llega después; el cálculo ya los recibe como dato |

**Dónde se despeja cada duda de la arquitectura**

| # | Duda | Dónde |
|---|---|---|
| 1 y 2 | ¿La lectura de fotos es suficientemente buena? ¿La búsqueda trae el fragmento correcto y el asistente lo cita bien? | Al empezar el bloque 3, con documentos inventados. Criterio: cero inventos, origen correcto en al menos nueve de cada diez respuestas y lectura aceptable de la foto nítida |
| 3 | ¿Los permisos por fila funcionan con un usuario sin privilegios en Render? | En el paso 1, apenas exista la base |
| 4 | ¿La cookie de sesión funciona entre el sitio y la API? | Al publicar en Render, cuando cierre el bloque 1 |

**Cómo avanza cada historia.** Pasa por las columnas del [tablero](planificacion/05-kanban.md). En la columna Diseño se fija lo que a propósito no se definió antes:

- Campos exactos de cada operación, códigos de error, permisos y tipo de cada columna.
- La pantalla, si no está en el lienzo: se arma con las piezas de la [base visual](diseno/08-base-visual.md), siguiendo el prototipo.
- Textos: borrador de la política de datos y de la autorización de IA (HU-003, HU-032) y plantillas de los correos (HU-005, HU-019, HU-024, HU-040).

En Desarrollo se escribe con sus pruebas; en Pruebas se revisa contra los criterios de aceptación en el ambiente de pruebas de Render; en Despliegue pasa a producción.

**Pruebas rápidas y pruebas de base.** Como la base está en Estados Unidos, las pruebas que la tocan tardan más. Las del dominio y los casos de uso no la necesitan y son las que se corren a cada cambio (`uv run pytest -m "not bd"`); las de base se corren antes de unir cada historia. Las de GitHub traen su propio PostgreSQL.

### Antes de usar datos reales

Todo lo anterior se construye y se prueba con datos inventados. Para atender pacientes reales hace falta:

1. **La respuesta del abogado** a tres de las ocho preguntas del [marco normativo](planificacion/03-marco-normativo.md): la 2 (datos fuera de Colombia), la 5 (envío del Resumen Digital de Atención) y la 7 (firma de la historia clínica).
2. **Contrato de tratamiento de datos** con el proveedor de IA, con el de alojamiento y con el de archivos.
3. **Un médico que revise los campos de la historia clínica** (sección 4.2 del marco normativo). La norma deja ese detalle a la práctica médica.
4. **Respaldo de largo plazo.** Render restaura hasta 3 días atrás, 7 en el plan Pro, y la historia clínica se conserva 15 años: hay que programar una exportación periódica.
5. **Cerrar el acceso a la base.** Hoy admite conexiones desde cualquier dirección, con contraseña y cifrado. Antes de datos reales se limita a las direcciones que la necesitan y pasa al plan pago, que sí tiene respaldos.

## 5. Lo que el dueño del proyecto tiene pendiente

1. **Las cuatro cosas del paso 0.**
2. **Ver el lienzo.** Los cambios del 13 de octubre nadie los ha visto dibujados: estados en caja con sombra, sombra en botones y tarjetas, notas sin caja amarilla, la pantalla de atención del médico y la de ingreso con documento.
3. **Dos fotos para el bloque 3**, con datos inventados que se le entregan: una de una hoja impresa y otra de un texto corto copiado a mano.
4. **Tablero Kanban en Jira.** El proyecto que existe es de tipo Scrum. No frena el código.
5. **Buscar el abogado y el médico** de la lista anterior. No frenan el desarrollo, pero sí el uso real.

## 6. Lo que no está verificado

| Tema | Situación |
|---|---|
| Servicios en la nube | Sin crear. Nada del código ha corrido contra Render, R2 ni Qwen |
| Pruebas de base de datos | Desde el 26 de octubre pasan contra PostgreSQL 18 en Docker, incluidas las extensiones `btree_gist` y `unaccent` (D-29). Falta correrlas contra Render |
| Permisos forzados para el dueño de las tablas | Con ellos, ni el usuario de las migraciones ve filas si se conecta directo. Para cargar datos en una migración futura hay que quitarlos un momento dentro de la misma transacción. Falta confirmar que el usuario por defecto de Render no sea superusuario, porque ese se salta los permisos |
| Ingreso, a la vista | El navegador del entorno estaba oculto y no entregó bien las teclas en la pantalla de ingreso. El ingreso correcto, el fallido y el bloqueo están probados de punta a punta en las pruebas automáticas, no a la vista |
| Pruebas automáticas de GitHub | Escritas, sin correr: no hay repositorio remoto |
| Privilegios del usuario dueño en Render | Su documentación no los indica. Dice que se pueden crear usuarios con SQL; lo despeja el paso 1 |
| Modelos `qwen3.7-plus` y `qwen-vl-ocr-2025-11-20` | Existen en la región Singapur; responden `AccessDenied.Unpurchased` hasta que Alibaba apruebe la verificación de identidad de la cuenta (en revisión desde el 27 de octubre). `qwen3.7-text-embedding` ya funciona |
| Búsqueda de fragmentos (D-30) | Construida y medida el 27 de octubre con `qwen3.7-text-embedding` y las 12 historias inventadas: 16 de 16 datos entre los 12 fragmentos, 14 entre los 3 primeros. Falta medirla con documentos de otras fuentes y con más volumen, y probar `pgvector` en Render. Los números (1.000 caracteres, 20 por método, 12 enviados) siguen siendo el punto de partida |
| Texto de la autorización de IA, versión 2 | Hace falta para que las atenciones entren a la búsqueda. Sin escribir; lo revisa el abogado junto con la versión 1 |
| Medio de pago en Cloudflare y en Alibaba Cloud | Es lo usual para activar el servicio; su documentación no lo confirma |
| Grosor de los iconos | Se usa el de dos tonos de Phosphor, fijado en un solo lugar de `pantallas/src/principal.tsx`. La base visual dice "un solo grosor" sin decir cuál. Los iconos que se usan están listados en `pantallas/src/comunes/iconos.ts` |
| Cambios del 13 de octubre en el lienzo | Se revisó que el código esté bien formado; no se vieron dibujados |
| Resto del lienzo | Aprobado por el dueño del proyecto como base visual. El contraste del texto se midió y pasa el nivel AA |
| Prototipo navegable | Probado con 143 comprobaciones automáticas. A la vista solo se revisó una pantalla. No refleja las decisiones del 13 de octubre: ver la sección 6 de [05-pantallas.md](diseno/05-pantallas.md) |
| Permisos por fila sin sesión | El diseño con funciones de la base está escrito, no probado. Lo despeja el bloque 1 |
| `pypdfium2` | Probado el 27 de octubre con las 12 historias inventadas en PDF: texto completo y en orden en todas. Falta probarlo con PDF de otras fuentes |
| Phosphor Icons | Confirmada por el dueño del proyecto e instalada. Falta comprobar que tenga todos los iconos médicos que usa Vitalia |
| Campos clínicos de la historia clínica | La lista la armó quien levantó los requisitos; falta que la revise un médico |
| Proyecto de resolución que reemplazaría la 1995 de 1999 | Publicado el 22 de julio de 2026. Al 13 de octubre no se encontró expedido. Solo se leyó su memoria justificativa, no el articulado |
| Lista vigente de tipo y finalidad de consulta | Está en un anexo de la Resolución 948 de 2026 que no se pudo consultar |
| Precios de Render y de los modelos de IA | Vienen de artículos de terceros |
| Memoria del servicio más pequeño de Render (512 MB) para leer escaneados | Sin medir |
| Uso de datos por Qwen | Su política de no entrenar con datos de clientes se conoce por fuentes de terceros |
| Fragmentos de código de la guía del asistente | Son esquemas sin ejecutar |
| Supuestos S-01 a S-23 | Se ajustan cuando haya un médico real |

**Confirmado el 13 de octubre de 2026 en la documentación oficial**

- **Render:** no hay región en Latinoamérica (Oregon, Ohio, Virginia, Fráncfort y Singapur); el plan gratuito se duerme a los 15 minutos y su base vence a los 30 días, sin respaldos; la base admite conexiones cifradas desde afuera y crear más bases en la misma instancia; la versión más reciente de PostgreSQL que admite es la 18; se puede desplegar solo después de que pasan las pruebas, y correr las migraciones antes de cada despliegue.
- **Almacenamiento de objetos de Render:** en alfa con lista de espera, sin documentación ni precios. Por eso los archivos van a Cloudflare R2.
- **MinIO:** dejó de publicarse. Su descarga responde "410 Gone" y su imagen de Docker fue retirada.
- **Cloudflare R2:** 10 GB al mes sin costo y sin cobro por descarga; la clave se puede limitar a un solo espacio.

Las herramientas de [09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md) que usa el esqueleto ya están instaladas y probadas juntas: FastAPI, SQLAlchemy con `asyncpg`, Alembic, `pytest`, `ruff`, `mypy`, `import-linter`, React con Vite, TanStack Query, Vitest y Phosphor. Las demás entran con la historia que las necesita.

## 7. Reglas que no se pueden olvidar

- **Solo datos inventados o anonimizados** hasta cumplir la lista de "Antes de usar datos reales".
- Lo que sube el paciente son antecedentes. La historia clínica de las atenciones del consultorio va aparte, en la épica E9.
- Una atención cerrada y un tratamiento guardado no se modifican ni se borran.
- El asistente ayuda a leer los antecedentes, pero no escribe la historia clínica.
- El documento identifica a la persona al ingresar; nunca hace de contraseña.
- Sin autorización del paciente no hay asistente, y las fotos no se envían al proveedor de IA.
- Ninguna clave entra al repositorio ni pasa por el chat: van solo en `servidor/.env`.
- Toda tabla nace con su permiso por fila en la misma migración.
- Lo que quedó para después: envío del Resumen Digital de Atención, cuentas de menores de edad, recordatorios de medicamento, factura con Factus, agente de voz y RIPS.

## 8. Forma de trabajo acordada

- Kanban sobre las cinco fases del ciclo de vida; primero las bases, después el código.
- Solo lo útil: sin generadores, sin funciones "por si acaso" y sin pantallas de verificación. Se construye por historias.
- Lo ya hecho y aprobado no se toca; se completa lo que falte.
- El diseño no debe verse genérico: reglas en la sección 6 de la [base visual](diseno/08-base-visual.md).
- Arquitectura limpia y código rápido: las reglas del consultorio no dependen de la tecnología, y la rapidez se mide antes de optimizar.
- Pocas preguntas: se decide, se escribe el supuesto y se corrige sobre el documento.
- Los commits van solo a nombre del dueño del proyecto, sin coautor, y en español.
