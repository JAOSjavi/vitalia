"""Tipos de cita y su duración (HU-010): ver, crear y editar.

Tres operaciones pequeñas sobre el mismo catálogo; la duración de una cita ya creada no cambia
al editar el tipo, porque cada cita guarda su propio inicio y fin (CA-2).
"""

from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import UnidadDeTrabajo
from vitalia.dominio.agenda import TipoDeCita
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.identidad import Identidad

DURACION_MINIMA = 5
DURACION_MAXIMA = 240


def _revisar(nombre: str, duracion_minutos: int) -> str:
    nombre = nombre.strip()
    campos = {}
    if not nombre:
        campos["nombre"] = "Escriba el nombre del tipo de cita"
    if not DURACION_MINIMA <= duracion_minutos <= DURACION_MAXIMA:
        campos["duracion_minutos"] = (
            f"La duración va de {DURACION_MINIMA} a {DURACION_MAXIMA} minutos"
        )
    if campos:
        raise DatosInvalidos(campos)
    return nombre


class TiposDeCita:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ver(self, identidad: Identidad) -> list[TipoDeCita]:
        """El paciente solo ve los que se ofrecen; el médico, todos."""
        await self._autorizador.exigir(identidad, "tipos_cita.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.agenda.tipos(solo_activos=identidad.clase == "paciente")

    async def crear(self, identidad: Identidad, nombre: str, duracion_minutos: int) -> TipoDeCita:
        await self._autorizador.exigir(identidad, "tipos_cita.editar")
        nombre = _revisar(nombre, duracion_minutos)
        async with self._unidad.abrir(identidad) as trabajo:
            tipo = await trabajo.agenda.crear_tipo(nombre, duracion_minutos)
            await trabajo.bitacora.registrar("creacion_de_tipo_de_cita", objeto=str(tipo.id))
        return tipo

    async def editar(
        self,
        identidad: Identidad,
        tipo_id: UUID,
        nombre: str | None = None,
        duracion_minutos: int | None = None,
        activo: bool | None = None,
    ) -> TipoDeCita:
        await self._autorizador.exigir(identidad, "tipos_cita.editar")
        async with self._unidad.abrir(identidad) as trabajo:
            actual = await trabajo.agenda.tipo(tipo_id)
            if actual is None:
                raise NoEncontrado()
            nuevo = TipoDeCita(
                id=actual.id,
                nombre=_revisar(
                    actual.nombre if nombre is None else nombre,
                    actual.duracion_minutos if duracion_minutos is None else duracion_minutos,
                ),
                duracion_minutos=(
                    actual.duracion_minutos if duracion_minutos is None else duracion_minutos
                ),
                activo=actual.activo if activo is None else activo,
            )
            await trabajo.agenda.guardar_tipo(nuevo)
            await trabajo.bitacora.registrar("edicion_de_tipo_de_cita", objeto=str(tipo_id))
        return nuevo
