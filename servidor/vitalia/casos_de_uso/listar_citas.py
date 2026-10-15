"""Listar citas: el paciente las suyas (HU-013), el médico las de un rango."""

from datetime import datetime

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cita, UnidadDeTrabajo
from vitalia.dominio.agenda import EstadoDeCita
from vitalia.dominio.identidad import Identidad


class ListarCitas:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ejecutar(
        self,
        identidad: Identidad,
        desde: datetime | None = None,
        hasta: datetime | None = None,
        estado: EstadoDeCita | None = None,
    ) -> list[Cita]:
        await self._autorizador.exigir(identidad, "citas.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.agenda.citas(desde=desde, hasta=hasta, estado=estado)
