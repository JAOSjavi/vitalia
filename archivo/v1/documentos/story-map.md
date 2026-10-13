# Vitalia Salud — User Story Map para Miro

**Documento:** 05 — Mapa de historias de usuario
**Destino:** Plantilla **User Story Map** de Miro (Miro → Plantillas → buscar «User Story Map» o «Story Mapping»)
**Estructura del mapa:** actividades (columna vertebral) → pasos del usuario → historias organizadas por entrega

---

## 1. Cómo armarlo en Miro

1. Abra Miro → **Plantillas** → busque **«User Story Map»** → *Usar plantilla*.
2. La plantilla trae tres zonas: fila superior de **actividades**, fila de **pasos** y franjas horizontales de **releases**. Renombre las franjas como: `Fase 1 — MVP`, `Fase 2 — Adherencia`, `Fase 3 — Escalamiento`, `Fase 4 — Interoperabilidad`.
3. Para cargar las notas: copie un bloque de esta guía, haga doble clic en el lienzo y pegue. **Miro crea una nota adhesiva por cada línea**, así que cada bloque llena una columna completa de un tirón.
4. Recomendación de color, para que el mapa se lea sin explicación:
   - **Azul** — actividades (columna vertebral)
   - **Gris** — pasos del usuario
   - **Amarillo** — historias de Fase 1
   - **Verde** — Fase 2
   - **Naranja** — Fase 3
   - **Morado** — Fase 4
5. Trace una línea horizontal gruesa bajo la franja de Fase 1: ese es el corte del MVP y es lo que hay que poder defender en una sola frase — *«con esto el consultorio ya opera»*.

---

## 2. Columna vertebral — Actividades del usuario

> Pegar como fila superior (notas azules). Es el recorrido del paciente de izquierda a derecha, y al final la operación de la clínica.

```
1. Tener una cuenta
2. Conseguir una cita
3. Prepararse para la consulta
4. Ser atendido
5. Entender qué debe hacer
6. Cumplir el tratamiento en casa
7. Resolver dudas entre consultas
8. Continuar el cuidado
9. Operar la clínica
```

---

## 3. Pasos del usuario por actividad

> Pegar bajo cada actividad (notas grises).

**1. Tener una cuenta**
```
Registrarse
Ingresar
Recuperar el acceso
Autorizar el uso de mis datos
```

**2. Conseguir una cita**
```
Elegir tipo de cita
Escoger profesional y horario
Confirmar la cita
Mover o cancelar la cita
```

**3. Prepararse para la consulta**
```
Recordar que tengo cita
Confirmar que asistiré
Enviar exámenes previos
```

**4. Ser atendido**
```
Ver la agenda del día
Revisar la historia del paciente
Registrar la consulta
Registrar asistencia
```

**5. Entender qué debe hacer**
```
Recibir medicamentos indicados
Recibir cuidados indicados
Conocer los próximos pasos
Consultar el plan cuando lo necesite
```

**6. Cumplir el tratamiento en casa**
```
Recibir el recordatorio a tiempo
Confirmar que cumplí
Ver cómo voy
Recibir ayuda si dejo de cumplir
```

**7. Resolver dudas entre consultas**
```
Reportar un síntoma
Recibir respuesta del médico
Saber que no es un canal de urgencias
```

**8. Continuar el cuidado**
```
Agendar el control
Consultar mi historia y documentos
Compartir mi información cuando lo autorizo
```

**9. Operar la clínica**
```
Gestionar profesionales y horarios
Ver el desempeño de la operación
Atender varias sedes
```

---

## 4. Historias por franja de entrega

### Franja — Fase 1 · MVP (notas amarillas)

**Bajo «Tener una cuenta»**
```
HU-001 Registro de paciente
HU-002 Ingreso con contraseña
HU-003 Ingreso con código por SMS
HU-004 Recuperación de contraseña
HU-005 Roles y permisos en base de datos
HU-006 Cierre de sesión y expiración
HU-037 Aceptación de política de datos
```

**Bajo «Conseguir una cita»**
```
HU-007 Agendar una cita desde la app
HU-008 Disponibilidad en tiempo real
HU-009 Reagendar una cita
HU-010 Cancelar una cita
HU-011 Consultar mis citas
```

**Bajo «Prepararse para la consulta»**
```
HU-030 Recordatorio de cita 24 h y 1 h
HU-012 Adjuntar documento al agendar
HU-032 Configurar canal preferido
HU-033 Envío por WhatsApp con plantillas
HU-034 Envío por SMS
```

**Bajo «Ser atendido»**
```
HU-014 Agenda del día del profesional
HU-017 Consultar historia clínica
HU-015 Registrar nota clínica
HU-016 Cargar documentos clínicos
HU-018 Visor de PDF integrado
HU-013 Registrar asistencia
```

