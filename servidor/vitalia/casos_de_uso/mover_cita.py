"""Mover una cita a otro espacio libre (HU-014 el paciente, HU-017 el médico)."""

from datetime import datetime, timedelta
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.calendario import alternativas_para, cargar_calendario, revisar_espacio
from vitalia.casos_de_uso.puertos import Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import (
    EspacioOcupado,
    FaltaAnticipacion,
    Intervalo,
    TipoDeCita,
    puede_cambiarla_el_paciente,
    revisar_que_se_pueda_cambiar,
)
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.identidad import Identidad


class MoverCita:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(
        self,
        identidad: Identidad,
        cita_id: UUID,
        inicio: datetime,
        motivo: str | None = None,
        confirmar_fuera_de_horario: bool = False,
    ) -> None:
        await self._autorizador.exigir(identidad, "citas.mover")
        assert identidad.usuario_id is not None
        ahora = self._reloj.ahora()
        try:
            async with self._unidad.abrir(identidad) as trabajo:
                # Los permisos por fila no le entregan al paciente una cita ajena.
                cita = await trabajo.agenda.cita(cita_id)
                if cita is None:
                    raise NoEncontrado()
                revisar_que_se_pueda_cambiar(cita.estado, cita.fin, ahora)
                calendario = await cargar_calendario(trabajo, identidad, ahora, ignorar=cita.id)
                horas = calendario.reglas.anticipacion_horas
                if identidad.clase == "paciente" and not puede_cambiarla_el_paciente(
                    cita.inicio, ahora, horas
                ):
                    raise FaltaAnticipacion(horas)

                # La duración es la que tenía la cita, aunque luego haya cambiado la del tipo,
                # y se puede mover aunque el tipo ya no se ofrezca (HU-010, CA-2 y CA-3).
                duracion = cita.fin - cita.inicio
                tipo = TipoDeCita(cita.tipo_id, cita.tipo, duracion // timedelta(minutes=1), True)
                intervalo = Intervalo(inicio, inicio + duracion)
                fuera = revisar_espacio(
                    identidad, intervalo, calendario, ahora, confirmar_fuera_de_horario
                )
                await trabajo.agenda.mover_cita(cita.id, intervalo, fuera)
                await trabajo.agenda.anotar_cambio(
                    cita.id,
                    identidad.usuario_id,
                    "movida",
                    inicio_anterior=cita.inicio,
                    inicio_nuevo=inicio,
                    motivo=(motivo or "").strip() or None,
                )
                await trabajo.bitacora.registrar(
                    "movimiento_de_cita", paciente_id=cita.paciente_id, objeto=str(cita.id)
                )
        except EspacioOcupado:
            # La cita original se conserva: la transacción se deshizo (HU-014, CA-3).
            raise EspacioOcupado(
                await alternativas_para(
                    self._unidad, self._reloj, identidad, tipo, inicio, ignorar=cita_id
                )
            ) from None
