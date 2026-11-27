"""El médico marca la asistencia a las citas (HU-018).

La fila ya lo permitía (política medico_cambia de la migración 0004) y el historial ya tenía los
tipos asistencia y correccion; faltaba el permiso de la operación.
"""

from alembic import op

revision: str = "0009"
down_revision: str | None = "0008"

_PERMISOS = {
    "citas.asistencia": ("Marcar una cita como atendida o no asistió", ("medico",)),
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


def downgrade() -> None:
    codigos = ", ".join(f"'{codigo}'" for codigo in _PERMISOS)
    _sin_forzar(
        ("permisos", "rol_permiso"),
        [
            f"DELETE FROM rol_permiso WHERE permiso IN ({codigos})",
            f"DELETE FROM permisos WHERE codigo IN ({codigos})",
        ],
    )
