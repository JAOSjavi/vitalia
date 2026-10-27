"""Reglas de la agenda: horario, espacios libres y cambios de una cita (HU-008 a HU-017).

Todo es hora de Colombia para mostrar y hora universal para guardar. Los espacios se calculan
aquí, en memoria, con tres datos: el horario, lo ocupado y la duración del tipo de cita.
"""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Literal
from uuid import UUID

from vitalia.dominio.cuentas import COLOMBIA, DatosInvalidos

DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
# Cuántos días hacia adelante se buscan espacios y cuántos días con espacio se ofrecen.
HORIZONTE = timedelta(days=45)
DIAS_OFRECIDOS = 6

EstadoDeCita = Literal["confirmada", "cancelada", "atendida", "no_asistio"]


@dataclass(frozen=True)
class Franja:
    """Un rato de atención de un día de la semana. 1 es lunes y 7 domingo."""

    dia_semana: int
    inicio: time
    fin: time


@dataclass(frozen=True)
class Intervalo:
    inicio: datetime
    fin: datetime

    def se_cruza_con(self, otro: "Intervalo") -> bool:
        return self.inicio < otro.fin and otro.inicio < self.fin


@dataclass(frozen=True)
class TipoDeCita:
    id: UUID
    nombre: str
    duracion_minutos: int
    activo: bool

    @property
    def duracion(self) -> timedelta:
        return timedelta(minutes=self.duracion_minutos)


class AgendaNoDisponible(Exception):
    """No hay horario o no hay tipos de cita activos (HU-010, CA-4)."""


class EspacioOcupado(Exception):
    """Otra cita tomó ese espacio. Trae los espacios libres más cercanos (HU-011, CA-2)."""

    def __init__(self, alternativas: Sequence[datetime] = ()) -> None:
        super().__init__("El espacio ya está ocupado")
        self.alternativas = list(alternativas)


class EspacioNoDisponible(Exception):
    """El paciente pidió una hora fuera del horario, ya pasada o con menos margen del debido."""


class FaltaAnticipacion(Exception):
    """El paciente solo mueve o cancela con la anticipación del consultorio (HU-014, HU-015)."""

    def __init__(self, horas: int) -> None:
        super().__init__(f"Faltan menos de {horas} horas")
        self.horas = horas


class FueraDeHorario(Exception):
    """El médico puede dar una cita por fuera del horario, pero debe confirmarlo (HU-016, CA-3)."""


class CitaRepetida(Exception):
    """El paciente ya tiene una cita futura de ese tipo y debe confirmar (HU-012, CA-3)."""


class CitaNoModificable(Exception):
    """Una cita atendida, cancelada o con inasistencia ya no se mueve ni se cancela."""


def revisar_horario(franjas: Sequence[Franja]) -> None:
    """Una franja debe terminar después de empezar y no cruzarse con otra del mismo día."""
    campos: dict[str, str] = {}
    for indice, franja in enumerate(franjas):
        if not 1 <= franja.dia_semana <= 7:
            campos[f"franjas.{indice}"] = "El día de la semana no existe"
        elif franja.inicio >= franja.fin:
            campos[f"franjas.{indice}"] = (
                f"La franja del {DIAS[franja.dia_semana - 1]} termina antes de empezar"
            )
    for indice, franja in enumerate(franjas):
        for otro, otra in enumerate(franjas[:indice]):
            if (
                franja.dia_semana == otra.dia_semana
                and franja.inicio < otra.fin
                and otra.inicio < franja.fin
            ):
                campos[f"franjas.{indice}"] = (
                    f"Se cruza con otra franja del {DIAS[franja.dia_semana - 1]}"
                )
                campos.setdefault(f"franjas.{otro}", campos[f"franjas.{indice}"])
    if campos:
        raise DatosInvalidos(campos)


def _en_colombia(dia: date, hora: time) -> datetime:
    return datetime.combine(dia, hora, tzinfo=COLOMBIA)


def dia_en_colombia(momento: datetime) -> date:
    return momento.astimezone(COLOMBIA).date()


