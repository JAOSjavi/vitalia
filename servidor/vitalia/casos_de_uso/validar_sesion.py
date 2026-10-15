"""Encontrar a quién pertenece la sesión de cada petición (HU-007)."""

from vitalia.casos_de_uso.fichas import huella_de
from vitalia.casos_de_uso.puertos import Reloj, UnidadDeTrabajo
from vitalia.dominio.identidad import Identidad


class ValidarSesion:
    def __init__(self, unidad: UnidadDeTrabajo, reloj: Reloj) -> None:
        self._unidad = unidad
        self._reloj = reloj

    async def ejecutar(self, ficha: str) -> Identidad | None:
        """None si la sesión no existe, se cerró o pasó media hora sin uso."""
        async with self._unidad.abrir(None) as trabajo:
            return await trabajo.cuentas.sesion_vigente(huella_de(ficha), self._reloj.ahora())
