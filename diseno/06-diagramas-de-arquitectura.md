# Diagramas de arquitectura

**Fase del ciclo de vida:** Diseño
**Versión:** 1.2 · 13 de octubre de 2026

Todos los diagramas están en código Mermaid: se ven dibujados en GitHub, en VS Code con la extensión de Mermaid o pegándolos en https://mermaid.live. Van de lo general a lo particular. La explicación de cada decisión está en [01-arquitectura.md](01-arquitectura.md).

---

## 1. Contexto: quién usa el sistema y con qué se conecta

```mermaid
flowchart LR
    PAC(["Paciente"])
    MED(["Médico"])
    V["Vitalia<br/>agenda, documentos, historia clínica,<br/>tratamientos y asistente"]
    IA["Proveedor de IA<br/>Qwen"]
    COR["Servicio de correo"]
    ALM["Almacenamiento<br/>de archivos"]

    PAC -- "agenda, sube documentos,<br/>consulta su tratamiento" --> V
    MED -- "atiende, escribe la historia clínica,<br/>pregunta al asistente" --> V
    V -- "texto de los documentos<br/>de un paciente" --> IA
    V -- "avisos y enlaces<br/>de un solo uso" --> COR
    V -- "archivos cifrados" --> ALM
```

## 2. Contenedores: las piezas que se despliegan

```mermaid
flowchart TB
    subgraph nav["Navegador del paciente o del médico"]
        SPA["Aplicación web<br/>React + TypeScript"]
    end

    subgraph render["Render"]
        EST["Sitio estático<br/>entrega la aplicación"]
        API["API<br/>Python + FastAPI"]
        LEC["Lector de documentos<br/>mismo servicio, en segundo plano"]
        BD[("PostgreSQL<br/>permisos por fila y bitácora")]
    end

    ALM[("Archivos privados<br/>compatible con S3")]
    IA["Proveedor de IA"]
    COR["Correo"]

    EST -. "se descarga una vez" .-> SPA
    SPA -- "HTTPS con cookie de sesión" --> API
    API --> BD
    API --> ALM
    API --> IA
    API --> COR
    LEC --> BD
    LEC --> ALM
    LEC --> IA
    SPA -. "enlace firmado de 15 minutos" .-> ALM
```

La aplicación web nunca llama al proveedor de IA ni al correo. A los archivos solo llega con el enlace temporal que la API le entrega.

## 3. Componentes de la API

La API se organiza con arquitectura limpia: las flechas continuas son dependencias y todas apuntan hacia el dominio.

```mermaid
flowchart TB
    subgraph entrada["Entrada: recibe la petición y la traduce"]
        R["Rutas de FastAPI<br/>cuentas, calendario, citas, pacientes,<br/>documentos, asistente, atenciones y bitácora"]
        L["Lector de documentos y envío de avisos<br/>en segundo plano"]
    end

    subgraph casos["Casos de uso: una operación cada uno"]
        C["Agendar una cita, mover una cita,<br/>subir un documento, preguntar al asistente,<br/>cerrar una atención, registrar un tratamiento…"]
        P["Puertos<br/>unidad de trabajo, repositorios, bitácora,<br/>archivos, proveedor de IA, correo y reloj"]
    end

    subgraph dominio["Dominio: reglas puras, sin tecnología"]
        D["Espacios libres, estados de la cita,<br/>anticipación, autorizaciones, vigencia del tratamiento,<br/>comprobación de orígenes, atención completa"]
    end

    subgraph adaptadores["Adaptadores: lo único que conoce a un tercero"]
        A1["PostgreSQL"]
        A2["Archivos"]
        A3["IA"]
        A4["Correo"]
    end

    R --> C
    L --> C
    C --> D
    C --> P
    A1 -. "cumple" .-> P
    A2 -. "cumple" .-> P
    A3 -. "cumple" .-> P
    A4 -. "cumple" .-> P
```

En cada petición, en este orden: la entrada encuentra la sesión; el caso de uso verifica el permiso del rol; la unidad de trabajo abre la transacción y le indica el usuario a la base; el dominio aplica la regla; se guarda y se escribe la bitácora en la misma transacción.

Cambiar de proveedor de IA, de almacenamiento o de correo toca un solo adaptador. El detalle de las capas está en la sección 7 de [01-arquitectura.md](01-arquitectura.md).

