"""Búsqueda de fragmentos por paciente y datos para retirar identificadores (D-30, HU-033).

La búsqueda combina dos listas dentro de los fragmentos de un solo paciente: la de los más
cercanos por significado (distancia entre vectores) y la de los que comparten palabras con la
pregunta (texto completo en español, sin tildes). Se mezclan por su posición en cada lista
(fusión por rango recíproco): sube lo que aparece arriba en cualquiera de las dos.
"""

from alembic import op

revision: str = "0007"
down_revision: str | None = "0006"

_PERMISOS = {
    "asistente.preguntar": ("Preguntar al asistente sobre un paciente", ("medico",)),
}

# Constante de la fusión por rango recíproco. 60 es el valor de la publicación original:
# suaviza la diferencia entre el primer puesto y los siguientes.
_K = 60


def _sin_forzar(tablas: tuple[str, ...], ordenes: list[str]) -> None:
    """Los catálogos tienen permisos forzados: el dueño los quita un momento para escribir."""
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} NO FORCE ROW LEVEL SECURITY")
    for orden in ordenes:
        op.execute(orden)
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")


def upgrade() -> None:
    ordenes = []
    for codigo, (descripcion, roles) in _PERMISOS.items():
        ordenes.append(f"INSERT INTO permisos VALUES ('{codigo}', '{descripcion}')")
        ordenes += [f"INSERT INTO rol_permiso VALUES ('{rol}', '{codigo}')" for rol in roles]
    _sin_forzar(("permisos", "rol_permiso"), ordenes)

    # Lo único que el lector necesita del paciente: lo que hay que tapar antes de enviar texto
    # al proveedor. Así el lector no tiene que poder leer las tablas de cuentas.
    op.execute(
        """
        CREATE FUNCTION identificadores_paciente(p_paciente uuid)
        RETURNS TABLE (nombres text, apellidos text, numero_documento text, telefono text,
                       correo text)
        LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
            SELECT p.nombres, p.apellidos, u.numero_documento, p.telefono, u.correo
            FROM pacientes p JOIN usuarios u ON u.id = p.usuario_id
            WHERE p.id = p_paciente AND identidad() IN ('sistema', 'medico')
        $$
        """
    )
    op.execute("REVOKE EXECUTE ON FUNCTION identificadores_paciente(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION identificadores_paciente(uuid) TO vitalia_api")

    # Corre con los permisos de quien llama: los permisos por fila de fragmentos siguen
    # valiendo, y además todo se filtra por el paciente que se pide.
    op.execute(
        f"""
        CREATE FUNCTION buscar_fragmentos(
            p_paciente uuid, p_vector vector, p_consulta text,
            p_por_metodo integer DEFAULT 20, p_total integer DEFAULT 12
        )
        RETURNS TABLE (fragmento_id uuid, puntaje double precision,
                       rango_significado integer, rango_palabras integer)
        LANGUAGE sql STABLE SET search_path = public, pg_temp
        AS $$
            WITH consulta AS (
                -- Cualquier palabra de la pregunta sirve: se unen con "o" en vez de "y".
                SELECT nullif(
                    replace(plainto_tsquery('vitalia_es', p_consulta)::text, ' & ', ' | '), ''
                )::tsquery AS q
            ),
            significado AS (
                SELECT id, row_number() OVER (ORDER BY vector <=> p_vector) AS rango
                FROM fragmentos
                WHERE paciente_id = p_paciente
                ORDER BY vector <=> p_vector
                LIMIT p_por_metodo
            ),
            palabras AS (
                SELECT f.id,
                       row_number() OVER (ORDER BY ts_rank_cd(f.lexico, c.q) DESC) AS rango
                FROM fragmentos f CROSS JOIN consulta c
                WHERE f.paciente_id = p_paciente AND c.q IS NOT NULL AND f.lexico @@ c.q
                ORDER BY ts_rank_cd(f.lexico, c.q) DESC
                LIMIT p_por_metodo
            )
            SELECT id,
                   coalesce(1.0 / ({_K} + s.rango), 0) + coalesce(1.0 / ({_K} + p.rango), 0),
                   s.rango::integer, p.rango::integer
            FROM significado s FULL JOIN palabras p USING (id)
            ORDER BY 2 DESC
            LIMIT p_total
        $$
        """
    )
    op.execute(
        "REVOKE EXECUTE ON FUNCTION buscar_fragmentos(uuid, vector, text, integer, integer) "
        "FROM PUBLIC"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION buscar_fragmentos(uuid, vector, text, integer, integer) "
        "TO vitalia_api"
    )


def downgrade() -> None:
    op.execute("DROP FUNCTION buscar_fragmentos(uuid, vector, text, integer, integer)")
    op.execute("DROP FUNCTION identificadores_paciente(uuid)")
    codigos = ", ".join(f"'{codigo}'" for codigo in _PERMISOS)
    _sin_forzar(
        ("permisos", "rol_permiso"),
        [
            f"DELETE FROM rol_permiso WHERE permiso IN ({codigos})",
            f"DELETE FROM permisos WHERE codigo IN ({codigos})",
        ],
    )
