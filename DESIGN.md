---
name: Vitalia Salud
description: Muro de títulos para un consultorio médico general; lo que sigue crece y se enmarca en ámbar.
colors:
  fondo: "#eceef2"
  superficie: "#ffffff"
  superficie-2: "#f5f6f8"
  tinta: "#11141a"
  tinta-suave: "#4a5160"
  linea: "#d3d7df"
  linea-suave: "#e6e8ed"
  linea-campo: "#7a8293"
  acento: "#e6a73c"
  acento-fuerte: "#d4942a"
  acento-texto: "#8a5a00"
  acento-oscuro: "#6b4500"
  acento-suave: "#fbefd8"
  sobre-acento: "#17120a"
  resalte: "#fff7e6"
  foco: "#8a5a00"
  velo: "rgba(10, 12, 16, 0.55)"
  punto-verde: "#1a8c55"
  punto-rojo: "#cc3a2e"
  punto-ambar: "#c98a00"
  punto-gris: "#7d8698"
  rojo-suave: "#fbeeed"
  verde-fuerte: "#0f6b43"
  alerta: "#a8211a"
typography:
  display:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "64px"
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: "-0.01em"
    fontFeature: "tnum"
  headline:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "34px"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "0.02em"
  title:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "24px"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "0.02em"
  body:
    fontFamily: "Atkinson Hyperlegible Next, Atkinson Hyperlegible, Verdana, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: "24px"
  body-medico:
    fontFamily: "Atkinson Hyperlegible Next, Atkinson Hyperlegible, Verdana, sans-serif"
    fontSize: "15.5px"
    fontWeight: 400
    lineHeight: "22px"
  secondary:
    fontFamily: "Atkinson Hyperlegible Next, Atkinson Hyperlegible, Verdana, sans-serif"
    fontSize: "14.5px"
    fontWeight: 400
    lineHeight: "20px"
  label:
    fontFamily: "Atkinson Hyperlegible Next, Atkinson Hyperlegible, Verdana, sans-serif"
    fontSize: "13px"
    fontWeight: 700
    lineHeight: "18px"
    letterSpacing: "0.05em"
  data:
    fontFamily: "Atkinson Hyperlegible Mono, ui-monospace, Consolas, monospace"
    fontSize: "15px"
    fontWeight: 400
    fontFeature: "tnum"
rounded:
  estado: "6px"
  campo: "8px"
  boton: "8px"
  tarjeta: "10px"
  hoja: "26px"
  completo: "999px"
spacing:
  xxs: "4px"
  xs: "8px"
  sm: "12px"
  md: "16px"
  lg: "20px"
  xl: "24px"
  xxl: "28px"
  xxxl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.acento}"
    textColor: "{colors.sobre-acento}"
    typography: "{typography.body}"
    rounded: "{rounded.boton}"
    padding: "0 20px"
    height: "54px"
  button-primary-hover:
    backgroundColor: "{colors.acento-fuerte}"
    textColor: "{colors.sobre-acento}"
  button-borde:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.boton}"
    padding: "0 20px"
    height: "52px"
  button-neutro:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.boton}"
    padding: "0 20px"
    height: "52px"
  button-borde-hover:
    backgroundColor: "{colors.acento-suave}"
    textColor: "{colors.tinta}"
  input:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.tinta}"
    typography: "{typography.body}"
    rounded: "{rounded.campo}"
    padding: "0 14px"
    height: "52px"
  estado:
    backgroundColor: "{colors.superficie-2}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    rounded: "{rounded.estado}"
    padding: "4px 10px 4px 8px"
  tarjeta:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.tarjeta}"
  mosaico-enfocado:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.tarjeta}"
    padding: "18px 18px 16px"
  nav-enlace:
    textColor: "{colors.tinta-suave}"
    rounded: "{rounded.campo}"
    padding: "0 12px"
    height: "44px"
  nav-enlace-activo:
    backgroundColor: "{colors.acento-suave}"
    textColor: "{colors.acento-oscuro}"
  hoja:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.hoja}"
    padding: "12px 20px 24px"
