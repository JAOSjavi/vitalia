"""Registro del paciente con sus autorizaciones, y entrada directa a su inicio (HU-002, HU-003)."""

from uuid import UUID

from vitalia.casos_de_uso.fichas import nueva_ficha
from vitalia.casos_de_uso.ingresar import SesionNueva
from vitalia.casos_de_uso.puertos import Contrasenas, Reloj, UnidadDeTrabajo
from vitalia.dominio.cuentas import COLOMBIA, DatosDelPaciente, revisar_paciente
from vitalia.dominio.ingreso import INACTIVIDAD_MAXIMA


class RegistrarPaciente:
    def __init__(self, unidad: UnidadDeTrabajo, contrasenas: Contrasenas, reloj: Reloj) -> None:
        self._unidad = unidad
        self._contrasenas = contrasenas
        self._reloj = reloj

    async def ejecutar(
        self,
        datos: DatosDelPaciente,
        contrasena: str,
        texto_datos: UUID,
        texto_ia: UUID | None,
    ) -> SesionNueva:
        """texto_ia es None si la persona no marcó la casilla de inteligencia artificial."""
        ahora = self._reloj.ahora()
        hoy = ahora.astimezone(COLOMBIA).date()
        datos = revisar_paciente(datos, contrasena, hoy)
        hash_contrasena = await self._contrasenas.cifrar(contrasena)

        ficha, huella = nueva_ficha()
        vence = ahora + INACTIVIDAD_MAXIMA
        async with self._unidad.abrir(None) as trabajo:
            usuario_id = await trabajo.cuentas.registrar_paciente(
                datos, hash_contrasena, texto_datos, texto_ia, hoy
            )
            await trabajo.cuentas.abrir_sesion(usuario_id, huella, ahora, vence)
        return SesionNueva(ficha, "paciente", vence)
