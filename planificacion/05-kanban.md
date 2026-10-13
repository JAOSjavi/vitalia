# Tablero Kanban

**Fase del ciclo de vida:** Planificación
**Versión:** 2.0 · 12 de octubre de 2026

Kanban no trabaja por sprints. El trabajo se **jala** de izquierda a derecha cuando hay capacidad, y cada columna tiene un tope de tarjetas en curso. El tablero sigue las cinco fases del ciclo de vida.

---

## 1. Columnas

| Columna | Qué hay aquí | Tope en curso | Para entrar | Para salir |
|---|---|---|---|---|
| **Por hacer** | Historias priorizadas, en orden | Sin tope | La historia existe en `historias-de-usuario/` | Hay capacidad en Planificación |
| **Planificación** | Se afinan criterios, tareas y supuestos | 3 | Es la siguiente en el orden de construcción | Criterios de aceptación completos, dependencias resueltas, supuestos marcados |
| **Diseño** | Pantallas, modelo de datos y contrato del servicio | 2 | Cumple la salida de Planificación | Diseño revisado y anexado a la historia |
| **Desarrollo** | Se construye | 2 | Diseño aprobado | Código revisado, pruebas automáticas en verde |
| **Pruebas** | Se verifica contra los criterios de aceptación | 2 | Desplegado en el ambiente de pruebas | Todos los criterios cumplidos; sin errores abiertos |
| **Despliegue** | Se pasa a producción | 1 | Pruebas aprobadas | En producción y verificado |
| **Hecho** | Terminado | Sin tope | — | — |

Los topes son la propuesta inicial para una persona o un equipo muy pequeño. Se ajustan mirando dónde se acumulan las tarjetas.

## 2. Reglas del tablero

1. **Se termina antes de empezar.** Si una columna está en su tope, no entra nada nuevo: se ayuda a sacar lo que ya está.
2. **Una tarjeta es una historia.** Las tareas viven dentro de la historia, como lista de verificación.
3. **Lo bloqueado se marca.** Una tarjeta bloqueada lleva la razón y de quién depende; sigue contando en el tope.
4. **El orden lo dan las dependencias.** Se respeta el [mapa de relaciones](../historias-de-usuario/RELACIONES.md): no se jala una historia antes que las que necesita.
5. **Los errores vuelven a Desarrollo.** Una historia que falla en Pruebas regresa con el criterio que no cumplió.

## 3. Tipos de tarjeta

| Tipo | Uso |
|---|---|
| Historia | Funcionalidad con valor para el médico o el paciente |
| Habilitador | Trabajo técnico necesario para otras historias (las de rol "Sistema") |
| Error | Fallo encontrado en Pruebas o en producción |
| Pregunta | Decisión abierta o consulta al abogado que bloquea trabajo |

## 4. Qué medir

| Medida | Para qué |
|---|---|
| Tiempo de ciclo | Días desde que una historia entra a Planificación hasta Hecho. Sirve para estimar fechas |
| Trabajo en curso | Tarjetas abiertas por columna. Si crece, algo está atascado |
| Tarjetas bloqueadas | Cuántas y por cuánto tiempo |

## 5. Estado del tablero

- **Pendiente:** crear el proyecto de tipo Kanban en Jira. El proyecto anterior es de tipo Scrum y contiene 96 tarjetas del backlog viejo; se archiva.
- **Carga inicial:** las 7 épicas y las 37 historias entran a "Por hacer" en el orden de construcción de [RELACIONES.md](../historias-de-usuario/RELACIONES.md).
- **Primeras en jalar:** HU-006, HU-036, HU-037 y HU-027, porque de ellas depende casi todo lo demás.
