"""Guardar el horario semanal (HU-008). Las citas que quedan por fuera se conservan y se listan."""

from collections.abc import Sequence

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cita, Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import Franja, Intervalo, en_horario, revisar_horario
from vitalia.dominio.identidad import Identidad


class GuardarHorario:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(self, identidad: Identidad, franjas: Sequence[Franja]) -> list[Cita]:
        """Devuelve las citas futuras que quedaron por fuera del horario nuevo (HU-008, CA-3)."""
        await self._autorizador.exigir(identidad, "horario.editar")
        revisar_horario(franjas)
        async with self._unidad.abrir(identidad) as trabajo:
            await trabajo.agenda.reemplazar_franjas(franjas)
            await trabajo.bitacora.registrar("edicion_del_horario")
            futuras = await trabajo.agenda.citas(desde=self._reloj.ahora(), estado="confirmada")
        return [c for c in futuras if not en_horario(Intervalo(c.inicio, c.fin), franjas)]
