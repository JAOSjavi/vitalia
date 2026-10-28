# Estado del desarrollo

**Fecha:** 26 de octubre de 2026
**Para qué sirve:** retomar el Desarrollo en una sesión nueva. Complementa a [ESTADO.md](ESTADO.md), que tiene el panorama de todo el proyecto (fases, decisiones, documentos y reglas).

---

## 1. Dónde quedó

| Qué | Estado |
|---|---|
| Rama de trabajo | `master`, con los bloques 1 y 2 completos. El bloque 3 empieza en una rama nueva |
| Repositorio remoto | No existe todavía. Todo está solo en este computador |
| Bloque 1 · Registro e ingreso | **Hecho y unido a `master`**. Servidor y pantallas |
| Bloque 2 · Citas | **Hecho y unido a `master`**. Servidor (105 pruebas) y pantallas (13 pruebas), recorridas en el navegador contra la base de Docker (sección 4) |
| Bloque 3 · Documentos y resumen con IA | Sin empezar |
| Base de datos para programar | **PostgreSQL 18 en Docker**, funcionando: 105 pruebas en verde contra él. Ver la sección 2 |
| Servicios en la nube (Render, R2, Qwen) | Sin crear. Ver la sección 3 |

### Commits

| Commit | Qué |
|---|---|
| `c6d3170` | Esqueleto del servidor y de las pantallas |
| `2aae707` | Decisiones D-27 y D-28: servicios en la nube y construcción por historias |
| `68db6f5` | HU-006, HU-036 y HU-037: roles, permisos por fila y bitácora |
| `7640201` | Servidor del bloque 1: HU-001 a HU-004 y HU-007 |
| `25643ea` | Pantallas del bloque 1 |
| `94794fc` | Servidor del bloque 2: citas |
| `87d9433` | Pantallas del bloque 2, a medio terminar |
| `f4553a8` | PostgreSQL 18 en Docker (D-29) |
| `e3c0ab5` | Menú del médico y pruebas de las pantallas del bloque 2 |

---

## 2. Base de datos en Docker

Desde el 26 de octubre la base para programar es **PostgreSQL 18 en Docker** (decisión D-29). No se instala nada más en el computador.

| Qué | Dónde |
|---|---|
| Servicio | `docker-compose.yml` en la raíz: imagen `postgres:18`, solo en `127.0.0.1:5432`, datos en el volumen `vitalia_datos` |
| Usuarios y base | `servidor/guiones/bd/01-usuarios.sh` crea `vitalia_migraciones` (dueño de las tablas), `vitalia_api` (sin privilegios) y `vitalia_dev` la primera vez que arranca |
| Contraseñas | Generadas al azar en `.env` (raíz, para Docker) y `servidor/.env` (para la aplicación). Git ignora los dos |
| Pruebas | Crean y borran `vitalia_pruebas` en el mismo contenedor |

```
docker compose up -d                  levanta la base
docker compose down                   la detiene; los datos quedan en el volumen
docker compose down -v                la borra por completo; al subir se vuelve a crear vacía
```

En las direcciones de conexión va `127.0.0.1`, no `localhost`: en Windows `localhost` intenta primero por IPv6 y el contenedor no escucha ahí, así que las conexiones se quedaban esperando.

Comprobado el 26 de octubre: migraciones aplicadas, deshechas y vueltas a aplicar, y las 105 pruebas del servidor en verde, incluida la de las extensiones `btree_gist` y `unaccent`.

Para publicar sigue Render (sección 3). El almacenamiento de documentos en local se agrega a este mismo archivo al empezar el bloque 3 (propuesta: `rustfs/rustfs`, porque MinIO dejó de publicarse).

## 3. Lo que sigue pendiente de Javier

1. **Repositorio privado en GitHub**, vacío. Al conectarlo, `master` pasa a llamarse `main`.
2. **Clave de Qwen** (Alibaba Cloud Model Studio, región Singapur): hace falta para el bloque 3. Paso a paso en la sección 3.3 de [diseno/09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md). Modelos: `qwen3.7-plus` y `qwen-vl-ocr-2025-11-20`. La clave va solo en `servidor/.env`, nunca en el chat.
3. **Render y Cloudflare R2**: para publicar, no para programar. Paso a paso en la misma sección 3.
4. **Dos fotos con datos inventados** para medir la lectura de la IA al empezar el bloque 3.

