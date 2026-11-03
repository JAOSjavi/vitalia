# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Existente: React con Vite y TypeScript en `pantallas/`; servidor Python con FastAPI y PostgreSQL 18 con `pgvector` en `servidor/`.

## Users

- **Médico (o médica) del consultorio:** una sola persona, usuaria de todo el sistema. Trabaja desde el computador, entre consultas: ve la agenda del día, abre la atención, escribe la historia clínica con el asistente al lado y la firma.
- **Paciente adulto:** usa el celular (y también el computador). Agenda y mueve citas, sube sus historias clínicas anteriores, pregunta al asistente sobre ellas y ve sus atenciones cerradas. Se espera que muchos sean adultos mayores.

Solo adultos pueden tener cuenta.

## Product Purpose

Sistema a la medida para un consultorio médico general privado en Colombia. Reúne cuentas, horario y citas, panel del médico, historias clínicas que sube el paciente, un asistente de IA que busca en esos documentos, tratamientos y la historia clínica que el consultorio lleva de cada atención. Éxito: el médico atiende sin papel ni búsquedas manuales y el paciente gestiona su atención sin llamar.

## Positioning

No se vende a otros consultorios: está hecho para uno solo. El asistente responde únicamente con lo que hay en los documentos de un solo paciente y cada cita se comprueba contra lo enviado; ante preguntas de diagnóstico se abstiene.

## Operating Context

- Todo corre hoy en el computador del desarrollador con Docker; nada publicado. Despliegue previsto en Render (API, PostgreSQL) y Cloudflare R2 (archivos).
- Datos de salud regulados en Colombia (Resolución 1995 de 1999, protección de datos). La historia clínica cerrada no se modifica: se corrige con notas aclaratorias y se firma con la contraseña del médico.
- Todo se prueba con datos inventados hasta contar con abogado y médico revisor.

## Capabilities and Constraints

- Ingreso con tipo y número de documento más contraseña; bloqueo por intentos.
- Permisos por fila forzados en la base; el asistente nunca cruza pacientes.
- IA detrás de un adaptador intercambiable: Qwen para vectores, NVIDIA mientras Qwen no esté habilitado.
- Dos citas nunca ocupan el mismo tiempo.
- Pendientes: tratamientos, registro de paciente desde el panel, recuperar contraseña y correos, copia en PDF de la historia, visor de documentos.

## Brand Commitments

- Nombre: **Vitalia Salud**.
- Mundo visual elegido el 3 de noviembre de 2026 (D-34): muro de títulos, donde lo que sigue crece, con un acento verde azulado; reemplaza al lienzo y a `diseno/08-base-visual.md`. Cada pantalla conserva su estructura. Nada que se vea genérico ni hecho por IA.
- Tema claro y oscuro para paciente y médico, elegido en Ajustes.
- Iconos de Hugeicons en trazo redondeado.
- Voz: trato de usted, español de Colombia, cercano y claro, sin tecnicismos para el paciente.
- No hay logo ni marca del consultorio fuera de lo que está en el repositorio.

## Evidence on Hand

- 12 historias clínicas inventadas con preguntas de prueba en `documentos-de-prueba/historias-clinicas/`.
- Lienzo y prototipo en `diseno/lienzo/` y `diseno/prototipo/`.
- No hay testimonios, clientes ni métricas reales; no inventarlos.

## Product Principles

1. La información clínica manda: claridad y confianza antes que ornamento.
2. El paciente nunca ve nada que no sea suyo; el asistente nunca afirma lo que los documentos no dicen.
3. Lo firmado no se reescribe; los cambios dejan rastro.
4. Cada pantalla se adapta a su usuario: el médico en computador, el paciente en celular.
5. Solo lo útil: sin extras ni adornos de plantilla.

## Accessibility & Inclusion

Pensar en pacientes adultos mayores: letra grande, alto contraste, áreas táctiles amplias y lenguaje sencillo en el celular.
