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
2. **Clave de Qwen** (Alibaba Cloud Model Studio, región Singapur): hace falta para el bloque 3. Paso a paso en la sección 3.3 de [diseno/09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md). Modelos: `qwen3.7-plus` y `qwen3.5-ocr`. La clave va solo en `servidor/.env`, nunca en el chat.
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

**Paso 0, hecho el 27 de octubre:** imagen `pgvector/pgvector:pg18-trixie` en `docker-compose.yml` y en las pruebas de GitHub; `pgvector` instalado como superusuario en `template1` por `servidor/guiones/bd/01-usuarios.sh` (en un volumen ya creado se instaló a mano una vez); migración `0005_documentos_y_fragmentos.py` con `documentos`, `paginas_documento`, `trabajos_lectura`, `fragmentos`, la configuración de búsqueda `vitalia_es` y el borrado de fragmentos al retirar la autorización de IA; variables `IA_MODELO_VECTORES` e `IA_DIMENSIONES` en `servidor/.env.example`; cinco pruebas en `pruebas/adaptadores/test_fragmentos.py`. Sigue el paso 1: subir un PDF y leerlo por página.

**Sin clave de Qwen se puede construir:** guardar y subir documentos, leer PDF con texto, partir en fragmentos, la tabla y la búsqueda con un adaptador de mentira cuyos vectores salen de las palabras, el aislamiento por paciente y la comprobación de orígenes. Con la clave: leer fotos, vectorizar de verdad, preguntar y medir la búsqueda con el conjunto de prueba.

**Las atenciones** entran a la búsqueda cuando se construya la épica E9, y solo para pacientes con la versión 2 del texto de autorización de IA, que falta escribir.

---

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
- Los iconos de Phosphor se importan uno por uno desde `pantallas/src/comunes/iconos.ts`. Importar el paquete completo hace que las pruebas tarden cuatro minutos.
- En el shell de esta máquina, los textos largos con comillas triples o plantillas dentro de `cat <<EOF` fallan: es más seguro escribir los archivos con la herramienta de escritura.
- El puerto 5173 lo ocupa otro proyecto de Javier (`Desktop\Multimedia`): las pantallas de Vitalia van en el 5174. El enlace de puesta en marcha sale con 5173; hay que cambiarlo a 5174 a mano.
- El navegador del entorno, si la ventana está oculta, no entrega bien los clics ni las teclas; los recorridos a la vista se hacen con la ventana visible.

### Lo que el bloque 2 dejó para después

Bloqueos (HU-009), asistencia (HU-018), avisos por correo (HU-019), calendario de semana y mes (HU-022), registrar paciente desde el panel (HU-024), cobro (HU-026), y en el inicio del paciente los tratamientos y documentos (HU-020, CA-3 a CA-5).
