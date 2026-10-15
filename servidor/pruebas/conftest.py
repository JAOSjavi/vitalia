"""Preparación común de las pruebas."""

import asyncio
import os
import secrets
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal
from uuid import UUID

import httpx
import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine

from vitalia.adaptadores.postgres.conexion import crear_motor
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.adaptadores.reloj import RelojDelSistema
from vitalia.casos_de_uso.crear_enlace_de_puesta_en_marcha import CrearEnlaceDePuestaEnMarcha
from vitalia.configuracion import Configuracion
from vitalia.principal import armar

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


CrearUsuario = Callable[[Literal["paciente"]], Awaitable[UUID]]


@pytest.fixture(scope="session")
def crear_usuario(motor_dueno: AsyncEngine) -> CrearUsuario:
    """Crea un paciente inventado sin contraseña, directo en la base, para probar permisos.

    Como dueño, quita por un momento los permisos forzados. Las cuentas que ingresan se crean
    por la API, como lo haría una persona.
    """

    async def _crear(rol: Literal["paciente"]) -> UUID:
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
            await conexion.execute(
                text(
                    "INSERT INTO pacientes (usuario_id, nombres, apellidos, fecha_nacimiento, "
                    "telefono) VALUES (:id, 'Paciente', 'De prueba', '1980-05-17', '3000000000')"
                ),
                {"id": usuario_id},
            )
            for tabla in tablas:
                await conexion.execute(text(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY"))
        return usuario_id

    return _crear


class RelojMovible:
    """Reloj de las pruebas: marca la hora real más lo que se le adelante."""

    def __init__(self) -> None:
        self.adelanto = timedelta()

    def ahora(self) -> datetime:
        return datetime.now(UTC) + self.adelanto


@pytest.fixture(scope="session")
def reloj() -> RelojMovible:
    return RelojMovible()


@pytest.fixture(autouse=True)
def reloj_en_hora(reloj: RelojMovible) -> Iterator[None]:
    yield
    reloj.adelanto = timedelta()


@pytest.fixture(scope="session")
async def api(url_api: str, reloj: RelojMovible) -> AsyncIterator[FastAPI]:
    aplicacion = armar(Configuracion(bd_url=url_api, sesion_secreto="pruebas"), reloj)
    async with aplicacion.router.lifespan_context(aplicacion):
        yield aplicacion


Cliente = Callable[..., httpx.AsyncClient]


@pytest.fixture
def cliente(api: FastAPI) -> Cliente:
    """Un navegador de mentira. Cada equipo tiene su propia dirección de red."""

    def _cliente(equipo: str = "10.0.0.1") -> httpx.AsyncClient:
        transporte = httpx.ASGITransport(app=api, client=(equipo, 50000))
        return httpx.AsyncClient(
            transport=transporte, base_url="https://vitalia.prueba", headers={"X-Vitalia": "1"}
        )

    return _cliente


DOCUMENTO_DEL_MEDICO = {"tipo_documento": "CC", "numero_documento": "52345678"}
CONTRASENA_DE_PRUEBA = "consultorio2026"


@pytest.fixture(scope="session")
async def medico(api: FastAPI, url_api: str) -> UUID:
    """El único médico del consultorio (supuesto S-01), creado con la puesta en marcha."""
    motor = crear_motor(url_api, reutilizar=False)
    try:
        caso = CrearEnlaceDePuestaEnMarcha(UnidadPostgres(motor), RelojDelSistema())
        enlace = await caso.ejecutar()
    finally:
        await motor.dispose()

    transporte = httpx.ASGITransport(app=api, client=("10.0.0.9", 50000))
    async with httpx.AsyncClient(
        transport=transporte, base_url="https://vitalia.prueba", headers={"X-Vitalia": "1"}
    ) as navegador:
        creada = await navegador.post(
            "/api/v1/puesta-en-marcha",
            json={
                "enlace": enlace,
                **DOCUMENTO_DEL_MEDICO,
                "nombres": "Camila",
                "apellidos": "Ríos",
                "correo": "camila@ejemplo.test",
                "contrasena": CONTRASENA_DE_PRUEBA,
            },
        )
        assert creada.status_code == 201, creada.text
        yo = await navegador.get("/api/v1/yo")
    return UUID(yo.json()["usuario_id"])
