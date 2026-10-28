"""Bloqueos del horario: listarlos, crearlos y eliminar los futuros (HU-009)."""

from datetime import datetime
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cita, Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import Bloqueo, Intervalo, revisar_bloqueo
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.identidad import Identidad


class BloqueoConCitas(Exception):
    """El bloqueo se cruza con citas: hay que moverlas o cancelarlas primero (HU-009, CA-2)."""

    def __init__(self, citas: list[Cita]) -> None:
        super().__init__("El bloqueo se cruza con citas agendadas")
        self.citas = citas


class Bloqueos:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def listar(self, identidad: Identidad, desde: datetime, hasta: datetime) -> list[Bloqueo]:
        await self._autorizador.exigir(identidad, "bloqueos.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.agenda.bloqueos(desde, hasta)

    async def crear(
        self, identidad: Identidad, inicio: datetime, fin: datetime, motivo: str
    ) -> UUID:
        """Un bloqueo de varios días es un solo rango (CA-4). No se guarda si tapa citas (CA-2)."""
        await self._autorizador.exigir(identidad, "bloqueos.crear")
        assert identidad.usuario_id is not None
        intervalo = Intervalo(inicio, fin)
        motivo = revisar_bloqueo(intervalo, motivo, self._reloj.ahora())
        async with self._unidad.abrir(identidad) as trabajo:
            afectadas = await trabajo.agenda.citas(
                desde=intervalo.inicio, hasta=intervalo.fin, estado="confirmada"
            )
            if afectadas:
                raise BloqueoConCitas(afectadas)
            bloqueo_id = await trabajo.agenda.crear_bloqueo(intervalo, motivo, identidad.usuario_id)
            await trabajo.bitacora.registrar("creacion_de_bloqueo", objeto=str(bloqueo_id))
        return bloqueo_id

    async def eliminar(self, identidad: Identidad, bloqueo_id: UUID) -> None:
        """Solo un bloqueo que todavía no termina: el pasado queda como fue (CA-3)."""
        await self._autorizador.exigir(identidad, "bloqueos.eliminar")
        async with self._unidad.abrir(identidad) as trabajo:
            bloqueo = await trabajo.agenda.bloqueo(bloqueo_id)
            if bloqueo is None:
                raise NoEncontrado()
            if bloqueo.intervalo.fin <= self._reloj.ahora():
                raise DatosInvalidos({"bloqueo": "Ese bloqueo ya pasó"})
            await trabajo.agenda.eliminar_bloqueo(bloqueo_id)
            await trabajo.bitacora.registrar("eliminacion_de_bloqueo", objeto=str(bloqueo_id))
