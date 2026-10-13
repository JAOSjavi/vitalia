"""${message}"""

from alembic import op

revision: str = ${repr(up_revision)}
down_revision: str | None = ${repr(down_revision)}


def upgrade() -> None:
    op.execute("")


def downgrade() -> None:
    op.execute("")
