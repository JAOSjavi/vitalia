"""Puertos: lo que los casos de uso necesitan de afuera, sin decir quién lo hace."""

from collections.abc import AsyncIterator, Mapping, Sequence
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol
from uuid import UUID

from vitalia.dominio.identidad import Identidad
from vitalia.dominio.permisos import MatrizDePermisos


class BaseDeDatos(Protocol):
    async def responde(self) -> bool:
        """Dice si la base atiende una consulta."""
        ...


class Bitacora(Protocol):
    async def registrar(
        self,
        accion: str,
        *,
        paciente_id: UUID | None = None,
        objeto: str | None = None,
        detalle: Mapping[str, object] | None = None,
    ) -> None:
        """Anota quién hizo qué. El detalle nunca lleva contenido clínico."""
        ...


class Permisos(Protocol):
    async def matriz(self) -> MatrizDePermisos: ...


class Trabajo(Protocol):
    """Una transacción abierta a nombre de alguien. Sus repositorios la comparten."""

    @property
    def bitacora(self) -> Bitacora: ...

    @property
    def permisos(self) -> Permisos: ...


class UnidadDeTrabajo(Protocol):
    def abrir(self, identidad: Identidad) -> AbstractAsyncContextManager[Trabajo]:
        """Abre la transacción y le dice a la base quién es. Confirma al salir; deshace si falla."""
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
