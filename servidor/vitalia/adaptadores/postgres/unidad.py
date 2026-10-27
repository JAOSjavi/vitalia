"""Unidad de trabajo sobre PostgreSQL: una transacción que le dice a la base quién pregunta."""

import json
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from vitalia.adaptadores.postgres.agenda import AgendaPostgres
from vitalia.adaptadores.postgres.consultorios import ConsultoriosPostgres
from vitalia.adaptadores.postgres.cuentas import CuentasPostgres
from vitalia.adaptadores.postgres.documentos import DocumentosPostgres
from vitalia.adaptadores.postgres.pacientes import PacientesPostgres
from vitalia.dominio.identidad import Identidad
from vitalia.dominio.permisos import MatrizDePermisos


class BitacoraPostgres:
    def __init__(self, conexion: AsyncConnection, identidad: Identidad | None) -> None:
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
        if self._identidad is None:
            raise RuntimeError("Sin sesión, la bitácora se escribe desde las funciones de la base")
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
    def __init__(self, conexion: AsyncConnection, identidad: Identidad | None) -> None:
        self.conexion = conexion
        self.bitacora = BitacoraPostgres(conexion, identidad)
        self.permisos = PermisosPostgres(conexion)
        self.cuentas = CuentasPostgres(conexion)
        self.consultorios = ConsultoriosPostgres(conexion)
        self.agenda = AgendaPostgres(conexion)
        self.pacientes = PacientesPostgres(conexion)
        self.documentos = DocumentosPostgres(conexion)


class UnidadPostgres:
    def __init__(self, motor: AsyncEngine) -> None:
        self._motor = motor

    @asynccontextmanager
    async def abrir(self, identidad: Identidad | None) -> AsyncIterator[TrabajoPostgres]:
        async with self._motor.begin() as conexion:
            if identidad is None:
                # Sin identidad ninguna política deja pasar filas: solo sirven las funciones.
                yield TrabajoPostgres(conexion, None)
                return
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
