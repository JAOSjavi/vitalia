# Estado del proyecto y etapas del Desarrollo

**Fecha:** 13 de octubre de 2026
**Para qué sirve este archivo:** retomar el trabajo sin releer toda la conversación. Léalo primero.

---

## 1. Qué es Vitalia

Sistema a la medida para **un consultorio médico general privado en Colombia**. Dos usuarios: el **médico**, que hace todo lo del consultorio, y el **paciente**. No se vende a otros consultorios.

Lo que cubre el alcance: cuentas, calendario de disponibilidad, citas de ambos lados, panel del médico, historias clínicas que sube el paciente, asistente de IA sobre esos documentos, tratamientos y la historia clínica que el consultorio lleva de cada atención.

## 2. En qué va

| Fase | Estado | Detalle |
|---|---|---|
| **1. Planificación** | Hecha | Alcance, requisitos, marco normativo, 46 historias en 9 épicas con 205 criterios, 109 tareas y 200 puntos |
| **2. Diseño** | Cerrada en documentos | Arquitectura limpia, modelo de datos con permisos por fila, API, asistente, pantallas, diagramas, base visual, herramientas y entrega |
| **3. Desarrollo** | **Es lo que sigue.** Sin iniciar | No hay código de la aplicación. Las etapas están en la sección 4 |
| **4. Pruebas** | Sin iniciar | — |
| **5. Despliegue** | Sin iniciar | — |

Planificación y Diseño están confirmados en git y son consistentes entre sí: el 13 de octubre se cruzaron las 46 historias contra requisitos, mapa de relaciones, modelo de datos, API y pantallas, y las 33 tablas contra sus permisos. Si se cambia una historia, una tabla o una operación, hay que volver a cruzar.

**Decisiones que definen el producto**

| Tema | Cómo quedó |
|---|---|
| Tecnología | Python con FastAPI, PostgreSQL en Render, React con Vite y TypeScript, archivos en almacenamiento compatible con S3 y Qwen como modelo de IA detrás de un adaptador intercambiable |
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
| Decisiones (D-01 a D-26), supuestos (S-01 a S-23) y decisiones de diseño (A-01 a A-14) | [planificacion/04-decisiones-y-supuestos.md](planificacion/04-decisiones-y-supuestos.md) |
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
| Herramientas, entorno local, ramas, pruebas y despliegue | [diseno/09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md) |
| Versión anterior del proyecto (solo consulta) | `archivo/v1/` |

**Fuera del repositorio**

| Qué | Enlace |
|---|---|
| Lienzo de diseño (aspecto, base visual aprobada) | https://claude.ai/artifact/R6WLHr5eAt7FQztseugqQY |
| Prototipo navegable (comportamiento) | https://claude.ai/artifact/4MN2vq99tcrQBzUWDJ4pEy |

El código del prototipo está en [diseno/prototipo/index.html](diseno/prototipo/index.html) y la fuente de las once pantallas del lienzo en [diseno/lienzo/](diseno/lienzo/). El lienzo solo se ve dibujado en el artefacto. Si el dueño del proyecto lo edita a mano, la copia del repositorio queda atrás: hay que volver a traerla.

Existe un tercer artefacto, "Vitalia Salud", de agosto: es el demo comercial de la versión anterior, con otra paleta y otro alcance, y no es referencia.

## 4. Etapas del Desarrollo

Son once, en este orden. Las tres primeras preparan el terreno; las ocho siguientes construyen las historias en el orden de [RELACIONES.md](historias-de-usuario/RELACIONES.md).

### Etapa 0 · Preparación

No se escribe código de la aplicación. Depende casi toda del dueño del proyecto.

| Qué hace falta | Quién | Para qué |
|---|---|---|
| Repositorio remoto privado (propuesta: GitHub) | Dueño del proyecto | Hoy la única copia está en un computador. Render además lo necesita para desplegar. Al crearlo, la rama `master` pasa a llamarse `main` |
| PostgreSQL instalado en el computador | Dueño del proyecto | Sin una base local no se pueden probar los permisos por fila. Ya hay Python, Node, `uv` y git |
| Tablero Kanban en Jira | Dueño del proyecto lo crea; después se cargan las 9 épicas y las 46 historias | Llevar el trabajo. El proyecto anterior es de tipo Scrum y se archiva |
| Cuenta y clave del proveedor de IA | Dueño del proyecto | La primera prueba de concepto |

**Termina cuando** el repositorio está en el remoto y PostgreSQL responde en el computador.

### Etapa 1 · Esqueleto

Se arma la estructura vacía sobre la que cae todo lo demás. Todavía sin historias.

