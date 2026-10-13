"""Único lugar que une los adaptadores con los casos de uso.

Se arranca con: uv run uvicorn --factory vitalia.principal:crear
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from vitalia.adaptadores.postgres.conexion import BasePostgres, crear_motor
from vitalia.casos_de_uso.revisar_salud import RevisarSalud
from vitalia.configuracion import Configuracion, leer
from vitalia.entrada.api import crear_api


def armar(configuracion: Configuracion) -> FastAPI:
    motor = crear_motor(configuracion.bd_url)

    @asynccontextmanager
    async def ciclo_de_vida(_: FastAPI) -> AsyncIterator[None]:
        yield
        await motor.dispose()

    return crear_api(RevisarSalud(BasePostgres(motor)), ciclo_de_vida)


def crear() -> FastAPI:
    return armar(leer())