---

## 4. Pantallas del bloque 2: cómo quedaron

Hecho el 26 de octubre:

- `medico/ZonaMedico.tsx` tiene el menú Hoy, Pacientes, Configuración y Consultorio, y las rutas `hoy` (inicial), `pacientes`, `citas/nueva`, `citas/:cita/mover`, `configuracion` y `consultorio`. Calendario, Bitácora y Cobro del lienzo llegan con HU-022, HU-037 y HU-026.
- Pruebas nuevas en `paciente/Agendar.test.tsx`, `paciente/MisCitas.test.tsx` y `medico/Hoy.test.tsx`: agendar solo con horas libres, espacio ocupado con alternativas, cancelar con confirmación, menos de 24 horas, motivo obligatorio al cancelar como médico y aviso de lo que falta configurar. 13 pruebas en verde; `npm run build` sin errores.
- **Recorrido contra la API y la base de Docker**: puesta en marcha de la médica, horario de lunes a viernes, tipo de cita, datos del consultorio (desaparece el aviso de pendientes), cita por fuera del horario con confirmación, moverla a otro día, ingreso de la paciente, inicio con la cita de mañana y solo el teléfono por faltar menos de 24 horas, agendar con aviso de cita repetida y cancelar con confirmación. La hora ocupada deja de ofrecerse.
- Corregido en el recorrido: el aviso de cita confirmada terminaba en "a. m.." y en celular la hora se partía en dos líneas.

Datos que quedaron en la base de Docker (inventados, los mismos de las pruebas): la médica con documento CC 52345678 y la paciente CC 41652318; las contraseñas están en `servidor/pruebas/conftest.py` y `pantallas/src/paciente/CrearCuenta.test.tsx`. Para empezar de cero: `docker compose down -v`.

**Sin verificar a la vista:** las pantallas del médico se revisaron leyendo su texto, no con capturas, porque la ventana del navegador estuvo oculta. Las del paciente (Mis citas en celular y Agendar en computador) sí se vieron y coinciden con el lienzo.

Después sigue el **bloque 3**, documentos y resumen con IA, con el orden de la sección 4 de [ESTADO.md](ESTADO.md). Antes de empezarlo hace falta la clave de Qwen y las dos fotos (sección 3).

## 4.1 Cambio de diseño: el asistente con RAG (D-30)

El 26 de octubre, antes de empezar el bloque 3, se decidió que el asistente busque fragmentos (RAG) en lugar de enviar todos los documentos, y que busque también en las atenciones cerradas del consultorio. Rama `bloque-3-documentos-e-ia`. Solo cambió el diseño; no hay código todavía.

| Documento | Qué cambió |
|---|---|
| [04-asistente-ia.md](diseno/04-asistente-ia.md) | Versión 2.0: fuentes, indexación, búsqueda por significado y por palabras, comprobación de orígenes contra lo enviado, lista de lo consultado, resumen sin búsqueda, costo y pruebas |
| [07-como-se-construye-el-asistente.md](diseno/07-como-se-construye-el-asistente.md) | Seis piezas en vez de cinco; partir, vectorizar y buscar, con esquemas; medir la búsqueda aparte de la respuesta |
| [02-modelo-de-datos.md](diseno/02-modelo-de-datos.md) | Tabla `fragmentos` con su permiso por fila e índices; tipos en `trabajos_lectura`; borrado al retirar la autorización |
| [01](diseno/01-arquitectura.md), [03](diseno/03-api.md), [05](diseno/05-pantallas.md), [09](diseno/09-herramientas-y-entrega.md) | `pgvector`, respuesta con lo consultado, imagen `pgvector/pgvector:pg18`, variables `IA_MODELO_VECTORES` e `IA_DIMENSIONES` |
| Requisitos y decisiones | RF-31, RF-32, RF-34 y RF-35; decisión D-30 |
| Historias | HU-031 a HU-035, HU-042 y HU-044: 7 criterios nuevos y 14 ajustados |

