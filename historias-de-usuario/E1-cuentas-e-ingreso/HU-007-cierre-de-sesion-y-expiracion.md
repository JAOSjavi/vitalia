# HU-007 — Cierre de sesión y expiración

| Dato | Valor |
|---|---|
| Épica | E1 Cuentas e ingreso |
| Rol | Paciente, Médico |
| Prioridad | Should (MoSCoW) |
| Estimación | 2 puntos |
| Requisitos | RF-05 |
| Origen | HU-006 de la versión anterior, ajustada |

## Historia

> Como usuario, quiero cerrar mi sesión y que se cierre sola si dejo de usarla, para que nadie más vea mi información.

## Criterios de aceptación

- **CA-1** · Dado que tengo la sesión abierta, cuando elijo cerrar sesión, entonces la sesión queda invalidada en el servidor y vuelvo a la pantalla de ingreso.
- **CA-2** · Dados 30 minutos sin actividad, cuando intento hacer algo, entonces el sistema me pide ingresar de nuevo.
- **CA-3** · Dado que cerré sesión, cuando uso el botón de atrás del navegador, entonces no veo información de la sesión anterior.

## Tareas y actividades

### T-007.1 Ciclo de vida de la sesión

- Invalidación de la sesión en el servidor
- Expiración por inactividad
- Limpieza de los datos guardados en el navegador

## Relación con otras historias

**Depende de:**

- [HU-004 Ingreso con contraseña](HU-004-ingreso-con-contrasena.md)

**Habilita:**

- Ninguna la tiene como requisito previo.

---

[← Volver a E1](README.md) · [Mapa de relaciones](../RELACIONES.md)