---

# Design System: Vitalia Salud

## Overview

**Creative North Star: "El muro de títulos"**

Vitalia se lee como el muro de una plataforma de streaming: una fila de mosaicos quietos y, entre ellos, uno solo que se presenta. Para el paciente es su próxima cita, con la hora enorme. Para el médico es quien sigue en la agenda. Todo lo demás se queda bajo, en filas de mosaicos de esquina corta separados por un filete de 1 px. El ámbar es la única luz del sistema: marca lo enfocado, lo elegido y la acción principal.

Hay un solo mundo para los dos usuarios, con dos densidades. El paciente lo ve en el celular, en una columna de 440 px, con letra grande y áreas táctiles de 52 a 72 px. El médico lo ve en el computador, con menú lateral y texto de 15.5 px. El tema claro es gris frío sin crema y el oscuro es neutro profundo. Los dos comparten cada rol de color, y el tema se elige en Ajustes o sigue al dispositivo.

Se rechaza el panel médico gris azulado de tarjetas blancas con sombra suave. Tampoco se usan píldoras con chulo, cajas amarillas de aviso ni iconos de relleno genérico: un estado es un punto de color más texto.

**Key Characteristics:**
- Un mosaico enfocado por pantalla, con borde ámbar de 2 px y cifras monumentales en Antonio.
- Títulos de pantalla y de mosaico en mayúsculas condensadas; el texto corrido nunca.
- Módulos planos con filete de 1 px; la sombra queda solo para lo que flota.
- Movimiento sobrio: los botones se hunden y no se elevan, y en una fila los vecinos del mosaico señalado bajan su brillo.
- Tema claro y oscuro con los mismos nombres de rol; ningún componente escribe un color a mano.

## Colors

Neutros fríos sin tinte cálido, más un único ámbar que se reparte en cinco escalones según dónde va: relleno, texto, presión, fondo tenue y tinta encima.

### Primary
- **Ámbar de marquesina** (acento): relleno del botón principal, borde del mosaico enfocado, marco del mosaico señalado en una fila, día y hora elegidos en el selector de turnos, barra de pasos hecha, sello de la marca y color de selección de texto.
- **Ámbar encendido** (acento-fuerte): hover del botón principal, anillo interior del hover principal y avatar del médico.
- **Ámbar de lectura** (acento-texto): enlaces, iconos de acento y el anillo de foco en el tema claro, donde el ámbar de relleno no alcanza contraste como texto.
- **Ámbar profundo** (acento-oscuro): texto sobre fondo ámbar tenue (enlace activo del menú, etiqueta "Mañana") y hover de enlaces.
- **Ámbar tenue** (acento-suave): fondo del enlace activo, de los pozos de icono y del hover de opciones elegibles, y halo del campo enfocado.
- **Tinta sobre ámbar** (sobre-acento): texto e iconos encima de cualquier relleno ámbar.

### Neutral
- **Gris de muro** (fondo): fondo de la página y hover de enlaces de menú.
- **Blanco de mosaico** (superficie): mosaicos, campos, botones de borde, menú lateral y barra de secciones.
- **Gris de reposo** (superficie-2): fondo del estado y de los pozos de icono sin elegir.
- **Tinta** (tinta): todo el texto principal y el borde del botón de borde.
- **Tinta suave** (tinta-suave): texto secundario, rótulos de grupo e iconos en reposo.
- **Filete** (linea): borde de 1 px de mosaicos y listas, divisores internos y pasos pendientes.
- **Filete suave** (linea-suave): divisores dentro del menú.
- **Borde de campo** (linea-campo): borde de 1.5 px de campos y botones neutros, que es el borde visible de lo que se escribe o se toca.
- **Resalte** (resalte): fondo de la fila de quien sigue y hover del acceso a documentos.
- **Velo** (velo): fondo detrás de las hojas.