**Paso 0, hecho el 27 de octubre:** imagen `pgvector/pgvector:pg18-trixie` en `docker-compose.yml` y en las pruebas de GitHub; `pgvector` instalado como superusuario en `template1` por `servidor/guiones/bd/01-usuarios.sh` (en un volumen ya creado se instaló a mano una vez); migración `0005_documentos_y_fragmentos.py` con `documentos`, `paginas_documento`, `trabajos_lectura`, `fragmentos`, la configuración de búsqueda `vitalia_es` y el borrado de fragmentos al retirar la autorización de IA; variables `IA_MODELO_VECTORES` e `IA_DIMENSIONES` en `servidor/.env.example`; cinco pruebas en `pruebas/adaptadores/test_fragmentos.py`.

**Paso 1, hecho el 27 de octubre: subir y leer.** El paciente sube un PDF, JPG o PNG de hasta 20 MB con `POST /api/v1/documentos` y ve su lista con `GET /api/v1/documentos` (HU-028; permisos `documentos.subir` y `documentos.ver` en la migración `0006`). El formato se reconoce por el contenido, no por el nombre; el mismo archivo dos veces responde 409 con el documento que ya existe; si la base falla, el archivo guardado se borra. Al subir queda "en proceso" y entra a la cola `trabajos_lectura`. El lector (`casos_de_uso/leer_documentos.py`) corre en segundo plano dentro de la API, cada 3 segundos: lee los PDF con texto con `pypdfium2` dentro del servidor y guarda el texto por página; los escaneados y las fotos solo van al modelo de lectura si el paciente autorizó la IA, y si no, quedan "sin leer" (HU-031, CA-1 a CA-4, CA-6 y CA-8). Si el documento queda legible y el paciente autorizó la IA, se encola su indexación. Un PDF dañado se reintenta tres veces y queda "no legible". 36 pruebas nuevas; 141 en verde.

- **Archivos.** Mientras R2 no esté conectado, se guardan en `servidor/.archivos/` (fuera del repositorio) con `adaptadores/archivos_en_disco.py`, que cumple el mismo puerto que tendrá el adaptador S3. Falta: el adaptador de R2 y el enlace temporal para abrir un documento (HU-027).
- **Prueba con las 12 historias inventadas** de `documentos-de-prueba/historias-clinicas/pdf/` (hechas con Edge desde los .txt; Word no se dejó automatizar en este equipo): subidas por la API como cuatro pacientes con IA autorizada, leídas en 0,6 s, 3 páginas cada una, y el dato clave de cada historia aparece tal cual en el texto guardado (12 de 12). Quedaron en la base de Docker con documentos CC 79482615, 31927448, 43578211 y 1098745318; la contraseña está en el guion de carga y no en el repositorio.
- **Qwen, comprobado el 27 de octubre:** la clave y la dirección funcionan; `qwen3.7-text-embedding` entrega vectores de 1024. `qwen3.7-plus` y `qwen-vl-ocr-2025-11-20` responden `AccessDenied.Unpurchased` porque la verificación de identidad de la cuenta está en revisión (hasta 3 días hábiles). El modelo de lectura en Singapur se llama `qwen-vl-ocr-2025-11-20`, no `qwen3.5-ocr`.

**Paso 2, hecho el 27 de octubre: fragmentos, vectores y búsqueda.** El indexador (`casos_de_uso/indexar_documentos.py`) toma de la cola los documentos legibles de pacientes con IA autorizada, parte cada página en trozos de hasta 1.000 caracteres cortados en fin de frase y con 150 repetidos, tapa nombre, documento, teléfono y correo del paciente con `[PACIENTE]`, `[DOCUMENTO]`, `[TELÉFONO]` y `[CORREO]` (con o sin tildes, con puntos o espacios en los números), pide los vectores a `qwen3.7-text-embedding` de a 10 textos y guarda los fragmentos; indexar dos veces reemplaza, no duplica. Corre en el mismo proceso de segundo plano que el lector. La búsqueda (`casos_de_uso/buscar_fragmentos.py`, permiso `asistente.preguntar` del médico) limpia la pregunta, la vectoriza y llama a la función de la base `buscar_fragmentos`, que combina distancia de vectores y palabras en español dentro de un solo paciente (fusión por rango recíproco, 20 por método y 12 al final). Sin autorización de IA del paciente responde "ia_no_autorizada". El lector solo ve del paciente lo que hay que tapar, por la función `identificadores_paciente`. Migración `0007`. Sin `IA_CLAVE`, los vectores salen de las palabras (`VectoresDeMentira`), con un aviso al arrancar. Todavía no hay ruta de la API: la búsqueda la usará la pregunta al asistente. 17 pruebas nuevas; 158 en verde.

