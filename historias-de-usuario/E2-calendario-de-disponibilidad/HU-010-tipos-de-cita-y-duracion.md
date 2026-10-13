# HU-010 — Tipos de cita y duración

| Dato | Valor |
|---|---|
| Épica | E2 Calendario de disponibilidad |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-10 |
| Origen | Nueva |

## Historia

> Como médico, quiero definir los tipos de cita que ofrezco y cuánto dura cada uno, para que la agenda reserve el tiempo correcto.

## Criterios de aceptación

- **CA-1** · Dado que creo un tipo con nombre y duración en minutos, cuando guardo, entonces el paciente lo ve como opción al agendar.
- **CA-2** · Dado un tipo con citas futuras, cuando cambio su duración, entonces el cambio aplica solo a las citas nuevas.
- **CA-3** · Dado un tipo que ya no ofrezco, cuando lo desactivo, entonces deja de ofrecerse y las citas existentes se conservan.
- **CA-4** · Dado que no hay ningún tipo activo, cuando un paciente intenta agendar, entonces ve un aviso de que la agenda no está disponible.

## Tareas y actividades

### T-010.1 Modelo de tipos de cita

- Tabla con nombre, duración y estado
- Regla de no alterar las citas existentes
- Tipos iniciales sugeridos (consulta general, control)

### T-010.2 Pantalla de tipos de cita

- Crear y editar
- Activar y desactivar
- Vista de lo que verá el paciente

## Relación con otras historias

**Depende de:**

- [HU-001 Configuración inicial del consultorio](../E1-cuentas-e-ingreso/HU-001-configuracion-inicial-del-consultorio.md)

**Habilita:**

- [HU-011 Cálculo de espacios libres sin choques](HU-011-calculo-de-espacios-libres.md)

---

[← Volver a E2](README.md) · [Mapa de relaciones](../RELACIONES.md)
