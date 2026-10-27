"""Traduce los errores del dominio a respuestas de la API, siempre con la misma forma.

{"codigo": ..., "mensaje": ..., "detalle": ...} (diseno/03-api.md, sección 1).
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from vitalia.casos_de_uso.puertos import ProveedorNoDisponible
from vitalia.dominio.agenda import (
    AgendaNoDisponible,
    CitaNoModificable,
    CitaRepetida,
    EspacioNoDisponible,
    EspacioOcupado,
    FaltaAnticipacion,
    FueraDeHorario,
)
from vitalia.dominio.asistente import SinFragmentos, TopeDeConsultas
from vitalia.dominio.cuentas import (
    AutorizacionDesactualizada,
    DatosInvalidos,
    DocumentoYaRegistrado,
    EnlaceInvalido,
    MenorDeEdad,
    YaHayMedico,
)
from vitalia.dominio.documentos import DocumentoRepetido
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.fragmentos import IANoAutorizada
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
    NoEncontrado: (404, "no_encontrado", "No se encontró lo que busca."),
    AgendaNoDisponible: (
        422,
        "agenda_no_disponible",
        "La agenda todavía no está disponible. Comuníquese con el consultorio.",
    ),
    EspacioNoDisponible: (
        422,
        "espacio_no_disponible",
        "Esa hora no está disponible. Elija una de las que se ofrecen.",
    ),
    FueraDeHorario: (
        409,
        "fuera_de_horario",
        "Esa hora está por fuera de su horario de atención. Confirme si quiere darla igual.",
    ),
    CitaRepetida: (
        409,
        "cita_repetida",
        "Ya tiene una cita futura de este tipo. Confirme si quiere agendar otra.",
    ),
    CitaNoModificable: (409, "cita_no_modificable", "Esta cita ya no se puede mover ni cancelar."),
    IANoAutorizada: (
        422,
        "ia_no_autorizada",
        "El paciente no ha autorizado el uso de inteligencia artificial con sus datos.",
    ),
    SinFragmentos: (
        422,
        "sin_documentos_indexados",
        "El paciente todavía no tiene documentos listos para el asistente.",
    ),
    ProveedorNoDisponible: (
        503,
        "proveedor_no_disponible",
        "El asistente no está disponible en este momento. "
        "Los documentos siguen disponibles en el visor.",
    ),
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

    async def espacio_ocupado(_: Request, error: Exception) -> JSONResponse:
        assert isinstance(error, EspacioOcupado)
        return respuesta_de_error(
            409,
            "espacio_ocupado",
            "Alguien tomó ese espacio mientras usted elegía. Estos son los más cercanos.",
            {"alternativas": [inicio.isoformat() for inicio in error.alternativas]},
        )

    async def falta_anticipacion(_: Request, error: Exception) -> JSONResponse:
        assert isinstance(error, FaltaAnticipacion)
        return respuesta_de_error(
            422,
            "falta_anticipacion",
            f"Faltan menos de {error.horas} horas. Para moverla o cancelarla, "
            "llame al consultorio.",
            {"horas": error.horas},
        )

    async def documento_repetido(_: Request, error: Exception) -> JSONResponse:
        assert isinstance(error, DocumentoRepetido)
        return respuesta_de_error(
            409,
            "documento_repetido",
            "Ese archivo ya está en sus documentos.",
            {"documento_id": str(error.documento_id)},
        )

    async def tope_de_consultas(_: Request, error: Exception) -> JSONResponse:
        assert isinstance(error, TopeDeConsultas)
        return respuesta_de_error(
            429,
            "tope_de_consultas",
            f"Llegó al máximo de {error.tope} preguntas por hora. Intente más tarde.",
            {"tope": error.tope},
        )

    api.add_exception_handler(TopeDeConsultas, tope_de_consultas)
    api.add_exception_handler(DocumentoRepetido, documento_repetido)
    api.add_exception_handler(EspacioOcupado, espacio_ocupado)
    api.add_exception_handler(FaltaAnticipacion, falta_anticipacion)
    api.add_exception_handler(DatosInvalidos, datos_invalidos)
    api.add_exception_handler(RequestValidationError, formato_invalido)
    api.add_exception_handler(IngresoBloqueado, bloqueado)
