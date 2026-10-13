# Vitalia Salud

Sistema a la medida para **un consultorio médico general privado en Colombia**. El médico maneja su agenda y a sus pacientes, escribe la historia clínica de cada atención y cuenta con un asistente de inteligencia artificial que lee las historias clínicas que el paciente sube y responde preguntas sobre ellas.

**Estado:** Planificación y Diseño cerrados. Desarrollo en curso: esqueleto del servidor y de las pantallas listo; siguen los servicios en la nube y el registro e ingreso.
**Última actualización:** 13 de octubre de 2026

---

## Por dónde empezar

| Si quiere… | Abra |
|---|---|
| **Retomar el trabajo: qué está hecho y qué sigue** | [ESTADO.md](ESTADO.md) |
| Entender qué se va a construir y el recorrido completo | [planificacion/01-alcance-y-flujo.md](planificacion/01-alcance-y-flujo.md) |
| Ver los requisitos | [planificacion/02-requisitos.md](planificacion/02-requisitos.md) |
| Saber qué exige la ley | [planificacion/03-marco-normativo.md](planificacion/03-marco-normativo.md) |
| Revisar qué se decidió y qué se supuso | [planificacion/04-decisiones-y-supuestos.md](planificacion/04-decisiones-y-supuestos.md) |
| Ver cómo se organiza el trabajo | [planificacion/05-kanban.md](planificacion/05-kanban.md) |
| Ver con qué tecnología se construye y por qué | [diseno/01-arquitectura.md](diseno/01-arquitectura.md) |
| Ver las tablas de la base de datos | [diseno/02-modelo-de-datos.md](diseno/02-modelo-de-datos.md) |
| Ver las operaciones del servidor | [diseno/03-api.md](diseno/03-api.md) |
| Entender cómo funciona el asistente de IA | [diseno/04-asistente-ia.md](diseno/04-asistente-ia.md) |
| Recorrer las pantallas | [diseno/05-pantallas.md](diseno/05-pantallas.md), el [prototipo navegable](https://claude.ai/artifact/4MN2vq99tcrQBzUWDJ4pEy) y el [lienzo de diseño](https://claude.ai/artifact/R6WLHr5eAt7FQztseugqQY) |
| Ver los diagramas de arquitectura | [diseno/06-diagramas-de-arquitectura.md](diseno/06-diagramas-de-arquitectura.md) |
| Aprender cómo se construye el asistente de IA | [diseno/07-como-se-construye-el-asistente.md](diseno/07-como-se-construye-el-asistente.md) |
| Ver los colores, la letra y las piezas aprobados | [diseno/08-base-visual.md](diseno/08-base-visual.md) |
| Saber con qué herramientas se construye y cómo se despliega | [diseno/09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md) |
| Leer una historia de usuario | [historias-de-usuario/](historias-de-usuario/) |
| Saber qué se construye antes que qué | [historias-de-usuario/RELACIONES.md](historias-de-usuario/RELACIONES.md) |

---

## Ciclo de vida

| Fase | Estado | Qué hay |
|---|---|---|
| **1. Planificación** | Hecha | Alcance, requisitos, marco normativo con el contenido mínimo de la historia clínica, historias y tareas |
| **2. Diseño** | Cerrada en documentos el 13 de octubre | Arquitectura, modelo de datos, contrato de la API, diseño del asistente, pantallas y prototipo navegable |
| **3. Desarrollo** | En curso | Esqueleto en `servidor/` y `pantallas/`. Se construye por historias; el orden está en [ESTADO.md](ESTADO.md) |
| **4. Pruebas** | Sin iniciar | — |
| **5. Despliegue** | Sin iniciar | — |

El trabajo se lleva con **Kanban**: las historias avanzan por estas fases con un tope de tarjetas en curso por columna.

---

## Cifras del backlog

| Elemento | Cantidad |
|---|---|
| Épicas | 9 |
| Requisitos funcionales | 46 |
| Requisitos no funcionales | 15 |
| Historias de usuario | 46 |
| Criterios de aceptación | 205 (mínimo 3 por historia) |
| Tareas | 109 |
| Actividades | 321 |
| Puntos de historia | 200 |

| Épica | Historias | Puntos |
|---|---|---|
| [E1 Cuentas e ingreso](historias-de-usuario/E1-cuentas-e-ingreso/README.md) | 8 | 29 |
| [E2 Calendario de disponibilidad](historias-de-usuario/E2-calendario-de-disponibilidad/README.md) | 4 | 19 |
| [E3 Citas](historias-de-usuario/E3-citas/README.md) | 9 | 32 |
| [E4 Panel del médico](historias-de-usuario/E4-panel-del-medico/README.md) | 6 | 22 |
| [E5 Historias clínicas del paciente](historias-de-usuario/E5-historias-clinicas-del-paciente/README.md) | 5 | 26 |
| [E6 Asistente de IA](historias-de-usuario/E6-asistente-de-ia/README.md) | 4 | 24 |
| [E7 Seguridad base](historias-de-usuario/E7-seguridad-base/README.md) | 2 | 13 |
| [E8 Tratamientos](historias-de-usuario/E8-tratamientos/README.md) | 2 | 8 |
| [E9 Historia clínica del consultorio](historias-de-usuario/E9-historia-clinica-del-consultorio/README.md) | 6 | 27 |

---

## Estructura de la carpeta

```
vitalia-proyecto/
├── README.md                    este archivo
├── ESTADO.md                    qué está hecho y qué sigue
├── planificacion/
│   ├── 01-alcance-y-flujo.md
│   ├── 02-requisitos.md
│   ├── 03-marco-normativo.md
│   ├── 04-decisiones-y-supuestos.md
│   └── 05-kanban.md
├── diseno/
│   ├── 01-arquitectura.md
│   ├── 02-modelo-de-datos.md
│   ├── 03-api.md
│   ├── 04-asistente-ia.md
│   ├── 05-pantallas.md
│   ├── 06-diagramas-de-arquitectura.md
│   ├── 07-como-se-construye-el-asistente.md
│   ├── 08-base-visual.md        colores, letra y piezas aprobados
│   ├── 09-herramientas-y-entrega.md
│   ├── lienzo/                  fuente de las once pantallas del lienzo
│   └── prototipo/index.html     prototipo navegable
├── servidor/                    API en Python: capas, migraciones y pruebas
├── pantallas/                   aplicación web en React
├── historias-de-usuario/
│   ├── RELACIONES.md            qué historia depende de cuál
│   ├── E1-cuentas-e-ingreso/
│   │   ├── README.md            índice de la épica
│   │   └── HU-001-….md          una historia por archivo
│   └── … (9 épicas)
└── archivo/
    └── v1/                      versión anterior del proyecto, solo de consulta
```

Cada historia trae: narrativa, criterios de aceptación en formato *dado / cuando / entonces*, tareas con sus actividades, requisito de origen y relaciones con otras historias.

---

## Roles

| Rol | Qué puede hacer |
|---|---|
| **Médico** | Configura el consultorio y su horario, maneja las citas, registra pacientes, lee sus documentos, pregunta al asistente, escribe la historia clínica y registra tratamientos |
| **Paciente** | Se registra, maneja sus citas, sube sus historias clínicas, autoriza o no el uso de inteligencia artificial y consulta sus tratamientos |

---

## Lo innegociable

1. **Nunca** el documento de identidad como contraseña. El documento identifica a la persona; la contraseña es propia.
2. **Nunca** una tabla con datos de salud sin política de acceso en la base de datos.
3. **Nunca** una clave de un proveedor externo dentro del navegador.
4. **Nunca** documentos de un paciente enviados a la inteligencia artificial sin su autorización, ni mezclados con los de otro.
5. **Nunca** un documento clínico en almacenamiento público.
6. **Nunca** una atención cerrada de la historia clínica modificada o borrada.

---

## Lo que queda para después

Envío del Resumen Digital de Atención al Ministerio, cuentas para menores de edad, recordatorios de medicamento, factura electrónica con Factus, agente de voz para citas y el reporte RIPS. El detalle y la razón están en [01-alcance-y-flujo.md](planificacion/01-alcance-y-flujo.md).

> Los documentos que sube el paciente son antecedentes. La historia clínica de las atenciones del consultorio se lleva dentro del sistema (épica E9), con el contenido mínimo que exige la norma.

---

## Pendientes inmediatos

La lista vigente, en orden, está en la sección 4 de [ESTADO.md](ESTADO.md). Se lleva en un solo lugar para que no se desfase.

**Tecnología:** Python con FastAPI, PostgreSQL en Render, archivos en Cloudflare R2, React en las pantallas y Qwen como modelo de IA de la primera versión. El código se organiza con arquitectura limpia.

---

## Material de la versión anterior

`archivo/v1/` conserva el backlog original (74 historias pensadas para clínicas) y su arquitectura. Sirve de consulta cuando se retome lo que quedó para después; no describe el producto actual. El demo visual que acompañaba esa versión tampoco refleja este alcance.
