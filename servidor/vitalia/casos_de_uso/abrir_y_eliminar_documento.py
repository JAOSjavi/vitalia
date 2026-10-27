"""Abrir un documento (HU-029 CA-2, HU-030) y eliminarlo (HU-029 CA-3).

El paciente abre los suyos y la médica los de cualquier paciente: los permisos por fila deciden
qué ve cada uno, y lo que no puede ver responde como si no existiera. Abrir y eliminar quedan en
la bitácora.

Mientras los archivos estén en la carpeta local, el servidor los entrega con la sesión. Con
Cloudflare R2 se entregará un enlace firmado que vence en 15 minutos (HU-027).
"""

from dataclasses import dataclass
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Archivos, UnidadDeTrabajo
from vitalia.dominio.documentos import Formato
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.identidad import Identidad


@dataclass(frozen=True)
class ArchivoAbierto:
    nombre: str
    formato: Formato
    contenido: bytes


class AbrirDocumento:
    def __init__(
        self, unidad: UnidadDeTrabajo, autorizador: Autorizador, archivos: Archivos
    ) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._archivos = archivos

    async def ejecutar(self, identidad: Identidad, documento_id: UUID) -> ArchivoAbierto:
        permiso = "documentos.ver" if identidad.clase == "paciente" else "pacientes.ver"
        await self._autorizador.exigir(identidad, permiso)
        async with self._unidad.abrir(identidad) as trabajo:
            documento = await trabajo.documentos.para_abrir(documento_id)
            if documento is None:
                raise NoEncontrado()
            await trabajo.bitacora.registrar(
                "documento_abierto", paciente_id=documento.paciente_id, objeto=str(documento_id)
            )
        contenido = await self._archivos.leer(documento.clave_archivo)
        return ArchivoAbierto(documento.nombre, documento.formato, contenido)


class EliminarDocumento:
    def __init__(
        self, unidad: UnidadDeTrabajo, autorizador: Autorizador, archivos: Archivos
    ) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._archivos = archivos

    async def ejecutar(self, identidad: Identidad, documento_id: UUID) -> None:
        await self._autorizador.exigir(identidad, "documentos.eliminar")
        async with self._unidad.abrir(identidad) as trabajo:
            clave = await trabajo.documentos.eliminar(documento_id)
            if clave is None:
                raise NoEncontrado()
            await trabajo.bitacora.registrar("documento_eliminado", objeto=str(documento_id))
        # Después de confirmar en la base: si falla, queda un archivo sin dueño, nunca una fila
        # que apunte a un archivo que ya no está.
        await self._archivos.borrar(clave)
