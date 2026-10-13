# HU-040 — Corregir los datos de un paciente

| Dato | Valor |
|---|---|
| Épica | E1 Cuentas e ingreso |
| Rol | Paciente, Médico |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-40 |
| Origen | Nueva (decisión D-23) |

## Historia

> Como paciente o como médico, quiero corregir los datos de un paciente que ya tiene cuenta, para que el consultorio pueda ubicarlo y su historia quede bien identificada.

## Criterios de aceptación

- **CA-1** · Dado que soy paciente, cuando cambio mi teléfono o mi correo desde mi perfil y confirmo con mi contraseña, entonces quedan actualizados.
- **CA-2** · Dado que soy paciente, cuando abro mi perfil, entonces mis nombres, mi documento y mi fecha de nacimiento aparecen sin opción de editarlos, con la indicación de pedir el cambio al consultorio.
- **CA-3** · Dado que soy médico, cuando corrijo cualquier dato de un paciente desde su ficha, entonces queda actualizado y el cambio queda en la bitácora con el valor anterior y el nuevo.
- **CA-4** · Dado que el médico cambia el número de documento por uno que ya tiene otro paciente, cuando intenta guardar, entonces el sistema lo impide y le muestra ese paciente.
- **CA-5** · Dado que cambia el correo o el número de documento de un paciente, cuando se guarda, entonces el paciente recibe un aviso en su correo anterior y, desde ese momento, ingresa con el documento nuevo.

## Tareas y actividades

### T-040.1 Servicio de corrección

- Regla de qué puede cambiar cada rol
- Validación de que el documento no se repita
- Registro del cambio en la bitácora

### T-040.2 Pantallas

- Edición de teléfono y correo en el perfil del paciente
- Edición de los datos en la ficha del paciente
- Aviso por correo del cambio

### T-040.3 Pruebas

- Paciente intentando cambiar su documento
- Documento repetido
- Ingreso con el documento nuevo

## Relación con otras historias

**Depende de:**

- [HU-025 Ficha del paciente](../E4-panel-del-medico/HU-025-ficha-del-paciente.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
