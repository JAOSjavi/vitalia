# HU-044 — Cerrar y firmar la atención

| Dato | Valor |
|---|---|
| Épica | E9 Historia clínica del consultorio |
| Rol | Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-44, RNF-15 |
| Origen | Nueva (decisión D-24) |

## Historia

> Como médico, quiero cerrar la atención con mi firma, para que el registro quede completo y nadie lo pueda cambiar después.

## Criterios de aceptación

- **CA-1** · Dado que todos los campos obligatorios están llenos, cuando cierro la atención y confirmo con mi contraseña, entonces queda con mi nombre, mi registro profesional, la fecha y la hora de cierre.
- **CA-2** · Dado que falta un campo obligatorio de la consulta o de la identificación del paciente, cuando intento cerrar, entonces el sistema no cierra y me dice qué falta.
- **CA-3** · Dada una atención cerrada, cuando alguien intenta modificarla o borrarla, entonces la base de datos lo rechaza.
- **CA-4** · Dada una atención cerrada que tiene un error, cuando agrego una nota aclaratoria, entonces queda debajo del registro original con mi nombre, la fecha y la hora, y el original no cambia.
- **CA-5** · Dado que cierro la atención, cuando termina, entonces la cita queda marcada como atendida y el cierre queda en la bitácora.
- **CA-6** · Dada una atención que lleva más de 24 horas abierta, cuando entro al panel, entonces veo el aviso de que está sin cerrar.

## Tareas y actividades

### T-044.1 Cierre

- Validación de campos obligatorios
- Sello con autor, registro profesional, fecha y hora
- Confirmación con la contraseña del médico

### T-044.2 Registro que no cambia

- Regla en la base de datos contra modificar o borrar
- Notas aclaratorias sumadas al registro
- Aviso de atenciones sin cerrar

### T-044.3 Pruebas

- Cierre con campos faltantes
- Intento de modificar una atención cerrada
- Nota aclaratoria

## Nota de alcance

La Resolución 1995 de 1999 pide que lo guardado no se pueda modificar y que el autor quede identificado por un medio que reemplace la firma (art. 18). Aquí ese medio es la sesión del médico confirmada con su contraseña (supuesto S-19). Si hace falta firma digital certificada es la pregunta 7 para el abogado.

## Relación con otras historias

**Depende de:**

- [HU-041 Datos de identificación de la historia clínica](HU-041-datos-de-identificacion-de-la-historia-clinica.md)
- [HU-043 Registrar la consulta en la historia clínica](HU-043-registrar-la-consulta-en-la-historia-clinica.md)

**Habilita:**

- [HU-045 Consultar la historia clínica de un paciente](HU-045-consultar-la-historia-clinica-de-un-paciente.md)
- [HU-046 Copia de la historia clínica para el paciente](HU-046-copia-de-la-historia-clinica-para-el-paciente.md)

---

[← Volver a E9](README.md) · [Mapa de relaciones](../RELACIONES.md)