- **Medición con Qwen y las 12 historias** (96 fragmentos, indexados en 27 s): de 16 datos esperados en 14 preguntas, la búsqueda trajo los 16 entre los 12 fragmentos y 14 entre los 3 primeros. Las dos preguntas dichas con otras palabras ("¿Tiene problemas del corazón?", "¿Le hormiguean los pies?") trajeron el fragmento correcto de primero. Los que quedaron más abajo: la fecha en que dejó de fumar (puesto 4) y la biopsia del endometrio (puesto 6). Cada búsqueda tarda unos 1,3 s, casi todo el viaje a Qwen en Singapur.
- **Corregido en el camino:** al apagar la API, una cancelación envuelta en un error de la base podía dejar el lector girando; ahora se detiene (prueba en `pruebas/entrada/test_lector_en_segundo_plano.py`).

**Paso 3, hecho el 27 de octubre con la IA de prueba: preguntar al asistente.** `POST /api/v1/pacientes/{id}/asistente/preguntas` (HU-034) responde por partes en líneas JSON: el texto mientras se escribe y, al final, las citas comprobadas, lo consultado y el aviso de que es un apoyo. Antes de llamar al proveedor comprueba, en orden, rol médico, autorización de IA del paciente (422), que tenga fragmentos (422) y el tope de 30 preguntas por hora contado en la bitácora (429). Si todo el texto del paciente cabe en `IA_TOPE_CONTEXTO` (16.000 caracteres) se envía entero; si no, la búsqueda con la pregunta anterior y la actual, hasta el tope. La pregunta y la conversación se limpian de identificadores. El contexto agrupa por documento con etiquetas D1, D2… en orden de fecha (`dominio/asistente.py`); el modelo cita `[D2, pág. 1: "frase"]` y el servidor descarta la cita a un documento o página que no se envió y marca "sin verificar" la frase que no aparece tal cual. La bitácora anota quién preguntó sobre quién, sin la pregunta. Si el modelo no responde en 60 s o el proveedor rechaza, llega un evento de error y no se reintenta. El adaptador `IAQwen` responde por partes y lee fotos; está probado contra un servidor de mentira con el formato de Alibaba. Sin clave, el asistente usa `IADeMentira`. 18 pruebas nuevas; 176 en verde.

- **Contra Qwen de verdad**, con las historias de la base de Docker: el asistente devuelve el evento `proveedor_no_disponible`, porque `qwen3.7-plus` sigue en `AccessDenied.Unpurchased` hasta que Alibaba apruebe la verificación de identidad. Cuando la apruebe, falta correr las preguntas del README de `documentos-de-prueba/historias-clinicas` y medir: cero inventos, origen correcto en al menos nueve de cada diez, abstención en las de diagnóstico.
- **Las fotos y escaneados** ya pasan por `IAQwen.leer_pagina` cuando hay clave. Si el proveedor no está disponible, el documento queda "sin leer" y no "no legible".

**Pantallas del bloque 3, hechas el 27 de octubre y rehechas el mismo día según el lienzo.** La primera versión se armó leyendo solo el texto del lienzo y no seguía su diseño; se rehízo con la estructura y las medidas de `Paciente-Documentos.dc.html` y `Medico-Ficha.dc.html`.

