"""Ver el horario semanal de atención (HU-008)."""

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import UnidadDeTrabajo
from vitalia.dominio.agenda import Franja
from vitalia.dominio.identidad import Identidad


class VerHorario:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ejecutar(self, identidad: Identidad) -> list[Franja]:
        await self._autorizador.exigir(identidad, "horario.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.agenda.franjas()
