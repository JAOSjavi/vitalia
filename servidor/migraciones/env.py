"""Entorno de Alembic. Las migraciones corren con el usuario dueño de las tablas."""

import asyncio
import os

from alembic import context
from dotenv import load_dotenv
from sqlalchemy.engine import Connection

from vitalia.adaptadores.postgres.conexion import crear_motor


def _url() -> str:
    # Las pruebas pasan aquí la dirección de su propia base.
    url = context.config.attributes.get("url")
    if url:
        return str(url)
    load_dotenv()
    return os.environ["BD_URL_MIGRACIONES"]


def _migrar(conexion: Connection) -> None:
    context.configure(connection=conexion, target_metadata=None)
    with context.begin_transaction():
        context.run_migrations()


async def _correr() -> None:
    motor = crear_motor(_url(), reutilizar=False)
    async with motor.connect() as conexion:
        await conexion.run_sync(_migrar)
    await motor.dispose()


asyncio.run(_correr())
