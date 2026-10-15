"""Traduce los errores del dominio a respuestas de la API, siempre con la misma forma.

{"codigo": ..., "mensaje": ..., "detalle": ...} (diseno/03-api.md, sección 1).
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from vitalia.dominio.cuentas import (
    AutorizacionDesactualizada,
    DatosInvalidos,
    DocumentoYaRegistrado,
    EnlaceInvalido,
    MenorDeEdad,
    YaHayMedico,
)
from vitalia.dominio.ingreso import CredencialesInvalidas, IngresoBloqueado
from vitalia.dominio.permisos import AccesoDenegado
from vitalia.entrada.sesion import SinSesion


def respuesta_de_error(
    estado: int, codigo: str, mensaje: str, detalle: object = None
) -> JSONResponse:
    return JSONResponse(
        status_code=estado, content={"codigo": codigo, "mensaje": mensaje, "detalle": detalle}
    )


# Errores sin datos propios: estado, código y mensaje para mostrar.
_FIJOS: dict[type[Exception], tuple[int, str, str]] = {
    SinSesion: (401, "sin_sesion", "Su sesión terminó. Ingrese de nuevo."),
    CredencialesInvalidas: (
        401,
        "credenciales_invalidas",
        "El documento o la contraseña no coinciden.",
    ),
    AccesoDenegado: (403, "acceso_denegado", "No tiene permiso para hacer esto."),
    DocumentoYaRegistrado: (
        409,
        "documento_registrado",
        "Ya existe una cuenta con ese documento. Puede ingresar o recuperar su contraseña.",
    ),
    YaHayMedico: (409, "ya_hay_medico", "La cuenta del médico ya fue creada."),
    AutorizacionDesactualizada: (
        409,
        "autorizacion_desactualizada",
        "El texto de la autorización cambió. Léalo de nuevo antes de aceptarlo.",
    ),
    MenorDeEdad: (
        422,
        "menor_de_edad",
        "Las cuentas son para mayores de edad. Comuníquese con el consultorio.",
    ),
    EnlaceInvalido: (422, "enlace_invalido", "El enlace ya se usó o venció."),
}


def registrar_traducciones(api: FastAPI) -> None:
    for tipo, (estado, codigo, mensaje) in _FIJOS.items():

        async def fijo(
            _: Request,
            __: Exception,
            estado: int = estado,
            codigo: str = codigo,
            mensaje: str = mensaje,
        ) -> JSONResponse:
            return respuesta_de_error(estado, codigo, mensaje)

        api.add_exception_handler(tipo, fijo)

    async def datos_invalidos(_: Request, error: Exception) -> JSONResponse:
        assert isinstance(error, DatosInvalidos)
        return respuesta_de_error(400, "datos_invalidos", "Revise los datos.", error.campos)

    async def formato_invalido(_: Request, error: Exception) -> JSONResponse:
        assert isinstance(error, RequestValidationError)
        campos = {
            str(problema["loc"][-1]): "Revise este dato"
            for problema in error.errors()
            if problema.get("loc")
        }
        return respuesta_de_error(400, "datos_invalidos", "Revise los datos.", campos)

    async def bloqueado(_: Request, error: Exception) -> JSONResponse:
        assert isinstance(error, IngresoBloqueado)
        return respuesta_de_error(
            429,
            "ingreso_bloqueado",
            "Hubo demasiados intentos. Espere 15 minutos o recupere su contraseña.",
            {"hasta": error.hasta.isoformat()},
        )

    api.add_exception_handler(DatosInvalidos, datos_invalidos)
    api.add_exception_handler(RequestValidationError, formato_invalido)
    api.add_exception_handler(IngresoBloqueado, bloqueado)
