# Decisiones y supuestos

**Fase del ciclo de vida:** Planificación
**Versión:** 2.8 · 26 de octubre de 2026

Una **decisión** la tomó el dueño del proyecto. Un **supuesto** lo puso quien levantó los requisitos para no frenar el trabajo, y se cambia en cuanto haya mejor información.

---

## 1. Decisiones tomadas

| # | Fecha | Decisión | Efecto |
|---|---|---|---|
| D-01 | 12 oct 2026 | El sistema es para un solo consultorio, a la medida. No se vende a otros | Sin cuentas por cliente ni cobro por uso del sistema |
| D-02 | 12 oct 2026 | El segmento es medicina general privada | Salen odontología, otras especialidades y atención de animales |
| D-03 | 12 oct 2026 | El médico hace todo lo del consultorio. No hay personal de recepción | Dos roles: médico y paciente |
| D-04 | 12 oct 2026 | El cobro queda como un botón en el panel, sin función | Una sola historia mínima (HU-026) |
| D-05 | 12 oct 2026 | La inteligencia artificial se adelanta: el paciente sube sus historias clínicas y el médico pregunta sobre ellas | Épicas E5 y E6 entran en este alcance |
| D-06 | 12 oct 2026 | El levantamiento de ahora cubre el flujo principal: registro de pacientes, panel del médico, citas de ambas partes y calendario de disponibilidad | 37 historias en 7 épicas al momento de decidirlo; 39 en 8 después de D-13 |
| D-07 | 12 oct 2026 | Se trabaja con Kanban sobre las cinco fases del ciclo de vida | Ver [05-kanban.md](05-kanban.md) |
| D-08 | 12 oct 2026 | Las historias se escriben directamente como archivos. No se usa el generador de la versión anterior | La carpeta `historias-de-usuario/` se edita a mano |
| D-09 | 12 oct 2026 | La facturación electrónica, cuando se retome, se hará con Factus | Queda para después |
| D-10 | 12 oct 2026 | El servidor se construye en Python con FastAPI y la base de datos es PostgreSQL en Render | Ver [arquitectura](../diseno/01-arquitectura.md) |
| D-11 | 12 oct 2026 | La primera versión usa un modelo de IA chino y económico; más adelante se evalúa una API empresarial | Se diseñó un adaptador que permite cambiar de proveedor por configuración |
| D-12 | 12 oct 2026 | Las pantallas se diseñan con un prototipo navegable | Ver [pantallas](../diseno/05-pantallas.md) |
| D-13 | 12 oct 2026 | El paciente tiene una sección "Mis tratamientos" donde ve el último tratamiento | Épica E8 nueva: el total pasa a 39 historias en 8 épicas |
| D-14 | 12 oct 2026 | Al registrarse, la política de tratamiento de datos sale en una ventana que resalta los puntos más importantes, entre ellos el uso de inteligencia artificial sobre las historias clínicas. El texto se afina después | HU-003 y HU-032 ajustadas |
| D-15 | 12 oct 2026 | Al agendar solo se muestran los días y las horas disponibles; lo ocupado no aparece | HU-012 ajustada |
| D-16 | 12 oct 2026 | El calendario del médico permite ir al mes anterior y al siguiente, y al tocar un día abre sus citas | HU-022 ajustada |
| D-17 | 12 oct 2026 | En el producto no hay botones para "ver como" otro rol: cada persona entra con su cuenta. Esos botones son solo del prototipo | Sin efecto en las historias |
| D-18 | 13 oct 2026 | Lo ya hecho en Diseño no se toca; se completa solo lo que falte para desarrollar. El lienzo de pantallas queda aprobado como base del aspecto: paleta de colores y diseño general | La base visual está en [08-base-visual.md](../diseno/08-base-visual.md). Lo que falta de Diseño está en la sección 4 de [ESTADO.md](../ESTADO.md). Las pantallas que no están en el lienzo no se dibujan antes: se arman con sus mismas piezas |
| D-19 | 13 oct 2026 | El código sigue los principios de la arquitectura limpia y debe ser rápido | Capas y reglas de rendimiento en las secciones 7 y 8 de la [arquitectura](../diseno/01-arquitectura.md) |
| D-20 | 13 oct 2026 | Se ingresa con el número de documento y la contraseña. El documento dice quién es la persona; la contraseña sigue siendo propia | RF-03, HU-004 y HU-005 ajustadas. El correo queda para los avisos y para recuperar la contraseña |
| D-21 | 13 oct 2026 | En el registro se piden nombres, apellidos, fecha de nacimiento, correo, documento y teléfono | RF-01 y HU-002. La edad se calcula con la fecha de nacimiento |
| D-22 | 13 oct 2026 | Las cuentas son para adultos. Documentos aceptados: cédula de ciudadanía, cédula de extranjería, pasaporte y permiso por protección temporal | HU-002 y HU-024. Sin menores de edad en la primera versión |
| D-23 | 13 oct 2026 | El paciente puede corregir su teléfono y su correo; el médico puede corregir cualquier dato de un paciente | HU-040 nueva |
| D-24 | 13 oct 2026 | La historia clínica del consultorio entra al alcance. Al atender, el médico ve a un lado el asistente con el resumen y en el centro el formulario de la historia clínica, con lo mínimo que exija la norma | Épica E9 nueva, con seis historias. El contenido está en la sección 4 del [marco normativo](03-marco-normativo.md). El total pasa a 46 historias en 9 épicas |
| D-25 | 13 oct 2026 | El diseño no debe verse genérico: los estados van con un punto de color y su nombre, las notas dejan la caja de color, y los iconos salen de una biblioteca que se vea muy bien. El estado va en una caja de bordes redondeados con peso y sombra, y botones y tarjetas llevan la misma sombra | Corregido en el lienzo. Reglas en la sección 6 de la [base visual](../diseno/08-base-visual.md) |
| D-26 | 13 oct 2026 | Los iconos de la aplicación salen de Phosphor Icons | Se aplica al construir las pantallas. Los iconos del lienzo son provisionales |
| D-27 | 13 oct 2026 | Los servicios se montan en la nube desde el primer día, sin instalar nada en el computador: la base de datos en Render y los archivos en Cloudflare R2 | Cambia el entorno de trabajo: sección 3 de [herramientas y entrega](../diseno/09-herramientas-y-entrega.md). Las pruebas que tocan la base tardan más; las de GitHub usan su propio PostgreSQL |
| D-28 | 13 oct 2026 | El Desarrollo se construye por historias, sin pantalla de verificación del sistema, en este orden: registro e ingreso de paciente y de médico; manejo básico de citas; resumen con IA sobre los documentos del paciente | Las pruebas de concepto de la arquitectura se despejan dentro de cada bloque. Ver la sección 4 de [ESTADO.md](../ESTADO.md) |
| D-29 | 26 oct 2026 | Para programar, la base de datos corre en Docker con la imagen de PostgreSQL 18; no se instala en el computador. Render sigue siendo donde se publica | Ajusta D-27. `docker-compose.yml` en la raíz; detalle en [estado_desarrollo.md](../estado_desarrollo.md) |
| D-30 | 26 oct 2026 | El asistente usa búsqueda de fragmentos (RAG) en lugar de enviar todos los documentos. Busca, siempre de un solo paciente, en sus documentos y en sus atenciones cerradas del consultorio. Los fragmentos y sus vectores van en la misma base PostgreSQL con `pgvector`, y la búsqueda combina significado y palabras. Vectores con `qwen3.7-text-embedding` | Reemplaza la sección 4.1 de la versión 1.1 del [diseño del asistente](../diseno/04-asistente-ia.md), que descartaba la búsqueda semántica, y levanta la regla de que el asistente no lee las atenciones. Nada se indexa sin autorización de IA; las atenciones exigen la versión 2 del texto de autorización. La imagen de Docker pasa a `pgvector/pgvector:pg18-trixie`. Cambian HU-031 a HU-035, HU-042 y HU-044 |

