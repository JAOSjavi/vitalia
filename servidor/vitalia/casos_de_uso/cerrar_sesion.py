"""Cerrar la sesión: queda anulada en el servidor (HU-007)."""

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.fichas import huella_de
from vitalia.casos_de_uso.puertos import Reloj, UnidadDeTrabajo
from vitalia.dominio.identidad import Identidad


class CerrarSesion:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador, reloj: Reloj) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._reloj = reloj

    async def ejecutar(self, identidad: Identidad, ficha: str) -> None:
        await self._autorizador.exigir(identidad, "sesion.cerrar")
        async with self._unidad.abrir(identidad) as trabajo:
            await trabajo.cuentas.anular_sesion(huella_de(ficha), self._reloj.ahora())
            await trabajo.bitacora.registrar("salida")
