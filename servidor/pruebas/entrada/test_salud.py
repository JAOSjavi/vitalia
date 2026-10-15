"""La ruta de salud dice si la API y la base están vivas. Es la que consulta Render."""

import httpx
import pytest

from conftest import Cliente
from vitalia.configuracion import Configuracion
from vitalia.principal import armar


@pytest.mark.bd
async def test_salud_con_la_base_en_linea(cliente: Cliente) -> None:
    async with cliente() as navegador:
        respuesta = await navegador.get("/salud")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"api": "en_linea", "base": "en_linea"}


async def test_salud_con_la_base_caida() -> None:
    api = armar(
        Configuracion(bd_url="postgresql://nadie@127.0.0.1:1/nada", sesion_secreto="pruebas")
    )

    async with api.router.lifespan_context(api):
        transporte = httpx.ASGITransport(app=api)
        async with httpx.AsyncClient(transport=transporte, base_url="https://prueba") as cliente:
            respuesta = await cliente.get("/salud")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"api": "en_linea", "base": "caida"}