def en_horario(intervalo: Intervalo, franjas: Iterable[Franja]) -> bool:
    dia = dia_en_colombia(intervalo.inicio)
    return any(
        franja.dia_semana == dia.isoweekday()
        and _en_colombia(dia, franja.inicio) <= intervalo.inicio
        and intervalo.fin <= _en_colombia(dia, franja.fin)
        for franja in franjas
    )


def espacios_del_dia(
    dia: date,
    franjas: Iterable[Franja],
    ocupados: Sequence[Intervalo],
    duracion: timedelta,
    desde: datetime,
) -> list[datetime]:
    """Inicios libres de un día, uno detrás de otro desde el comienzo de cada franja.

    Un espacio que no cabe completo en la franja no se ofrece (HU-011, CA-4), y tampoco los
    que empiezan antes de "desde": ya pasaron o no dejan el margen pedido (HU-011, CA-3).
    """
    libres = []
    for franja in sorted(
        (f for f in franjas if f.dia_semana == dia.isoweekday()), key=lambda f: f.inicio
    ):
        inicio = _en_colombia(dia, franja.inicio)
        cierre = _en_colombia(dia, franja.fin)
        while inicio + duracion <= cierre:
            espacio = Intervalo(inicio, inicio + duracion)
            if inicio >= desde and not any(espacio.se_cruza_con(o) for o in ocupados):
                libres.append(inicio)
            inicio += duracion
    return libres


def dias_con_espacio(
    desde: datetime,
    franjas: Sequence[Franja],
    ocupados: Sequence[Intervalo],
    duracion: timedelta,
    cuantos: int = DIAS_OFRECIDOS,
) -> list[date]:
    """Los próximos días que tienen al menos un espacio libre. Lo ocupado no se muestra."""
    dias: list[date] = []
    dia = dia_en_colombia(desde)
    ultimo = dia_en_colombia(desde + HORIZONTE)
    while dia <= ultimo and len(dias) < cuantos:
        if espacios_del_dia(dia, franjas, ocupados, duracion, desde):
            dias.append(dia)
        dia += timedelta(days=1)
    return dias


def alternativas(
    pedido: datetime,
    franjas: Sequence[Franja],
    ocupados: Sequence[Intervalo],
    duracion: timedelta,
    desde: datetime,
    cuantas: int = 3,
) -> list[datetime]:
    """Los espacios libres más cercanos a la hora pedida, ese día o los siguientes."""
    candidatos: list[datetime] = []
    for dia in dias_con_espacio(
        max(desde, pedido - timedelta(hours=12)), franjas, ocupados, duracion
    ):
        candidatos += espacios_del_dia(dia, franjas, ocupados, duracion, desde)
        if len(candidatos) >= cuantas * 3:
            break
    return sorted(candidatos, key=lambda inicio: abs(inicio - pedido))[:cuantas]


def puede_cambiarla_el_paciente(inicio: datetime, ahora: datetime, anticipacion_horas: int) -> bool:
    return inicio - ahora > timedelta(hours=anticipacion_horas)


def revisar_que_se_pueda_cambiar(estado: EstadoDeCita, fin: datetime, ahora: datetime) -> None:
    if estado != "confirmada" or fin <= ahora:
        raise CitaNoModificable()


Asistencia = Literal["atendida", "no_asistio"]


def revisar_asistencia(
    estado: EstadoDeCita, nuevo: Asistencia, inicio: datetime, ahora: datetime
) -> Literal["asistencia", "correccion"]:
    """Se marca el día de la cita o después; "no asistió" solo cuando su hora ya pasó (HU-018).

    Una cita ya marcada se corrige solo el mismo día. Una cancelada no se marca.
    """
    if estado == "cancelada":
        raise CitaNoModificable()
    if dia_en_colombia(inicio) > dia_en_colombia(ahora):
        raise DatosInvalidos({"estado": "La cita todavía no es hoy"})
    if nuevo == "no_asistio" and inicio > ahora:
        raise DatosInvalidos({"estado": "La hora de la cita todavía no ha pasado"})
    if estado == "confirmada":
        return "asistencia"
    if estado == nuevo:
        raise DatosInvalidos({"estado": "La cita ya tiene ese estado"})
    if dia_en_colombia(inicio) != dia_en_colombia(ahora):
        raise DatosInvalidos({"estado": "La asistencia solo se corrige el mismo día de la cita"})
    return "correccion"