- **Paciente, Mis documentos (P-07):** botón "Subir" arriba, que abre la hoja inferior para elegir varios archivos o tomar una foto (nombre por archivo, fecha y tipo, resultado de cada uno y "Reintentar"); franja azul oscuro con el estado del asistente de IA; rótulo "N documentos subidos"; una tarjeta con cada documento, su icono (hoja o foto), su estado y explicación, "Ver" y eliminar con confirmación. La lista se actualiza sola mientras alguno se lee. `GET /api/v1/documentos` devuelve `{documentos, ia_autorizada}`.
- **Médica, ficha del paciente (M-06):** ruta "Pacientes › Nombre", tarjeta con avatar de iniciales, edad, documento en grupos de tres, teléfono y estado de la cuenta, y "Agendar cita"; citas; documentos con su etiqueta D1, D2… y el botón para verlos; asistente a la derecha con burbujas, cada cita como botón "D1 · pág. 2" que abre el documento en esa página (punto ámbar si la frase no se verificó, tachada si el servidor la descartó), "Consultó: …", preguntas sugeridas, caja de pregunta y nota final. `GET /api/v1/pacientes/{id}` (HU-025) deja "ficha_vista" en la bitácora.
- **Servidor nuevo para estas pantallas:** `GET /api/v1/documentos/{id}/archivo` (el paciente los suyos, la médica todos; deja "documento_abierto" en la bitácora; con R2 pasará a enlace firmado de 15 minutos, HU-027) y `DELETE /api/v1/documentos/{id}` (migración `0008`, permiso `documentos.eliminar`; borra páginas y fragmentos en cascada y el archivo). Las etiquetas D1, D2… son fijas por orden de subida, las mismas en la ficha y en las respuestas del asistente.
- **Verificado a la vista** contra la base de Docker: Mis documentos y la hoja de subir en celular; "Ver" entrega el PDF; la ficha de Hernando en computador; una pregunta devuelve el aviso de "no disponible" porque Qwen sigue bloqueado. Las burbujas de respuesta con citas están cubiertas por pruebas, no vistas en vivo.
- 23 pruebas de pantallas y 183 del servidor en verde.

Queda por fuera: el enlace temporal firmado cuando exista R2 (HU-027); cambiar la autorización de IA desde Mis documentos (la franja del lienzo lleva a eso); la pestaña Tratamientos y el botón "Registrar tratamiento" del lienzo (E8); los tratamientos en la ficha (E8); el resumen del paciente (HU-035). También, que al autorizar la IA después del registro los documentos sin leer y los legibles entren a la cola (diseño 04, sección 4), y probar el asistente con Qwen cuando Alibaba apruebe la cuenta.

**Sin clave de Qwen se puede construir:** guardar y subir documentos, leer PDF con texto, partir en fragmentos, la tabla y la búsqueda con un adaptador de mentira cuyos vectores salen de las palabras, el aislamiento por paciente y la comprobación de orígenes. Con la clave: leer fotos, vectorizar de verdad, preguntar y medir la búsqueda con el conjunto de prueba.

**Las atenciones** entran a la búsqueda cuando se construya la épica E9, y solo para pacientes con la versión 2 del texto de autorización de IA, que falta escribir.

---

## 4.2 Interfaz corregida según el lienzo (27 de octubre)

