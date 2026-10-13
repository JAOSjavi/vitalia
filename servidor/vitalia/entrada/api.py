"""Rutas de la API: traducen cada petición a un caso de uso y su resultado a una respuesta."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.types import Lifespan

from vitalia.casos_de_uso.revisar_salud import RevisarSalud


class RespuestaSalud(BaseModel):
    api: Literal["en_linea"]
    base: Literal["en_linea", "caida"]


def crear_api(
    revisar_salud: RevisarSalud, ciclo_de_vida: Lifespan[FastAPI] | None = None
) -> FastAPI:
    api = FastAPI(title="Vitalia", lifespan=ciclo_de_vida)

    @api.get("/salud")
    async def salud() -> RespuestaSalud:
        resultado = await revisar_salud.ejecutar()
        return RespuestaSalud(
            api="en_linea", base="en_linea" if resultado.base_responde else "caida"
        )

    return api
