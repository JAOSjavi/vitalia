"""Agenda de hoy del médico, con lo que falta por configurar (HU-021, HU-001 CA-4)."""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Literal
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cita, Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import dia_en_colombia
from vitalia.dominio.cuentas import COLOMBIA
from vitalia.dominio.identidad import Identidad

Pendiente = Literal["horario", "tipos_cita", "consultorio"]


@dataclass(frozen=True)
class QuienSigue:
    """Lo justo del paciente que sigue para prepararse, sin abrir su ficha ni dejar rastro."""

    cita_id: UUID
    edad: int
    documentos: int
    legibles: int
    ia_autorizada: bool


@dataclass(frozen=True)
class AgendaDeHoy:
    dia: datetime
    citas: list[Cita]
    # Si hoy no hay citas, la próxima que haya agendada (HU-021, CA-3).
    proxima: Cita | None
    pendientes: list[Pendiente]
    sigue: QuienSigue | None = None


def edad(nacimiento: date, hoy: date) -> int:
    return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))


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
            sigue = None
            cita = next((c for c in citas if c.estado == "confirmada" and c.fin > ahora), None)
            if cita is not None:
                datos = await trabajo.pacientes.ficha(cita.paciente_id)
                documentos = await trabajo.documentos.listar_de(cita.paciente_id)
                if datos is not None:
                    sigue = QuienSigue(
                        cita_id=cita.id,
                        edad=edad(datos.fecha_nacimiento, dia_en_colombia(ahora)),
                        documentos=len(documentos),
                        legibles=sum(d.estado_lectura == "legible" for d in documentos),
                        ia_autorizada=await trabajo.documentos.ia_autorizada(cita.paciente_id),
                    )
        return AgendaDeHoy(inicio_del_dia, citas, proxima, pendientes, sigue)
