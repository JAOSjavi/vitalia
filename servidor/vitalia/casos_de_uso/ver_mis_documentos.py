"""El paciente ve la lista de sus documentos con su estado de lectura (HU-028, HU-031)."""

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import DocumentoSubido, UnidadDeTrabajo
from vitalia.dominio.identidad import Identidad


class VerMisDocumentos:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ejecutar(self, identidad: Identidad) -> list[DocumentoSubido]:
        await self._autorizador.exigir(identidad, "documentos.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.documentos.listar()
