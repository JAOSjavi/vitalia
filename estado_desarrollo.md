# Estado del desarrollo

**Fecha:** 26 de octubre de 2026
**Para qué sirve:** retomar el Desarrollo en una sesión nueva. Complementa a [ESTADO.md](ESTADO.md), que tiene el panorama de todo el proyecto (fases, decisiones, documentos y reglas).

---

## 1. Dónde quedó

| Qué | Estado |
|---|---|
| Rama de trabajo | `bloque-2-citas`. `master` tiene el bloque 1 completo |
| Repositorio remoto | No existe todavía. Todo está solo en este computador |
| Bloque 1 · Registro e ingreso | **Hecho y unido a `master`**. Servidor y pantallas |
| Bloque 2 · Citas, servidor | **Hecho y confirmado** en la rama: 104 pruebas en verde |
| Bloque 2 · Citas, pantallas | **Escritas, sin terminar**: compilan sin errores de tipos, pero falta conectarlas al menú del médico, sus pruebas y verlas en el navegador (sección 4) |
| Bloque 3 · Documentos y resumen con IA | Sin empezar |
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
| (pendiente) | Pantallas del bloque 2, a medio terminar |

---

## 2. Base de datos: cómo se ha probado y qué sigue

**No se instaló PostgreSQL en el computador.** Para correr las pruebas se usó un PostgreSQL 18.4 temporal que trae el paquete de Python `pixeltable-pgserver`, levantado dentro de la carpeta de trabajo temporal de la sesión y apagado al terminar. Ese PostgreSQL no trae las extensiones `btree_gist` y `unaccent`, así que para probar se quitaban esas dos líneas de la migración `0001` en una copia; el código del repositorio no se tocó.

**Decisión pendiente de aplicar (pedida el 26 de octubre):** usar **Docker con una imagen de PostgreSQL** en vez de ese PostgreSQL temporal.

| Paso | Quién |
|---|---|
| 1. Instalar Docker Desktop (`winget install --id Docker.DockerDesktop`). El computador ya tiene WSL2, que es lo que necesita | Javier |
| 2. Agregar `docker-compose.yml` en la raíz con `postgres:18` (puerto 5432, volumen con nombre) y un guion que cree `vitalia_migraciones` (dueño, con CREATEDB), `vitalia_api` (sin privilegios) y la base `vitalia_dev` | Claude |
| 3. Opcional: el mismo archivo con un servidor S3 local para los documentos. MinIO ya no se publica; la alternativa vigente es `rustfs/rustfs` (puertos 9000 y 9001) | Claude |
| 4. `servidor/.env` con `BD_URL` y `BD_URL_MIGRACIONES` apuntando a `localhost:5432` | Claude, sin claves reales |
| 5. Correr las migraciones y toda la suite contra el contenedor | Claude |

Con esto cambia la decisión D-27 (servicios en la nube desde el primer día): local con Docker para programar y Render para publicar. Hay que registrarlo en [planificacion/04-decisiones-y-supuestos.md](planificacion/04-decisiones-y-supuestos.md) y en la sección 3 de [diseno/09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md).

Las pruebas de GitHub (`.github/workflows/pruebas.yml`) ya usan la imagen `postgres:18` como servicio.

---

## 3. Lo que sigue pendiente de Javier

1. **Docker Desktop** (sección 2).
2. **Repositorio privado en GitHub**, vacío. Al conectarlo, `master` pasa a llamarse `main`.
3. **Clave de Qwen** (Alibaba Cloud Model Studio, región Singapur): hace falta para el bloque 3. Paso a paso en la sección 3.3 de [diseno/09-herramientas-y-entrega.md](diseno/09-herramientas-y-entrega.md). Modelos: `qwen3.7-plus` y `qwen3.5-ocr`. La clave va solo en `servidor/.env`, nunca en el chat.
4. **Render y Cloudflare R2**: para publicar, no para programar. Paso a paso en la misma sección 3.
5. **Dos fotos con datos inventados** para medir la lectura de la IA al empezar el bloque 3.

---

## 4. Pantallas del bloque 2: lo que falta

Ya escritos en `pantallas/src/`:

| Archivo | Qué es |
|---|---|
| `api/citas.ts` | Todas las llamadas de citas, horario, tipos, disponibilidad, agenda y pacientes |
| `comunes/fechas.ts` | Fechas y horas en hora de Colombia con `Intl` |
| `comunes/estados.ts` | Nombre y color de cada estado de cita |
| `comunes/SelectorDeEspacio.tsx` | Elegir día y hora; solo muestra lo disponible. Lo usan paciente y médico |
| `paciente/ZonaPaciente.tsx` | Rutas del paciente y barra de abajo (Inicio, Citas) |
| `paciente/Inicio.tsx` | P-04: próxima cita con mover y cancelar, o el acceso para agendar |
| `paciente/MisCitas.tsx` | P-06: próximas y anteriores, mover, cancelar con confirmación, aviso de 24 horas |
| `paciente/Agendar.tsx` | P-05: tipo, día y hora, confirmación. También mueve una cita |
| `medico/Hoy.tsx` | M-01: agenda de hoy, pendientes de configuración, mover y cancelar con motivo |
| `medico/Pacientes.tsx` | M-04: búsqueda y lista por páginas |
| `medico/NuevaCita.tsx` | M-03: cita para un paciente o mover una; permite una hora por fuera del horario con confirmación |
| `medico/Configuracion.tsx` | M-08 y M-10: horario semanal y tipos de cita |

Falta, en este orden:

1. **Conectar `medico/ZonaMedico.tsx`**: menú con Hoy, Pacientes, Configuración y Consultorio, y las rutas `hoy`, `pacientes`, `citas/nueva`, `citas/:cita/mover`, `configuracion` y `consultorio`. La ruta inicial pasa a ser `hoy`.
2. Pruebas de pantallas (Vitest), como las del bloque 1: agendar solo con espacios libres, espacio ocupado con alternativas, cancelar con confirmación, menos de 24 horas, cancelar como médico exige motivo.
3. `npm run test` y `npm run build`.
4. Recorrerlas en el navegador contra la API y la base del contenedor de Docker, comparando con el lienzo (`diseno/lienzo/Paciente-Agendar`, `Paciente-Citas`, `Main` y `Medico-Hoy`).
5. Confirmar, unir `bloque-2-citas` a `master` y actualizar [ESTADO.md](ESTADO.md).

Después sigue el **bloque 3**, documentos y resumen con IA, con el orden de la sección 4 de [ESTADO.md](ESTADO.md).

---

## 5. Cómo se trabaja con el código

| Para | Orden, desde la carpeta indicada |
|---|---|
| Revisar el servidor | En `servidor/`: `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`, `uv run lint-imports` |
| Pruebas rápidas, sin base | En `servidor/`: `uv run pytest -m "not bd"` |
| Todas las pruebas | En `servidor/`: `uv run pytest` (necesita `BD_URL` y `BD_URL_MIGRACIONES`) |
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
- El puerto 5173 lo ocupa otro proyecto de Javier (`Desktop\Multimedia`): Vite toma el 5174. No hay que cerrarlo.
- El navegador del entorno, si la ventana está oculta, no entrega bien los clics ni las teclas; los recorridos a la vista se hacen con la ventana visible.

### Lo que el bloque 2 dejó para después

Bloqueos (HU-009), asistencia (HU-018), avisos por correo (HU-019), calendario de semana y mes (HU-022), registrar paciente desde el panel (HU-024), cobro (HU-026), y en el inicio del paciente los tratamientos y documentos (HU-020, CA-3 a CA-5).
