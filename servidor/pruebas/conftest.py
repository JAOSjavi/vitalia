"""Preparación común de las pruebas."""

import asyncio
import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine

from vitalia.adaptadores.postgres.conexion import crear_motor

SERVIDOR = Path(__file__).parent.parent
BASE_DE_PRUEBAS = "vitalia_pruebas"

load_dotenv(SERVIDOR / ".env")


def _en_la_base_de_pruebas(variable: str) -> str:
    direccion = make_url(os.environ[variable]).set(database=BASE_DE_PRUEBAS)
    return direccion.render_as_string(hide_password=False)


async def _administrar(orden: str) -> None:
    # Crear y borrar bases se hace conectado a la de desarrollo, con su dueño.
    motor = crear_motor(os.environ["BD_URL_MIGRACIONES"], reutilizar=False)
    async with motor.connect() as conexion:
        en_directo = await conexion.execution_options(isolation_level="AUTOCOMMIT")
        await en_directo.execute(text(orden))
    await motor.dispose()


@pytest.fixture(scope="session")
def url_api() -> Iterator[str]:
    """Crea la base de pruebas con sus migraciones y la borra al terminar."""
    asyncio.run(_administrar(f"DROP DATABASE IF EXISTS {BASE_DE_PRUEBAS} WITH (FORCE)"))
    asyncio.run(_administrar(f"CREATE DATABASE {BASE_DE_PRUEBAS}"))
    alembic = Config(SERVIDOR / "alembic.ini")
    alembic.attributes["url"] = _en_la_base_de_pruebas("BD_URL_MIGRACIONES")
    command.upgrade(alembic, "head")
    yield _en_la_base_de_pruebas("BD_URL")
    asyncio.run(_administrar(f"DROP DATABASE {BASE_DE_PRUEBAS} WITH (FORCE)"))


@pytest.fixture(scope="session")
async def motor_api(url_api: str) -> AsyncIterator[AsyncEngine]:
    """Motor conectado como vitalia_api, el usuario sin privilegios de la aplicación."""
    motor = crear_motor(url_api)
    yield motor
    await motor.dispose()
