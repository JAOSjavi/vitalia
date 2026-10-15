"""Inicio del paciente: su próxima cita y si todavía la puede mover o cancelar (HU-020)."""

from dataclasses import dataclass

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cita, ReglasDelConsultorio, Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import puede_cambiarla_el_paciente
from vitalia.dominio.identidad import Identidad


@dataclass(frozen=True)
class InicioDelPaciente:
    proxima: Cita | None
    puede_cambiarla: bool
    reglas: ReglasDelConsultorio


class VerInicioDelPaciente:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(self, identidad: Identidad) -> InicioDelPaciente:
        await self._autorizador.exigir(identidad, "inicio.ver")
        ahora = self._reloj.ahora()
        # Una pantalla, una operación: todo lo del inicio en la misma transacción.
        async with self._unidad.abrir(identidad) as trabajo:
            proximas = await trabajo.agenda.citas(desde=ahora, estado="confirmada", limite=1)
            reglas = await trabajo.consultorios.reglas()
        proxima = proximas[0] if proximas else None
        puede = proxima is not None and puede_cambiarla_el_paciente(
            proxima.inicio, ahora, reglas.anticipacion_horas
        )
        return InicioDelPaciente(proxima, puede, reglas)
