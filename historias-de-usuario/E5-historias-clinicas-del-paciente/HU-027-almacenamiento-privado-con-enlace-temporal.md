# HU-027 — Almacenamiento privado con enlace temporal

| Dato | Valor |
|---|---|
| Épica | E5 Historias clínicas del paciente |
| Rol | Sistema |
| Prioridad | Must (MoSCoW) |
| Estimación | 5 puntos |
| Requisitos | RF-29 |
| Origen | HU-036 de la versión anterior, ajustada |

## Historia

> Como sistema, quiero guardar los documentos en un espacio privado y entregarlos con enlaces que vencen, para que un enlace filtrado no exponga la historia de nadie.

## Criterios de aceptación

- **CA-1** · Dado un documento guardado, cuando se intenta abrir por una dirección directa sin firma, entonces el acceso es rechazado.
- **CA-2** · Dado un usuario con permiso, cuando pide abrir un documento, entonces recibe un enlace que vence en máximo 15 minutos.
- **CA-3** · Dado un usuario sin permiso sobre ese documento, cuando pide el enlace, entonces el sistema se lo niega y registra el intento.
- **CA-4** · Dado un documento guardado, cuando se revisa el almacenamiento, entonces está cifrado y no existe ninguna ruta pública.

## Tareas y actividades

### T-027.1 Almacenamiento

- Espacio privado y cifrado
- Sin rutas públicas
- Nombres de archivo que no se puedan adivinar

### T-027.2 Servicio de enlaces firmados

- Validar el permiso antes de firmar
- Vigencia máxima de 15 minutos
- Registrar cada enlace emitido

### T-027.3 Pruebas

- Acceso directo sin firma
- Enlace vencido
- Usuario sin permiso

## Relación con otras historias

**Depende de:**

- [HU-006 Roles y permisos de médico y paciente](../E1-cuentas-e-ingreso/HU-006-roles-y-permisos.md)

**Habilita:**

- [HU-028 Subir mis historias clínicas](HU-028-subir-mis-historias-clinicas.md)

---

[← Volver a E5](README.md) · [Mapa de relaciones](../RELACIONES.md)