Una sesión anterior armó pantallas a su manera. Se rehicieron siguiendo el lienzo ([artefacto](https://claude.ai/artifact/R6WLHr5eAt7FQztseugqQY) y su copia en `diseno/lienzo/`): el paciente en celular y el médico en computador. En el lienzo publicado el tablero "Paciente · Inicio" quedó borrado salvo la barra de abajo; la copia completa está en `diseno/lienzo/Main.dc.html`.

| Pantalla | Qué cambió |
|---|---|
| Menú del médico | Hoy, Calendario, Pacientes, Configuración; Bitácora y Cobro como "Pronto"; abajo las iniciales, el nombre, el registro y salir. Los datos del consultorio se abren desde Configuración |
| Hoy | Buscador de pacientes, columna derecha con la tarjeta de quien sigue y el avance del día, pausas entre franjas, botones Atendida, No asistió, Mover, Cancelar y Corregir |
| Calendario (nuevo, HU-022) | Vista de mes como el tablero, más semana y día; festivos de Colombia calculados en `comunes/festivos.ts`; "Agendar en este día" abre la cita nueva en ese día |
| Inicio del paciente | Iniciales arriba (abren "Salir"), tarjeta "Mis documentos" con subidos y legibles; se quitó la tarjeta del consultorio, que no está en el lienzo |
| Mis citas | Botón Agendar lleno, rótulos en mayúscula pequeña, bloque de fecha azul cuando es hoy, teléfono como botón |
| Fechas | Sin coma, como en el lienzo: "martes 13 de octubre", "mié 14 oct" |

Para que los botones de Hoy funcionen se construyó **HU-018 asistencia** en el servidor: `POST /citas/{id}/asistencia` (migración `0009`), y la agenda de hoy trae `sigue` con edad, documentos y autorización de IA de quien sigue, sin abrir su ficha ni dejar rastro en la bitácora.

**Quedan fuera hasta que existan:** bloqueos (HU-009: no aparecen en el calendario ni el botón "Bloquear horario"), registrar paciente desde el panel (HU-024), tratamientos (E8: ni la pestaña del paciente ni la línea de la tarjeta de quien sigue), "Próximo espacio libre" del avance del día.

## 5. Cómo se trabaja con el código

| Para | Orden, desde la carpeta indicada |
|---|---|
| Revisar el servidor | En `servidor/`: `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`, `uv run lint-imports` |
| Pruebas rápidas, sin base | En `servidor/`: `uv run pytest -m "not bd"` |
| Todas las pruebas | Con la base arriba (`docker compose up -d`), en `servidor/`: `uv run pytest` |
| Migraciones | En `servidor/`: `uv run alembic upgrade head` |
| Arrancar la API | En `servidor/`: `uv run uvicorn --factory vitalia.principal:crear --port 8000` |
| Enlace para la cuenta del médico | En `servidor/`: `uv run python -m vitalia.principal puesta-en-marcha` |
| Pantallas | En `pantallas/`: `npm run dev`, `npm run test`, `npm run build` |

Variables del servidor: ver `servidor/.env.example` (`BD_URL`, `BD_URL_MIGRACIONES`, `SESION_SECRETO`, `SITIO_URL`, `ARCHIVOS_*`, `IA_*`).

### Cosas que conviene saber

- **Permisos por fila forzados**, también para el dueño de las tablas: conectado directo no ve filas. Para escribir datos en una migración se quitan un momento en la misma transacción (ver `_sin_forzar` en la migración `0004`).
- Lo que ocurre sin sesión (ingreso, registro, puesta en marcha, sesión vigente, lo ocupado de la agenda) pasa por funciones de la base con permiso propio.
- Las pruebas de base usan su propia base `vitalia_pruebas`, que crean y borran. Cada prueba de citas usa una semana distinta del futuro y pone el reloj con `reloj.poner(...)`. La médica ingresa con `ingresar_doctora()` **después** de poner el reloj, o su sesión vence.
- Los iconos son de Hugeicons y las pantallas los toman de `pantallas/src/comunes/iconos.tsx`, con nombres propios: si se cambia otra vez de biblioteca, solo cambia ese archivo. Los hovers de toda la aplicación están en `comunes/estilos/hovers.css`.
- En el shell de esta máquina, los textos largos con comillas triples o plantillas dentro de `cat <<EOF` fallan: es más seguro escribir los archivos con la herramienta de escritura.
- El puerto 5173 lo ocupa otro proyecto de Javier (`Desktop\Multimedia`): las pantallas de Vitalia van en el 5174. El enlace de puesta en marcha sale con 5173; hay que cambiarlo a 5174 a mano.
- El navegador del entorno, si la ventana está oculta, no entrega bien los clics ni las teclas; los recorridos a la vista se hacen con la ventana visible.

### Lo que el bloque 2 dejó para después

Bloqueos (HU-009), avisos por correo (HU-019), registrar paciente desde el panel (HU-024), cobro (HU-026) y, en el inicio del paciente, los tratamientos (HU-020). Asistencia (HU-018) y calendario (HU-022) se hicieron el 27 de octubre (sección 4.2).