## 4. Despliegue

```mermaid
flowchart LR
    U(["Navegador"])

    subgraph render["Render · Estados Unidos"]
        EST["Sitio estático<br/>app.dominio"]
        WEB["Servicio web<br/>api.dominio"]
        PG[("PostgreSQL")]
    end

    R2[("Archivos<br/>Cloudflare R2")]
    QW["Qwen<br/>Singapur o Estados Unidos"]
    MAIL["Correo<br/>Resend"]

    U --> EST
    U --> WEB
    WEB --> PG
    WEB --> R2
    WEB --> QW
    WEB --> MAIL
```

| Variable de entorno del servicio web | Para qué |
|---|---|
| `BD_URL` | Conexión a PostgreSQL con el usuario sin privilegios de dueño |
| `ARCHIVOS_*` | Dirección, espacio y claves del almacenamiento |
| `IA_DIRECCION`, `IA_CLAVE`, `IA_MODELO_RESPUESTAS`, `IA_MODELO_LECTURA` | Proveedor de IA |
| `CORREO_CLAVE` | Servicio de correo |
| `SESION_SECRETO` | Firma de enlaces de un solo uso |

Ninguna de estas variables llega al navegador.

## 5. Secuencias

### 5.1 Ingreso y petición con sesión

```mermaid
sequenceDiagram
    participant N as Navegador
    participant A as API
    participant B as Base de datos

    N->>A: Ingresa con documento y contraseña
    A->>B: Función de búsqueda por documento
    B-->>A: Solo el hash, el rol y si está bloqueada
    A->>A: Compara la contraseña con el hash
    A->>B: Guarda la sesión, solo su hash
    A-->>N: Cookie segura

    N->>A: Pide sus citas, con la cookie
    A->>B: Valida la sesión y lee el rol
    A->>A: Verifica el permiso del rol
    A->>B: Abre transacción e indica usuario y rol
    B-->>A: Solo las filas que ese usuario puede ver
    A->>B: Registra en la bitácora
    A-->>N: Respuesta
```

### 5.2 Dos pacientes confirman el mismo espacio

```mermaid
sequenceDiagram
    participant P1 as Paciente A
    participant P2 as Paciente B
    participant A as API
    participant B as Base de datos

    P1->>A: Confirma las 10:00
    P2->>A: Confirma las 10:00
    A->>B: Inserta la cita de A
    B-->>A: Aceptada
    A->>B: Inserta la cita de B
    B-->>A: Rechazada por la restricción de choque
    A-->>P1: Cita confirmada
    A-->>P2: Espacio ocupado, con alternativas
```

La base de datos es la que impide el choque, no solo el código.

### 5.3 Subida y lectura de un documento

```mermaid
sequenceDiagram
    participant P as Paciente
    participant A as API
    participant S as Archivos
    participant B as Base de datos
    participant L as Lector
    participant I as Proveedor de IA

    P->>A: Sube el archivo
    A->>A: Valida formato y tamaño
    A->>S: Guarda cifrado
    A->>B: Registra el documento y encola la lectura
    A-->>P: Guardado, en proceso

    L->>B: Toma el siguiente trabajo
    L->>S: Descarga el archivo
    alt PDF con texto
        L->>L: Extrae el texto por página
    else Foto o escaneado, con IA autorizada
        L->>I: Envía la página como imagen
        I-->>L: Texto reconocido
    else Foto o escaneado, sin autorización
        L->>B: Deja el documento sin leer
    end
    L->>B: Guarda las páginas y el estado
```

### 5.4 Pregunta al asistente

```mermaid
sequenceDiagram
    participant M as Médico
    participant A as API
    participant B as Base de datos
    participant I as Proveedor de IA

    M->>A: Pregunta sobre el paciente X
    A->>B: Rol, autorización vigente y tope de consultas
    alt Algo falla
        A-->>M: No se puede, con la razón
    else Todo en orden
        A->>B: Texto de los documentos legibles de X
        A->>A: Retira identificadores y arma el contexto
        A->>I: Instrucciones, documentos de X y pregunta
        I-->>A: Respuesta por partes con orígenes
        A->>A: Comprueba cada origen contra el texto guardado
        A->>B: Bitácora: quién, sobre quién y cuándo
        A-->>M: Respuesta con documento y página
    end
```