**Bajo «Entender qué debe hacer»**
```
HU-021 Registrar medicamentos del plan
HU-022 Catálogo de medicamentos
HU-023 Aviso de interacciones
HU-024 Registrar cuidados
HU-025 Registrar próximos pasos
HU-026 Fecha de fin automática
HU-027 Ver Mi plan de tratamiento
HU-028 Historial de planes
```

**Bajo «Cumplir el tratamiento en casa»**
```
HU-029 Programación de recordatorios de medicamento
HU-031 Recordatorio de cuidados
```

**Bajo «Continuar el cuidado»**
```
HU-019 Ver mis documentos
HU-020 Bitácora de auditoría
HU-035 Seguridad a nivel de fila
HU-036 Documentos con URL firmada
```

---

### Franja — Fase 2 · Adherencia y WhatsApp (notas verdes)

**Bajo «Conseguir una cita»**
```
HU-038 Agendar por WhatsApp
HU-039 Registrar paciente desde WhatsApp
HU-040 Cancelar o reagendar por el mensaje
HU-042 Consultar mi próxima cita
HU-043 Plantillas y ventana de 24 horas
```

**Bajo «Prepararse para la consulta»**
```
HU-041 Confirmar asistencia el día anterior
```

**Bajo «Cumplir el tratamiento en casa»**
```
HU-044 Marcar recordatorio como cumplido
HU-045 Confirmar la toma desde WhatsApp
HU-046 Reintento por canal alterno
HU-047 Cálculo del indicador de adherencia
HU-050 Ver mi propia adherencia
HU-048 Panel de adherencia del médico
HU-049 Alerta por incumplimiento
```

**Bajo «Resolver dudas entre consultas»**
```
HU-051 Reportar un síntoma o duda
HU-052 Responder o derivar a control
HU-053 Aviso de no urgencias
HU-054 Notificación de respuesta
```

---

### Franja — Fase 3 · Escalamiento (notas naranjas)

**Bajo «Entender qué debe hacer»**
```
HU-065 Exportar el plan en PDF
HU-064 Lectura en voz alta
HU-062 Contenido educativo curado
```

**Bajo «Cumplir el tratamiento en casa»**
```
HU-063 Modo accesible
HU-067 Autorizar a un cuidador
HU-068 Vista del cuidador
HU-069 Revocar acceso del cuidador
```

**Bajo «Ser atendido»**
```
HU-059 Consentimiento para uso de IA
HU-060 Asistente clínico sobre la historia
HU-061 Intermediación de IA por backend
```

**Bajo «Continuar el cuidado»**
```
HU-070 Ver quién accedió a mi historia
HU-066 Encuesta de satisfacción
```

**Bajo «Operar la clínica»**
```
HU-055 Gestionar profesionales
HU-056 Gestionar horarios
HU-057 Aislamiento entre sedes
HU-058 Reportes de operación
```

---

### Franja — Fase 4 · Interoperabilidad (notas moradas)

**Bajo «Continuar el cuidado»**
```
HU-074 Consentimiento para compartir el resumen
HU-071 Generar el Resumen Digital de Atención
HU-072 Intercambiar el RDA
```

**Bajo «Operar la clínica»**
```
HU-073 Registro de eventos de interoperabilidad
```

---

## 5. El corte del MVP, en una frase

> Con la **Fase 1**, un consultorio ya opera completo: el paciente se registra, agenda, es atendido con historia clínica digital válida, recibe su plan de tratamiento en pantalla y le llegan los recordatorios por WhatsApp. Lo que la Fase 2 agrega no es funcionalidad nueva del ciclo, sino la **prueba del diferencial**: que el paciente confirme y que el médico lo vea.

**Riesgo consciente del corte:** en Fase 1 los recordatorios salen, pero nadie confirma que se cumplieron. La adherencia todavía no se mide. Es aceptable para operar, pero **no** para vender el diferencial del producto: por eso la Fase 2 no es opcional y debe ir inmediatamente después.

---

## 6. Notas para la sesión de mapeo

Cuando arme el tablero, deje a la vista estas tres preguntas —son las que hacen útil un story map frente a una lista:

1. **¿Qué pasa si esta historia no está?** Si el paciente igual completa su recorrido, no es de Fase 1.
2. **¿Hay algún paso del recorrido sin ninguna historia en la franja del MVP?** Ese es un hueco: el usuario se queda a mitad de camino.
3. **¿Qué historia de una franja posterior está sosteniendo la promesa comercial?** Si el argumento de venta depende de ella, la franja está mal cortada.
