"""El paciente ve sus facturas y descarga su PDF (D-35).

La tabla ya deja al paciente leer solo las suyas (política "propias" de 0012); falta el permiso.
"""

from alembic import op

revision: str = "0013"
down_revision: str | None = "0012"

_PERMISOS = {
    "facturas.propias": ("Ver sus propias facturas", ("paciente",)),
}


def _sin_forzar(tablas: tuple[str, ...], ordenes: list[str]) -> None:
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


def downgrade() -> None:
    codigos = ", ".join(f"'{codigo}'" for codigo in _PERMISOS)
    _sin_forzar(
        ("permisos", "rol_permiso"),
        [
            f"DELETE FROM rol_permiso WHERE permiso IN ({codigos})",
            f"DELETE FROM permisos WHERE codigo IN ({codigos})",
        ],
    )
