"""La sesión viaja en una cookie que el código de la página no puede leer (arquitectura, 3.7)."""

import hashlib
import hmac
from typing import Annotated

from fastapi import Depends, Request, Response

from vitalia.casos_de_uso.ingresar import SesionNueva
from vitalia.dominio.identidad import Identidad
from vitalia.entrada.casos import Ajustes, CasosDeUso

COOKIE = "vitalia_sesion"
RUTA_DE_LA_COOKIE = "/api"


class SinSesion(Exception):
    pass


def casos(request: Request) -> CasosDeUso:
    resultado: CasosDeUso = request.app.state.casos
    return resultado


def ajustes(request: Request) -> Ajustes:
    resultado: Ajustes = request.app.state.ajustes
    return resultado


async def _identidad(request: Request) -> Identidad:
    ficha = request.cookies.get(COOKIE)
    if not ficha:
        raise SinSesion()
    identidad = await casos(request).validar_sesion.ejecutar(ficha)
    if identidad is None:
        raise SinSesion()
    return identidad


Sesion = Annotated[Identidad, Depends(_identidad)]


def ficha_de_la_sesion(request: Request) -> str:
    return request.cookies.get(COOKIE, "")


def poner_cookie(respuesta: Response, sesion: SesionNueva) -> None:
    respuesta.set_cookie(
        COOKIE,
        sesion.ficha,
        httponly=True,
        secure=True,
        samesite="lax",
        path=RUTA_DE_LA_COOKIE,
    )


def quitar_cookie(respuesta: Response) -> None:
    respuesta.delete_cookie(
        COOKIE,
        httponly=True,
        secure=True,
        samesite="lax",
        path=RUTA_DE_LA_COOKIE,
    )


def origen(request: Request) -> str:
    """Resumen de la dirección de red del equipo. La dirección misma no se guarda."""
    direccion = request.client.host if request.client else "desconocida"
    secreto = ajustes(request).secreto_del_origen
    return hmac.new(secreto, direccion.encode(), hashlib.sha256).hexdigest()[:32]
