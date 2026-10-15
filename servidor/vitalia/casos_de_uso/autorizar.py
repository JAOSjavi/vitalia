"""Paso común a todas las operaciones: el rol debe tener el permiso en la matriz (HU-006)."""

from vitalia.casos_de_uso.puertos import UnidadDeTrabajo
from vitalia.dominio.identidad import SISTEMA, Identidad
from vitalia.dominio.permisos import AccesoDenegado, MatrizDePermisos


class Autorizador:
    def __init__(self, unidad: UnidadDeTrabajo) -> None:
        self._unidad = unidad
        self._matriz: MatrizDePermisos | None = None

    async def exigir(self, identidad: Identidad, permiso: str) -> None:
        matriz = await self._cargada()
        if matriz.permite(identidad.clase, permiso):
            return
        # La operación negada no llega a abrir su transacción: el intento se anota en una propia.
        async with self._unidad.abrir(identidad) as trabajo:
            await trabajo.bitacora.registrar("acceso_denegado", objeto=permiso)
        raise AccesoDenegado(permiso)

    async def _cargada(self) -> MatrizDePermisos:
        # Se lee una vez: la matriz solo cambia con un despliegue.
        if self._matriz is None:
            async with self._unidad.abrir(SISTEMA) as trabajo:
                self._matriz = await trabajo.permisos.matriz()
        return self._matriz
