# HU-019 — Ver mis documentos como paciente

| Dato | Valor |
|---|---|
| Épica | E4 Historia clínica y documentos |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Should (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-19, RF-21 |
| Jira | SCRUM-82 |

## Historia

> Como paciente, quiero ver mis exámenes y fórmulas en la aplicación, para tenerlos a la mano cuando los necesite.

## Criterios de aceptación

- **CA-1** · Dado que abro «Mi historia», cuando carga, entonces veo mis documentos con tipo, fecha y origen, del más reciente al más antiguo.
- **CA-2** · Dado que abro un documento, cuando se despliega, entonces se carga mediante URL firmada temporal y se registra el acceso.
- **CA-3** · Dado que otro usuario intenta acceder a un documento mío, cuando hace la petición, entonces el sistema responde 403 y registra el intento.
- **CA-4** · Dado que la pantalla se muestra, cuando la leo, entonces incluye una nota explicando que los enlaces son temporales y privados.

## Tareas y actividades

### T-019.1 Endpoint de documentos del paciente

- Filtrar por identidad autenticada
- Ordenar por fecha
- Emitir firma al solicitar apertura

### T-019.2 Pantalla «Mi historia»

- Lista con tipo, fecha y origen
- Apertura en visor
- Nota de privacidad

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-016 Cargar documentos clínicos del paciente](HU-016-cargar-documentos-clinicos-del-paciente.md)
- [HU-036 Documentos servidos con URL firmada](../E11-seguridad-privacidad-y-cumplimiento/HU-036-documentos-servidos-con-url-firmada.md)

**Habilita** — no pueden construirse sin esta:

- Ninguna la tiene como requisito previo.


---

[← Volver a E4](README.md) · [Mapa de relaciones](../RELACIONES.md)
