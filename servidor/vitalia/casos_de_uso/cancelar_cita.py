"""Cancelar una cita: queda en el historial como cancelada (HU-015 paciente, HU-017 médico)."""

from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import (
    FaltaAnticipacion,
    puede_cambiarla_el_paciente,
    revisar_que_se_pueda_cambiar,
)
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.identidad import Identidad


class CancelarCita:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(self, identidad: Identidad, cita_id: UUID, motivo: str | None) -> None:
        """El motivo es obligatorio para el médico y opcional para el paciente."""
        await self._autorizador.exigir(identidad, "citas.cancelar")
        assert identidad.usuario_id is not None
        motivo = (motivo or "").strip() or None
        if identidad.clase == "medico" and motivo is None:
            raise DatosInvalidos({"motivo": "Escriba el motivo de la cancelación"})

        ahora = self._reloj.ahora()
        async with self._unidad.abrir(identidad) as trabajo:
            cita = await trabajo.agenda.cita(cita_id)
            if cita is None:
                raise NoEncontrado()
            revisar_que_se_pueda_cambiar(cita.estado, cita.fin, ahora)
            if identidad.clase == "paciente":
                horas = (await trabajo.consultorios.reglas()).anticipacion_horas
                if not puede_cambiarla_el_paciente(cita.inicio, ahora, horas):
                    raise FaltaAnticipacion(horas)

            await trabajo.agenda.cancelar_cita(cita.id)
            await trabajo.agenda.anotar_cambio(
                cita.id,
                identidad.usuario_id,
                "cancelada",
                inicio_anterior=cita.inicio,
                motivo=motivo,
            )
            await trabajo.bitacora.registrar(
                "cancelacion_de_cita", paciente_id=cita.paciente_id, objeto=str(cita.id)
            )
