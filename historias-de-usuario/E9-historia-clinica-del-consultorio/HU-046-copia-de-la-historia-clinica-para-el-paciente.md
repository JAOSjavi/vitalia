# HU-046 — Copia de la historia clínica para el paciente

| Dato | Valor |
|---|---|
| Épica | E9 Historia clínica del consultorio |
| Rol | Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-46 |
| Origen | Nueva (decisión D-24) |

## Historia

> Como médico, quiero generar una copia de la historia clínica de un paciente, para entregársela cuando la pida.

## Criterios de aceptación

- **CA-1** · Dado un paciente con atenciones cerradas, cuando genero la copia, entonces obtengo un PDF con sus datos de identificación y las atenciones que elija, cada una con su autor, fecha y hora.
- **CA-2** · Dada una atención que sigue abierta, cuando genero la copia, entonces no se incluye.
- **CA-3** · Dado que genero una copia, cuando termina, entonces queda en la bitácora quién la generó, de qué paciente y cuándo.
- **CA-4** · Dado el PDF, cuando se revisa, entonces su texto se puede seleccionar y leer; no es una imagen.

## Tareas y actividades

### T-046.1 Generación del PDF

- Plantilla con identificación y atenciones
- Selección de las atenciones a incluir
- Registro en la bitácora

### T-046.2 Pruebas

- Copia con varias atenciones
- Atención abierta excluida

## Nota de alcance

El paciente es dueño de su historia clínica (Ley 2015 de 2020) y tiene derecho a pedir copia. En esta versión se la entrega el médico; que el paciente la vea desde su cuenta queda para después.

## Relación con otras historias

**Depende de:**

- [HU-044 Cerrar y firmar la atención](HU-044-cerrar-y-firmar-la-atencion.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