## 2. Supuestos

| # | Supuesto | Dónde pesa | Quién lo confirma |
|---|---|---|---|
| S-01 | Hay un solo médico en el consultorio | HU-001, HU-008, HU-011 | Dueño del proyecto |
| S-02 | El paciente se registra solo, y el médico también puede registrarlo | HU-002, HU-024 | Dueño del proyecto |
| S-03 | El paciente puede mover o cancelar hasta 24 horas antes | HU-014, HU-015 | Primer médico real |
| S-04 | No se ofrecen al paciente espacios que empiecen en menos de una hora | HU-011 | Primer médico real |
| S-05 | Se aceptan PDF, JPG y PNG de hasta 20 MB por archivo | HU-028 | Diseño |
| S-06 | La sesión se cierra a los 30 minutos sin actividad | HU-007 | Diseño |
| S-07 | El ingreso se bloquea 15 minutos después de cinco intentos fallidos | HU-004 | Diseño |
| S-08 | Los avisos de cambios en la cita salen por correo electrónico | HU-019 | Dueño del proyecto |
| S-09 | El asistente solo resume lo registrado; no diagnostica ni sugiere tratamiento | HU-034, HU-035 | Dueño del proyecto |
| S-10 | La aplicación es web y se adapta al celular | Todas las pantallas | Diseño |
| S-11 | Todavía no existe un consultorio real; las reglas se ajustan cuando aparezca | Todos los supuestos de operación | Dueño del proyecto |
| S-12 | El tratamiento lo registra el médico desde la ficha del paciente, con los medicamentos en texto libre; no sale de los documentos que sube el paciente | HU-038, HU-039 | Dueño del proyecto |
| S-13 | En la ventana del registro, el uso de inteligencia artificial tiene su propia casilla, opcional y sin marcar. La Ley 1581 pide que la autorización de datos sensibles sea específica y que no se condicione el servicio a darla | HU-003, HU-032 | Abogado |
| S-14 | El médico también ingresa con su número de documento y su contraseña | HU-004 | Dueño del proyecto |
| S-15 | El correo puede repetirse entre dos pacientes, por ejemplo un hijo que le ayuda a su madre. Lo que no se repite es el documento | HU-002, HU-005 | Dueño del proyecto |
| S-16 | El contenido de la historia clínica sale de la Resolución 1995 de 1999 y de la 866 de 2021. Se revisa cuando se expida la norma que las reemplace | E9 | Abogado |
| S-17 | El detalle clínico del formulario (antecedentes, revisión por sistemas, signos vitales, examen físico) sigue la práctica médica aceptada, porque la norma lo deja a ella | HU-043 | Primer médico real |
| S-18 | Los diagnósticos se eligen de la lista CIE-10 cargada en el sistema. Los medicamentos y las órdenes siguen en texto libre | HU-043, HU-038 | Dueño del proyecto |
| S-19 | La firma de cada atención es la sesión del médico más su nombre y su registro profesional, con fecha y hora | HU-044 | Abogado (pregunta 7) |
| S-20 | El envío del Resumen Digital de Atención al Ministerio no está en este alcance. Los datos se guardan de forma que se pueda generar después | E9 | Abogado (pregunta 5) |
| S-21 | Los datos de identificación que pide la historia clínica y no están en el registro los puede llenar el paciente desde su perfil o el médico desde la ficha | HU-041 | Dueño del proyecto |
| S-22 | Cuando el médico registra a un paciente, el correo es opcional. Sin correo no hay cuenta activa hasta que el médico le agregue uno | HU-024, HU-040 | Dueño del proyecto |
| S-23 | La primera versión sale solo con la apariencia clara, con los tamaños de letra del lienzo aprobado | Todas las pantallas | Dueño del proyecto |
| S-24 | Los fallos de ingreso cuentan por un resumen del documento y no por la cuenta, para que una cuenta que no existe se bloquee igual y el ingreso no revele cuál existe. Quince minutos sin fallar vuelven a contar desde cero. El tope por equipo es de 20 fallos en 15 minutos | HU-004 | Diseño |
| S-25 | En la puesta en marcha el médico escribe también sus nombres y apellidos, además del documento, el correo y la contraseña. El registro profesional se escribe en los datos del consultorio | HU-001 | Dueño del proyecto |
| S-26 | El paciente que se registra entra de inmediato a su inicio, sin confirmar el correo | HU-002 | Dueño del proyecto |
| S-27 | Los iconos usan el grosor de dos tonos de Phosphor | Todas las pantallas | Dueño del proyecto |

