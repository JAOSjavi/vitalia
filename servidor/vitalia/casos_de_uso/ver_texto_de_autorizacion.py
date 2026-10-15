"""Leer el texto vigente de una autorización, también sin sesión (HU-003, HU-032)."""

from typing import Literal

from vitalia.casos_de_uso.puertos import ConsultorioPublico, TextoDeAutorizacion, UnidadDeTrabajo


class VerTextoDeAutorizacion:
    def __init__(self, unidad: UnidadDeTrabajo) -> None:
        self._unidad = unidad

    async def ejecutar(
        self, tipo: Literal["datos", "ia"]
    ) -> tuple[TextoDeAutorizacion, ConsultorioPublico]:
        """El texto nombra al consultorio responsable: se entrega junto con sus datos."""
        async with self._unidad.abrir(None) as trabajo:
            texto = await trabajo.cuentas.texto_vigente(tipo)
            consultorio = await trabajo.consultorios.publico()
        return texto, consultorio
