# Vitalia Salud

Sistema a la medida para **un consultorio médico general privado en Colombia**. El médico maneja su agenda y a sus pacientes, y cuenta con un asistente de inteligencia artificial que lee las historias clínicas que el paciente sube y responde preguntas sobre ellas.

**Estado:** fase de Planificación cerrada para el flujo principal. Sin desarrollo iniciado.
**Última actualización:** 12 de octubre de 2026

---

## Por dónde empezar

| Si quiere… | Abra |
|---|---|
| Entender qué se va a construir y el recorrido completo | [planificacion/01-alcance-y-flujo.md](planificacion/01-alcance-y-flujo.md) |
| Ver los requisitos | [planificacion/02-requisitos.md](planificacion/02-requisitos.md) |
| Saber qué exige la ley | [planificacion/03-marco-normativo.md](planificacion/03-marco-normativo.md) |
| Revisar qué se decidió y qué se supuso | [planificacion/04-decisiones-y-supuestos.md](planificacion/04-decisiones-y-supuestos.md) |
| Ver cómo se organiza el trabajo | [planificacion/05-kanban.md](planificacion/05-kanban.md) |
| Leer una historia de usuario | [historias-de-usuario/](historias-de-usuario/) |
| Saber qué se construye antes que qué | [historias-de-usuario/RELACIONES.md](historias-de-usuario/RELACIONES.md) |

---

## Ciclo de vida

| Fase | Estado | Qué hay |
|---|---|---|
| **1. Planificación** | Hecha para el flujo principal | Alcance, requisitos, marco normativo, historias y tareas |
| **2. Diseño** | Siguiente | Tecnología, modelo de datos, pantallas, contrato de los servicios. Las decisiones abiertas están en [04-decisiones-y-supuestos.md](planificacion/04-decisiones-y-supuestos.md) |
| **3. Desarrollo** | Sin iniciar | — |
| **4. Pruebas** | Sin iniciar | — |
| **5. Despliegue** | Sin iniciar | — |

El trabajo se lleva con **Kanban**: las historias avanzan por estas fases con un tope de tarjetas en curso por columna.

---

## Cifras del backlog

| Elemento | Cantidad |
|---|---|
| Épicas | 7 |
| Requisitos funcionales | 37 |
| Requisitos no funcionales | 14 |
| Historias de usuario | 37 |
| Criterios de aceptación | 151 (mínimo 3 por historia) |
| Tareas | 84 |
| Actividades | 248 |
| Puntos de historia | 162 |

| Épica | Historias | Puntos |
|---|---|---|
| [E1 Cuentas e ingreso](historias-de-usuario/E1-cuentas-e-ingreso/README.md) | 7 | 26 |
| [E2 Calendario de disponibilidad](historias-de-usuario/E2-calendario-de-disponibilidad/README.md) | 4 | 19 |
| [E3 Citas](historias-de-usuario/E3-citas/README.md) | 9 | 32 |
| [E4 Panel del médico](historias-de-usuario/E4-panel-del-medico/README.md) | 6 | 22 |
| [E5 Historias clínicas del paciente](historias-de-usuario/E5-historias-clinicas-del-paciente/README.md) | 5 | 26 |
| [E6 Asistente de IA](historias-de-usuario/E6-asistente-de-ia/README.md) | 4 | 24 |
| [E7 Seguridad base](historias-de-usuario/E7-seguridad-base/README.md) | 2 | 13 |

---

## Estructura de la carpeta

```
vitalia-proyecto/
├── README.md                    este archivo
├── planificacion/
│   ├── 01-alcance-y-flujo.md
│   ├── 02-requisitos.md
│   ├── 03-marco-normativo.md
│   ├── 04-decisiones-y-supuestos.md
│   └── 05-kanban.md
├── historias-de-usuario/
│   ├── RELACIONES.md            qué historia depende de cuál
│   ├── E1-cuentas-e-ingreso/
│   │   ├── README.md            índice de la épica
│   │   └── HU-001-….md          una historia por archivo
│   └── … (7 épicas)
└── archivo/
    └── v1/                      versión anterior del proyecto, solo de consulta
```

Cada historia trae: narrativa, criterios de aceptación en formato *dado / cuando / entonces*, tareas con sus actividades, requisito de origen y relaciones con otras historias.

---

## Roles

| Rol | Qué puede hacer |
|---|---|
| **Médico** | Configura el consultorio y su horario, maneja las citas, registra pacientes, lee sus documentos y pregunta al asistente |
| **Paciente** | Se registra, maneja sus citas, sube sus historias clínicas y autoriza o no el uso de inteligencia artificial |

---

## Lo innegociable

1. **Nunca** el documento de identidad como clave de ingreso.
2. **Nunca** una tabla con datos de salud sin política de acceso en la base de datos.
3. **Nunca** una clave de un proveedor externo dentro del navegador.
4. **Nunca** documentos de un paciente enviados a la inteligencia artificial sin su autorización, ni mezclados con los de otro.
5. **Nunca** un documento clínico en almacenamiento público.

---

## Lo que queda para después

Nota clínica escrita por el médico, plan de tratamiento, recordatorios, factura electrónica con Factus, agente de voz para citas, y los reportes RDA y RIPS. El detalle y la razón están en [01-alcance-y-flujo.md](planificacion/01-alcance-y-flujo.md).

> Los documentos que sube el paciente no reemplazan la historia clínica que el consultorio debe llevar de sus propias atenciones. Esa parte es lo primero que conviene levantar después.

---

## Pendientes inmediatos

- Crear el tablero Kanban y cargar las 37 historias ([05-kanban.md](planificacion/05-kanban.md)).
- Llevar al abogado las seis preguntas del [marco normativo](planificacion/03-marco-normativo.md).
- Abrir la fase de Diseño con las decisiones A-01 a A-06.

---

## Material de la versión anterior

`archivo/v1/` conserva el backlog original (74 historias pensadas para clínicas) y su arquitectura. Sirve de consulta cuando se retome lo que quedó para después; no describe el producto actual. El demo visual que acompañaba esa versión tampoco refleja este alcance.