- `servidor/` con las cuatro capas de la [arquitectura](diseno/01-arquitectura.md) y la prueba que falla si una capa importa lo que no debe.
- `pantallas/` con las variables de color, letra y sombra de la [base visual](diseno/08-base-visual.md) y los iconos de Phosphor.
- Pruebas automáticas corriendo en cada cambio: estilo, tipos, capas, servidor contra PostgreSQL y pantallas.
- Los adaptadores de desarrollo (archivos en carpeta, correo en consola, IA de mentira) y el guion de datos inventados.

**Termina cuando** las pruebas corren solas y una pantalla vacía recibe respuesta de la API.

### Etapa 2 · Pruebas de concepto

Despejan las cuatro dudas de la [arquitectura](diseno/01-arquitectura.md) antes de construir en serio.

| Duda | Cómo se prueba | Qué necesita |
|---|---|---|
| ¿La lectura de fotos y de letra a mano es suficientemente buena? | Guion de la sección 10 de la [guía del asistente](diseno/07-como-se-construye-el-asistente.md), con cinco documentos inventados, uno de ellos largo | Proveedor de IA |
| ¿El asistente cita bien el documento y la página? | Preguntas con respuesta conocida, en el mismo guion | Proveedor de IA |
| ¿Los permisos por fila funcionan con un usuario sin privilegios en Render, y con las funciones para lo que pasa sin sesión? | Crear el usuario, dos pacientes y comprobar que uno no ve al otro | Cuenta de Render |
| ¿La cookie de sesión funciona entre el sitio y la API? | Un ingreso mínimo publicado en Render | Cuenta de Render y un dominio propio |

**Criterio para seguir con la IA:** cero inventos, origen correcto en al menos nueve de cada diez respuestas y lectura aceptable de la foto nítida.

**Termina cuando** cada duda tiene su respuesta escrita aquí. Si una falla, se ajusta el diseño antes de seguir.

### Etapas 3 a 10 · Construcción

| Etapa | Qué se construye | Historias | Puntos | Qué necesita |
|---|---|---|---|---|
| 3 · Cimientos | Roles, permisos por fila, bitácora y almacenamiento privado | HU-006, HU-036, HU-037, HU-027 | 23 | Almacenamiento de archivos |
| 4 · Identidad | Cuenta del médico, registro, autorización de datos, ingreso con documento, recuperación y cierre de sesión | HU-001 a HU-005, HU-007 | 21 | Servicio de correo |
| 5 · Calendario | Horario, tipos de cita, bloqueos y cálculo de espacios libres | HU-008 a HU-011 | 19 | — |
| 6 · Citas y panel | Citas de paciente y de médico, agenda, calendario, pacientes, ficha, corrección de datos y avisos por correo | HU-012 a HU-026, HU-040 | 57 | — |
| 7 · Documentos | Carga, lista, visor y lectura de documentos | HU-028 a HU-031 | 21 | Proveedor de IA, para leer fotos |
| 8 · Asistente | Autorización de IA, aislamiento por paciente, preguntas y resumen | HU-032 a HU-035 | 24 | Proveedor de IA |
| 9 · Tratamientos | Registro por el médico y consulta del paciente | HU-038, HU-039 | 8 | — |
| 10 · Historia clínica | Datos de identificación, pantalla de atención, consulta, cierre con firma, historial y copia | HU-041 a HU-046 | 27 | Listas oficiales de diagnósticos y municipios |
| | | **46** | **200** | |

Las etapas 6 y 7 pueden avanzar al tiempo. La 9 solo necesita la ficha del paciente, así que se puede adelantar. La 10 necesita la ficha, la agenda y el tratamiento, y funciona aunque el asistente todavía no esté.

**Cómo avanza cada historia.** Pasa por las columnas del [tablero](planificacion/05-kanban.md). En la columna Diseño se fija lo que a propósito no se definió antes:

- Campos exactos de cada operación, códigos de error, permisos y tipo de cada columna.
- La pantalla, si no está en el lienzo: se arma con las piezas de la [base visual](diseno/08-base-visual.md), siguiendo el prototipo.
- Textos: borrador de la política de datos y de la autorización de IA (HU-003, HU-032) y plantillas de los correos (HU-005, HU-019, HU-024, HU-040).

En Desarrollo se escribe con sus pruebas; en Pruebas se revisa contra los criterios de aceptación en el ambiente de pruebas de Render; en Despliegue pasa a producción.

### Antes de usar datos reales

Todo lo anterior se construye y se prueba con datos inventados. Para atender pacientes reales hace falta:

1. **La respuesta del abogado** a tres de las ocho preguntas del [marco normativo](planificacion/03-marco-normativo.md): la 2 (datos fuera de Colombia), la 5 (envío del Resumen Digital de Atención) y la 7 (firma de la historia clínica).
2. **Contrato de tratamiento de datos** con el proveedor de IA y con el de alojamiento.
3. **Un médico que revise los campos de la historia clínica** (sección 4.2 del marco normativo). La norma deja ese detalle a la práctica médica.
4. **Respaldo de largo plazo.** Render restaura hasta 3 días atrás, 7 en el plan Pro, y la historia clínica se conserva 15 años: hay que programar una exportación periódica.

