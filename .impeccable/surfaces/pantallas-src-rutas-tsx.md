---
version: 1
slug: "pantallas-src-rutas-tsx"
primary_target: "pantallas/src/Rutas.tsx"
related_targets: ["pantallas/src/paciente","pantallas/src/medico","pantallas/src/comunes"]
---

# Vitalia · toda la app (paciente y médico)

Modo: Operate. Alcance: todas las pantallas de `pantallas/src`, un solo mundo para los dos usuarios. El paciente lo ve más grande en el celular y el médico más denso en el computador. La estructura de cada pantalla no cambia: contenido, orden y comportamiento se quedan como están.

Pedido del usuario (3 nov 2026): que no parezca hecho por Claude. Eligió en la página de decisión "Muro de streaming" con tema claro y oscuro, y un selector en una pestaña de Ajustes para los dos usuarios.

## Direction contract

THESIS: Vitalia como un muro de títulos. Lo que sigue (la próxima cita, el próximo paciente, el documento enfocado) crece y se presenta, y lo demás se queda quieto y más bajo. Se rechaza el panel médico gris azulado de tarjetas blancas con sombra suave.

OWN-WORLD: fondo neutro profundo en el tema oscuro (#0e1116, superficies #161a21 y #1d222b) y gris frío claro en el tema claro (#eef0f3 y blanco), sin crema. Un solo acento ámbar (#e8b04a sobre oscuro, #8a5a00 para texto sobre claro) que marca solo el foco, la selección y la acción principal. Títulos y cifras en Antonio, condensada y alta, en mayúsculas para los títulos de fila. Texto en Atkinson Hyperlegible Next y datos en Atkinson Hyperlegible Mono. Mosaicos de proporción fija con filete de 1 px, sin sombras de nube. El foco es un borde ámbar de 2 px.

STORY: el paciente abre y ve de inmediato su próxima cita como el título destacado: hora enorme, día y lugar. Luego ve sus filas (documentos e historia) y actúa en un toque. El médico ve a quién atiende ahora y el día en fila, sin buscar.

FIRST VIEWPORT: paciente en celular. Arriba, el saludo y el nombre en Antonio grande. La próxima cita es el mosaico enfocado, con borde ámbar, hora monumental, día y tipo, y Mover y Cancelar. Debajo va el botón principal ámbar de agendar, luego la fila de accesos con Mis documentos, y la barra de secciones abajo. Médico en computador: menú lateral con el activo enmarcado en ámbar. En Hoy, la tarjeta de quien sigue es el mosaico enfocado y la agenda del día va en fila debajo.

FORM: muro de streaming (pop-culture-shelf-streaming-title-card-wall), retadora adoptada por el usuario; la asignada era la caja de medicamento, candidata 4 de 7. seed:b7ceccb1892e3f0e

Signature move: al enfocar o pasar sobre un mosaico de una fila (cita, documento, paciente), ese crece con un marco ámbar de 2 px por fuera y los vecinos bajan su brillo. No se escala el texto que se lee. Los datos de cada fila ya están a la vista, porque la estructura no cambia (decisión del usuario). Con `prefers-reduced-motion` el marco y el atenuado se mantienen sin movimiento.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Decisiones abiertas

- El tema por defecto sigue al dispositivo; el usuario puede fijarlo en claro u oscuro desde Ajustes. Queda guardado en el navegador.
