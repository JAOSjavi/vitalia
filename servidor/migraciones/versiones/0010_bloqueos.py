"""Bloqueos del horario: tiempo en que el médico no atiende (HU-009).

Un bloqueo de varios días es un solo rango (diseno/02-modelo-de-datos.md). Solo el médico ve y
maneja la tabla. El paciente no la lee: le basta saber que ese tiempo está ocupado, y para eso
tiempos_ocupados ahora devuelve también los bloqueos, sin cita ni motivo.
"""

from alembic import op

revision: str = "0010"
down_revision: str | None = "0009"

_INTERNA = "session_user <> current_user"

_PERMISOS = {
    "bloqueos.ver": ("Ver los bloqueos del horario", ("medico",)),
    "bloqueos.crear": ("Bloquear un tiempo del horario", ("medico",)),
    "bloqueos.eliminar": ("Eliminar un bloqueo futuro", ("medico",)),
}

_OCUPADOS_CON_BLOQUEOS = """
    CREATE OR REPLACE FUNCTION tiempos_ocupados(p_desde timestamptz, p_hasta timestamptz)
    RETURNS TABLE (cita_id uuid, inicio timestamptz, fin timestamptz)
    LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp
    AS $$
        SELECT * FROM (
            SELECT id, inicio, fin FROM citas
            WHERE estado <> 'cancelada' AND inicio < p_hasta AND fin > p_desde
            UNION ALL
            SELECT NULL::uuid, inicio, fin FROM bloqueos
            WHERE inicio < p_hasta AND fin > p_desde
        ) ocupado
        WHERE identidad() IN ('paciente', 'medico')
        ORDER BY inicio
    $$
"""

_OCUPADOS_SIN_BLOQUEOS = """
    CREATE OR REPLACE FUNCTION tiempos_ocupados(p_desde timestamptz, p_hasta timestamptz)
    RETURNS TABLE (cita_id uuid, inicio timestamptz, fin timestamptz)
    LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp
    AS $$
        SELECT id, inicio, fin FROM citas
        WHERE identidad() IN ('paciente', 'medico')
          AND estado <> 'cancelada' AND inicio < p_hasta AND fin > p_desde
        ORDER BY inicio
    $$
"""


def _sin_forzar(tablas: tuple[str, ...], ordenes: list[str]) -> None:
    """Los catálogos tienen permisos forzados: el dueño los quita un momento para escribir."""
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} NO FORCE ROW LEVEL SECURITY")
    for orden in ordenes:
        op.execute(orden)
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE bloqueos (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            inicio timestamptz NOT NULL,
            fin timestamptz NOT NULL,
            motivo text NOT NULL CHECK (length(motivo) BETWEEN 1 AND 120),
            creado_por uuid NOT NULL REFERENCES usuarios,
            creado_en timestamptz NOT NULL DEFAULT now(),
            CHECK (inicio < fin)
        )
        """
    )
    op.execute("CREATE INDEX bloqueos_por_inicio ON bloqueos (inicio)")

    op.execute("ALTER TABLE bloqueos ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE bloqueos FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY interna ON bloqueos TO CURRENT_USER "
        f"USING ({_INTERNA}) WITH CHECK ({_INTERNA})"
    )
    op.execute("GRANT SELECT, INSERT, DELETE ON bloqueos TO vitalia_api")
    op.execute(
        "CREATE POLICY medico_lee ON bloqueos FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY medico_crea ON bloqueos FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'medico' AND creado_por = usuario_actual())"
    )
    op.execute(
        "CREATE POLICY medico_elimina ON bloqueos FOR DELETE TO vitalia_api "
        "USING (identidad() = 'medico')"
    )

    # Lo ocupado incluye los bloqueos: así nunca se le ofrecen al paciente (HU-009, CA-1).
    op.execute(_OCUPADOS_CON_BLOQUEOS)

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
    op.execute(_OCUPADOS_SIN_BLOQUEOS)
    op.execute("DROP TABLE bloqueos")
