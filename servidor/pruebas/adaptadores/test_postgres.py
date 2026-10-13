"""El adaptador de PostgreSQL y el usuario de la aplicación, contra una base de verdad."""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from vitalia.adaptadores.postgres.conexion import BasePostgres, crear_motor


@pytest.mark.bd
async def test_la_base_responde(motor_api: AsyncEngine) -> None:
    assert await BasePostgres(motor_api).responde()


async def test_una_base_apagada_no_responde() -> None:
    motor = crear_motor("postgresql+asyncpg://nadie@127.0.0.1:1/nada")
    assert not await BasePostgres(motor).responde()
    await motor.dispose()


@pytest.mark.bd
async def test_el_usuario_de_la_api_no_tiene_privilegios(motor_api: AsyncEngine) -> None:
    async with motor_api.connect() as conexion:
        privilegios = (
            await conexion.execute(
                text(
                    "SELECT rolsuper, rolbypassrls, rolcreatedb, rolcreaterole "
                    "FROM pg_roles WHERE rolname = current_user"
                )
            )
        ).one()
        es_duena_de_la_base = await conexion.scalar(
            text(
                "SELECT pg_get_userbyid(datdba) = current_user "
                "FROM pg_database WHERE datname = current_database()"
            )
        )
        objetos_propios = await conexion.scalar(
            text("SELECT count(*) FROM pg_class WHERE relowner = current_user::regrole")
        )
        roles_heredados = await conexion.scalar(
            text("SELECT count(*) FROM pg_auth_members WHERE member = current_user::regrole")
        )

    assert tuple(privilegios) == (False, False, False, False)
    assert es_duena_de_la_base is False
    assert objetos_propios == 0
    assert roles_heredados == 0


@pytest.mark.bd
async def test_las_migraciones_dejan_las_extensiones(motor_api: AsyncEngine) -> None:
    async with motor_api.connect() as conexion:
        extensiones = set(await conexion.scalars(text("SELECT extname FROM pg_extension")))

    assert {"btree_gist", "unaccent"} <= extensiones
