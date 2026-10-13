# Vitalia Salud

Aplicación de salud para consultorios y clínicas pequeñas y medianas en Colombia. Cubre el ciclo completo del paciente: **agendar cita → consulta con historia clínica digital → plan de tratamiento claro → recordatorios por WhatsApp → seguimiento de adherencia**.

El diferencial frente a la competencia (Alegra, Dentalink, Okvet, agendadores genéricos) es que no se queda en agendar y archivar: **acompaña activamente al paciente después de la consulta**.

**Estado:** producto definido y priorizado. Sin desarrollo iniciado.
**Última actualización:** 29 de septiembre de 2026

---

## Por dónde empezar

| Si quiere… | Abra |
|---|---|
| Entender qué se va a construir y por qué | Este archivo, y luego [documentos/requisitos-y-epicas.md](documentos/requisitos-y-epicas.md) |
| Ver cómo se construye | [arquitectura.md](arquitectura.md) |
| Leer una historia de usuario concreta | [historias-de-usuario/](historias-de-usuario/) |
| Saber qué se construye antes que qué | [historias-de-usuario/RELACIONES.md](historias-de-usuario/RELACIONES.md) |
| Ver el producto funcionando | El demo (enlace abajo) |

---

## El problema

El software existente resuelve la agenda y archiva un PDF, pero abandona al paciente en el momento en que sale del consultorio. El resultado clínico queda dependiendo de que el paciente recuerde, entienda y cumpla un plan escrito en un papel.

La población objetivo agrava esto: adultos mayores y pacientes con baja alfabetización digital. Por eso **WhatsApp es canal de primera clase, no un extra**: nadie tiene que descargar una app ni recordar una contraseña para recibir su tratamiento.

---

## Cifras del backlog

| Elemento | Cantidad |
|---|---|
| Épicas | 12 |
| Requisitos funcionales | 60 |
| Requisitos no funcionales | 16 |
| Historias de usuario | 74 |
| Criterios de aceptación | 288 (mínimo 3 por historia) |
| Tareas | 161 |
| Actividades | 475 |
| Puntos de historia | 433 |

**Por fase:** Fase 1 (MVP) 37 historias / 191 puntos · Fase 2 (adherencia) 17 / 104 · Fases 3-4 (escalamiento e interoperabilidad) 20 / 138.

---

## Las cuatro fases

| Fase | Qué entrega | Por qué ese corte |
|---|---|---|
| **1 — MVP** | Autenticación, agenda, historia clínica digital, plan de tratamiento y recordatorios por WhatsApp/SMS | Con esto un consultorio ya opera completo |
| **2 — Adherencia** | Agendamiento conversacional por WhatsApp, confirmación de tomas, panel de adherencia, alertas | Aquí se vuelve demostrable el diferencial del producto |
| **3 — Escalamiento** | Multi-sede, administración y reportes, cuidador autorizado, asistente de IA, accesibilidad avanzada | Habilita clínicas con varias sedes |
| **4 — Interoperabilidad** | Resumen Digital de Atención (RDA) | Solo si el producto apunta a IPS formales |

**Riesgo consciente del corte:** en la Fase 1 los recordatorios salen, pero nadie confirma que se cumplieron. La adherencia todavía no se mide. Es suficiente para operar, pero **no** para vender el diferencial: por eso la Fase 2 no es opcional y debe ir inmediatamente después.

---

## Estructura de esta carpeta

```
vitalia-proyecto/
├── README.md                      este archivo
├── arquitectura.md                cómo se construye y por qué
├── documentos/
│   ├── requisitos-y-epicas.md     60 RF, 16 RNF, actores, trazabilidad, glosario
│   ├── story-map.md               mapa de historias por fase de entrega
│   ├── estado-carga-jira.md       qué está cargado en Jira y con qué clave
│   └── jira-import.csv            backlog completo listo para importar
└── historias-de-usuario/
    ├── RELACIONES.md              qué historia depende de cuál
    ├── E01-autenticacion-cuentas-y-roles/
    │   ├── README.md              índice de la épica
    │   ├── HU-001-registro-de-paciente.md
    │   └── …
    ├── E02-gestion-de-citas/
    └── … (12 épicas)
```

