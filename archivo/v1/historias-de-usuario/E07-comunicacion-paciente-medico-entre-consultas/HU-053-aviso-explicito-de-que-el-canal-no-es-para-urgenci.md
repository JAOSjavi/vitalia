# HU-053 — Aviso explícito de que el canal no es para urgencias

| Dato | Valor |
|---|---|
| Épica | E7 Comunicación paciente–médico entre consultas |
| Fase | 2 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 2 puntos |
| Requisitos | RF-43 |
| Jira | pendiente de cargar |

## Historia

> Como responsable del producto, quiero que nadie confunda este canal con una urgencia, para evitar un daño por una respuesta tardía.

## Criterios de aceptación

- **CA-1** · Dado que abro el canal de mensajes, cuando se muestra la pantalla, entonces aparece de forma permanente y legible el aviso de que no atiende urgencias, indicando llamar a la línea de emergencias.
- **CA-2** · Dado que escribo por primera vez en una conversación, cuando envío el mensaje, entonces el sistema muestra el aviso completo antes de confirmar el envío.
- **CA-3** · Dado que el aviso se muestra, cuando se evalúa su accesibilidad, entonces cumple el contraste mínimo y se mantiene visible en modo accesible.

## Tareas y actividades

### T-053.1 Componente de advertencia

- Diseñar el aviso persistente
- Validar contraste y tamaño
- Incluir la línea de emergencias

### T-053.2 Confirmación en el primer mensaje

- Diálogo previo al primer envío
- Registro de que fue mostrado

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-051 Reportar un síntoma o una duda](HU-051-reportar-un-sintoma-o-una-duda.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E7](README.md) · [Mapa de relaciones](../RELACIONES.md)
