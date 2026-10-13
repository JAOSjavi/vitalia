# HU-032 — Configurar canal preferido de aviso

| Dato | Valor |
|---|---|
| Épica | E6 Recordatorios multicanal y adherencia |
| Fase | 1 |
| Rol | Paciente |
| Prioridad | Must (MoSCoW) |
| Estimación | 3 puntos |
| Requisitos | RF-35 |
| Jira | SCRUM-95 |

## Historia

> Como paciente, quiero elegir por dónde me avisan, para recibir los recordatorios donde realmente los veo.

## Criterios de aceptación

- **CA-1** · Dado que abro la configuración de avisos, cuando selecciono WhatsApp, SMS, notificación o una combinación, entonces el sistema guarda la preferencia y la aplica a los siguientes envíos.
- **CA-2** · Dado que no configuro nada, cuando se envía un recordatorio, entonces el sistema usa WhatsApp como canal por defecto.
- **CA-3** · Dado que desactivo todos los canales, cuando intento guardar, entonces el sistema advierte que dejará de recibir recordatorios y exige confirmación explícita.
- **CA-4** · Dado que cambio mi preferencia, cuando se guarda, entonces los recordatorios ya programados adoptan el nuevo canal.

## Tareas y actividades

### T-032.1 Modelo de preferencias

- Tabla preferencia_notificacion por paciente
- Valor por defecto al crear la cuenta
- Aplicación a recordatorios pendientes

### T-032.2 Pantalla de preferencias

- Selección múltiple de canales
- Advertencia al desactivar todo
- Confirmación del cambio

## Relación con otras historias

**Depende de** — no puede construirse antes que:

- [HU-001 Registro de paciente](../E01-autenticacion-cuentas-y-roles/HU-001-registro-de-paciente.md)

**Habilita** — no pueden construirse sin esta:

- [HU-033 Envío por WhatsApp con plantillas aprobadas](HU-033-envio-por-whatsapp-con-plantillas-aprobadas.md)
- [HU-034 Envío por SMS](HU-034-envio-por-sms.md)
- [HU-054 Notificación de respuesta del médico](../E07-comunicacion-paciente-medico-entre-consultas/HU-054-notificacion-de-respuesta-del-medico.md)


---

[← Volver a E6](README.md) · [Mapa de relaciones](../RELACIONES.md)
