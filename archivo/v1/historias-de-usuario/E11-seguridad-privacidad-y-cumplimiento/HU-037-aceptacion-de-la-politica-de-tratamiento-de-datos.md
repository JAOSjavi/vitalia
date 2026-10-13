# HU-037 — Aceptación de la política de tratamiento de datos

| Dato | Valor |
|---|---|
| Épica | E11 Seguridad, privacidad y cumplimiento |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-58 |
| Jira | SCRUM-100 |

## Historia

> Como paciente, quiero saber qué hacen con mis datos y dejar constancia de mi autorización, para estar informado y ejercer mis derechos.

## Criterios de aceptación

- **CA-1** · Dado que me registro, cuando acepto la política, entonces el sistema guarda la aceptación con fecha, hora y versión del documento.
- **CA-2** · Dado que la política cambia de versión, cuando ingreso después del cambio, entonces el sistema me solicita aceptarla nuevamente antes de continuar.
- **CA-3** · Dado que consulto mi perfil, cuando abro la sección de privacidad, entonces veo la versión aceptada, su fecha y el canal para ejercer mis derechos de habeas data.
- **CA-4** · Dado que no acepto la política, cuando intento usar la aplicación, entonces no puedo completar el registro.

## Tareas y actividades

### T-037.1 Versionado de la política

- Repositorio de versiones del documento
- Marca de versión vigente
- Detección de versión pendiente por usuario

### T-037.2 Registro de consentimiento

- Tabla consentimiento con tipo y versión
- Endpoint de registro
- Consulta desde el perfil

### T-037.3 Pantalla de privacidad del perfil

- Mostrar versión y fecha aceptadas
- Enlace al texto completo
- Canal de contacto para derechos

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-001 Registro de paciente](../E01-autenticacion-cuentas-y-roles/HU-001-registro-de-paciente.md)

**Habilita** — no pueden construirse sin esta:

- [HU-039 Registrar paciente nuevo desde WhatsApp](../E03-agendamiento-y-atencion-por-whatsapp/HU-039-registrar-paciente-nuevo-desde-whatsapp.md)
- [HU-059 Consentimiento del paciente para el uso de IA](../E08-asistente-de-ia-y-contenido-educativo/HU-059-consentimiento-del-paciente-para-el-uso-de-ia.md)
- [HU-067 Autorizar a un cuidador](HU-067-autorizar-a-un-cuidador.md)
- [HU-074 Consentimiento para compartir el resumen con otras instituciones](../E12-interoperabilidad-rda/HU-074-consentimiento-para-compartir-el-resumen-con-otras.md)


---

[← Volver a E11](README.md) · [Mapa de relaciones](../RELACIONES.md)
