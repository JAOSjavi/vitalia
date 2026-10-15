"""Preparación común de las pruebas."""

import asyncio
import os
import secrets
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from pathlib import Path
from typing import Literal
from uuid import UUID

import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine

from vitalia.adaptadores.postgres.conexion import crear_motor
from vitalia.adaptadores.postgres.unidad import UnidadPostgres

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


@pytest.fixture(scope="session")
async def motor_dueno(url_api: str) -> AsyncIterator[AsyncEngine]:
    """Motor conectado como el dueño de las tablas, el mismo usuario de las migraciones."""
    motor = crear_motor(_en_la_base_de_pruebas("BD_URL_MIGRACIONES"))
    yield motor
    await motor.dispose()


@pytest.fixture(scope="session")
def unidad(motor_api: AsyncEngine) -> UnidadPostgres:
    return UnidadPostgres(motor_api)


CrearUsuario = Callable[[Literal["medico", "paciente"]], Awaitable[UUID]]


@pytest.fixture(scope="session")
def crear_usuario(motor_dueno: AsyncEngine) -> CrearUsuario:
    """Crea una cuenta inventada. Como dueño, quita por un momento los permisos forzados."""

    async def _crear(rol: Literal["medico", "paciente"]) -> UUID:
        tablas = ("usuarios", "pacientes", "medicos")
        async with motor_dueno.begin() as conexion:
            for tabla in tablas:
                await conexion.execute(text(f"ALTER TABLE {tabla} NO FORCE ROW LEVEL SECURITY"))
            usuario_id: UUID = await conexion.scalar(
                text(
                    "INSERT INTO usuarios (tipo_documento, numero_documento, rol) "
                    "VALUES ('CC', :numero, :rol) RETURNING id"
                ),
                {"numero": str(secrets.randbelow(10**10)), "rol": rol},
            )
            if rol == "paciente":
                orden = (
                    "INSERT INTO pacientes (usuario_id, nombres, apellidos, fecha_nacimiento, "
                    "telefono) VALUES (:id, 'Paciente', 'De prueba', '1980-05-17', '3000000000')"
                )
            else:
                orden = (
                    "INSERT INTO medicos (usuario_id, nombres, apellidos) "
                    "VALUES (:id, 'Médica', 'De prueba')"
                )
            await conexion.execute(text(orden), {"id": usuario_id})
            for tabla in tablas:
                await conexion.execute(text(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY"))
        return usuario_id

    return _crear


@pytest.fixture(scope="session")
async def medico(crear_usuario: CrearUsuario) -> UUID:
    """El único médico del consultorio (supuesto S-01)."""
    return await crear_usuario("medico")
