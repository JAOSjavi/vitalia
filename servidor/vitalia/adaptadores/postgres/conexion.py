"""Conexión a PostgreSQL: un motor asíncrono con conexiones reutilizadas."""

import asyncio
import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

SEGUNDOS_PARA_CONECTAR = 10
SEGUNDOS_POR_CONSULTA = 30
SEGUNDOS_PARA_RESPONDER = 3

_EQUIPOS_LOCALES = {"localhost", "127.0.0.1", "::1"}

_registro = logging.getLogger(__name__)


def crear_motor(url: str, *, reutilizar: bool = True) -> AsyncEngine:
    """Acepta la dirección tal como la entrega Render: postgresql://usuario:clave@servidor/base."""
    direccion = make_url(url).set(drivername="postgresql+asyncpg")
    al_conectar: dict[str, Any] = {
        "timeout": SEGUNDOS_PARA_CONECTAR,
        "command_timeout": SEGUNDOS_POR_CONSULTA,
    }
    # Fuera del propio equipo la conexión cruza internet: siempre cifrada.
    if direccion.host not in _EQUIPOS_LOCALES:
        al_conectar["ssl"] = "require"
    if not reutilizar:
        return create_async_engine(direccion, poolclass=NullPool, connect_args=al_conectar)
    return create_async_engine(
        direccion, pool_size=5, max_overflow=5, pool_pre_ping=True, connect_args=al_conectar
    )


class BasePostgres:
    def __init__(self, motor: AsyncEngine) -> None:
        self._motor = motor

    async def responde(self) -> bool:
        try:
            async with asyncio.timeout(SEGUNDOS_PARA_RESPONDER), self._motor.connect() as conexion:
                await conexion.execute(text("SELECT 1"))
        except Exception as error:
            # Solo el tipo: el mensaje del controlador puede traer el usuario y el servidor.
            _registro.warning("La base no responde: %s", type(error).__name__)
            return False
        return True
