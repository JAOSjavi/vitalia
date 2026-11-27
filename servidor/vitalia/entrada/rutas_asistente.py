"""Preguntas al asistente (diseno/03-api.md, E6).

La respuesta llega por partes, una línea JSON por evento (application/x-ndjson):
  {"tipo": "texto", "texto": "..."}           mientras el modelo escribe
  {"tipo": "fin", "origenes": [...], ...}     al terminar, con las citas comprobadas
  {"tipo": "error", "codigo": ..., ...}       si el proveedor falla a mitad de camino
Lo que falla antes de llamar al proveedor responde con su estado de siempre (422, 429...).
"""

import json
import logging
from collections.abc import AsyncIterator
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from vitalia.casos_de_uso.preguntar_al_asistente import Cierre, PreguntaLista
from vitalia.casos_de_uso.puertos import ProveedorNoDisponible, Turno
from vitalia.entrada.sesion import Sesion, casos

rutas = APIRouter(prefix="/api/v1")

_registro = logging.getLogger(__name__)


class TurnoAnterior(BaseModel):
    autor: Literal["medico", "asistente"]
    texto: str


class Pregunta(BaseModel):
    pregunta: str = Field(max_length=2000)
    # La conversación no se guarda en la base: la pantalla la reenvía en cada pregunta.
    conversacion: Annotated[list[TurnoAnterior], Field(max_length=40)] = []


def _linea(evento: dict[str, object]) -> bytes:
    return (json.dumps(evento, ensure_ascii=False) + "\n").encode()


def _fin(cierre: Cierre) -> dict[str, object]:
    return {
        "tipo": "fin",
        "origenes": [
            {
                "etiqueta": o.etiqueta,
                "documento_id": str(o.documento_id),
                "documento": o.documento,
                "pagina": o.pagina,
                "frase": o.frase,
                "verificado": o.verificado,
            }
            for o in cierre.origenes
        ],
        "consultado": [
            {
                "documento_id": str(c.documento_id),
                "documento": c.documento,
                "fecha_documento": c.fecha_documento.isoformat(),
                "paginas": list(c.paginas),
            }
            for c in cierre.consultado
        ],
        "aviso": cierre.aviso,
    }


@rutas.post("/pacientes/{paciente_id}/asistente/preguntas")
async def preguntar(
    paciente_id: UUID, datos: Pregunta, identidad: Sesion, request: Request
) -> StreamingResponse:
    caso = casos(request).preguntar_al_asistente
    lista: PreguntaLista = await caso.preparar(
        identidad,
        paciente_id,
        datos.pregunta,
        [Turno(t.autor, t.texto) for t in datos.conversacion],
    )

    async def eventos() -> AsyncIterator[bytes]:
        try:
            async for evento in caso.responder(lista):
                if isinstance(evento, Cierre):
                    yield _linea(_fin(evento))
                else:
                    yield _linea({"tipo": "texto", "texto": evento})
        except ProveedorNoDisponible as error:
            _registro.warning("El proveedor de IA no respondió: %s", type(error).__name__)
            yield _linea(
                {
                    "tipo": "error",
                    "codigo": "proveedor_no_disponible",
                    "mensaje": "El asistente no está disponible en este momento. "
                    "Los documentos siguen disponibles en el visor.",
                }
            )

    return StreamingResponse(eventos(), media_type="application/x-ndjson")
