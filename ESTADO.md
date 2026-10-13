# Estado del proyecto y siguientes pasos

**Fecha:** 13 de octubre de 2026
**Para qué sirve este archivo:** retomar el trabajo sin releer toda la conversación. Léalo primero.

---

## 1. Qué es Vitalia

Sistema a la medida para **un consultorio médico general privado en Colombia**. Dos usuarios: el **médico**, que hace todo lo del consultorio, y el **paciente**. No se vende a otros consultorios.

Lo que cubre el alcance actual: cuentas, calendario de disponibilidad, citas de ambos lados, panel del médico, historias clínicas que sube el paciente, asistente de IA sobre esos documentos y tratamientos.

## 2. Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Alcance y flujo principal | [planificacion/01-alcance-y-flujo.md](planificacion/01-alcance-y-flujo.md) |
| 39 requisitos funcionales y 14 no funcionales | [planificacion/02-requisitos.md](planificacion/02-requisitos.md) |
| Leyes y seis preguntas para el abogado | [planificacion/03-marco-normativo.md](planificacion/03-marco-normativo.md) |
| Decisiones (D-01 a D-19) y supuestos (S-01 a S-13) | [planificacion/04-decisiones-y-supuestos.md](planificacion/04-decisiones-y-supuestos.md) |
| Reglas del tablero Kanban | [planificacion/05-kanban.md](planificacion/05-kanban.md) |
| 39 historias en 8 épicas, con criterios y tareas | [historias-de-usuario/](historias-de-usuario/) |
| Orden de construcción | [historias-de-usuario/RELACIONES.md](historias-de-usuario/RELACIONES.md) |
| Tecnología, capas del código y reglas de rendimiento | [diseno/01-arquitectura.md](diseno/01-arquitectura.md) |
| Tablas y permisos por fila | [diseno/02-modelo-de-datos.md](diseno/02-modelo-de-datos.md) |
| Operaciones de la API | [diseno/03-api.md](diseno/03-api.md) |
| Decisiones del asistente de IA | [diseno/04-asistente-ia.md](diseno/04-asistente-ia.md) |
| Inventario de pantallas | [diseno/05-pantallas.md](diseno/05-pantallas.md) |
| Diagramas de arquitectura en Mermaid | [diseno/06-diagramas-de-arquitectura.md](diseno/06-diagramas-de-arquitectura.md) |
| Cómo se construye el asistente, paso a paso | [diseno/07-como-se-construye-el-asistente.md](diseno/07-como-se-construye-el-asistente.md) |
| Versión anterior del proyecto (solo consulta) | `archivo/v1/` |

**Fuera del repositorio**

| Qué | Enlace |
|---|---|
| Prototipo navegable (comportamiento) | https://claude.ai/artifact/4MN2vq99tcrQBzUWDJ4pEy |
| Lienzo de diseño pulido (aspecto) | https://claude.ai/artifact/R6WLHr5eAt7FQztseugqQY |

El código del prototipo está en [diseno/prototipo/index.html](diseno/prototipo/index.html). El código del lienzo vive solo en el artefacto.

## 3. Qué está hecho

| Fase | Estado | Detalle |
|---|---|---|
| **1. Planificación** | Hecha | Alcance, requisitos, marco normativo, 39 historias con 166 criterios y 89 tareas |
| **2. Diseño** | Hecha en su primera versión; queda así por ahora (D-18) | Arquitectura, modelo de datos, API, asistente, pantallas, prototipo navegable, lienzo pulido y diagramas |
| **3. Desarrollo** | Sin iniciar | No hay código de la aplicación |
| **4. Pruebas** | Sin iniciar | — |
| **5. Despliegue** | Sin iniciar | — |

**Tecnología decidida:** Python con FastAPI, PostgreSQL en Render, React con Vite y TypeScript, archivos en almacenamiento compatible con S3, y Qwen como modelo de IA de la primera versión detrás de un adaptador intercambiable. El código se organiza con arquitectura limpia (D-19).

## 4. Siguientes pasos, en orden

Planificación y Diseño ya están confirmados en git. Los commits van solo a nombre del dueño del proyecto, sin coautor. El repositorio no tiene remoto: la única copia está en este computador.

