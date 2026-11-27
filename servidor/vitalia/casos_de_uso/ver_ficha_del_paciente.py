"""La médica abre la ficha de un paciente (HU-025): una pantalla, una operación.

Trae los datos de identificación y contacto, sus citas, los documentos que subió y si autorizó
el uso de IA, que decide si el asistente se puede usar (CA-3). Abrirla queda en la bitácora (CA-4).
Los tratamientos se suman cuando se construya la épica E8.
"""

from dataclasses import dataclass
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cita, DatosDeLaFicha, DocumentoSubido, UnidadDeTrabajo
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.identidad import Identidad


@dataclass(frozen=True)
class Ficha:
    paciente: DatosDeLaFicha
    ia_autorizada: bool
    citas: list[Cita]
    documentos: list[DocumentoSubido]


class VerFichaDelPaciente:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ejecutar(self, identidad: Identidad, paciente_id: UUID) -> Ficha:
        await self._autorizador.exigir(identidad, "pacientes.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            paciente = await trabajo.pacientes.ficha(paciente_id)
            if paciente is None:
                raise NoEncontrado()
            ficha = Ficha(
                paciente=paciente,
                ia_autorizada=await trabajo.documentos.ia_autorizada(paciente_id),
                citas=await trabajo.agenda.citas(paciente_id=paciente_id),
                documentos=await trabajo.documentos.listar_de(paciente_id),
            )
            await trabajo.bitacora.registrar("ficha_vista", paciente_id=paciente_id)
        return ficha