## 5. Lo que el dueño del proyecto tiene pendiente

1. **Las cuatro cosas de la etapa 0.**
2. **Ver el lienzo.** Los cambios del 13 de octubre nadie los ha visto dibujados: estados en caja con sombra, sombra en botones y tarjetas, notas sin caja amarilla, la pantalla de atención del médico y la de ingreso con documento.
3. **Buscar el abogado y el médico** de la lista anterior. No frenan el desarrollo, pero sí el uso real.

## 6. Lo que no está verificado

| Tema | Situación |
|---|---|
| Cambios del 13 de octubre en el lienzo | Se revisó que el código esté bien formado; no se vieron dibujados |
| Resto del lienzo | Aprobado por el dueño del proyecto como base visual. El contraste del texto se midió y pasa el nivel AA |
| Prototipo navegable | Probado con 143 comprobaciones automáticas. A la vista solo se revisó una pantalla. No refleja las decisiones del 13 de octubre: ver la sección 6 de [05-pantallas.md](diseno/05-pantallas.md) |
| Permisos por fila sin sesión | El diseño con funciones de la base está escrito, no probado. Lo despeja la etapa 2 |
| Herramientas de [09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md) | Son propuestas; no se han instalado ni probado juntas. `pypdfium2` reemplaza a PyMuPDF por licencia y falta probar qué tan bien lee |
| Phosphor Icons | Confirmada por el dueño del proyecto. Falta comprobar que tenga todos los iconos médicos que usa Vitalia |
| Campos clínicos de la historia clínica | La lista la armó quien levantó los requisitos; falta que la revise un médico |
| Proyecto de resolución que reemplazaría la 1995 de 1999 | Publicado el 22 de julio de 2026. Al 13 de octubre no se encontró expedido. Solo se leyó su memoria justificativa, no el articulado |
| Lista vigente de tipo y finalidad de consulta | Está en un anexo de la Resolución 948 de 2026 que no se pudo consultar |
| Precios de Render y de los modelos de IA | Vienen de artículos de terceros |
| Privilegios del usuario por defecto de la base en Render | Su documentación no los indica; lo despeja la etapa 2 |
| Memoria del servicio más pequeño de Render (512 MB) para leer escaneados | Sin medir |
| Uso de datos por Qwen | Su política de no entrenar con datos de clientes se conoce por fuentes de terceros |
| Fragmentos de código de la guía del asistente | Son esquemas sin ejecutar |
| Supuestos S-01 a S-23 | Se ajustan cuando haya un médico real |

**Confirmado el 13 de octubre de 2026 en la documentación oficial de Render:** no hay región en Latinoamérica (Oregon, Ohio, Virginia, Fráncfort y Singapur); el plan gratuito se duerme a los 15 minutos y su base se elimina a los 30 días, sin respaldos; se pueden crear usuarios adicionales de base de datos; se puede desplegar solo después de que pasan las pruebas, y correr las migraciones antes de cada despliegue.

## 7. Reglas que no se pueden olvidar

- **Solo datos inventados o anonimizados** hasta cumplir la lista de "Antes de usar datos reales".
- Lo que sube el paciente son antecedentes. La historia clínica de las atenciones del consultorio va aparte, en la épica E9.
- Una atención cerrada y un tratamiento guardado no se modifican ni se borran.
- El asistente ayuda a leer los antecedentes, pero no escribe la historia clínica.
- El documento identifica a la persona al ingresar; nunca hace de contraseña.
- Sin autorización del paciente no hay asistente, y las fotos no se envían al proveedor de IA.
- Ninguna clave entra al repositorio.
- Lo que quedó para después: envío del Resumen Digital de Atención, cuentas de menores de edad, recordatorios de medicamento, factura con Factus, agente de voz y RIPS.

## 8. Forma de trabajo acordada

- Kanban sobre las cinco fases del ciclo de vida; primero las bases, después el código.
- Solo lo útil: sin generadores, sin funciones "por si acaso".
- Lo ya hecho y aprobado no se toca; se completa lo que falte.
- El diseño no debe verse genérico: reglas en la sección 6 de la [base visual](diseno/08-base-visual.md).
- Arquitectura limpia y código rápido: las reglas del consultorio no dependen de la tecnología, y la rapidez se mide antes de optimizar.
- Pocas preguntas: se decide, se escribe el supuesto y se corrige sobre el documento.
- Los commits van solo a nombre del dueño del proyecto, sin coautor, y en español.