1. **Prueba de concepto de la IA.** Es la de mayor riesgo. El plan está en la sección 10 de [07-como-se-construye-el-asistente.md](diseno/07-como-se-construye-el-asistente.md): un guion suelto con cinco documentos inventados, uno de ellos largo, antes de tocar la aplicación. Hace falta una cuenta en el proveedor de IA y su clave.
2. **Las otras tres pruebas de concepto** de la [arquitectura](diseno/01-arquitectura.md): permisos por fila en Render, cookie de sesión entre el sitio y la API, y calidad de las citas de origen.
3. **Crear el tablero Kanban.** Hay que crear a mano un proyecto de tipo Kanban en Jira; luego se cargan las 8 épicas y las 39 historias. El proyecto anterior es de tipo Scrum y se archiva.
4. **Llevar las seis preguntas al abogado.** La segunda (datos fuera de Colombia) condiciona el uso de datos reales.
5. **Mostrar el prototipo a un médico**, cuando lo haya, y ajustar los supuestos.
6. **Empezar Desarrollo** por los cimientos: HU-006, HU-036, HU-037 y HU-027, con las capas y las reglas de rendimiento de las secciones 7 y 8 de la [arquitectura](diseno/01-arquitectura.md).

**En pausa por decisión del 13 de octubre (D-18).** El diseño queda como está por ahora. Cuando se retome: revisar los [diagramas](diseno/06-diagramas-de-arquitectura.md), aprobar el lienzo, llevar su aspecto al prototipo navegable y diseñar las pantallas que le faltan (recuperar contraseña, subir documento, visor, perfil, configuración, bitácora, registrar tratamiento, lista de pacientes, vistas de día y semana).

## 5. Lo que no está verificado

| Tema | Situación |
|---|---|
| Lienzo de diseño | No se revisó a la vista; los tamaños se calcularon a mano. El dueño del proyecto lo vio y lo aprobó en general |
| Prototipo navegable | Probado con 143 comprobaciones automáticas. A la vista solo se revisó una pantalla; no se revisó celular ni modo oscuro |
| Precios de Render y de los modelos de IA | Vienen de artículos de terceros |
| Privilegios del usuario por defecto de la base en Render | Su documentación no los indica; lo despeja la prueba de permisos por fila |
| Memoria del servicio más pequeño de Render (512 MB) para leer escaneados | Sin medir |
| Respaldo de la base por más de 7 días | Render restaura hasta 3 días atrás (7 en el plan Pro). Está por decidir si se programa una exportación periódica |
| Uso de datos por Qwen | Su política de no entrenar con datos de clientes se conoce por fuentes de terceros |
| Fragmentos de código de la guía del asistente | Son esquemas sin ejecutar |
| Supuestos S-01 a S-13 | Se ajustan cuando haya un médico real |

**Confirmado el 13 de octubre de 2026 en la documentación oficial de Render:** no hay región en Latinoamérica (Oregon, Ohio, Virginia, Fráncfort y Singapur); el plan gratuito se duerme a los 15 minutos y su base se elimina a los 30 días, sin respaldos; se pueden crear usuarios adicionales de base de datos.

## 6. Reglas que no se pueden olvidar

- **Solo datos inventados o anonimizados** hasta tener la respuesta del abogado y un contrato de tratamiento de datos con el proveedor de IA y con el de alojamiento.
- Lo que sube el paciente son antecedentes. No reemplaza la historia clínica que el consultorio debe llevar de sus propias consultas; la nota clínica del médico quedó para después.
- Un tratamiento guardado no se modifica ni se borra.
- Sin autorización del paciente no hay asistente, y las fotos no se envían al proveedor de IA.
- Lo que quedó para después: nota clínica, recordatorios de medicamento, factura con Factus, agente de voz, RDA y RIPS.

## 7. Forma de trabajo acordada

- Kanban sobre las cinco fases del ciclo de vida; primero las bases, después el código.
- Solo lo útil: sin generadores, sin funciones "por si acaso".
- Arquitectura limpia y código rápido: las reglas del consultorio no dependen de la tecnología, y la rapidez se mide antes de optimizar.
- Pocas preguntas: se decide, se escribe el supuesto y se corrige sobre el documento.