## 3. Decisiones que se cerraron en la fase de Diseño

| # | Decisión | Cómo quedó | Quién decidió |
|---|---|---|---|
| A-01 | Tecnología de la aplicación y del servidor | FastAPI en el servidor; React con Vite y TypeScript en las pantallas | El servidor, el dueño del proyecto. React frente a Astro, propuesta de diseño |
| A-02 | Base de datos | PostgreSQL en Render, con permisos por fila | Dueño del proyecto |
| A-03 | Dónde se aloja el sistema y los documentos | Render para la aplicación; archivos en Cloudflare R2, que habla el protocolo S3. El almacenamiento de objetos de Render está en alfa y MinIO dejó de publicarse en 2026 | Render, el dueño del proyecto. R2 era propuesta de diseño y quedó en firme con D-27 |
| A-04 | Proveedor de inteligencia artificial | Qwen por la plataforma internacional de Alibaba Cloud | El dueño propuso DeepSeek o Qwen; se eligió Qwen por las razones de [04-asistente-ia.md](../diseno/04-asistente-ia.md) |
| A-05 | Cómo se lee el texto de fotos y documentos escaneados | PDF con texto, dentro del servidor; fotos y escaneados, con el modelo de visión del mismo proveedor y solo con autorización del paciente | Propuesta de diseño |
| A-06 | Proveedor de correo | Por API (propuesta: Resend) | Propuesta de diseño |
| A-07 | Ingreso con un documento que es fácil de conocer | Tipo y número de documento más contraseña. El bloqueo por intentos fallidos es por cuenta y por equipo, para que un tercero no le bloquee la cuenta a su dueño | Propuesta de diseño, sobre D-20 |
| A-08 | Permisos por fila cuando todavía no hay sesión, y en los procesos en segundo plano | Funciones de la base que hacen una sola cosa cada una, y una identidad `sistema` para el lector y el envío de avisos. Ver la sección 3 del [modelo de datos](../diseno/02-modelo-de-datos.md) | Propuesta de diseño |
| A-09 | Historia clínica que no cambia | Un disparador en la base rechaza modificar o borrar una atención cerrada; se corrige con notas aclaratorias | Propuesta de diseño, sobre D-24 |
| A-10 | Pantalla de atención | Formulario en el centro, en ocho secciones; asistente a la derecha, plegable; el asistente nunca escribe en la historia | Propuesta de diseño, sobre D-24 |
| A-11 | Herramientas, servicios y flujo de entrega | Ver [09-herramientas-y-entrega.md](../diseno/09-herramientas-y-entrega.md). Repositorio remoto privado y pruebas automáticas antes de cada despliegue. El entorno de trabajo cambió con D-27 | Propuesta de diseño |
| A-12 | Biblioteca para leer PDF | `pypdfium2` en lugar de PyMuPDF, cuya licencia obligaría a publicar el código | Propuesta de diseño |
| A-13 | Pantallas que no están en el lienzo | No se dibujan antes: se arman con las piezas de la [base visual](../diseno/08-base-visual.md), siguiendo el prototipo | Propuesta de diseño, sobre D-18 |
| A-14 | Biblioteca de iconos | Phosphor Icons, en un solo grosor | Propuesta de diseño que el dueño del proyecto confirmó (D-26) |
| A-15 | Modelos de Qwen | `qwen3.7-plus` para las respuestas y `qwen3.5-ocr` para la lectura, en la región Singapur. Los que nombraba el diseño (`qwen-plus` y `qwen-vl-ocr`) son de la generación anterior. Se confirman con la primera llamada | Propuesta de diseño, sobre A-04 |

Las "propuestas de diseño" se pueden cambiar sin rehacer el resto: están aisladas detrás de una sola pieza cada una.

**Condición para usar datos reales.** La primera versión se prueba solo con documentos inventados o anonimizados. Antes de cargar historias de pacientes reales hacen falta la respuesta del abogado a la pregunta 2 del [marco normativo](03-marco-normativo.md) y un contrato de tratamiento de datos con el proveedor de IA y con el de alojamiento.

## 4. Investigación ya hecha que servirá después

| Tema | Hallazgo |
|---|---|
| Factus | Emite facturas del sector salud y tiene ambiente de pruebas gratuito. Su documentación no menciona el RIPS |
| Factus Pay | Cobra con código QR y avisa cuando el pago entra. No tiene devolución automática |
| RIPS | La Resolución 948 de 2026 reemplazó a la 2275 de 2023. No está claro si aplica a un consultorio que solo atiende particulares |
| RDA | La Resolución 1888 de 2025 aplica a prestadores privados; puede ser obligatoria cuando el médico escriba la nota clínica en el sistema |

Fuentes: [Factus API](https://developers.factus.com.co/) · [Factus Pay](https://pay-developers.factus.com.co)
