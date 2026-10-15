"""El médico crea su cuenta con el enlace de puesta en marcha y entra (HU-001, CA-1 y CA-3)."""

from vitalia.casos_de_uso.fichas import huella_de, nueva_ficha
from vitalia.casos_de_uso.ingresar import SesionNueva
from vitalia.casos_de_uso.puertos import Contrasenas, Reloj, UnidadDeTrabajo
from vitalia.dominio.cuentas import DatosDelMedico, revisar_medico
from vitalia.dominio.ingreso import INACTIVIDAD_MAXIMA


class PonerEnMarcha:
    def __init__(self, unidad: UnidadDeTrabajo, contrasenas: Contrasenas, reloj: Reloj) -> None:
        self._unidad = unidad
        self._contrasenas = contrasenas
        self._reloj = reloj

    async def ejecutar(
        self, ficha_del_enlace: str, datos: DatosDelMedico, contrasena: str
    ) -> SesionNueva:
        datos = revisar_medico(datos, contrasena)
        hash_contrasena = await self._contrasenas.cifrar(contrasena)

        ahora = self._reloj.ahora()
        ficha, huella = nueva_ficha()
        vence = ahora + INACTIVIDAD_MAXIMA
        async with self._unidad.abrir(None) as trabajo:
            usuario_id = await trabajo.cuentas.usar_enlace_de_puesta_en_marcha(
                huella_de(ficha_del_enlace), ahora, datos, hash_contrasena
            )
            await trabajo.cuentas.abrir_sesion(usuario_id, huella, ahora, vence)
        return SesionNueva(ficha, "medico", vence)
