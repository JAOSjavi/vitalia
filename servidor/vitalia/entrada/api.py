"""La API: une las rutas, la traducción de errores y las reglas comunes a toda petición."""

from collections.abc import Awaitable, Callable
from typing import Literal

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from starlette.types import Lifespan

from vitalia.entrada import (
    rutas_asistente,
    rutas_citas,
    rutas_consultorio,
    rutas_cuentas,
    rutas_documentos,
)
from vitalia.entrada.casos import Ajustes, CasosDeUso
from vitalia.entrada.errores import registrar_traducciones, respuesta_de_error

# Toda operación que modifica exige este encabezado: un formulario de otro sitio no puede
# ponerlo, y así no se puede actuar con la sesión de alguien desde afuera.
ENCABEZADO_PROPIO = "X-Vitalia"
_MODIFICAN = {"POST", "PUT", "PATCH", "DELETE"}


class RespuestaSalud(BaseModel):
    api: Literal["en_linea"]
    base: Literal["en_linea", "caida"]


def crear_api(
    casos: CasosDeUso, ajustes: Ajustes, ciclo_de_vida: Lifespan[FastAPI] | None = None
) -> FastAPI:
    api = FastAPI(title="Vitalia", lifespan=ciclo_de_vida)
    api.state.casos = casos
    api.state.ajustes = ajustes
    registrar_traducciones(api)
    api.include_router(rutas_cuentas.rutas)
    api.include_router(rutas_consultorio.rutas)
    api.include_router(rutas_citas.rutas)
    api.include_router(rutas_documentos.rutas)
    api.include_router(rutas_asistente.rutas)

    @api.middleware("http")
    async def reglas_comunes(
        request: Request, siguiente: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        es_de_la_api = request.url.path.startswith("/api/")
        if (
            es_de_la_api
            and request.method in _MODIFICAN
            and not request.headers.get(ENCABEZADO_PROPIO)
        ):
            return respuesta_de_error(
                403, "falta_encabezado", "La petición no salió de la aplicación."
            )
        respuesta = await siguiente(request)
        if es_de_la_api:
            # Nada de la API se guarda en el navegador: al volver atrás no queda información.
            respuesta.headers["Cache-Control"] = "no-store"
        return respuesta

    @api.get("/salud")
    async def salud() -> RespuestaSalud:
        """Lo consulta Render para saber si el servicio está vivo."""
        resultado = await casos.revisar_salud.ejecutar()
        return RespuestaSalud(
            api="en_linea", base="en_linea" if resultado.base_responde else "caida"
        )

    return api
