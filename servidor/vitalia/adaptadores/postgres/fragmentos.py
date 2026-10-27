"""Fragmentos del asistente en PostgreSQL con pgvector."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from vitalia.casos_de_uso.puertos import FragmentoEncontrado, FragmentoNuevo
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.fragmentos import Identificadores


def como_vector(numeros: Sequence[float]) -> str:
    """pgvector recibe el vector como texto: [0.1,0.2,...]."""
    return "[" + ",".join(repr(float(n)) for n in numeros) + "]"


class FragmentosPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def identificadores(self, paciente_id: UUID) -> Identificadores:
        fila = (
            await self._conexion.execute(
                text("SELECT * FROM identificadores_paciente(:p)"), {"p": paciente_id}
            )
        ).one_or_none()
        if fila is None:
            raise NoEncontrado()
        return Identificadores(
            fila.nombres, fila.apellidos, fila.numero_documento, fila.telefono, fila.correo
        )

    async def reemplazar_del_documento(
        self, documento_id: UUID, fragmentos: Sequence[FragmentoNuevo], modelo: str
    ) -> None:
        await self._conexion.execute(
            text("DELETE FROM fragmentos WHERE documento_id = :d"), {"d": documento_id}
        )
        if not fragmentos:
            return
        # El paciente sale del documento, no del código: un fragmento no puede quedar con otro.
        await self._conexion.execute(
            text(
                "INSERT INTO fragmentos (paciente_id, documento_id, pagina, orden, texto, "
                "vector, modelo) SELECT paciente_id, id, :pagina, :orden, :texto, "
                "CAST(:vector AS vector), :modelo FROM documentos WHERE id = :d"
            ),
            [
                {
                    "d": documento_id,
                    "pagina": f.pagina,
                    "orden": f.orden,
                    "texto": f.texto,
                    "vector": como_vector(f.vector),
                    "modelo": modelo,
                }
                for f in fragmentos
            ],
        )

    async def buscar(
        self,
        paciente_id: UUID,
        vector: Sequence[float],
        consulta: str,
        por_metodo: int,
        total: int,
    ) -> list[FragmentoEncontrado]:
        filas = await self._conexion.execute(
            text(
                "SELECT f.id, f.documento_id, d.nombre, d.fecha_documento, f.pagina, f.texto, "
                "b.puntaje, b.rango_significado, b.rango_palabras "
                "FROM buscar_fragmentos(:p, CAST(:v AS vector), :q, :por_metodo, :total) b "
                "JOIN fragmentos f ON f.id = b.fragmento_id "
                "JOIN documentos d ON d.id = f.documento_id "
                "ORDER BY b.puntaje DESC, f.documento_id, f.pagina, f.orden"
            ),
            {
                "p": paciente_id,
                "v": como_vector(vector),
                "q": consulta,
                "por_metodo": por_metodo,
                "total": total,
            },
        )
        return [
            FragmentoEncontrado(
                id=f.id,
                documento_id=f.documento_id,
                documento=f.nombre,
                fecha_documento=f.fecha_documento,
                pagina=f.pagina,
                texto=f.texto,
                puntaje=float(f.puntaje),
                rango_significado=f.rango_significado,
                rango_palabras=f.rango_palabras,
            )
            for f in filas
        ]
