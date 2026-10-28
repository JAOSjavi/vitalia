"""Lo que comparten consultar, agendar y mover: el horario, lo ocupado y el espacio pedido."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from vitalia.casos_de_uso.puertos import ReglasDelConsultorio, Reloj, Trabajo, UnidadDeTrabajo
from vitalia.dominio.agenda import (
    HORIZONTE,
    EspacioBloqueado,
    EspacioNoDisponible,
    Franja,
    FueraDeHorario,
    Intervalo,
    TipoDeCita,
    alternativas,
    en_horario,
)
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.identidad import Identidad


@dataclass(frozen=True)
class Calendario:
    franjas: list[Franja]
    # Citas y bloqueos: nada de esto se ofrece.
    ocupados: list[Intervalo]
    # Solo los bloqueos, para no dar una cita encima de uno (HU-009).
    bloqueos: list[Intervalo]
    # Primer momento que se puede ofrecer: al paciente, con el margen del consultorio.
    desde: datetime
    reglas: ReglasDelConsultorio


async def cargar_calendario(
    trabajo: Trabajo, identidad: Identidad, ahora: datetime, ignorar: UUID | None = None
) -> Calendario:
    """Tres consultas: horario, reglas del consultorio y lo ocupado hasta el horizonte."""
    franjas = await trabajo.agenda.franjas()
    reglas = await trabajo.consultorios.reglas()
    margen = timedelta(minutes=reglas.margen_agenda_minutos)
    desde = ahora + margen if identidad.clase == "paciente" else ahora
    todo = await trabajo.agenda.ocupados(ahora, ahora + HORIZONTE + timedelta(days=1))
    ocupados = [intervalo for cita_id, intervalo in todo if cita_id is None or cita_id != ignorar]
    # Lo ocupado sin cita es un bloqueo.
    bloqueos = [intervalo for cita_id, intervalo in todo if cita_id is None]
    return Calendario(franjas, ocupados, bloqueos, desde, reglas)


async def tipo_activo(trabajo: Trabajo, tipo_id: UUID) -> TipoDeCita:
    tipo = await trabajo.agenda.tipo(tipo_id)
    if tipo is None or not tipo.activo:
        raise DatosInvalidos({"tipo_cita": "Elija un tipo de cita disponible"})
    return tipo


def revisar_espacio(
    identidad: Identidad,
    intervalo: Intervalo,
    calendario: Calendario,
    ahora: datetime,
    confirmar_fuera_de_horario: bool,
) -> bool:
    """Revisa que el espacio pedido se pueda dar. Devuelve si queda por fuera del horario.

    Al paciente solo se le da lo que está en el horario y respeta el margen. El médico puede
    salirse del horario si lo confirma (HU-016, CA-3), pero no dar citas en el pasado.
    """
    dentro = en_horario(intervalo, calendario.franjas)
    bloqueado = any(intervalo.se_cruza_con(b) for b in calendario.bloqueos)
    if identidad.clase == "paciente":
        if bloqueado:
            raise EspacioNoDisponible()
        if not dentro or intervalo.inicio < calendario.desde:
            raise EspacioNoDisponible()
        return False
    if intervalo.inicio < ahora:
        raise EspacioNoDisponible()
    if bloqueado:
        raise EspacioBloqueado()
    if not dentro and not confirmar_fuera_de_horario:
        raise FueraDeHorario()
    return not dentro


async def alternativas_para(
    unidad: UnidadDeTrabajo,
    reloj: Reloj,
    identidad: Identidad,
    tipo: TipoDeCita,
    pedido: datetime,
    ignorar: UUID | None = None,
) -> list[datetime]:
    """Después de un choque, en una transacción nueva: la anterior quedó deshecha."""
    async with unidad.abrir(identidad) as trabajo:
        calendario = await cargar_calendario(trabajo, identidad, reloj.ahora(), ignorar)
    return alternativas(
        pedido, calendario.franjas, calendario.ocupados, tipo.duracion, calendario.desde
    )
