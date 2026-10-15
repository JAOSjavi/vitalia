"""Crear el enlace de un solo uso con el que el médico crea su cuenta (HU-001)."""

from vitalia.casos_de_uso.fichas import nueva_ficha
from vitalia.casos_de_uso.puertos import Reloj, UnidadDeTrabajo
from vitalia.dominio.ingreso import VIGENCIA_DEL_ENLACE_DE_PUESTA_EN_MARCHA


class CrearEnlaceDePuestaEnMarcha:
    def __init__(self, unidad: UnidadDeTrabajo, reloj: Reloj) -> None:
        self._unidad = unidad
        self._reloj = reloj

    async def ejecutar(self) -> str:
        """Devuelve la ficha del enlace. Lanza YaHayMedico si la cuenta ya existe."""
        ficha, huella = nueva_ficha()
        vence = self._reloj.ahora() + VIGENCIA_DEL_ENLACE_DE_PUESTA_EN_MARCHA
        async with self._unidad.abrir(None) as trabajo:
            await trabajo.cuentas.crear_enlace_de_puesta_en_marcha(huella, vence)
        return ficha
