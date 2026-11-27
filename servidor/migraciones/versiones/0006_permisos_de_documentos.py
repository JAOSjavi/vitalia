"""Permisos para subir y ver documentos (HU-028, HU-029) y lo que el lector necesita leer.

El lector trabaja con la identidad sistema. Para saber si un paciente autorizó la IA cruza sus
autorizaciones con el tipo de texto, así que necesita leer los textos de autorización.
"""

from alembic import op

revision: str = "0006"
down_revision: str | None = "0005"

_PERMISOS = {
    "documentos.subir": ("Subir mis documentos", ("paciente",)),
    "documentos.ver": ("Ver la lista de mis documentos", ("paciente",)),
}


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

    op.execute(
        "CREATE POLICY sistema_lee ON textos_autorizacion FOR SELECT TO vitalia_api "
        "USING (identidad() = 'sistema')"
    )


def downgrade() -> None:
    op.execute("DROP POLICY sistema_lee ON textos_autorizacion")
    codigos = ", ".join(f"'{codigo}'" for codigo in _PERMISOS)
    _sin_forzar(
        ("permisos", "rol_permiso"),
        [
            f"DELETE FROM rol_permiso WHERE permiso IN ({codigos})",
            f"DELETE FROM permisos WHERE codigo IN ({codigos})",
        ],
    )
