"""Horario, tipos de cita y citas (HU-008, HU-010, HU-011 a HU-017, HU-020, HU-021, HU-023).

Dos citas no pueden ocupar el mismo tiempo: lo garantiza una restricción de la base, no solo el
código (HU-011, CA-2). Para ofrecer espacios, el paciente necesita saber qué está ocupado sin ver
de quién: eso lo entrega la función tiempos_ocupados, que solo devuelve intervalos.
"""

from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"

_INTERNA = "session_user <> current_user"
_TABLAS = ("franjas_horario", "tipos_cita", "citas", "cambios_cita")

_PERMISOS = {
    "horario.ver": ("Ver el horario semanal", ("medico",)),
    "horario.editar": ("Guardar el horario semanal", ("medico",)),
    "tipos_cita.ver": ("Ver los tipos de cita", ("medico", "paciente")),
    "tipos_cita.editar": ("Crear, editar, activar y desactivar tipos de cita", ("medico",)),
    "disponibilidad.ver": ("Consultar los días y las horas libres", ("medico", "paciente")),
    "citas.crear": ("Crear una cita", ("medico", "paciente")),
    "citas.ver": ("Listar citas", ("medico", "paciente")),
    "citas.mover": ("Mover una cita", ("medico", "paciente")),
    "citas.cancelar": ("Cancelar una cita", ("medico", "paciente")),
    "inicio.ver": ("Ver el inicio del paciente", ("paciente",)),
    "agenda.ver": ("Ver la agenda del día", ("medico",)),
    "pacientes.ver": ("Buscar y listar pacientes", ("medico",)),
}


def _forzar(tabla: str) -> None:
    op.execute(f"ALTER TABLE {tabla} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY interna ON {tabla} TO CURRENT_USER "
        f"USING ({_INTERNA}) WITH CHECK ({_INTERNA})"
    )


def _sin_forzar(tablas: tuple[str, ...], ordenes: list[str]) -> None:
    """Los catálogos tienen permisos forzados: el dueño los quita un momento para escribir."""
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} NO FORCE ROW LEVEL SECURITY")
    for orden in ordenes:
        op.execute(orden)
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")


