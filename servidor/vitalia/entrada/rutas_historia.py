"""Historia clínica del consultorio (diseno/03-api.md, E9)."""

from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field

from vitalia.casos_de_uso.historia_clinica import AtencionParaEscribir, VistaDeAtencion
from vitalia.dominio.historia_clinica import (
    CAMPOS_DE_IDENTIFICACION,
    CAMPOS_DE_LA_ATENCION,
    LISTAS,
    Campo,
)
from vitalia.entrada.sesion import Sesion, casos

rutas = APIRouter(prefix="/api/v1")


class Nota(BaseModel):
    texto: str
    fecha: datetime
    firma_nombre: str
    firma_registro: str | None


class Firma(BaseModel):
    nombre: str
    registro: str | None
    documento: str | None


class Atencion(BaseModel):
    id: UUID
    paciente_id: UUID
    cita_id: UUID | None
    estado: str
    inicio: datetime
    fin: datetime | None
    guardada_en: datetime
    datos: dict[str, Any]
    diagnosticos: list[dict[str, Any]]
    medicamentos: list[dict[str, Any]]
    imc: float | None
    firma: Firma | None
    notas: list[Nota]

    @classmethod
    def de(cls, vista: VistaDeAtencion) -> "Atencion":
        a = vista.atencion
        return cls(
            id=a.id,
            paciente_id=a.paciente_id,
            cita_id=a.cita_id,
            estado=a.estado,
            inicio=a.inicio,
            fin=a.fin,
            guardada_en=a.guardada_en,
            # Los decimales van como número: la pantalla los muestra con coma.
            datos={k: float(v) if isinstance(v, Decimal) else v for k, v in a.datos.items()},
            diagnosticos=[asdict(d) for d in a.diagnosticos],
            medicamentos=[asdict(m) for m in a.medicamentos],
            imc=None if vista.imc is None else float(vista.imc),
            firma=None
            if a.firma_nombre is None
            else Firma(
                nombre=a.firma_nombre, registro=a.firma_registro, documento=a.firma_documento
            ),
            notas=[
                Nota(
                    texto=n.texto,
                    fecha=n.fecha,
                    firma_nombre=n.firma_nombre,
                    firma_registro=n.firma_registro,
                )
                for n in vista.notas
            ],
        )


class Faltantes(BaseModel):
    identificacion: list[str]
    atencion: list[str]


class AtencionParaEscribirRespuesta(BaseModel):
    atencion: Atencion
    identificacion: dict[str, Any]
    faltantes: Faltantes

    @classmethod
    def de(cls, datos: AtencionParaEscribir) -> "AtencionParaEscribirRespuesta":
        return cls(
            atencion=Atencion.de(datos.vista),
            identificacion=dict(datos.identificacion),
            faltantes=Faltantes(
                identificacion=datos.faltantes.identificacion, atencion=datos.faltantes.atencion
            ),
        )


class Apertura(BaseModel):
    cita_id: UUID | None = None


class Abierta(BaseModel):
    id: UUID


class Borrador(BaseModel):
    datos: dict[str, Any] = Field(default_factory=dict)
    diagnosticos: list[dict[str, Any]] | None = None
    medicamentos: list[dict[str, Any]] | None = None


class Guardado(BaseModel):
    guardada_en: datetime


class Cierre(BaseModel):
    contrasena: str = Field(min_length=1, max_length=200)


class Cerrada(BaseModel):
    fin: datetime


class NuevaNota(BaseModel):
    texto: str = Field(max_length=4000)


class Identificacion(BaseModel):
    datos: dict[str, Any]


class Diagnostico(BaseModel):
    codigo: str
    nombre: str


def _campo(campo: Campo) -> dict[str, Any]:
    return {
        "nombre": campo.nombre,
        "clase": campo.clase,
        "obligatorio": campo.obligatorio,
        "lista": campo.lista,
        "minimo": None if campo.minimo is None else float(campo.minimo),
        "maximo": None if campo.maximo is None else float(campo.maximo),
        "unidad": campo.unidad,
        "largo": campo.largo,
    }


@rutas.get("/historia-clinica/formulario")
async def formulario(identidad: Sesion) -> dict[str, Any]:
    """Los campos y las listas de valores, para que las pantallas no los repitan."""
    del identidad
    return {
        "atencion": {k: _campo(c) for k, c in CAMPOS_DE_LA_ATENCION.items()},
        "identificacion": {k: _campo(c) for k, c in CAMPOS_DE_IDENTIFICACION.items()},
        "listas": LISTAS,
    }


@rutas.post("/pacientes/{paciente_id}/atenciones", status_code=status.HTTP_201_CREATED)
async def abrir_atencion(
    paciente_id: UUID, datos: Apertura, identidad: Sesion, request: Request
) -> Abierta:
    atencion_id = await casos(request).atenciones.abrir(identidad, paciente_id, datos.cita_id)
    return Abierta(id=atencion_id)


@rutas.get("/pacientes/{paciente_id}/atenciones")
async def historia_del_paciente(
    paciente_id: UUID, identidad: Sesion, request: Request
) -> list[Atencion]:
    vistas = await casos(request).atenciones.historia_del_paciente(identidad, paciente_id)
    return [Atencion.de(v) for v in vistas]


@rutas.put("/pacientes/{paciente_id}/identificacion", status_code=status.HTTP_204_NO_CONTENT)
async def guardar_identificacion(
    paciente_id: UUID, datos: Identificacion, identidad: Sesion, request: Request
) -> None:
    await casos(request).atenciones.guardar_identificacion(identidad, paciente_id, datos.datos)


@rutas.get("/atenciones/{atencion_id}")
async def ver_atencion(
    atencion_id: UUID, identidad: Sesion, request: Request
) -> AtencionParaEscribirRespuesta:
    datos = await casos(request).atenciones.para_escribir(identidad, atencion_id)
    return AtencionParaEscribirRespuesta.de(datos)


@rutas.patch("/atenciones/{atencion_id}")
async def guardar_borrador(
    atencion_id: UUID, datos: Borrador, identidad: Sesion, request: Request
) -> Guardado:
    guardada_en = await casos(request).atenciones.guardar(
        identidad, atencion_id, datos.datos, datos.diagnosticos, datos.medicamentos
    )
    return Guardado(guardada_en=guardada_en)


@rutas.post("/atenciones/{atencion_id}/cierre")
async def cerrar_atencion(
    atencion_id: UUID, datos: Cierre, identidad: Sesion, request: Request
) -> Cerrada:
    fin = await casos(request).atenciones.cerrar(identidad, atencion_id, datos.contrasena)
    return Cerrada(fin=fin)


@rutas.post("/atenciones/{atencion_id}/notas", status_code=status.HTTP_201_CREATED)
async def agregar_nota(
    atencion_id: UUID, datos: NuevaNota, identidad: Sesion, request: Request
) -> None:
    await casos(request).atenciones.agregar_nota(identidad, atencion_id, datos.texto)


@rutas.get("/cie10")
async def buscar_cie10(identidad: Sesion, request: Request, buscar: str = "") -> list[Diagnostico]:
    encontrados = await casos(request).atenciones.buscar_cie10(identidad, buscar)
    return [Diagnostico(codigo=c, nombre=n) for c, n in encontrados]


@rutas.get("/mi-historia")
async def mi_historia(identidad: Sesion, request: Request) -> list[Atencion]:
    return [Atencion.de(v) for v in await casos(request).atenciones.mi_historia(identidad)]
