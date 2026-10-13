# Base visual

**Fase del ciclo de vida:** Diseño
**Versión:** 1.4 · 13 de octubre de 2026

El dueño del proyecto aprobó el lienzo de pantallas como base del aspecto de Vitalia (decisión D-18). Este documento recoge lo que ese lienzo define, para que el desarrollo lo use sin copiar valores a ojo.

| | |
|---|---|
| **Lienzo** | https://claude.ai/artifact/R6WLHr5eAt7FQztseugqQY |
| **Copia en el repositorio** | [lienzo/](lienzo/): la fuente de las once pantallas. Solo se ven dibujadas en el artefacto |
| **Comportamiento** | Sigue mandando el [prototipo navegable](05-pantallas.md) |

El lienzo tiene once pantallas. Diez son las aprobadas. La undécima, la de **atención del médico**, se agregó el 13 de octubre con las mismas piezas, y ese mismo día la pantalla de ingreso pasó de pedir el correo a pedir el documento (D-20). Las dos están publicadas en el lienzo y **falta que el dueño del proyecto las vea**.

Ese mismo día el dueño del proyecto pidió tres correcciones para que el diseño no se vea genérico (D-25): los estados se muestran con un punto de color, las notas dejan la caja de color y los iconos salen de otra biblioteca. Después pidió que el punto de estado vaya dentro de una caja de bordes redondeados, con peso y sombra, y que botones y tarjetas lleven la misma sombra. Todo eso ya está en el lienzo; los iconos se aplican al construir. Ver las secciones 3, 4 y 6.

---

## 1. Colores

| Nombre | Variable | Valor | Dónde se usa |
|---|---|---|---|
| Fondo | `--fondo` | `#F1F4F9` | Fondo de la aplicación |
| Superficie | `--superficie` | `#FFFFFF` | Tarjetas, campos y barras |
| Tinta | `--tinta` | `#121C33` | Texto principal |
| Tinta suave | `--tinta-suave` | `#4C5973` | Texto secundario e iconos |
| Línea | `--linea` | `#D5DCE8` | Borde de tarjetas |
| Línea suave | `--linea-suave` | `#E7ECF4` | Separadores dentro de una tarjeta |
| Línea de campo | `--linea-campo` | `#7F8BA3` | Borde de los campos de un formulario |
| Acento | `--acento` | `#1F47B8` | Botón principal, enlaces y selección |
| Acento oscuro | `--acento-oscuro` | `#162F7A` | Texto sobre acento suave |
| Acento suave | `--acento-suave` | `#E3EAFB` | Fondo de iconos, pestaña activa, estado "confirmada" |
| Punto verde | `--punto-verde` | `#1F9D61` | Atendida, legible, vigente, autorizado, cuenta activa, borrador guardado |
| Punto rojo | `--punto-rojo` | `#D0392E` | Cancelada, no legible, alergia |
| Punto ámbar | `--punto-ambar` | `#D99A00` | Notas de aviso, festivo, no asistió, datos pendientes |
| Punto gris | `--punto-gris` | `#8A94A9` | Terminado, bloqueo, relacionado |
| Alerta | `--alerta` | `#A8211A` | Texto de las acciones que borran o cancelan |

**Contraste medido.** El texto pasa el nivel AA de WCAG (4,5 a 1): el secundario da 6,38 sobre el fondo y 7,04 sobre la superficie. Los estados ya no dependen del color: el nombre del estado va siempre escrito en la tinta principal, y el punto solo lo acompaña. Por eso el punto ámbar, que da 2,45 sobre blanco, no es un problema de lectura.

**Línea de campo.** Es el único color que no viene de las diez pantallas aprobadas. La línea `#D5DCE8` da un contraste de 1,38 sobre blanco, y para el borde de un campo WCAG pide 3 a 1; `#7F8BA3` da 3,43. Sirve para tarjetas, no para campos. La pantalla de atención ya la usa.

## 2. Tipografía

| Familia | Variable | Uso |
|---|---|---|
| Zilla Slab, pesos 600 y 700 | `--letra-titulo` | Títulos y cifras grandes, como la hora de la cita |
| Atkinson Hyperlegible Next, pesos 400, 600 y 700 | `--letra-texto` | Todo el texto. Es una letra diseñada para baja visión |
| Atkinson Hyperlegible Mono | `--letra-dato` | Horas, documentos y datos en columnas |

El lienzo usa 23 tamaños distintos. En el código se reducen a esta escala, que conserva el aspecto:

| Uso | Tamaño |
|---|---|
| Etiquetas y píldoras | 13 px |
| Texto secundario | 14,5 px |
| Texto | 15,5 px en el panel del médico; 16 px en las pantallas del paciente |
| Títulos de tarjeta | 20 px |
| Títulos de pantalla | 23 a 30 px |
| Cifra destacada | 30 a 34 px |

## 3. Formas

