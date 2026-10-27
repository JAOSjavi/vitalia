"""Documentos del paciente (diseno/03-api.md, E5)."""

from datetime import date, datetime
from typing import Annotated
from urllib.parse import quote
from uuid import UUID

from fastapi import APIRouter, File, Form, Request, Response, UploadFile, status
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
from vitalia.entrada.rutas_citas import Cita
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


_TIPOS_DE_ARCHIVO = {"pdf": "application/pdf", "jpg": "image/jpeg", "png": "image/png"}


@rutas.get("/documentos/{documento_id}/archivo")
async def abrir_documento(documento_id: UUID, identidad: Sesion, request: Request) -> Response:
    """El archivo, para verlo en el navegador. La página va en la dirección: #page=2."""
    archivo = await casos(request).abrir_documento.ejecutar(identidad, documento_id)
    nombre = quote(f"{archivo.nombre}.{archivo.formato}")
    return Response(
        archivo.contenido,
        media_type=_TIPOS_DE_ARCHIVO[archivo.formato],
        headers={
            "Content-Disposition": f"inline; filename*=UTF-8''{nombre}",
            # El navegador no adivina otro tipo: un archivo nunca se vuelve una página.
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'none'; img-src 'self'; "
            "style-src 'unsafe-inline'",
        },
    )


@rutas.delete("/documentos/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_documento(documento_id: UUID, identidad: Sesion, request: Request) -> None:
    await casos(request).eliminar_documento.ejecutar(identidad, documento_id)


class ListaDeDocumentos(BaseModel):
    documentos: list[Documento]
    ia_autorizada: bool


@rutas.get("/documentos")
async def mis_documentos(identidad: Sesion, request: Request) -> ListaDeDocumentos:
    mios = await casos(request).ver_mis_documentos.ejecutar(identidad)
    return ListaDeDocumentos(
        documentos=[_documento(d) for d in mios.documentos], ia_autorizada=mios.ia_autorizada
    )


class DatosDelPaciente(BaseModel):
    id: UUID
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    fecha_nacimiento: date
    telefono: str
    correo: str | None
    activo: bool


class Ficha(BaseModel):
    paciente: DatosDelPaciente
    ia_autorizada: bool
    citas: list[Cita]
    documentos: list[Documento]


@rutas.get("/pacientes/{paciente_id}")
async def ficha_del_paciente(paciente_id: UUID, identidad: Sesion, request: Request) -> Ficha:
    """M-06. Datos, citas, documentos y si el asistente se puede usar (HU-025)."""
    ficha = await casos(request).ver_ficha_del_paciente.ejecutar(identidad, paciente_id)
    p = ficha.paciente
    return Ficha(
        paciente=DatosDelPaciente(
            id=p.id,
            nombres=p.nombres,
            apellidos=p.apellidos,
            tipo_documento=p.documento.tipo,
            numero_documento=p.documento.numero,
            fecha_nacimiento=p.fecha_nacimiento,
            telefono=p.telefono,
            correo=p.correo,
            activo=p.activo,
        ),
        ia_autorizada=ficha.ia_autorizada,
        citas=[Cita.de(c) for c in ficha.citas],
        documentos=[_documento(d) for d in ficha.documentos],
    )
