"""Marcar una cita como atendida o "no asistió", y corregirlo el mismo día (HU-018)."""

from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import Asistencia, revisar_asistencia
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.identidad import Identidad


class RegistrarAsistencia:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(self, identidad: Identidad, cita_id: UUID, estado: Asistencia) -> None:
        await self._autorizador.exigir(identidad, "citas.asistencia")
        assert identidad.usuario_id is not None
        async with self._unidad.abrir(identidad) as trabajo:
            cita = await trabajo.agenda.cita(cita_id)
            if cita is None:
                raise NoEncontrado()
            # El historial guarda la hora del registro y si fue corrección (HU-018, CA-1 y CA-3).
            tipo = revisar_asistencia(cita.estado, estado, cita.inicio, self._reloj.ahora())
            await trabajo.agenda.marcar_asistencia(cita.id, estado)
            await trabajo.agenda.anotar_cambio(cita.id, identidad.usuario_id, tipo)
            await trabajo.bitacora.registrar(
                "asistencia_de_cita", paciente_id=cita.paciente_id, objeto=str(cita.id)
            )
