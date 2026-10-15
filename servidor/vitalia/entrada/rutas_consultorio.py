"""Datos del consultorio (diseno/03-api.md, E1 y E2)."""

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field

from vitalia.casos_de_uso.puertos import DatosDelConsultorio
from vitalia.entrada.sesion import Sesion, casos

rutas = APIRouter(prefix="/api/v1")


class ConsultorioPublico(BaseModel):
    nombre: str | None
    telefono: str | None
    medico: str | None


class Consultorio(BaseModel):
    nombre: str | None = Field(max_length=120)
    direccion: str | None = Field(max_length=200)
    telefono: str | None = Field(max_length=30)
    correo: str | None = Field(max_length=120)
    medico_nombres: str = Field(max_length=120)
    medico_apellidos: str = Field(max_length=120)
    registro_profesional: str | None = Field(max_length=40)


@rutas.get("/consultorio/publico")
async def consultorio_publico(request: Request) -> ConsultorioPublico:
    """Lo que se muestra antes de ingresar: nombre, teléfono y médico."""
    datos = await casos(request).ver_consultorio.publico()
    return ConsultorioPublico(nombre=datos.nombre, telefono=datos.telefono, medico=datos.medico)


@rutas.get("/consultorio")
async def ver_consultorio(identidad: Sesion, request: Request) -> Consultorio:
    datos = await casos(request).ver_consultorio.ejecutar(identidad)
    return Consultorio(**datos.__dict__)


@rutas.put("/consultorio", status_code=status.HTTP_204_NO_CONTENT)
async def editar_consultorio(datos: Consultorio, identidad: Sesion, request: Request) -> None:
    await casos(request).editar_consultorio.ejecutar(
        identidad, DatosDelConsultorio(**datos.model_dump())
    )
