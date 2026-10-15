"""Horario, tipos de cita y citas en PostgreSQL."""

from collections.abc import Sequence
from datetime import datetime
from typing import Any, Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from vitalia.adaptadores.postgres.errores import traducir_errores
from vitalia.casos_de_uso.puertos import Cita
from vitalia.dominio.agenda import EstadoDeCita, Franja, Intervalo, TipoDeCita

# El último motivo de cada cita sale de su historial de cambios.
_CITAS = """
    SELECT c.id, c.paciente_id, p.nombres || ' ' || p.apellidos AS paciente,
           c.tipo_cita_id, t.nombre AS tipo, c.inicio, c.fin, c.estado, c.fuera_de_horario,
           (SELECT motivo FROM cambios_cita m
            WHERE m.cita_id = c.id AND m.motivo IS NOT NULL
            ORDER BY m.fecha DESC LIMIT 1) AS motivo
    FROM citas c
    JOIN pacientes p ON p.id = c.paciente_id
    JOIN tipos_cita t ON t.id = c.tipo_cita_id
"""


def _cita(fila: Any) -> Cita:
    return Cita(
        id=fila.id,
        paciente_id=fila.paciente_id,
        paciente=fila.paciente,
        tipo_id=fila.tipo_cita_id,
        tipo=fila.tipo,
        inicio=fila.inicio,
        fin=fila.fin,
        estado=cast(EstadoDeCita, fila.estado),
        fuera_de_horario=fila.fuera_de_horario,
        motivo=fila.motivo,
    )


def _tipo(fila: Any) -> TipoDeCita:
    return TipoDeCita(fila.id, fila.nombre, fila.duracion_minutos, fila.activo)


class AgendaPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def franjas(self) -> list[Franja]:
        filas = await self._conexion.execute(
            text(
                "SELECT dia_semana, hora_inicio, hora_fin FROM franjas_horario "
                "ORDER BY dia_semana, hora_inicio"
            )
        )
        return [Franja(f.dia_semana, f.hora_inicio, f.hora_fin) for f in filas]

    async def reemplazar_franjas(self, franjas: Sequence[Franja]) -> None:
        await self._conexion.execute(text("DELETE FROM franjas_horario"))
        if franjas:
            await self._conexion.execute(
                text(
                    "INSERT INTO franjas_horario (dia_semana, hora_inicio, hora_fin) "
                    "VALUES (:dia, :inicio, :fin)"
                ),
                [{"dia": f.dia_semana, "inicio": f.inicio, "fin": f.fin} for f in franjas],
            )

    async def tipos(self, solo_activos: bool) -> list[TipoDeCita]:
        filas = await self._conexion.execute(
            text(
                "SELECT id, nombre, duracion_minutos, activo FROM tipos_cita "
                "WHERE activo OR NOT :solo_activos ORDER BY nombre"
            ),
            {"solo_activos": solo_activos},
        )
        return [_tipo(f) for f in filas]

    async def tipo(self, tipo_id: UUID) -> TipoDeCita | None:
        fila = (
            await self._conexion.execute(
                text("SELECT id, nombre, duracion_minutos, activo FROM tipos_cita WHERE id = :id"),
                {"id": tipo_id},
            )
        ).one_or_none()
        return _tipo(fila) if fila else None

    async def crear_tipo(self, nombre: str, duracion_minutos: int) -> TipoDeCita:
        fila = (
            await self._conexion.execute(
                text(
                    "INSERT INTO tipos_cita (nombre, duracion_minutos) VALUES (:nombre, :duracion) "
                    "RETURNING id, nombre, duracion_minutos, activo"
                ),
                {"nombre": nombre, "duracion": duracion_minutos},
            )
        ).one()
        return _tipo(fila)

    async def guardar_tipo(self, tipo: TipoDeCita) -> None:
        await self._conexion.execute(
            text(
                "UPDATE tipos_cita SET nombre = :nombre, duracion_minutos = :duracion, "
                "activo = :activo WHERE id = :id"
            ),
            {
                "id": tipo.id,
                "nombre": tipo.nombre,
                "duracion": tipo.duracion_minutos,
                "activo": tipo.activo,
            },
        )

    async def ocupados(self, desde: datetime, hasta: datetime) -> list[tuple[UUID, Intervalo]]:
        filas = await self._conexion.execute(
            text("SELECT cita_id, inicio, fin FROM tiempos_ocupados(:desde, :hasta)"),
            {"desde": desde, "hasta": hasta},
        )
        return [(f.cita_id, Intervalo(f.inicio, f.fin)) for f in filas]

    async def citas(
        self,
        *,
        desde: datetime | None = None,
        hasta: datetime | None = None,
        paciente_id: UUID | None = None,
        estado: EstadoDeCita | None = None,
        limite: int | None = None,
    ) -> list[Cita]:
        condiciones = []
        valores: dict[str, Any] = {}
        # "desde" toma las que todavía no terminan: una cita en curso sigue siendo de hoy.
        if desde is not None:
            condiciones.append("c.fin > :desde")
            valores["desde"] = desde
        if hasta is not None:
            condiciones.append("c.inicio < :hasta")
            valores["hasta"] = hasta
        if paciente_id is not None:
            condiciones.append("c.paciente_id = :paciente")
            valores["paciente"] = paciente_id
        if estado is not None:
            condiciones.append("c.estado = :estado")
            valores["estado"] = estado
        donde = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""
        hasta_cuantas = f"LIMIT {int(limite)}" if limite else ""
        filas = await self._conexion.execute(
            text(f"{_CITAS} {donde} ORDER BY c.inicio {hasta_cuantas}"), valores
        )
        return [_cita(f) for f in filas]

    async def cita(self, cita_id: UUID) -> Cita | None:
        fila = (
            await self._conexion.execute(text(f"{_CITAS} WHERE c.id = :id"), {"id": cita_id})
        ).one_or_none()
        return _cita(fila) if fila else None

    async def crear_cita(
        self,
        paciente_id: UUID,
        tipo_id: UUID,
        intervalo: Intervalo,
        creada_por: UUID,
        fuera_de_horario: bool,
    ) -> UUID:
        with traducir_errores():
            cita_id: UUID = await self._conexion.scalar(
                text(
                    "INSERT INTO citas "
                    "(paciente_id, tipo_cita_id, inicio, fin, creada_por, fuera_de_horario) "
                    "VALUES (:paciente, :tipo, :inicio, :fin, :creada_por, :fuera) RETURNING id"
                ),
                {
                    "paciente": paciente_id,
                    "tipo": tipo_id,
                    "inicio": intervalo.inicio,
                    "fin": intervalo.fin,
                    "creada_por": creada_por,
                    "fuera": fuera_de_horario,
                },
            )
        return cita_id

    async def mover_cita(self, cita_id: UUID, intervalo: Intervalo, fuera_de_horario: bool) -> None:
        with traducir_errores():
            await self._conexion.execute(
                text(
                    "UPDATE citas SET inicio = :inicio, fin = :fin, fuera_de_horario = :fuera "
                    "WHERE id = :id"
                ),
                {
                    "id": cita_id,
                    "inicio": intervalo.inicio,
                    "fin": intervalo.fin,
                    "fuera": fuera_de_horario,
                },
            )

    async def cancelar_cita(self, cita_id: UUID) -> None:
        await self._conexion.execute(
            text("UPDATE citas SET estado = 'cancelada' WHERE id = :id"), {"id": cita_id}
        )

    async def anotar_cambio(
        self,
        cita_id: UUID,
        usuario_id: UUID,
        tipo: Literal["creada", "movida", "cancelada"],
        inicio_anterior: datetime | None = None,
        inicio_nuevo: datetime | None = None,
        motivo: str | None = None,
    ) -> None:
        await self._conexion.execute(
            text(
                "INSERT INTO cambios_cita "
                "(cita_id, usuario_id, tipo, inicio_anterior, inicio_nuevo, motivo) "
                "VALUES (:cita, :usuario, :tipo, :anterior, :nuevo, :motivo)"
            ),
            {
                "cita": cita_id,
                "usuario": usuario_id,
                "tipo": tipo,
                "anterior": inicio_anterior,
                "nuevo": inicio_nuevo,
                "motivo": motivo,
            },
        )

    async def paciente_de_la_sesion(self) -> UUID | None:
        paciente_id: UUID | None = await self._conexion.scalar(text("SELECT paciente_actual()"))
        return paciente_id