def upgrade() -> None:
    # El paciente de la sesión. Corre con los permisos de quien llama: solo ve su propia fila.
    op.execute(
        """
        CREATE FUNCTION paciente_actual() RETURNS uuid LANGUAGE sql STABLE
        AS $$ SELECT id FROM pacientes WHERE usuario_id = usuario_actual() $$
        """
    )

    # Día de la semana como en la norma ISO: 1 es lunes y 7 domingo. Horas de Colombia.
    op.execute(
        """
        CREATE TABLE franjas_horario (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            dia_semana smallint NOT NULL CHECK (dia_semana BETWEEN 1 AND 7),
            hora_inicio time NOT NULL,
            hora_fin time NOT NULL,
            CHECK (hora_inicio < hora_fin)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE tipos_cita (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            nombre text NOT NULL,
            duracion_minutos integer NOT NULL CHECK (duracion_minutos BETWEEN 5 AND 240),
            activo boolean NOT NULL DEFAULT true
        )
        """
    )
    op.execute(
        """
        CREATE TABLE citas (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            paciente_id uuid NOT NULL REFERENCES pacientes,
            tipo_cita_id uuid NOT NULL REFERENCES tipos_cita,
            inicio timestamptz NOT NULL,
            fin timestamptz NOT NULL,
            estado text NOT NULL DEFAULT 'confirmada'
                CHECK (estado IN ('confirmada', 'cancelada', 'atendida', 'no_asistio')),
            creada_por uuid NOT NULL REFERENCES usuarios,
            fuera_de_horario boolean NOT NULL DEFAULT false,
            creado_en timestamptz NOT NULL DEFAULT now(),
            CHECK (inicio < fin),
            CONSTRAINT sin_choques EXCLUDE USING gist (tstzrange(inicio, fin, '[)') WITH &&)
                WHERE (estado <> 'cancelada')
        )
        """
    )
    op.execute("CREATE INDEX citas_por_inicio ON citas (inicio)")
    op.execute("CREATE INDEX citas_por_paciente ON citas (paciente_id, inicio)")
    op.execute(
        """
        CREATE TABLE cambios_cita (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            cita_id uuid NOT NULL REFERENCES citas,
            usuario_id uuid NOT NULL REFERENCES usuarios,
            tipo text NOT NULL
                CHECK (tipo IN ('creada', 'movida', 'cancelada', 'asistencia', 'correccion')),
            inicio_anterior timestamptz,
            inicio_nuevo timestamptz,
            motivo text,
            fecha timestamptz NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX cambios_por_cita ON cambios_cita (cita_id, fecha)")
    # Búsqueda de pacientes sin tildes ni mayúsculas (HU-023). Una traducción fija de letras
    # basta para los nombres en español y, a diferencia de unaccent, sirve para un índice.
    op.execute(
        """
        CREATE FUNCTION sin_tildes(texto text) RETURNS text LANGUAGE sql IMMUTABLE PARALLEL SAFE
        AS $$
            SELECT lower(translate(texto,
                'ÁÀÂÄÉÈÊËÍÌÎÏÓÒÔÖÚÙÛÜÑÇáàâäéèêëíìîïóòôöúùûüñç',
                'AAAAEEEEIIIIOOOOUUUUNCaaaaeeeeiiiioooouuuunc'))
        $$
        """
    )
    op.execute(
        "CREATE INDEX pacientes_por_nombre ON pacientes "
        "(sin_tildes(nombres || ' ' || apellidos) text_pattern_ops)"
    )

    for tabla in _TABLAS:
        _forzar(tabla)

    # --- Horario y tipos: el paciente los lee para agendar; el médico los maneja.
    op.execute("GRANT SELECT, INSERT, DELETE ON franjas_horario TO vitalia_api")
    op.execute(
        "CREATE POLICY lectura ON franjas_horario FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('paciente', 'medico'))"
    )
    op.execute(
        "CREATE POLICY medico_inserta ON franjas_horario FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY medico_borra ON franjas_horario FOR DELETE TO vitalia_api "
        "USING (identidad() = 'medico')"
    )
    op.execute(
        "GRANT SELECT, INSERT, UPDATE (nombre, duracion_minutos, activo) ON tipos_cita "
        "TO vitalia_api"
    )
    op.execute(
        "CREATE POLICY lectura ON tipos_cita FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('paciente', 'medico'))"
    )
    op.execute(
        "CREATE POLICY medico_inserta ON tipos_cita FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY medico_edita ON tipos_cita FOR UPDATE TO vitalia_api "
        "USING (identidad() = 'medico') WITH CHECK (identidad() = 'medico')"
    )

    # --- Citas: el paciente las suyas, y solo puede dejarlas confirmadas o canceladas.
    op.execute(
        "GRANT SELECT, INSERT, UPDATE (inicio, fin, estado, fuera_de_horario) "
        "ON citas TO vitalia_api"
    )
    suya = "identidad() = 'paciente' AND paciente_id = paciente_actual()"
    op.execute(f"CREATE POLICY propias ON citas FOR SELECT TO vitalia_api USING ({suya})")
    op.execute(
        f"CREATE POLICY propias_crea ON citas FOR INSERT TO vitalia_api "
        f"WITH CHECK ({suya} AND estado = 'confirmada' AND creada_por = usuario_actual())"
    )
    op.execute(
        f"CREATE POLICY propias_cambia ON citas FOR UPDATE TO vitalia_api "
        f"USING ({suya}) WITH CHECK ({suya} AND estado IN ('confirmada', 'cancelada'))"
    )
    op.execute(
        "CREATE POLICY medico_lee ON citas FOR SELECT TO vitalia_api USING (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY medico_crea ON citas FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'medico' AND creada_por = usuario_actual())"
    )
    op.execute(
        "CREATE POLICY medico_cambia ON citas FOR UPDATE TO vitalia_api "
        "USING (identidad() = 'medico') WITH CHECK (identidad() = 'medico')"
    )

    # --- Historial de cada cita: quién la creó, movió o canceló, y cuándo (HU-014, CA-4).
    op.execute("GRANT SELECT, INSERT ON cambios_cita TO vitalia_api")
    de_sus_citas = (
        "identidad() = 'paciente' AND cita_id IN "
        "(SELECT id FROM citas WHERE paciente_id = paciente_actual())"
    )
    op.execute(
        f"CREATE POLICY propias ON cambios_cita FOR SELECT TO vitalia_api USING ({de_sus_citas})"
    )
    op.execute(
        f"CREATE POLICY propias_anota ON cambios_cita FOR INSERT TO vitalia_api "
        f"WITH CHECK ({de_sus_citas} AND usuario_id = usuario_actual())"
    )
    op.execute(
        "CREATE POLICY medico_lee ON cambios_cita FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY medico_anota ON cambios_cita FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'medico' AND usuario_id = usuario_actual())"
    )

    # --- Lo ocupado, sin decir de quién. Solo para quien tiene sesión.
    op.execute(
        """
        CREATE FUNCTION tiempos_ocupados(p_desde timestamptz, p_hasta timestamptz)
        RETURNS TABLE (cita_id uuid, inicio timestamptz, fin timestamptz)
        LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
            SELECT id, inicio, fin FROM citas
            WHERE identidad() IN ('paciente', 'medico')
              AND estado <> 'cancelada' AND inicio < p_hasta AND fin > p_desde
            ORDER BY inicio
        $$
        """
    )
    op.execute("REVOKE EXECUTE ON FUNCTION tiempos_ocupados(timestamptz, timestamptz) FROM PUBLIC")
    op.execute(
        "GRANT EXECUTE ON FUNCTION tiempos_ocupados(timestamptz, timestamptz) TO vitalia_api"
    )

    # --- Permisos de las operaciones nuevas (HU-006): lo que no está aquí queda negado.
    ordenes = []
    for codigo, (descripcion, roles) in _PERMISOS.items():
        ordenes.append(f"INSERT INTO permisos VALUES ('{codigo}', '{descripcion}')")
        ordenes += [f"INSERT INTO rol_permiso VALUES ('{rol}', '{codigo}')" for rol in roles]
    _sin_forzar(("permisos", "rol_permiso"), ordenes)


def downgrade() -> None:
    codigos = ", ".join(f"'{codigo}'" for codigo in _PERMISOS)
    _sin_forzar(
        ("permisos", "rol_permiso"),
        [
            f"DELETE FROM rol_permiso WHERE permiso IN ({codigos})",
            f"DELETE FROM permisos WHERE codigo IN ({codigos})",
        ],
    )
    op.execute("DROP FUNCTION tiempos_ocupados(timestamptz, timestamptz)")
    op.execute("DROP INDEX pacientes_por_nombre")
    op.execute("DROP FUNCTION sin_tildes(text)")
    for tabla in reversed(_TABLAS):
        op.execute(f"DROP TABLE {tabla}")
    op.execute("DROP FUNCTION paciente_actual()")
