"""Fichas secretas de un solo dueño: sesiones y enlaces. En la base se guarda solo su huella."""

import hashlib
import secrets


def nueva_ficha() -> tuple[str, str]:
    """Devuelve la ficha, que va a la persona, y su huella, que va a la base."""
    ficha = secrets.token_urlsafe(32)
    return ficha, huella_de(ficha)


def huella_de(ficha: str) -> str:
    return hashlib.sha256(ficha.encode()).hexdigest()
