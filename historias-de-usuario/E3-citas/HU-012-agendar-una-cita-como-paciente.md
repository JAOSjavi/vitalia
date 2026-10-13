# HU-012 — Agendar una cita como paciente

| Dato | Valor |
|---|---|
| Épica | E3 Citas |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-12 |
| Origen | HU-007 de la versión anterior, ajustada |

## Historia

> Como paciente, quiero agendar mi cita eligiendo tipo, día y hora, para no tener que llamar al consultorio.

## Criterios de aceptación

- **CA-1** · Dado que elijo un tipo de cita, un día y un espacio libre, cuando confirmo, entonces la cita queda creada como confirmada y veo el resumen con fecha, hora y tipo.
- **CA-2** · Dado que el espacio fue tomado mientras yo elegía, cuando confirmo, entonces el sistema me avisa y me muestra los espacios libres más cercanos.
- **CA-3** · Dado que ya tengo una cita futura del mismo tipo, cuando intento agendar otra, entonces el sistema me lo advierte y me pide confirmar.
- **CA-4** · Dado que no he aceptado la autorización de tratamiento de datos, cuando intento agendar, entonces el sistema me lleva primero a aceptarla.
- **CA-5** · Dado un día sin horas libres o una hora ya ocupada, cuando elijo día y hora, entonces no aparecen: solo se listan los días y las horas disponibles. *(Agregado en Diseño.)*

## Tareas y actividades

### T-012.1 Servicio de agendamiento

- Crear la cita validando el espacio
- Estados de la cita: confirmada, cancelada, atendida, no asistió
- Regla de advertencia por cita repetida

### T-012.2 Asistente de agendamiento

- Paso de tipo de cita
- Paso de día y hora
- Paso de confirmación y resumen

### T-012.3 Pruebas

- Recorrido completo
- Espacio tomado durante la elección
- Paciente sin autorización aceptada

## Relación con otras historias

**Depende de:**

- [HU-004 Ingreso con contraseña](../E1-cuentas-e-ingreso/HU-004-ingreso-con-contrasena.md)
- [HU-011 Cálculo de espacios libres sin choques](../E2-calendario-de-disponibilidad/HU-011-calculo-de-espacios-libres.md)

**Habilita:**

- [HU-013 Consultar mis citas](HU-013-consultar-mis-citas.md)
- [HU-014 Mover mi cita](HU-014-mover-mi-cita.md)
- [HU-015 Cancelar mi cita](HU-015-cancelar-mi-cita.md)
- [HU-019 Aviso por correo de cambios en la cita](HU-019-aviso-por-correo-de-cambios-en-la-cita.md)

---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
