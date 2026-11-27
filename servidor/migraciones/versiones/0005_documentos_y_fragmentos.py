"""Documentos, páginas leídas, cola del lector y fragmentos del asistente (HU-027 a HU-033, D-30).

Un documento se lee página por página. Cada página se parte en fragmentos, y cada fragmento
guarda su texto, su vector (lo que significa) y su léxico (las palabras), para que el
asistente busque de las dos formas, siempre dentro de un solo paciente.

Las atenciones del consultorio también tendrán fragmentos, pero su tabla llega con la épica E9:
por ahora atencion_id no tiene llave foránea.
"""

from alembic import op

revision: str = "0005"
down_revision: str | None = "0004"

_INTERNA = "session_user <> current_user"
_TABLAS = ("documentos", "paginas_documento", "trabajos_lectura", "fragmentos")

# Tiene que coincidir con IA_DIMENSIONES: el modelo entrega vectores de este tamaño.
_DIMENSIONES = 1024


def _forzar(tabla: str) -> None:
    op.execute(f"ALTER TABLE {tabla} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY interna ON {tabla} TO CURRENT_USER "
        f"USING ({_INTERNA}) WITH CHECK ({_INTERNA})"
    )


def upgrade() -> None:
    # pgvector: el tipo vector y la distancia entre vectores (<=>). Solo la instala un
    # superusuario: en Docker y en las pruebas ya viene en template1, y aquí no hace nada.
    # Donde no esté y el usuario no pueda instalarla, la migración se detiene en esta línea.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Búsqueda por palabras en español sin tildes: "diabetes", "diabético" y "DIABÉTICA"
    # quedan como la misma raíz. Es la configuración de español con unaccent delante.
    op.execute("CREATE TEXT SEARCH CONFIGURATION vitalia_es (COPY = spanish)")
    op.execute(
        "ALTER TEXT SEARCH CONFIGURATION vitalia_es "
        "ALTER MAPPING FOR hword, hword_part, word WITH unaccent, spanish_stem"
    )

    op.execute(
        """
        CREATE TABLE documentos (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            paciente_id uuid NOT NULL REFERENCES pacientes,
            nombre text NOT NULL CHECK (length(nombre) BETWEEN 1 AND 120),
            fecha_documento date NOT NULL,
            tipo text NOT NULL
                CHECK (tipo IN ('historia_clinica', 'examen', 'formula', 'imagen', 'otro')),
            formato text NOT NULL CHECK (formato IN ('pdf', 'jpg', 'png')),
            tamano integer NOT NULL CHECK (tamano BETWEEN 1 AND 20 * 1024 * 1024),
            huella text NOT NULL,
            clave_archivo text NOT NULL UNIQUE,
            estado_lectura text NOT NULL DEFAULT 'sin_leer'
                CHECK (estado_lectura IN ('sin_leer', 'en_proceso', 'legible', 'no_legible')),
            paginas integer CHECK (paginas > 0),
            subido_en timestamptz NOT NULL DEFAULT now(),
            -- El mismo archivo dos veces se detecta (HU-027).
            UNIQUE (paciente_id, huella),
            -- Para que un fragmento no pueda quedar con otro paciente que el de su documento.
            UNIQUE (id, paciente_id)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE paginas_documento (
            documento_id uuid NOT NULL REFERENCES documentos ON DELETE CASCADE,
            numero integer NOT NULL CHECK (numero > 0),
            texto text NOT NULL,
            origen text NOT NULL CHECK (origen IN ('pdf', 'reconocido')),
            legibilidad real CHECK (legibilidad BETWEEN 0 AND 1),
            PRIMARY KEY (documento_id, numero)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE trabajos_lectura (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            tipo text NOT NULL CHECK (tipo IN ('leer', 'indexar_documento', 'indexar_atencion')),
            documento_id uuid REFERENCES documentos ON DELETE CASCADE,
            atencion_id uuid,
            estado text NOT NULL DEFAULT 'pendiente'
                CHECK (estado IN ('pendiente', 'en_curso', 'hecho', 'fallido')),
            intentos integer NOT NULL DEFAULT 0 CHECK (intentos >= 0),
            error text,
            creado_en timestamptz NOT NULL DEFAULT now(),
            CHECK (
                CASE tipo
                    WHEN 'indexar_atencion' THEN atencion_id IS NOT NULL AND documento_id IS NULL
                    ELSE documento_id IS NOT NULL AND atencion_id IS NULL
                END
            )
        )
        """
    )
    op.execute("CREATE INDEX trabajos_por_estado ON trabajos_lectura (estado, creado_en)")
    op.execute("CREATE INDEX trabajos_por_documento ON trabajos_lectura (documento_id)")

    # Lo que busca el asistente. Un fragmento sale de una sola página de un documento o de una
    # sección de una atención, nunca de las dos. lexico lo calcula la base a partir del texto.
    op.execute(
        f"""
        CREATE TABLE fragmentos (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            paciente_id uuid NOT NULL REFERENCES pacientes,
            documento_id uuid,
            pagina integer,
            atencion_id uuid,
            seccion text,
            orden integer NOT NULL CHECK (orden >= 0),
            texto text NOT NULL CHECK (texto <> ''),
            vector vector({_DIMENSIONES}) NOT NULL,
            lexico tsvector GENERATED ALWAYS AS (to_tsvector('vitalia_es', texto)) STORED,
            modelo text NOT NULL,
            creado_en timestamptz NOT NULL DEFAULT now(),
            CHECK (
                (documento_id IS NOT NULL AND pagina IS NOT NULL
                    AND atencion_id IS NULL AND seccion IS NULL)
                OR (documento_id IS NULL AND pagina IS NULL
                    AND atencion_id IS NOT NULL AND seccion IS NOT NULL)
            ),
            FOREIGN KEY (documento_id, paciente_id)
                REFERENCES documentos (id, paciente_id) ON DELETE CASCADE,
            FOREIGN KEY (documento_id, pagina)
                REFERENCES paginas_documento (documento_id, numero) ON DELETE CASCADE
        )
        """
    )
    # Sin índice aproximado de vectores: se comparan todos los fragmentos de un paciente,
    # que son cientos. Se agrega solo si una medición lo pide (D-19).
    op.execute("CREATE INDEX fragmentos_por_paciente ON fragmentos (paciente_id)")
    op.execute("CREATE INDEX fragmentos_por_palabras ON fragmentos USING gin (lexico)")
    op.execute("CREATE INDEX fragmentos_por_documento ON fragmentos (documento_id, pagina)")
    op.execute("CREATE INDEX fragmentos_por_atencion ON fragmentos (atencion_id)")

    for tabla in _TABLAS:
        _forzar(tabla)

    suyos = "identidad() = 'paciente' AND paciente_id = paciente_actual()"
    de_sus_documentos = (
        "identidad() = 'paciente' AND documento_id IN "
        "(SELECT id FROM documentos WHERE paciente_id = paciente_actual())"
    )

    # --- Documentos: el paciente maneja los suyos; el médico los lee; el lector los lee y
    # marca el estado de lectura.
    op.execute(
        "GRANT SELECT, INSERT, DELETE, UPDATE (estado_lectura, paginas) "
        "ON documentos TO vitalia_api"
    )
    op.execute(f"CREATE POLICY propios_lee ON documentos FOR SELECT TO vitalia_api USING ({suyos})")
    op.execute(
        f"CREATE POLICY propios_sube ON documentos FOR INSERT TO vitalia_api WITH CHECK ({suyos})"
    )
    op.execute(
        f"CREATE POLICY propios_elimina ON documentos FOR DELETE TO vitalia_api USING ({suyos})"
    )
    op.execute(
        "CREATE POLICY medico_y_sistema_leen ON documentos FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('medico', 'sistema'))"
    )
    op.execute(
        "CREATE POLICY sistema_marca ON documentos FOR UPDATE TO vitalia_api "
        "USING (identidad() = 'sistema') WITH CHECK (identidad() = 'sistema')"
    )

    # --- Páginas leídas: las ve el dueño del documento y el médico; las escribe el lector.
    op.execute("GRANT SELECT, INSERT ON paginas_documento TO vitalia_api")
    op.execute(
        f"CREATE POLICY propias ON paginas_documento FOR SELECT TO vitalia_api "
        f"USING ({de_sus_documentos})"
    )
    op.execute(
        "CREATE POLICY medico_y_sistema_leen ON paginas_documento FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('medico', 'sistema'))"
    )
    op.execute(
        "CREATE POLICY sistema_escribe ON paginas_documento FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'sistema')"
    )

    # --- Cola del lector: el paciente encola al subir o al autorizar la IA; el lector trabaja.
    op.execute(
        "GRANT SELECT, INSERT, UPDATE (estado, intentos, error) ON trabajos_lectura TO vitalia_api"
    )
    op.execute(
        f"CREATE POLICY propios_encola ON trabajos_lectura FOR INSERT TO vitalia_api "
        f"WITH CHECK ({de_sus_documentos} AND tipo IN ('leer', 'indexar_documento'))"
    )
    op.execute(
        "CREATE POLICY medico_lee ON trabajos_lectura FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY sistema_trabaja ON trabajos_lectura FOR ALL TO vitalia_api "
        "USING (identidad() = 'sistema') WITH CHECK (identidad() = 'sistema')"
    )

    # --- Fragmentos: los crea y borra el lector; el médico los consulta con la búsqueda, que
    # siempre filtra por un paciente. El paciente no los ve: se borran con su documento.
    op.execute("GRANT SELECT, INSERT, DELETE ON fragmentos TO vitalia_api")
    op.execute(
        "CREATE POLICY medico_y_sistema_leen ON fragmentos FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('medico', 'sistema'))"
    )
    op.execute(
        "CREATE POLICY sistema_escribe ON fragmentos FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'sistema')"
    )
    op.execute(
        "CREATE POLICY sistema_borra ON fragmentos FOR DELETE TO vitalia_api "
        "USING (identidad() = 'sistema')"
    )

    # Al retirar la autorización de IA se borran los fragmentos del paciente en la misma
    # transacción (HU-032, CA-4). Lo hace la base, para que ningún camino del código lo olvide.
    op.execute(
        """
        CREATE FUNCTION borrar_fragmentos_al_retirar() RETURNS trigger
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
        BEGIN
            IF NEW.decision = 'retirada' AND EXISTS (
                SELECT 1 FROM textos_autorizacion WHERE id = NEW.texto_id AND tipo = 'ia'
            ) THEN
                DELETE FROM fragmentos WHERE paciente_id = NEW.paciente_id;
            END IF;
            RETURN NULL;
        END
        $$
        """
    )
    op.execute("REVOKE EXECUTE ON FUNCTION borrar_fragmentos_al_retirar() FROM PUBLIC")
    op.execute(
        "CREATE TRIGGER retiro_de_ia AFTER INSERT ON autorizaciones "
        "FOR EACH ROW EXECUTE FUNCTION borrar_fragmentos_al_retirar()"
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER retiro_de_ia ON autorizaciones")
    op.execute("DROP FUNCTION borrar_fragmentos_al_retirar()")
    for tabla in ("fragmentos", "trabajos_lectura", "paginas_documento", "documentos"):
        op.execute(f"DROP TABLE {tabla}")
    op.execute("DROP TEXT SEARCH CONFIGURATION vitalia_es")
    # La extensión vector se queda: la instaló el superusuario, no esta migración.
