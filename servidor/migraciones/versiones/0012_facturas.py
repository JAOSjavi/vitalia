"""Factura electrónica de la consulta con Factus (D-35).

- Una factura por cita atendida: la cita es la referencia única que se le envía a Factus, y la
  base no deja guardar dos para la misma cita.
- Una factura emitida no cambia ni se borra: la API solo puede leer y agregar. Se anula con una
  nota crédito, que queda para después.
- No guarda nada clínico: el concepto es el tipo de cita, nunca el diagnóstico.
"""

from alembic import op

revision: str = "0012"
down_revision: str | None = "0011"

_INTERNA = "session_user <> current_user"

_PERMISOS = {
    "facturas.ver": ("Ver los cobros y las facturas emitidas", ("medico",)),
    "facturas.emitir": ("Emitir la factura electrónica de una cita atendida", ("medico",)),
}


def _sin_forzar(tablas: tuple[str, ...], ordenes: list[str]) -> None:
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} NO FORCE ROW LEVEL SECURITY")
    for orden in ordenes:
        op.execute(orden)
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE facturas (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            cita_id uuid NOT NULL UNIQUE REFERENCES citas,
            paciente_id uuid NOT NULL REFERENCES pacientes,
            emitida_por uuid NOT NULL REFERENCES usuarios,
            concepto text NOT NULL CHECK (length(concepto) BETWEEN 1 AND 200),
            valor numeric(12, 2) NOT NULL CHECK (valor > 0),
            medio_pago text NOT NULL CHECK (medio_pago IN
                ('efectivo', 'transferencia', 'tarjeta_debito', 'tarjeta_credito')),
            numero text NOT NULL,
            cufe text NOT NULL,
            enlace_publico text,
            enlace_qr text,
            ambiente text NOT NULL CHECK (ambiente IN ('pruebas', 'produccion', 'de_mentira')),
            emitida_en timestamptz NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX facturas_por_paciente ON facturas (paciente_id, emitida_en)")

    op.execute("ALTER TABLE facturas ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE facturas FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY interna ON facturas TO CURRENT_USER "
        f"USING ({_INTERNA}) WITH CHECK ({_INTERNA})"
    )
    op.execute("GRANT SELECT, INSERT ON facturas TO vitalia_api")
    op.execute(
        "CREATE POLICY medico_lee ON facturas FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY medico_emite ON facturas FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'medico' AND emitida_por = usuario_actual())"
    )
    op.execute(
        "CREATE POLICY propias ON facturas FOR SELECT TO vitalia_api "
        "USING (identidad() = 'paciente' AND paciente_id = paciente_actual())"
    )

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
    op.execute("DROP TABLE facturas")
