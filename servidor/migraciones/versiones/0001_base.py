"""Extensiones de la base y acceso del usuario de la aplicación al esquema."""

from alembic import op

revision: str = "0001"
down_revision: str | None = None


def upgrade() -> None:
    # btree_gist: restricción contra choques de citas. unaccent: búsqueda sin tildes.
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.execute("CREATE EXTENSION IF NOT EXISTS unaccent")
    op.execute("GRANT USAGE ON SCHEMA public TO vitalia_api")


def downgrade() -> None:
    op.execute("REVOKE USAGE ON SCHEMA public FROM vitalia_api")
    op.execute("DROP EXTENSION unaccent")
    op.execute("DROP EXTENSION btree_gist")