### 5.5 El médico registra un tratamiento

```mermaid
sequenceDiagram
    participant M as Médico
    participant A as API
    participant B as Base de datos
    participant P as Paciente

    M->>A: Guarda motivo, medicamentos e indicaciones
    A->>A: Valida que no falte nada
    A->>B: Inserta el tratamiento y sus medicamentos
    A->>B: Registra en la bitácora
    A-->>M: Guardado
    P->>A: Abre Mis tratamientos
    A->>B: Lee los tratamientos del paciente
    A-->>P: Último tratamiento, con fecha de fin calculada
```

### 5.6 Atención y cierre de la historia clínica

```mermaid
sequenceDiagram
    participant M as Médico
    participant A as API
    participant B as Base de datos

    M->>A: Atender, desde la cita o desde la ficha
    A->>B: ¿Hay una atención abierta de este paciente?
    alt Ya hay una
        B-->>A: La atención abierta
    else No hay
        A->>B: Crea la atención con los antecedentes de la última cerrada
    end
    A-->>M: Formulario y, a un lado, el resumen del asistente

    loop Mientras escribe
        M->>A: Guarda la sección que cambió
        A->>B: Actualiza el borrador
    end

    M->>A: Cerrar, con su contraseña
    A->>B: Verifica la contraseña
    A->>A: Revisa qué le falta a la atención
    alt Falta algo
        A-->>M: No se cierra, con la lista de lo que falta
    else Está completa
        A->>B: Cierra con nombre, registro, fecha y hora
        A->>B: Marca la cita como atendida y guarda la fórmula como tratamiento
        A->>B: Registra en la bitácora
        A-->>M: Atención cerrada
    end
```

Desde ese momento la base rechaza cualquier cambio. Una corrección es una nota aclaratoria que se suma.

## 6. Estados

### 6.1 Cita

```mermaid
stateDiagram-v2
    state "No asistió" as NoAsistio

    [*] --> Confirmada: se agenda
    Confirmada --> Confirmada: se mueve
    Confirmada --> Cancelada: paciente o médico cancela
    Confirmada --> Atendida: el médico la marca
    Confirmada --> NoAsistio: el médico la marca
    Atendida --> Confirmada: corrección el mismo día
    NoAsistio --> Confirmada: corrección el mismo día
    Cancelada --> [*]
    Atendida --> [*]
    NoAsistio --> [*]
```

### 6.2 Lectura de un documento

```mermaid
stateDiagram-v2
    state "Sin leer" as SinLeer
    state "En proceso" as EnProceso
    state "No legible" as NoLegible

    [*] --> EnProceso: PDF con texto, o foto con IA autorizada
    [*] --> SinLeer: foto sin IA autorizada
    SinLeer --> EnProceso: el paciente autoriza la IA
    EnProceso --> Legible: texto suficiente
    EnProceso --> NoLegible: texto insuficiente
    Legible --> [*]: el paciente lo elimina
    NoLegible --> [*]: el paciente lo elimina
```

### 6.3 Autorización de IA del paciente

```mermaid
stateDiagram-v2
    state "Sin responder" as SinResponder

    [*] --> SinResponder: cuenta creada sin marcar la casilla
    [*] --> Aceptada: marcó la casilla al registrarse
    SinResponder --> Aceptada: autoriza desde su perfil
    SinResponder --> Rechazada: no autoriza
    Rechazada --> Aceptada: cambia de opinión
    Aceptada --> Retirada: la retira
    Retirada --> Aceptada: vuelve a autorizar
```

El asistente solo funciona en el estado **Aceptada**.

### 6.4 Atención de la historia clínica

```mermaid
stateDiagram-v2
    [*] --> Abierta: el médico elige atender
    Abierta --> Abierta: guarda el borrador
    Abierta --> Cerrada: cierra con su contraseña y todo completo
    Cerrada --> Cerrada: nota aclaratoria
    Cerrada --> [*]
```

Una atención cerrada no vuelve a abrirse ni se borra. Un paciente tiene como mucho una atención abierta.

## 7. Datos

El diagrama de tablas y sus relaciones está en [02-modelo-de-datos.md](02-modelo-de-datos.md).
