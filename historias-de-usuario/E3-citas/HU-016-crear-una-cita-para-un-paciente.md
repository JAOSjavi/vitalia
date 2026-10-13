# HU-016 — Crear una cita para un paciente

| Dato | Valor |
|---|---|
| Épica | E3 Citas |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-15 |
| Origen | Nueva |

## Historia

> Como médico, quiero agendarle una cita a un paciente desde mi panel, para atender a quien llama o llega sin haber usado la aplicación.

## Criterios de aceptación

- **CA-1** · Dado que busco un paciente y elijo tipo, día y hora, cuando confirmo, entonces la cita queda creada y el paciente la ve en "Mis citas".
- **CA-2** · Dado que el paciente no existe, cuando lo busco, entonces el sistema me ofrece registrarlo ahí mismo y continuar con la cita.
- **CA-3** · Dado que necesito un horario por fuera de mi horario habitual, cuando lo elijo, entonces el sistema me advierte y me deja confirmar, siempre que no se cruce con otra cita.
- **CA-4** · Dado que el horario se cruza con otra cita, cuando intento confirmar, entonces el sistema lo impide.

## Tareas y actividades

### T-016.1 Servicio de cita creada por el médico

- Crear la cita a nombre del paciente
- Permitir un horario fuera de franja con advertencia
- Impedir cruces con otras citas

### T-016.2 Formulario en el panel

- Buscador de paciente
- Selección de tipo, día y hora
- Acceso al registro rápido de paciente

## Relación con otras historias

**Depende de:**

- [HU-011 Cálculo de espacios libres sin choques](../E2-calendario-de-disponibilidad/HU-011-calculo-de-espacios-libres.md)
- [HU-023 Lista y búsqueda de pacientes](../E4-panel-del-medico/HU-023-lista-y-busqueda-de-pacientes.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E3](README.md) · [Mapa de relaciones](../RELACIONES.md)
