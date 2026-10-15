"""Puertos: lo que los casos de uso necesitan de afuera, sin decir quién lo hace."""

from collections.abc import AsyncIterator, Mapping, Sequence
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, Protocol
from uuid import UUID

from vitalia.dominio.cuentas import DatosDelMedico, DatosDelPaciente, Documento
from vitalia.dominio.identidad import Identidad, Rol
from vitalia.dominio.ingreso import Intentos
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


@dataclass(frozen=True)
class Credencial:
    """Lo que la base entrega para verificar un ingreso. Sin cuenta, usuario_id es None."""

    usuario_id: UUID | None
    hash_contrasena: str | None
    rol: Rol | None
    activo: bool
    intentos: Intentos
    intentos_del_equipo: Intentos


@dataclass(frozen=True)
class PuntoDelTexto:
    titulo: str
    texto: str
    resaltado: bool = False


@dataclass(frozen=True)
class TextoDeAutorizacion:
    id: UUID
    tipo: Literal["datos", "ia"]
    version: int
    puntos: Sequence[PuntoDelTexto]
    contenido: str
    vigente_desde: datetime


@dataclass(frozen=True)
class Cuenta:
    usuario_id: UUID
    rol: Rol
    documento: Documento
    nombres: str
    apellidos: str
    correo: str | None


class Cuentas(Protocol):
    """Lo de las cuentas. Lo que ocurre sin sesión pasa por funciones de la base."""

    async def buscar_credencial(
        self, documento: Documento, resumen_de_la_cuenta: str, origen: str
    ) -> Credencial: ...

    async def guardar_intentos(
        self, resumen_de_la_cuenta: str | None, origen: str, intentos: Intentos
    ) -> None:
        """Sin resumen de cuenta, guarda el tope del equipo. Sin fallos, borra la fila."""
        ...

    async def anotar_sin_sesion(self, usuario_id: UUID | None, accion: str) -> None: ...

    async def abrir_sesion(
        self, usuario_id: UUID, huella: str, ahora: datetime, vence: datetime
    ) -> None: ...

    async def sesion_vigente(self, huella: str, ahora: datetime) -> Identidad | None: ...

    async def anular_sesion(self, huella: str, ahora: datetime) -> None: ...

    async def texto_vigente(self, tipo: Literal["datos", "ia"]) -> TextoDeAutorizacion: ...

    async def registrar_paciente(
        self,
        datos: DatosDelPaciente,
        hash_contrasena: str,
        texto_datos: UUID,
        texto_ia: UUID | None,
        hoy: date,
    ) -> UUID:
        """Lanza DocumentoYaRegistrado, MenorDeEdad o AutorizacionDesactualizada."""
        ...

    async def crear_enlace_de_puesta_en_marcha(self, huella: str, vence: datetime) -> None:
        """Lanza YaHayMedico."""
        ...

    async def usar_enlace_de_puesta_en_marcha(
        self, huella: str, ahora: datetime, datos: DatosDelMedico, hash_contrasena: str
    ) -> UUID:
        """Lanza EnlaceInvalido, YaHayMedico o DocumentoYaRegistrado."""
        ...

    async def cuenta(self, usuario_id: UUID) -> Cuenta: ...


@dataclass(frozen=True)
class ConsultorioPublico:
    nombre: str | None
    telefono: str | None
    medico: str | None


@dataclass(frozen=True)
class DatosDelConsultorio:
    nombre: str | None
    direccion: str | None
    telefono: str | None
    correo: str | None
    medico_nombres: str
    medico_apellidos: str
    registro_profesional: str | None


class Consultorios(Protocol):
    async def publico(self) -> ConsultorioPublico: ...

    async def datos(self) -> DatosDelConsultorio: ...

    async def guardar(self, medico_id: UUID, datos: DatosDelConsultorio) -> None: ...


class Trabajo(Protocol):
    """Una transacción abierta a nombre de alguien. Sus repositorios la comparten."""

    @property
    def bitacora(self) -> Bitacora: ...

    @property
    def permisos(self) -> Permisos: ...

    @property
    def cuentas(self) -> Cuentas: ...

    @property
    def consultorios(self) -> Consultorios: ...


class UnidadDeTrabajo(Protocol):
    def abrir(self, identidad: Identidad | None) -> AbstractAsyncContextManager[Trabajo]:
        """Abre la transacción y le dice a la base quién es; sin identidad no ve ninguna fila.

        Confirma al salir y deshace si algo falla.
        """
        ...


class Contrasenas(Protocol):
    async def cifrar(self, contrasena: str) -> str: ...

    async def verificar(self, contrasena: str, hash_contrasena: str | None) -> bool:
        """Sin hash tarda lo mismo y responde que no: así no se sabe si la cuenta existe."""
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
