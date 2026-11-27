"""El paciente ve la lista de sus documentos con su estado de lectura (HU-028, HU-029, HU-031).

En la misma operación va si autorizó el uso de IA: la pantalla lo muestra junto a la lista.
"""

from dataclasses import dataclass

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import DocumentoSubido, UnidadDeTrabajo
from vitalia.dominio.identidad import Identidad


@dataclass(frozen=True)
class MisDocumentos:
    documentos: list[DocumentoSubido]
    ia_autorizada: bool


class VerMisDocumentos:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ejecutar(self, identidad: Identidad) -> MisDocumentos:
        await self._autorizador.exigir(identidad, "documentos.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            documentos = await trabajo.documentos.listar()
            paciente = await trabajo.agenda.paciente_de_la_sesion()
            autorizada = paciente is not None and await trabajo.documentos.ia_autorizada(paciente)
        return MisDocumentos(documentos, autorizada)
