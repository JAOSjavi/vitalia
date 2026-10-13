"""Puertos: lo que los casos de uso necesitan de afuera, sin decir quién lo hace."""

from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol


class BaseDeDatos(Protocol):
    async def responde(self) -> bool:
        """Dice si la base atiende una consulta."""
        ...


class Correo(Protocol):
    async def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None: ...


@dataclass(frozen=True)
class Turno:
    autor: Literal["medico", "asistente"]
    texto: str


class ProveedorIA(Protocol):
    async def leer_pagina(self, imagen: bytes) -> str:
        """Transcribe el texto de la imagen de una página."""
        ...

    def responder(self, instrucciones: str, turnos: Sequence[Turno]) -> AsyncIterator[str]:
        """Entrega la respuesta por partes, a medida que el proveedor la escribe."""
        ...


class Reloj(Protocol):
    def ahora(self) -> datetime: ...
