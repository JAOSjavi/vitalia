"""Reloj del sistema, en hora universal."""

from datetime import UTC, datetime


class RelojDelSistema:
    def ahora(self) -> datetime:
        return datetime.now(UTC)
