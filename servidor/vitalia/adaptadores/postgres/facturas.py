"""Facturas emitidas en PostgreSQL. Solo se leen y se agregan: lo emitido no cambia."""

from collections.abc import Sequence
from typing import Any, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from vitalia.casos_de_uso.puertos import FacturaNueva
from vitalia.dominio.facturas import Ambiente, Factura, MedioDePago

_COLUMNAS = (
    "id, cita_id, paciente_id, concepto, valor, medio_pago, numero, cufe, "
    "enlace_publico, enlace_qr, ambiente, emitida_en"
)


def _factura(fila: Any) -> Factura:
    return Factura(
        id=fila.id,
        cita_id=fila.cita_id,
        paciente_id=fila.paciente_id,
        concepto=fila.concepto,
        valor=fila.valor,
        medio=cast(MedioDePago, fila.medio_pago),
        numero=fila.numero,
        cufe=fila.cufe,
        enlace_publico=fila.enlace_publico,
        enlace_qr=fila.enlace_qr,
        ambiente=cast(Ambiente, fila.ambiente),
        emitida_en=fila.emitida_en,
    )


class FacturasPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def de_la_cita(self, cita_id: UUID) -> Factura | None:
        fila = (
            await self._conexion.execute(
                text(f"SELECT {_COLUMNAS} FROM facturas WHERE cita_id = :cita"), {"cita": cita_id}
            )
        ).one_or_none()
        return _factura(fila) if fila else None

    async def de_las_citas(self, citas: Sequence[UUID]) -> dict[UUID, Factura]:
        if not citas:
            return {}
        filas = await self._conexion.execute(
            text(f"SELECT {_COLUMNAS} FROM facturas WHERE cita_id = ANY(:citas)"),
            {"citas": list(citas)},
        )
        return {f.cita_id: _factura(f) for f in filas}

    async def todas(self) -> list[Factura]:
        filas = await self._conexion.execute(
            text(f"SELECT {_COLUMNAS} FROM facturas ORDER BY emitida_en DESC")
        )
        return [_factura(f) for f in filas]

    async def guardar(self, nueva: FacturaNueva) -> Factura:
        # Dos clics seguidos llegan con la misma factura de Factus: se queda la primera.
        fila = (
            await self._conexion.execute(
                text(
                    "INSERT INTO facturas (cita_id, paciente_id, emitida_por, concepto, valor, "
                    "medio_pago, numero, cufe, enlace_publico, enlace_qr, ambiente) "
                    "VALUES (:cita, :paciente, :emitida_por, :concepto, :valor, :medio, :numero, "
                    ":cufe, :publico, :qr, :ambiente) "
                    f"ON CONFLICT (cita_id) DO NOTHING RETURNING {_COLUMNAS}"
                ),
                {
                    "cita": nueva.cita_id,
                    "paciente": nueva.paciente_id,
                    "emitida_por": nueva.emitida_por,
                    "concepto": nueva.concepto,
                    "valor": nueva.valor,
                    "medio": nueva.medio,
                    "numero": nueva.emitida.numero,
                    "cufe": nueva.emitida.cufe,
                    "publico": nueva.emitida.enlace_publico,
                    "qr": nueva.emitida.enlace_qr,
                    "ambiente": nueva.ambiente,
                },
            )
        ).one_or_none()
        if fila is not None:
            return _factura(fila)
        existente = await self.de_la_cita(nueva.cita_id)
        assert existente is not None
        return existente

    async def direccion_del_paciente(self, paciente_id: UUID) -> str | None:
        direccion: str | None = await self._conexion.scalar(
            text("SELECT direccion FROM pacientes WHERE id = :id"), {"id": paciente_id}
        )
        return direccion
