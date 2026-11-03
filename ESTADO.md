# Estado del proyecto

**Fecha:** 3 de noviembre de 2026
**Para qué sirve este archivo:** retomar el trabajo sin releer las conversaciones. Léalo primero. El detalle técnico de cada paso del desarrollo está en [estado_desarrollo.md](estado_desarrollo.md).

---

## 1. Qué es Vitalia

Sistema a la medida para **un consultorio médico general privado en Colombia**. Dos usuarios: el **médico**, que hace todo lo del consultorio desde el computador, y el **paciente**, que usa el celular. No se vende a otros consultorios.

Cubre: cuentas, horario y citas de los dos lados, panel del médico, historias clínicas que sube el paciente, un asistente de IA que busca en esos documentos, tratamientos y la historia clínica que el consultorio lleva de cada atención.

## 2. En qué va

| Fase | Estado | Detalle |
|---|---|---|
| **1. Planificación** | Hecha | Alcance, requisitos, marco normativo, 46 historias en 9 épicas, 212 criterios, 110 tareas, 200 puntos |
| **2. Diseño** | Hecha | Arquitectura limpia, modelo de datos con permisos por fila, API, asistente con RAG, pantallas, diagramas, base visual y herramientas |
| **3. Desarrollo** | **En curso** | 28 de 46 historias hechas o casi; 191 pruebas del servidor y 31 de pantallas en verde. Todo corre en el computador con PostgreSQL en Docker; nada se ha publicado. Sección 3 |
| **4. Pruebas** | Sin iniciar | Se hace en Render contra los criterios de aceptación |
| **5. Despliegue** | Sin iniciar | — |

**Código en GitHub:** https://github.com/JAOSjavi/vitalia (privado). Ramas `master` (hasta el bloque 2) y `bloque-3-documentos-e-ia` (todo lo de después). Ver la sección 5.

## 3. Lo que está hecho

### 3.1 Por bloques

