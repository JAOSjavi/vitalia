"""Ver los datos del consultorio: lo público sin sesión, y todo con ella (HU-001)."""

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import ConsultorioPublico, DatosDelConsultorio, UnidadDeTrabajo
from vitalia.dominio.identidad import Identidad


class VerConsultorio:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def publico(self) -> ConsultorioPublico:
        """Nombre, teléfono y médico: lo que se muestra antes de ingresar."""
        async with self._unidad.abrir(None) as trabajo:
            return await trabajo.consultorios.publico()

    async def ejecutar(self, identidad: Identidad) -> DatosDelConsultorio:
        await self._autorizador.exigir(identidad, "consultorio.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.consultorios.datos()
