"""Agendar una cita: el paciente para sí mismo (HU-012) o el médico para un paciente (HU-016)."""

from datetime import datetime
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.calendario import (
    alternativas_para,
    cargar_calendario,
    revisar_espacio,
    tipo_activo,
)
from vitalia.casos_de_uso.puertos import Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import CitaRepetida, EspacioOcupado, Intervalo
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.identidad import Identidad


class AgendarCita:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(
        self,
        identidad: Identidad,
        tipo_id: UUID,
        inicio: datetime,
        paciente_id: UUID | None = None,
        confirmar_repetida: bool = False,
        confirmar_fuera_de_horario: bool = False,
    ) -> UUID:
        """El paciente agenda para sí mismo; el médico indica para quién."""
        await self._autorizador.exigir(identidad, "citas.crear")
        assert identidad.usuario_id is not None
        ahora = self._reloj.ahora()
        try:
            async with self._unidad.abrir(identidad) as trabajo:
                if identidad.clase == "paciente":
                    paciente_id = await trabajo.agenda.paciente_de_la_sesion()
                elif paciente_id is None:
                    raise DatosInvalidos({"paciente": "Elija el paciente"})
                if paciente_id is None or not await trabajo.pacientes.existe(paciente_id):
                    raise NoEncontrado()

                tipo = await tipo_activo(trabajo, tipo_id)
                intervalo = Intervalo(inicio, inicio + tipo.duracion)
                calendario = await cargar_calendario(trabajo, identidad, ahora)
                fuera = revisar_espacio(
                    identidad, intervalo, calendario, ahora, confirmar_fuera_de_horario
                )

                if identidad.clase == "paciente" and not confirmar_repetida:
                    futuras = await trabajo.agenda.citas(
                        paciente_id=paciente_id, desde=ahora, estado="confirmada"
                    )
                    if any(cita.tipo_id == tipo.id for cita in futuras):
                        raise CitaRepetida()

                cita_id = await trabajo.agenda.crear_cita(
                    paciente_id, tipo.id, intervalo, identidad.usuario_id, fuera
                )
                await trabajo.agenda.anotar_cambio(
                    cita_id, identidad.usuario_id, "creada", inicio_nuevo=inicio
                )
                await trabajo.bitacora.registrar(
                    "creacion_de_cita", paciente_id=paciente_id, objeto=str(cita_id)
                )
        except EspacioOcupado:
            # Otra persona confirmó primero (HU-011, CA-2): se ofrecen los más cercanos.
            raise EspacioOcupado(
                await alternativas_para(self._unidad, self._reloj, identidad, tipo, inicio)
            ) from None
        return cita_id
