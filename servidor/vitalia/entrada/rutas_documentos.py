"""Documentos del paciente (diseno/03-api.md, E5)."""

from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, File, Form, Request, UploadFile, status
from pydantic import BaseModel

from vitalia.casos_de_uso.puertos import DocumentoSubido
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.documentos import (
    TAMANO_MAXIMO,
    TIPOS,
    ArchivoRecibido,
    EstadoDeLectura,
    Formato,
    TipoDeDocumento,
)
from vitalia.entrada.sesion import Sesion, casos

rutas = APIRouter(prefix="/api/v1")


class Documento(BaseModel):
    id: UUID
    nombre: str
    fecha_documento: date
    tipo: TipoDeDocumento
    formato: Formato
    tamano: int
    estado_lectura: EstadoDeLectura
    paginas: int | None
    subido_en: datetime


def _documento(documento: DocumentoSubido) -> Documento:
    return Documento(**documento.__dict__)


@rutas.post("/documentos", status_code=status.HTTP_201_CREATED)
async def subir_documento(
    identidad: Sesion,
    request: Request,
    archivo: Annotated[UploadFile, File()],
    nombre: Annotated[str, Form(max_length=200)],
    fecha_documento: Annotated[date, Form()],
    tipo: Annotated[str, Form()],
) -> Documento:
    """Un archivo por petición: la pantalla sube varios en paralelo y muestra cada resultado."""
    # Se lee un byte de más para saber si se pasa del tope sin cargar un archivo enorme.
    contenido = await archivo.read(TAMANO_MAXIMO + 1)
    if tipo not in TIPOS:
        raise DatosInvalidos({"tipo": "Elija el tipo de documento"})
    recibido = ArchivoRecibido(
        nombre=nombre,
        fecha_documento=fecha_documento,
        tipo=tipo,  # se revisó arriba que está en TIPOS
        contenido=contenido,
    )
    documento = await casos(request).subir_documento.ejecutar(identidad, recibido)
    return _documento(documento)


@rutas.get("/documentos")
async def mis_documentos(identidad: Sesion, request: Request) -> list[Documento]:
    documentos = await casos(request).ver_mis_documentos.ejecutar(identidad)
    return [_documento(d) for d in documentos]
