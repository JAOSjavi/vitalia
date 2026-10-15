"""Unidad de trabajo sobre PostgreSQL: una transacción que le dice a la base quién pregunta."""

import json
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from vitalia.dominio.identidad import Identidad
from vitalia.dominio.permisos import MatrizDePermisos


class BitacoraPostgres:
    def __init__(self, conexion: AsyncConnection, identidad: Identidad) -> None:
        self._conexion = conexion
        self._identidad = identidad

    async def registrar(
        self,
        accion: str,
        *,
        paciente_id: UUID | None = None,
        objeto: str | None = None,
        detalle: Mapping[str, object] | None = None,
    ) -> None:
        await self._conexion.execute(
            text(
                "INSERT INTO bitacora (usuario_id, rol, paciente_id, accion, objeto, detalle) "
                "VALUES (:usuario, :rol, :paciente, :accion, :objeto, CAST(:detalle AS jsonb))"
            ),
            {
                "usuario": self._identidad.usuario_id,
                "rol": self._identidad.clase,
                "paciente": paciente_id,
                "accion": accion,
                "objeto": objeto,
                "detalle": None if detalle is None else json.dumps(detalle),
            },
        )


class PermisosPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def matriz(self) -> MatrizDePermisos:
        filas = await self._conexion.execute(text("SELECT rol, permiso FROM rol_permiso"))
        return MatrizDePermisos(frozenset((fila.rol, fila.permiso) for fila in filas))


class TrabajoPostgres:
    def __init__(self, conexion: AsyncConnection, identidad: Identidad) -> None:
        self.conexion = conexion
        self.bitacora = BitacoraPostgres(conexion, identidad)
        self.permisos = PermisosPostgres(conexion)


class UnidadPostgres:
    def __init__(self, motor: AsyncEngine) -> None:
        self._motor = motor

    @asynccontextmanager
    async def abrir(self, identidad: Identidad) -> AsyncIterator[TrabajoPostgres]:
        async with self._motor.begin() as conexion:
            # El tercer argumento hace que valgan solo dentro de esta transacción.
            await conexion.execute(
                text(
                    "SELECT set_config('vitalia.identidad', :clase, true), "
                    "set_config('vitalia.usuario', :usuario, true)"
                ),
                {
                    "clase": identidad.clase,
                    "usuario": "" if identidad.usuario_id is None else str(identidad.usuario_id),
                },
            )
            yield TrabajoPostgres(conexion, identidad)
