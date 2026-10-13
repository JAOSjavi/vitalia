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
| D-06 | 12 oct 2026 | El levantamiento de ahora cubre el flujo principal: registro de pacientes, panel del médico, citas de ambas partes y calendario de disponibilidad | 37 historias en 7 épicas |
| D-07 | 12 oct 2026 | Se trabaja con Kanban sobre las cinco fases del ciclo de vida | Ver [05-kanban.md](05-kanban.md) |
| D-08 | 12 oct 2026 | Las historias se escriben directamente como archivos. No se usa el generador de la versión anterior | La carpeta `historias-de-usuario/` se edita a mano |
| D-09 | 12 oct 2026 | La facturación electrónica, cuando se retome, se hará con Factus | Queda para después |

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

## 3. Decisiones abiertas para la fase de Diseño

| # | Decisión | Qué hay que considerar |
|---|---|---|
| A-01 | Tecnología de la aplicación y del servidor | Pesa más quién la va a mantener que el lenguaje |
| A-02 | Base de datos | Debe permitir permisos por fila de forma nativa (HU-036) |
| A-03 | Dónde se aloja el sistema y los documentos | Cifrado, respaldos y ubicación de los datos (pregunta 2 del [marco normativo](03-marco-normativo.md)) |
| A-04 | Proveedor de inteligencia artificial | Que lea PDF e imágenes, cite la página de origen y firme un acuerdo de tratamiento de datos |
| A-05 | Cómo se lee el texto de fotos y documentos escaneados | Calidad con letra manuscrita y costo por página (HU-031) |
| A-06 | Proveedor de correo | Entrega confiable de la recuperación de contraseña y de los avisos |

## 4. Investigación ya hecha que servirá después

| Tema | Hallazgo |
|---|---|
| Factus | Emite facturas del sector salud y tiene ambiente de pruebas gratuito. Su documentación no menciona el RIPS |
| Factus Pay | Cobra con código QR y avisa cuando el pago entra. No tiene devolución automática |
| RIPS | La Resolución 948 de 2026 reemplazó a la 2275 de 2023. No está claro si aplica a un consultorio que solo atiende particulares |
| RDA | La Resolución 1888 de 2025 aplica a prestadores privados; puede ser obligatoria cuando el médico escriba la nota clínica en el sistema |

Fuentes: [Factus API](https://developers.factus.com.co/) · [Factus Pay](https://pay-developers.factus.com.co)