### Estado
- **Puntos** (punto-verde, punto-rojo, punto-ambar, punto-gris): el punto de 8 a 9 px que acompaña cada estado, nota o error. Siempre van con texto.
- **Rojo tenue y alerta** (rojo-suave, alerta): fondo y texto de acciones destructivas y avisos graves.
- **Verde fuerte** (verde-fuerte): confirmaciones de lo atendido.

El tema oscuro redefine cada rol con el mismo nombre (fondo #0d1015, superficie #161a21, acento #e8b04a, acento-texto #f0c063). Los valores están en el sidecar. El que se elige con `data-tema="oscuro"` y el del dispositivo son idénticos.

### Named Rules
**The Una Sola Luz Rule.** El ámbar lleno marca solo tres cosas: el foco, la selección y la acción principal. El ámbar tenue puede servir de fondo a iconos y hovers, pero nunca hay dos ámbares llenos compitiendo en un mismo mosaico.

**The Rol, No Valor Rule.** Todo color sale de `variables.css` por su nombre de rol. Un color escrito a mano en una pantalla rompe el tema oscuro.

**The Punto Y Texto Rule.** Un estado es un punto de color más su palabra, sobre fondo gris de reposo y esquina de 6 px. No lleva píldora redonda con chulo ni caja de color.

## Typography

**Display Font:** Antonio (con Arial Narrow)
**Body Font:** Atkinson Hyperlegible Next (con Atkinson Hyperlegible, Verdana)
**Label/Mono Font:** Atkinson Hyperlegible Mono (con ui-monospace, Consolas)

**Character:** Antonio, condensada y alta, hace de cartel. Atkinson, diseñada para baja visión, hace el trabajo de leer. Las dos están separadas con disciplina, porque el muro tiene que ser legible para adultos mayores.

### Hierarchy
- **Display** (700, 56–64 px, 0.95–1): la hora monumental de la próxima cita (64 px) y el título "Agenda de hoy" del médico (56 px). Con cifras tabulares.
- **Headline** (700, 34 px, 1.05, mayúsculas, 0.02em): título de cada pantalla y nombre de quien sigue. El nombre del paciente en el saludo sube a 44 px.
- **Title** (600, 23–24 px, 1.1, mayúsculas, 0.02em): título de mosaico y de hoja ("Su próxima cita", "Sigue · 4:47 p. m.", grupos de Ajustes).
- **Body** (400, 16 px / 24 px): texto del paciente. En la zona del médico baja a 15.5 px.
- **Secondary** (400, 14.5 px / 20 px): ayudas de campo, detalle de filas y subtítulos.
- **Label** (700, 13 px / 18 px, 0.05em, mayúsculas): rótulos de grupo y de columna, como los días del calendario, "Mañana y tarde", la cantidad de documentos y las secciones de una atención. Lo que rotulan es una lista o una columna, no un título.
- **Data** (Mono 400, 15–15.5 px, tabular): horas en la agenda del médico y números de documento en los campos.

### Named Rules
**The Cartel Rule.** Antonio solo va en títulos y cifras. El texto que se lee de corrido, los botones y los campos van siempre en Atkinson.

**The Cifra Tabular Rule.** Toda hora y todo número que se compara (`time`, `.cifras`) usa cifras tabulares, para que las filas de la agenda alineen.

## Layout

El paciente trabaja en una columna de 440 px como máximo, con margen lateral de 20 a 24 px y separación vertical de 16 a 28 px. La barra de secciones va fija abajo. Desde 900 px se convierte en un menú lateral de 240 px y el contenido se abre hasta 1040 px.

El médico trabaja con un menú lateral fijo de 240 px y contenido a todo el ancho, con 28 a 32 px de margen. Las pantallas de formulario se quedan en 920 px. En Hoy, la lista del día ocupa el ancho flexible y el mosaico de quien sigue va en una columna lateral. Por debajo de 820 px el menú pasa arriba en fila.

El ritmo usa pasos de 4 px: 4, 8, 10, 12, 16, 20, 24 y 28. Lo que se toca mide al menos 44 px de alto, los botones y campos 52 a 54 px, y las opciones de Ajustes y los accesos 72 px. Cada pantalla conserva la estructura del lienzo: el mundo cambia la piel, no el orden.

## Elevation & Depth

El sistema es plano. Los mosaicos y las listas se separan del fondo por el cambio de superficie y por su filete de 1 px. Lo enfocado se distingue por un borde ámbar, no por altura. Las sombras de módulo (`--sombra-1`, `--sombra-2`, `--sombra-acento`) existen como tokens pero valen `none`, y se mantienen así.

### Shadow Vocabulary
- **Flotante** (`box-shadow: 0 2px 4px rgba(12,14,18,.08), 0 12px 32px rgba(12,14,18,.14)`; en oscuro con opacidad .5): menús desplegables, como el menú del avatar.
- **Halo de campo** (`box-shadow: 0 0 0 3px var(--acento-suave)`): campo o buscador con foco.
- **Borde de hover** (`box-shadow: inset 0 0 0 1px var(--linea-campo)`): botones de superficie y mosaicos que se tocan.
- **Borde de hover principal** (`box-shadow: inset 0 0 0 2px var(--acento-fuerte)`): botón principal al pasar el cursor.
- **Marco de activo** (`box-shadow: inset 0 0 0 1.5px var(--acento)`): enlace activo del menú y opción elegida en Ajustes (con 1 px).

### Named Rules
**The Solo Flota Lo Que Flota Rule.** La sombra difusa es para menús y hojas que se superponen al contenido. Un mosaico en su sitio no la lleva.

**The Hundirse, No Elevarse Rule.** Al presionar, un botón se escala a 0.97 en 90 ms. Nada sube con `translateY` ni gana sombra al pasar el cursor.

## Shapes

Las esquinas son cortas, como mosaicos de un muro: 6 px para estados, 8 px para campos, botones y pozos de icono, y 10 px para mosaicos y listas. La única forma redonda completa es la del avatar y los puntos de estado. La hoja inferior es la excepción blanda (26 px arriba en celular y 22 px como ventana en computador), porque es una superficie que sube desde el borde.

Los bordes tienen tres grosores con significado: 1 px es filete de módulo, 1.5 px es borde de campo o de botón que se toca, y 2 px es lo enfocado o el foco de teclado.

## Components

### Buttons
Firmes y grandes; llenan el ancho cuando son la acción de la pantalla.
- **Shape:** esquina corta (8 px), alto mínimo de 52 px (54 px el principal), texto Atkinson 700 de 16 a 17 px con icono a 10 px.
- **Primary:** relleno ámbar de marquesina con tinta sobre ámbar y sin borde. Es la única acción principal de la vista ("Agendar otra cita", "Abrir la ficha", "Nueva cita").
- **Hover / Focus:** al pasar el cursor pasa a ámbar encendido con un anillo interior de 2 px. El foco es un contorno de 2 px en color de foco con 2 px de separación. Al presionar se hunde (0.97).
- **Borde:** superficie con borde de 1.5 px en tinta. Al pasar el cursor toma fondo ámbar tenue.
- **Neutro:** superficie con borde de 1.5 px en borde de campo. Al pasar el cursor el borde se marca y el fondo pasa a ámbar tenue.
- **Enlace:** texto ámbar de lectura en 700 y 15 px, sin subrayado, con 44 px de área.

### Chips (estado)
- **Style:** fondo gris de reposo, esquina de 6 px, punto de 9 px y palabra en 13 px 700. La variante de acento usa texto ámbar de lectura y punto ámbar o en aro.
- **State:** no se tocan; solo informan.

### Cards / Containers
- **Corner Style:** 10 px.
- **Background:** blanco de mosaico sobre gris de muro.
- **Shadow Strategy:** ninguna (ver Elevation & Depth).
- **Border:** filete de 1 px.
- **Internal Padding:** 14–20 px. Las filas internas van a 14 px × 20 px y se separan por filete.

### Inputs / Fields
- **Style:** 52 px de alto, borde de 1.5 px en borde de campo, esquina de 8 px y fondo de superficie. Etiqueta en 14.5 px 700 arriba y ayuda en tinta suave debajo. Los números de documento van en Mono.
- **Focus:** borde ámbar más halo ámbar tenue de 3 px.
- **Error / Disabled:** borde en punto rojo y mensaje con punto rojo de 8 px más texto. El botón deshabilitado baja a 0.7 de opacidad con cursor de espera.

### Navigation
- **Paciente, celular:** barra fija abajo sobre superficie, con filete superior y cinco secciones de icono más palabra de 12.5 px. La activa pinta su icono sobre un pozo ámbar tenue y su texto en ámbar de lectura.
- **Paciente desde 900 px y médico:** menú lateral de 240 px con la marca arriba y enlaces de 44 a 48 px con esquina de 8 px. El activo lleva fondo ámbar tenue, marco interior ámbar de 1.5 px y texto ámbar profundo en 700. Lo que aún no existe se marca "Pronto" y no navega.

### Mosaico enfocado (signature)
La próxima cita del paciente y quien sigue para el médico. Es un mosaico con borde ámbar de 2 px, título de mosaico en mayúsculas con icono ámbar, etiqueta de cuándo sobre ámbar tenue y la cifra en Display. Debajo, los datos separados por un filete y las acciones. Al aparecer "enciende" su borde una sola vez: un halo ámbar tenue de 6 px se abre y se cierra en 700 ms. Con movimiento reducido aparece ya encendido. Hay uno por pantalla.

### Fila de mosaicos (signature)
En las listas de citas, pacientes, documentos, atenciones y en la agenda, la fila señalada con cursor o foco toma un contorno ámbar de 2 px que se cierra desde adentro (offset de −6 a −2 px, 220 ms), y sus vecinos bajan a 0.62 de opacidad. El texto no se escala. Solo ocurre con cursor (`hover: hover`). Con movimiento reducido el contorno y el atenuado se mantienen, sin transición de posición.

### Selector de tema (Ajustes)
Tres opciones (Sistema, Claro, Oscuro) como mosaicos enteros de 72 px que se tocan, con pozo de icono, nombre y explicación. La elegida se enmarca en ámbar y su pozo pasa a ámbar tenue. El cambio de tema se funde con una transición de vista de 320 ms, salvo con movimiento reducido.

## Do's and Don'ts

### Do:
- **Do** tomar todo color de su rol en `variables.css` y comprobar la pantalla en los dos temas.
- **Do** dejar un solo mosaico enfocado por pantalla, con borde ámbar de 2 px, y la cifra que importa en Antonio Display.
- **Do** separar módulos con filete de 1 px y esquina de 10 px; campos y botones con 8 px.
- **Do** poner los títulos de pantalla y de mosaico en Antonio mayúscula con 0.02em de espaciado, y todo lo demás en Atkinson.
- **Do** mostrar cada estado como punto de color más palabra.
- **Do** usar iconos de Hugeicons en trazo redondeado a través de `comunes/iconos.tsx`, a 18–20 px.
- **Do** usar `cubic-bezier(0.16, 1, 0.3, 1)` a 160 ms para color y borde, y a 220 ms para opacidad y contorno.
- **Do** mantener 44 px como área táctil mínima y 52 px para botones y campos del paciente.

### Don't:
- **Don't** poner sombras difusas en mosaicos, listas o botones: la sombra es solo para menús y hojas.
- **Don't** usar fondos crema ni el gris azulado de panel médico con tarjetas blancas sombreadas.
- **Don't** usar el ámbar lleno para decorar: no va en titulares, fondos de sección ni más de una acción principal.
- **Don't** escalar el texto de un mosaico al señalarlo ni elevar botones con `translateY`.
- **Don't** poner un rótulo pequeño en mayúsculas encima de un título como antetítulo: el rótulo de 13 px nombra listas y columnas, no anuncia titulares.
- **Don't** usar píldoras con chulo, cajas amarillas de aviso ni iconos de otra biblioteca.
- **Don't** escribir texto corrido, botones o campos en Antonio.
