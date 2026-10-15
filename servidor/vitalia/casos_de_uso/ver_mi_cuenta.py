"""Ver mi usuario y mi rol (GET /yo)."""

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cuenta, UnidadDeTrabajo
from vitalia.dominio.identidad import Identidad


class VerMiCuenta:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ejecutar(self, identidad: Identidad) -> Cuenta:
        await self._autorizador.exigir(identidad, "cuenta.ver")
        assert identidad.usuario_id is not None
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.cuentas.cuenta(identidad.usuario_id)
