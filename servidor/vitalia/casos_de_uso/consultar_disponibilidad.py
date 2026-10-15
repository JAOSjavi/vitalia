"""Los próximos días con espacio y las horas libres de un día (HU-011, HU-012, CA-5)."""

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.calendario import cargar_calendario, tipo_activo
from vitalia.casos_de_uso.puertos import Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import (
    AgendaNoDisponible,
    TipoDeCita,
    dias_con_espacio,
    espacios_del_dia,
)
from vitalia.dominio.identidad import Identidad


@dataclass(frozen=True)
class Disponibilidad:
    tipo: TipoDeCita
    dias: list[date]
    dia: date | None
    horas: list[datetime]


class ConsultarDisponibilidad:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(
        self,
        identidad: Identidad,
        tipo_id: UUID,
        dia: date | None = None,
        ignorar_cita: UUID | None = None,
    ) -> Disponibilidad:
        """Sin día, muestra las horas del primer día con espacio. Al mover, ignora esa cita."""
        await self._autorizador.exigir(identidad, "disponibilidad.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            tipo = await tipo_activo(trabajo, tipo_id)
            calendario = await cargar_calendario(
                trabajo, identidad, self._reloj.ahora(), ignorar_cita
            )
        if not calendario.franjas:
            raise AgendaNoDisponible()

        dias = dias_con_espacio(
            calendario.desde, calendario.franjas, calendario.ocupados, tipo.duracion
        )
        elegido = dia or (dias[0] if dias else None)
        horas = (
            espacios_del_dia(
                elegido, calendario.franjas, calendario.ocupados, tipo.duracion, calendario.desde
            )
            if elegido
            else []
        )
        return Disponibilidad(tipo, dias, elegido, horas)
