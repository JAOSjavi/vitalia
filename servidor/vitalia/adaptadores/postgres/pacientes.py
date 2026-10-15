"""Lista y búsqueda de pacientes en PostgreSQL (HU-023)."""

from typing import cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from vitalia.casos_de_uso.puertos import PacienteEnLista
from vitalia.dominio.cuentas import Documento, TipoDocumento

# Por nombre, sin tildes ni mayúsculas y con cada palabra en cualquier parte ("ana mejia" encuentra
# a Ana María Mejía), o por el comienzo del documento escrito con puntos o espacios.
_COINCIDE = """
    (CAST(:texto AS text) IS NULL
     OR NOT EXISTS (
         SELECT 1 FROM regexp_split_to_table(sin_tildes(trim(:texto)), '\\s+') AS palabra
         WHERE sin_tildes(p.nombres || ' ' || p.apellidos) NOT LIKE '%' || palabra || '%')
     OR u.numero_documento LIKE regexp_replace(upper(:texto), '[\\s.\\-]', '', 'g') || '%')
"""


class PacientesPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def buscar(
        self, texto: str | None, pagina: int, tamano: int
    ) -> tuple[list[PacienteEnLista], int]:
        # Una sola consulta trae la página y el total.
        filas = (
            await self._conexion.execute(
                text(
                    "SELECT p.id, p.nombres, p.apellidos, p.telefono, u.tipo_documento, "
                    "u.numero_documento, count(*) OVER () AS total "
                    "FROM pacientes p JOIN usuarios u ON u.id = p.usuario_id "
                    f"WHERE {_COINCIDE} "
                    "ORDER BY sin_tildes(p.apellidos), sin_tildes(p.nombres) "
                    "LIMIT :tamano OFFSET :salto"
                ),
                {"texto": texto, "tamano": tamano, "salto": (pagina - 1) * tamano},
            )
        ).all()
        pacientes = [
            PacienteEnLista(
                id=f.id,
                nombres=f.nombres,
                apellidos=f.apellidos,
                documento=Documento(cast(TipoDocumento, f.tipo_documento), f.numero_documento),
                telefono=f.telefono,
            )
            for f in filas
        ]
        return pacientes, (filas[0].total if filas else 0)

    async def existe(self, paciente_id: UUID) -> bool:
        return bool(
            await self._conexion.scalar(
                text("SELECT EXISTS (SELECT 1 FROM pacientes WHERE id = :id)"), {"id": paciente_id}
            )
        )
