"""La ruta de salud dice si la API y la base están vivas."""

import httpx
import pytest
from fastapi import FastAPI

from vitalia.casos_de_uso.revisar_salud import RevisarSalud
from vitalia.configuracion import Configuracion
from vitalia.entrada.api import crear_api
from vitalia.principal import armar


class BaseFija:
    def __init__(self, responde: bool) -> None:
        self._responde = responde

    async def responde(self) -> bool:
        return self._responde


async def _pedir_salud(api: FastAPI) -> httpx.Response:
    transporte = httpx.ASGITransport(app=api)
    async with httpx.AsyncClient(transport=transporte, base_url="http://prueba") as cliente:
        return await cliente.get("/salud")


async def test_salud_con_la_base_en_linea() -> None:
    respuesta = await _pedir_salud(crear_api(RevisarSalud(BaseFija(True))))

    assert respuesta.status_code == 200
    assert respuesta.json() == {"api": "en_linea", "base": "en_linea"}


async def test_salud_con_la_base_caida() -> None:
    respuesta = await _pedir_salud(crear_api(RevisarSalud(BaseFija(False))))

    assert respuesta.status_code == 200
    assert respuesta.json() == {"api": "en_linea", "base": "caida"}


@pytest.mark.bd
async def test_salud_de_punta_a_punta(url_api: str) -> None:
    api = armar(Configuracion(bd_url=url_api))

    async with api.router.lifespan_context(api):
        respuesta = await _pedir_salud(api)

    assert respuesta.json() == {"api": "en_linea", "base": "en_linea"}