| Elemento | Valor |
|---|---|
| Radio de botones | 14 px |
| Radio de campos y botones pequeños | 10 a 12 px |
| Radio de tarjetas | 16 a 20 px |
| Píldoras de estado y avatares | Redondo completo |
| Alto de botones y campos | 52 a 54 px en los principales; 44 a 48 px en los secundarios |
| Sombra de caja, `--sombra-1` | `0 1px 2px rgba(18, 28, 51, 0.10), 0 2px 6px rgba(18, 28, 51, 0.06)`. Estados, notas y botones con borde |
| Sombra de tarjeta, `--sombra-2` | `0 1px 2px rgba(18, 28, 51, 0.06), 0 8px 24px rgba(18, 28, 51, 0.08)`. Tarjetas |
| Sombra de acento, `--sombra-acento` | `0 6px 16px rgba(31, 71, 184, 0.30)`. Botones principales y tarjetas azules |
| Lo que no lleva sombra | Los campos de formulario, los paneles hundidos de fondo gris y los botones que son solo texto |
| Iconos | Los del lienzo son provisionales. En la aplicación salen de Phosphor Icons: ver la sección 6 |

## 4. Piezas que ya existen en el lienzo

| Pieza | Dónde aparece |
|---|---|
| Tarjeta y tarjeta de acento | Próxima cita, mi tratamiento, documentos |
| Botón principal, botón con borde y enlace | Todas |
| Campo con icono, lista desplegable y área de texto | Ingresar y atención |
| Estado: una caja blanca de bordes redondeados (10 px) con sombra, que lleva un punto de color de 9 px y el nombre del estado en negrita | Citas, documentos, tratamientos y diagnósticos |
| Nota: una caja blanca redondeada con sombra, con un punto ámbar y el texto en tinta principal | Mis citas, calendario y atención |
| Barra inferior de cuatro pestañas | Paciente |
| Menú lateral | Médico |
| Hoja que sube desde abajo | Tratamiento de datos al registrarse |
| Selector de día y botones de hora | Agendar |
| Barra de pasos e índice de secciones | Agendar, crear cuenta y atención |
| Agenda del día con acciones por cita | Médico: hoy |
| Calendario de mes con convenciones | Médico: calendario |
| Resumen por secciones y conversación con el asistente | Médico: ficha y atención |
| Aviso en franja: tarjeta blanca con punto ámbar | Atención: datos pendientes |

## 5. Cómo se lleva a código

Estas son decisiones de diseño para la primera versión. Las que tocan lo aprobado quedan como supuestos y se corrigen si el dueño del proyecto lo pide.

| Tema | Decisión |
|---|---|
| Pantallas que no están dibujadas | No se dibujan antes. Se arman con las piezas de la sección 4, siguiendo el comportamiento del prototipo y el inventario de [05-pantallas.md](05-pantallas.md) (A-13) |
| Modo oscuro | La primera versión sale solo en claro (S-23). La paleta oscura del prototipo queda como punto de partida para después |
| Tamaño de letra | Se respetan los tamaños del lienzo aprobado, con la escala de la sección 2 (S-23). [05-pantallas.md](05-pantallas.md) pedía 16 puntos como mínimo; el texto base del paciente los cumple, el secundario no |
| Controles pequeños | En las pantallas del paciente ningún control baja de 44 px: el enlace "Ver cómo tomarlos" del inicio sube de 24 a 44. En el panel del médico, que se usa con ratón, se dejan como están en el lienzo |
| Borde de los campos | `--linea-campo` en todos los formularios, también en los que el lienzo dibujó con la línea clara |
| Variables | Los colores y las letras de este documento son las variables CSS de la aplicación. Ningún componente escribe un color a mano |

## 6. Para que no se vea genérico

Correcciones del dueño del proyecto del 13 de octubre (D-25). Valen para todas las pantallas, también las que falta armar.

| Regla | En vez de |
|---|---|
| El estado va en una caja blanca de bordes redondeados y con sombra: un punto de color y el nombre en negrita | Una píldora con fondo de color y un chulo |
| "Confirmada" es un aro azul; "sigue" es un punto azul lleno con el texto en azul | Dos píldoras azules casi iguales |
| Una nota es una caja blanca redondeada con sombra, con un punto ámbar y texto en tinta principal | Una caja amarilla con letra café y un icono de alerta |
| Las tarjetas y los botones llevan sombra suave además del borde redondeado; los botones principales, sombra azul | Piezas planas con solo una línea de borde |
| Las alergias van en una tarjeta neutra con un punto rojo | Una tarjeta amarilla con un triángulo |
| Las cuentas y las etiquetas sueltas ("pronto", "6 citas") son texto; sobre una tarjeta azul van en caja blanca | Una píldora |
| Los iconos salen de Phosphor Icons, en un solo grosor | Iconos de trazo fino dibujados a mano en cada pantalla |

**Por qué Phosphor Icons.** Tiene más de mil iconos en seis grosores, incluido uno de dos tonos que no se parece a los juegos de iconos más usados; su licencia es libre (MIT) y tiene paquete para React. Trae iconos médicos básicos; falta comprobar que estén todos los que usa Vitalia. El dueño del proyecto la confirmó el 13 de octubre (D-26). Se puede ver completa en https://phosphoricons.com.

Los iconos que hoy se ven en el lienzo no se redibujan: son provisionales y se reemplazan al construir.
