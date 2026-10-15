"""Agenda de hoy del médico, con lo que falta por configurar (HU-021, HU-001 CA-4)."""

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Literal

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cita, Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import dia_en_colombia
from vitalia.dominio.cuentas import COLOMBIA
from vitalia.dominio.identidad import Identidad

Pendiente = Literal["horario", "tipos_cita", "consultorio"]


@dataclass(frozen=True)
class AgendaDeHoy:
    dia: datetime
    citas: list[Cita]
    # Si hoy no hay citas, la próxima que haya agendada (HU-021, CA-3).
    proxima: Cita | None
    pendientes: list[Pendiente]


class VerAgendaDeHoy:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(self, identidad: Identidad) -> AgendaDeHoy:
        await self._autorizador.exigir(identidad, "agenda.ver")
        ahora = self._reloj.ahora()
        inicio_del_dia = datetime.combine(dia_en_colombia(ahora), time(), tzinfo=COLOMBIA)
        fin_del_dia = inicio_del_dia + timedelta(days=1)
        async with self._unidad.abrir(identidad) as trabajo:
            citas = await trabajo.agenda.citas(desde=inicio_del_dia, hasta=fin_del_dia)
            proxima = None
            if not citas:
                siguientes = await trabajo.agenda.citas(
                    desde=fin_del_dia, estado="confirmada", limite=1
                )
                proxima = siguientes[0] if siguientes else None
            pendientes: list[Pendiente] = []
            if not await trabajo.agenda.franjas():
                pendientes.append("horario")
            if not await trabajo.agenda.tipos(solo_activos=True):
                pendientes.append("tipos_cita")
            if not (await trabajo.consultorios.publico()).nombre:
                pendientes.append("consultorio")
        return AgendaDeHoy(inicio_del_dia, citas, proxima, pendientes)
