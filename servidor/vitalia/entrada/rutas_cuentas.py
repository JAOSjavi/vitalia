"""Cuentas e ingreso (diseno/03-api.md, E1)."""

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel, Field

from vitalia.casos_de_uso.ingresar import SesionNueva
from vitalia.dominio.cuentas import DatosDelMedico, DatosDelPaciente, Documento, TipoDocumento
from vitalia.dominio.identidad import Rol
from vitalia.entrada.sesion import (
    Sesion,
    casos,
    ficha_de_la_sesion,
    origen,
    poner_cookie,
    quitar_cookie,
)

rutas = APIRouter(prefix="/api/v1")

Texto = Field(max_length=120)


class RespuestaDeSesion(BaseModel):
    rol: Rol
    vence: datetime


class SolicitudDeIngreso(BaseModel):
    tipo_documento: TipoDocumento
    numero_documento: str = Field(max_length=30)
    contrasena: str = Field(max_length=200)


class SolicitudDeRegistro(BaseModel):
    tipo_documento: TipoDocumento
    numero_documento: str = Field(max_length=30)
    nombres: str = Texto
    apellidos: str = Texto
    fecha_nacimiento: date
    telefono: str = Field(max_length=30)
    correo: str = Texto
    contrasena: str = Field(max_length=200)
    texto_datos: UUID
    # Vacío si la persona no marcó la casilla de inteligencia artificial.
    texto_ia: UUID | None = None


class SolicitudDePuestaEnMarcha(BaseModel):
    enlace: str = Field(max_length=100)
    tipo_documento: TipoDocumento
    numero_documento: str = Field(max_length=30)
    nombres: str = Texto
    apellidos: str = Texto
    correo: str = Texto
    contrasena: str = Field(max_length=200)


class MiCuenta(BaseModel):
    usuario_id: UUID
    rol: Rol
    tipo_documento: TipoDocumento
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str | None


class Punto(BaseModel):
    titulo: str
    texto: str
    resaltado: bool


class TextoDeAutorizacion(BaseModel):
    id: UUID
    tipo: Literal["datos", "ia"]
    version: int
    vigente_desde: datetime
    puntos: list[Punto]
    contenido: str


def _con_sesion(respuesta: Response, sesion: SesionNueva) -> RespuestaDeSesion:
    poner_cookie(respuesta, sesion)
    return RespuestaDeSesion(rol=sesion.rol, vence=sesion.vence)


@rutas.post("/sesion")
async def ingresar(
    solicitud: SolicitudDeIngreso, request: Request, respuesta: Response
) -> RespuestaDeSesion:
    sesion = await casos(request).ingresar.ejecutar(
        Documento(solicitud.tipo_documento, solicitud.numero_documento),
        solicitud.contrasena,
        origen(request),
    )
    return _con_sesion(respuesta, sesion)


@rutas.delete("/sesion", status_code=status.HTTP_204_NO_CONTENT)
async def cerrar_sesion(identidad: Sesion, request: Request, respuesta: Response) -> None:
    await casos(request).cerrar_sesion.ejecutar(identidad, ficha_de_la_sesion(request))
    quitar_cookie(respuesta)


@rutas.post("/cuentas/registro", status_code=status.HTTP_201_CREATED)
async def registrarse(
    solicitud: SolicitudDeRegistro, request: Request, respuesta: Response
) -> RespuestaDeSesion:
    datos = DatosDelPaciente(
        documento=Documento(solicitud.tipo_documento, solicitud.numero_documento),
        nombres=solicitud.nombres,
        apellidos=solicitud.apellidos,
        fecha_nacimiento=solicitud.fecha_nacimiento,
        telefono=solicitud.telefono,
        correo=solicitud.correo,
    )
    sesion = await casos(request).registrar_paciente.ejecutar(
        datos, solicitud.contrasena, solicitud.texto_datos, solicitud.texto_ia
    )
    return _con_sesion(respuesta, sesion)


@rutas.post("/puesta-en-marcha", status_code=status.HTTP_201_CREATED)
async def poner_en_marcha(
    solicitud: SolicitudDePuestaEnMarcha, request: Request, respuesta: Response
) -> RespuestaDeSesion:
    datos = DatosDelMedico(
        documento=Documento(solicitud.tipo_documento, solicitud.numero_documento),
        nombres=solicitud.nombres,
        apellidos=solicitud.apellidos,
        correo=solicitud.correo,
    )
    sesion = await casos(request).poner_en_marcha.ejecutar(
        solicitud.enlace, datos, solicitud.contrasena
    )
    return _con_sesion(respuesta, sesion)


@rutas.get("/yo")
async def yo(identidad: Sesion, request: Request) -> MiCuenta:
    cuenta = await casos(request).ver_mi_cuenta.ejecutar(identidad)
    return MiCuenta(
        usuario_id=cuenta.usuario_id,
        rol=cuenta.rol,
        tipo_documento=cuenta.documento.tipo,
        numero_documento=cuenta.documento.numero,
        nombres=cuenta.nombres,
        apellidos=cuenta.apellidos,
        correo=cuenta.correo,
    )


@rutas.get("/autorizaciones/texto")
async def texto_de_autorizacion(
    tipo: Literal["datos", "ia"], request: Request
) -> TextoDeAutorizacion:
    texto, consultorio = await casos(request).ver_texto_de_autorizacion.ejecutar(tipo)
    responsable = consultorio.nombre or "El consultorio"

    def con_responsable(valor: str) -> str:
        return valor.replace("{consultorio}", responsable)

    return TextoDeAutorizacion(
        id=texto.id,
        tipo=texto.tipo,
        version=texto.version,
        vigente_desde=texto.vigente_desde,
        puntos=[
            Punto(titulo=p.titulo, texto=con_responsable(p.texto), resaltado=p.resaltado)
            for p in texto.puntos
        ],
        contenido=con_responsable(texto.contenido),
    )