| Bloque | Qué quedó | Rama |
|---|---|---|
| **1 · Registro e ingreso** (14 oct) | Roles y matriz de permisos, permisos por fila forzados en todas las tablas, bitácora, cuenta del médico con enlace de un solo uso, registro del paciente en tres pasos con la autorización de datos y la casilla de IA, ingreso con documento y contraseña con bloqueo por intentos, cierre de sesión | `master` |
| **2 · Citas** (26 oct) | Horario semanal, tipos de cita, cálculo de espacios libres, agendar, consultar, mover y cancelar de los dos lados, agenda de hoy con lo que falta configurar, lista y búsqueda de pacientes. Dos citas nunca ocupan el mismo tiempo: lo impide la base | `master` |
| **3 · Documentos y asistente de IA** (27 oct) | Subir PDF, JPG o PNG; leerlos por página; partirlos en fragmentos sin datos de identificación; vectores con Qwen; búsqueda por significado y por palabras dentro de un solo paciente (RAG, D-30); preguntar al asistente con cada cita comprobada contra lo enviado; ficha del paciente; ver y eliminar documentos | `bloque-3-documentos-e-ia` |
| **Interfaz según el lienzo** (27 oct) | Las pantallas se rehicieron copiando la estructura y las medidas del [lienzo](https://claude.ai/artifact/R6WLHr5eAt7FQztseugqQY): el paciente en celular y el médico en computador. Menú del médico, Hoy con la tarjeta de quien sigue y el avance del día, Calendario con día, semana y mes y los festivos de Colombia, inicio y citas del paciente | `bloque-3-documentos-e-ia` |
| **Asistencia y bloqueos** (27 oct) | Marcar atendida o no asistió y corregirlo el mismo día (HU-018). Bloquear horas o días: lo bloqueado deja de ofrecerse y un bloqueo que tapa citas pide moverlas o cancelarlas antes (HU-009) | `bloque-3-documentos-e-ia` |
| **Iconos y hovers** (27 oct) | Iconos de Hugeicons en trazo redondeado, elegidos entre siete bibliotecas (D-31). Respuesta sutil al pasar el cursor en todos los botones: color y sombra en 150 ms y elevación de 1 px | `bloque-3-documentos-e-ia` |

### 3.2 Por historia

| Estado | Historias |
|---|---|
| **Hechas** | HU-001, HU-002, HU-004, HU-006, HU-007, HU-036 · HU-008, HU-009, HU-010, HU-011, HU-012, HU-013, HU-014, HU-015, HU-016, HU-017, HU-018, HU-021, HU-023 · HU-028, HU-029, HU-031, HU-033 |
| **Hechas con algo pendiente** | HU-003 (falta aceptar una versión nueva del texto y verla en el perfil) · HU-020 (falta la tarjeta de tratamiento) · HU-022 (falta mostrar el tiempo libre y crear la cita tocando un espacio) · HU-025 (faltan los tratamientos en la ficha) · HU-027 (los archivos van a una carpeta local; falta R2 con enlace firmado de 15 minutos) · HU-030 (el documento abre en otra pestaña en su página; falta el visor propio con la frase resaltada) · HU-032 (la casilla está en el registro; falta cambiarla después y que al autorizar se lean los documentos pendientes) · HU-034 (construida y probada con una IA de prueba; falta probarla con Qwen) · HU-037 (falta la pantalla de consulta de la bitácora) |
| **Sin empezar** | HU-005 recuperar contraseña · HU-019 avisos por correo · HU-024 registrar paciente desde el panel · HU-026 botón de cobro · HU-035 resumen del paciente · HU-038 y HU-039 tratamientos · HU-040 corregir datos del paciente · HU-041 a HU-046 historia clínica del consultorio |

### 3.3 Lo que se probó

- **Servidor:** 191 pruebas en verde contra PostgreSQL 18 con `pgvector` en Docker, una o más por criterio de aceptación. Las 10 migraciones se aplican, se deshacen y se vuelven a aplicar.
- **Pantallas:** 31 pruebas en verde y construcción sin errores.
- **En el navegador**, contra la API y la base de Docker: registro e ingreso; agendar, mover y cancelar; Hoy con asistencia; calendario en sus tres vistas; bloquear un día con citas (las lista y no guarda) y sin citas (guarda y aparece); subir documentos y verlos; ficha del paciente.
- **El asistente:** la búsqueda se midió con Qwen y 12 historias clínicas inventadas: trajo los 16 datos esperados entre los 12 fragmentos y 14 entre los 3 primeros. Las respuestas no se han probado con Qwen, porque el modelo de respuestas seguía bloqueado (sección 4).

## 4. Lo que se necesita del dueño del proyecto

En orden de urgencia. Ninguna clave pasa por el chat ni entra al repositorio: todas van en `servidor/.env`.

| # | Qué | Para qué | Cómo |
|---|---|---|---|
| 1 | **Poner `master` como rama principal en GitHub** | Que el repositorio abra en la rama estable | GitHub → `vitalia` → Settings → Default branch → `master` → Update |
| 2 | **Confirmar que Alibaba aprobó la verificación de identidad** | Sin ella, `qwen3.7-plus` (respuestas) y `qwen-vl-ocr-2025-11-20` (lectura de fotos) responden `AccessDenied.Unpurchased`. Estaba en revisión desde el 27 de octubre | Consola de Alibaba Cloud Model Studio. Los vectores (`qwen3.7-text-embedding`) ya funcionan |
| 3 | **Dos fotos con datos inventados**: una hoja impresa y un texto corto escrito a mano | Medir la lectura de fotos con IA | Se le entregan los datos para copiar |
| 4 | **Crear la base en Render** (PostgreSQL 18, región Virginia) | Publicar y correr las pruebas de la fase 4 | Paso a paso en la sección 3 de [herramientas y entrega](diseno/09-herramientas-y-entrega.md). El plan gratuito vence a los 30 días |
| 5 | **Crear el espacio en Cloudflare R2** (`vitalia-dev`, con una clave limitada a ese espacio) | Guardar los documentos fuera del computador y abrirlos con enlace firmado | Misma sección 3 |
| 6 | **Tablero Kanban en Jira** | Seguir las historias. El proyecto que existe es de tipo Scrum | No frena el código |
| 7 | **Un abogado y un médico** | Antes de usar datos reales (sección 9) | No frenan el desarrollo |
| 8 | **Revisar el lienzo** | El tablero "Paciente · Inicio" del artefacto quedó borrado salvo la barra de abajo. La copia completa está en `diseno/lienzo/Main.dc.html`. Decir si se borró a propósito | — |

## 5. Lo que sigue

### 5.1 Inmediato, sin depender de nadie

1. **Unir el bloque 3 a `master`.** Abrir en GitHub una solicitud de cambio de `bloque-3-documentos-e-ia` hacia `master`, revisarla y unirla. Las pruebas automáticas de `.github/workflows/pruebas.yml` deberían correr ahí por primera vez.
2. **Terminar lo que el bloque 3 dejó a medias:**
   - Cambiar la autorización de IA desde el perfil o desde Mis documentos, y que al autorizar entren a la cola los documentos sin leer y los legibles (HU-032).
   - Resumen del paciente en la ficha (HU-035): un resumen por documento al indexarlo y uno del paciente hecho con esos resúmenes.
   - Visor propio de documentos con la frase citada resaltada (HU-030).
3. **Completar el calendario:** mostrar el tiempo libre y crear una cita tocando un espacio (HU-022, CA-1 y CA-2).

### 5.2 Cuando Qwen esté aprobado

4. Correr las preguntas del [README de las historias de prueba](documentos-de-prueba/historias-clinicas/README.md) contra el asistente y medir: cero inventos, origen correcto en al menos nueve de cada diez respuestas y abstención en las preguntas de diagnóstico.
5. Medir la lectura de las dos fotos.

### 5.3 Cuando existan Render y R2

6. Adaptador de R2 con enlace firmado de 15 minutos (HU-027). Hoy los archivos van a `servidor/.archivos/` con un adaptador que cumple el mismo puerto.
7. Conectar a Render, crear `vitalia_api` sin privilegios, activar `pgvector` y correr las pruebas contra esa base. Despeja si los permisos por fila funcionan allá.
8. Publicar API y pantallas en Render y comprobar que la cookie de sesión funciona entre los dos.

### 5.4 Historias que faltan, en este orden

| Orden | Historias | Necesita |
|---|---|---|
| 1 | Tratamientos: registrarlos y que el paciente los vea (HU-038, HU-039) | — |
| 2 | Registrar un paciente desde el panel y corregir sus datos (HU-024, HU-040) | HU-024 manda un correo de activación |
| 3 | Recuperar contraseña y avisos por correo de cambios en la cita (HU-005, HU-019) | Un servicio de correo |
| 4 | Historia clínica del consultorio: identificación, pantalla de atención con el asistente al lado, registrar, cerrar y firmar, consultar y copia para el paciente (HU-041 a HU-046) | El médico que revise los campos. Al cerrar una atención, se indexa para el asistente si el paciente aceptó la versión 2 del texto de IA, que falta escribir |
| 5 | Pantalla de la bitácora y botón de cobro (HU-037 CA-4, HU-026) | — |

## 6. Cómo levantar todo en el computador

1. Abrir Docker Desktop.
2. En la raíz del proyecto: `docker compose up -d` (PostgreSQL 18 con `pgvector`).
3. En `servidor/`: `uv run alembic upgrade head` y luego `uv run uvicorn --factory vitalia.principal:crear --port 8000`.
4. En `pantallas/`: `npm run dev -- --port 5174 --strictPort`. Abrir http://localhost:5174.

Cuentas de prueba en la base de Docker, con datos inventados: la médica con cédula 52345678 y la paciente Rosa Elena Duarte con cédula 41652318. Las contraseñas están en `servidor/pruebas/conftest.py` y `pantallas/src/paciente/CrearCuenta.test.tsx`. Hay además cuatro pacientes con las 12 historias de prueba ya subidas e indexadas. Para empezar de cero: `docker compose down -v`.

Si después de instalar un paquete las pantallas salen en blanco, hay que reiniciar `npm run dev`. Los demás comandos están en la sección 5 de [estado_desarrollo.md](estado_desarrollo.md).

## 7. Decisiones que definen el producto

| Tema | Cómo quedó |
|---|---|
| Tecnología | Python con FastAPI, PostgreSQL, React con Vite y TypeScript, archivos en Cloudflare R2 y Qwen (Alibaba, Singapur) detrás de un adaptador intercambiable |
| Base para programar | PostgreSQL 18 en Docker con la imagen `pgvector/pgvector:pg18-trixie` (D-29) |
| Asistente | Busca fragmentos (RAG) en los documentos del paciente y, cuando exista E9, en sus atenciones cerradas; siempre de un solo paciente, con `pgvector` en la misma base. Cada cita se comprueba contra lo enviado (D-30) |
| Código | Arquitectura limpia: dominio, casos de uso, adaptadores y entrada. Rápido, midiendo antes de optimizar (D-19) |
| Ingreso | Tipo y número de documento más contraseña. El documento identifica; nunca hace de contraseña (D-20) |
| Cuentas | Solo adultos (D-21, D-22) |
| Historia clínica | Dentro del sistema, con lo mínimo de la Resolución 1995 de 1999. Lo cerrado no se modifica (D-24) |
| Aspecto | Las pantallas copian el lienzo: el paciente en celular, el médico en computador. Estados en caja blanca con sombra y punto de color; nada que se vea genérico (D-18, D-25) |
| Iconos | Hugeicons, trazo redondeado (D-31, reemplaza D-26) |

Todas las decisiones (D-01 a D-31) y supuestos están en [04-decisiones-y-supuestos.md](planificacion/04-decisiones-y-supuestos.md).

## 8. Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Alcance, requisitos, marco normativo, decisiones y Kanban | [planificacion/](planificacion/) |
| 46 historias con criterios y tareas, y su orden | [historias-de-usuario/](historias-de-usuario/) y [RELACIONES.md](historias-de-usuario/RELACIONES.md) |
| Arquitectura, modelo de datos, API, asistente, pantallas, diagramas, base visual y herramientas | [diseno/01](diseno/01-arquitectura.md) a [diseno/09](diseno/09-herramientas-y-entrega.md) |
| Cómo se construye el asistente, paso a paso | [diseno/07-como-se-construye-el-asistente.md](diseno/07-como-se-construye-el-asistente.md) |
| Copia de los tableros del lienzo | [diseno/lienzo/](diseno/lienzo/) |
| Historias clínicas inventadas para probar el asistente, con sus preguntas | [documentos-de-prueba/historias-clinicas/](documentos-de-prueba/historias-clinicas/) |
| Servidor: capas, migraciones (`0001` a `0010`) y pruebas | `servidor/` |
| Pantallas | `pantallas/`. Iconos en `src/comunes/iconos.tsx`, hovers en `src/comunes/estilos/hovers.css` |
| Pruebas automáticas de GitHub | `.github/workflows/pruebas.yml` |
| Detalle técnico de cada paso del desarrollo | [estado_desarrollo.md](estado_desarrollo.md) |

**Fuera del repositorio**

| Qué | Enlace |
|---|---|
| Código | https://github.com/JAOSjavi/vitalia |
| Lienzo de diseño, la referencia de las pantallas | https://claude.ai/artifact/R6WLHr5eAt7FQztseugqQY |
| Prototipo navegable (comportamiento, versión del 13 de octubre) | https://claude.ai/artifact/4MN2vq99tcrQBzUWDJ4pEy |

El artefacto "Vitalia Salud", de agosto, es el demo de la versión anterior y no es referencia.

## 9. Antes de usar datos reales

Todo se construye y se prueba con datos inventados. Para atender pacientes reales hace falta:

1. **La respuesta del abogado** a las preguntas 2 (datos fuera de Colombia), 5 (envío del Resumen Digital de Atención) y 7 (firma de la historia clínica) del [marco normativo](planificacion/03-marco-normativo.md), y su revisión de los textos de autorización (versión 1 en `servidor/migraciones/textos/`; la versión 2, que incluye las atenciones, falta escribirla).
2. **Contrato de tratamiento de datos** con Alibaba, Render y Cloudflare.
3. **Un médico que revise los campos** de la historia clínica.
4. **Respaldo de largo plazo:** la historia clínica se conserva 15 años y Render restaura pocos días.
5. **Cerrar el acceso a la base** a las direcciones que la necesitan y pasarla al plan pago.

## 10. Lo que no está verificado

| Tema | Situación |
|---|---|
| Servicios en la nube | Nada ha corrido contra Render ni R2. De Qwen solo los vectores |
| Respuestas del asistente con Qwen | Probadas con una IA de prueba y un servidor que imita el formato de Alibaba |
| Lectura de fotos | El adaptador existe; sin medir con fotos reales |
| Pruebas automáticas de GitHub | Escritas; no han corrido porque ninguna rama ha pasado por una solicitud de cambio |
| Permisos por fila en Render | Falta confirmar que el usuario por defecto no sea superusuario, porque ese se salta los permisos |
| `pgvector` en Render | Su documentación dice que se activa; sin probar |
| `pypdfium2` | Lee bien las 12 historias de prueba; falta probarlo con PDF de otras fuentes |
| Búsqueda del asistente | Medida con 12 historias; falta con más volumen y documentos de otras fuentes |
| Campos clínicos de la historia clínica | Falta que los revise un médico |
| Memoria del servicio más pequeño de Render (512 MB) para leer escaneados | Sin medir |
| Proyecto de resolución que reemplazaría la 1995 de 1999 | Publicado el 22 de julio de 2026; al 13 de octubre no estaba expedido |

## 11. Reglas que no se pueden olvidar

- **Solo datos inventados o anonimizados** hasta cumplir la sección 9.
- Lo que sube el paciente son antecedentes. La historia clínica de las atenciones del consultorio va aparte, en la épica E9.
- Una atención cerrada y un tratamiento guardado no se modifican ni se borran.
- El asistente ayuda a leer, no diagnostica ni escribe la historia clínica.
- Sin autorización del paciente no hay asistente, no se indexa nada y las fotos no se envían al proveedor. Al retirarla se borran sus fragmentos.
- Ninguna clave entra al repositorio ni pasa por el chat.
- Toda tabla nace con su permiso por fila en la misma migración.
- Cada pantalla copia la estructura y las medidas de su tablero del lienzo; lo que todavía no existe se omite y se dice, no se inventa.

## 12. Forma de trabajo acordada

- Kanban sobre las cinco fases del ciclo de vida; primero las bases, después el código.
- Solo lo útil: sin funciones "por si acaso" ni pantallas de verificación. Se construye por historias.
- Pocas preguntas: se decide, se escribe el supuesto y se corrige sobre el documento. Los gustos visuales se deciden viendo opciones lado a lado.
- Al construir el asistente, cada paso se explica con su código real, de forma sencilla.
- Los commits van solo a nombre del dueño del proyecto, sin coautor, y en español.
- Al terminar una sesión se actualiza este archivo.