Cada archivo de historia trae: narrativa, criterios de aceptación en formato *dado / cuando / entonces*, tareas con sus actividades, trazabilidad al requisito, clave de Jira y sus relaciones con otras historias.

---

## Dónde vive cada cosa

| Recurso | Dónde |
|---|---|
| **Backlog en Jira** | https://notapricolt-1789520939910.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog — requiere invitación al sitio |
| **Story map en Miro** | https://miro.com/app/board/uXjVHm9DhOI=/ |
| **Demo del producto** | https://claude.ai/code/artifact/7d0798af-6675-4df8-9967-5ed34504fdbf |
| **Código del demo** | `C:\Users\Javier\vitalia-demo\` (HTML, CSS y JS; sin backend) |
| **Generadores del backlog** | `C:\Users\Javier\vitalia-backlog\` |

### Estado de la carga en Jira

96 issues creados de 247: **12 épicas**, **37 historias** (toda la Fase 1) y **47 subtareas** (E1 y E2 completas). El detalle con cada clave está en [documentos/estado-carga-jira.md](documentos/estado-carga-jira.md).

Falta cargar: 37 historias (fases 2, 3 y 4) y 114 subtareas.

**Nota sobre los tipos de issue:** el proyecto de Jira no trae el tipo *Historia*, solo *Epic*, *Tarea* y *Subtask*. Las historias de usuario están cargadas como **Tarea** y se identifican con la etiqueta `historia-de-usuario`. Si se agrega el tipo *Historia* al proyecto, se pueden convertir en bloque.

---

## Roles del sistema

| Rol | Qué puede hacer |
|---|---|
| **Paciente** | Agenda citas, consulta su historia y su plan, recibe y confirma recordatorios |
| **Médico** | Atiende, registra diagnóstico y plan de tratamiento, consulta historia clínica, ve adherencia |
| **Cuidador / familiar** | Solo recordatorios y plan de cuidado. **Nunca** la historia clínica completa. Requiere consentimiento del paciente |
| **Administrador** | Gestiona profesionales, horarios y sedes; consulta reportes. Sin acceso clínico |
| **Sistema** | Envía recordatorios, calcula adherencia, detecta incumplimiento |

---

## Lo innegociable

Estos puntos vienen de fallas concretas de una versión anterior. No son preferencias:

1. **Nunca** cédula o EPS como mecanismo de autenticación.
2. **Nunca** políticas de base de datos abiertas (`USING true`) en tablas con datos de salud.
3. **Nunca** claves de API de terceros dentro del cliente.
4. **Nunca** historias clínicas completas a APIs de IA sin control ni consentimiento.
5. **Nunca** WhatsApp con librerías no oficiales o números personales: solo API oficial de Meta o un BSP certificado.

El detalle está en los requisitos no funcionales RNF-01 a RNF-16.

---

## Marco normativo

| Norma | Qué exige |
|---|---|
| **Ley 1581 de 2012** | Habeas Data — protección de datos sensibles de salud |
| **Ley 2015 de 2020** y **Resolución 1888 de 2025** | Historia clínica electrónica interoperable, RDA, control de accesos y trazabilidad |
| **Decreto 580 de 2024** | Validez de la historia clínica exclusivamente digital |

> Estas referencias provienen del brief del proyecto. **Antes de producción deben verificarse su vigencia y alcance con asesoría jurídica especializada en salud digital.**

---

## Decisiones pendientes

Cosas que el backlog asume y conviene confirmar con la clínica antes de comprometer fechas:

- Reglas de anticipación para cancelar y reagendar citas.
- Umbrales de adherencia que disparan la alerta al médico, y qué tratamientos se consideran críticos.
- Fuente del catálogo de medicamentos y de la base de interacciones.
- Stack técnico concreto (ver [arquitectura.md](arquitectura.md)).
