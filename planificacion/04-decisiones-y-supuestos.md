# Decisiones y supuestos

**Fase del ciclo de vida:** Planificación
**Versión:** 2.0 · 12 de octubre de 2026

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

## 3. Decisiones que se cerraron en la fase de Diseño

| # | Decisión | Cómo quedó | Quién decidió |
|---|---|---|---|
| A-01 | Tecnología de la aplicación y del servidor | FastAPI en el servidor; React con Vite y TypeScript en las pantallas | El servidor, el dueño del proyecto. React frente a Astro, propuesta de diseño |
| A-02 | Base de datos | PostgreSQL en Render, con permisos por fila | Dueño del proyecto |
| A-03 | Dónde se aloja el sistema y los documentos | Render para la aplicación; archivos en almacenamiento compatible con S3 (propuesta: Cloudflare R2) | Render, el dueño del proyecto. El almacenamiento, propuesta de diseño |
| A-04 | Proveedor de inteligencia artificial | Qwen por la plataforma internacional de Alibaba Cloud | El dueño propuso DeepSeek o Qwen; se eligió Qwen por las razones de [04-asistente-ia.md](../diseno/04-asistente-ia.md) |
| A-05 | Cómo se lee el texto de fotos y documentos escaneados | PDF con texto, dentro del servidor; fotos y escaneados, con el modelo de visión del mismo proveedor y solo con autorización del paciente | Propuesta de diseño |
| A-06 | Proveedor de correo | Por API (propuesta: Resend) | Propuesta de diseño |

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
