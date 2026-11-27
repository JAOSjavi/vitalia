"""El indexador: deja cada documento legible listo para la búsqueda del asistente (HU-031, CA-7).

Parte cada página en fragmentos, tapa los identificadores del paciente y pide al proveedor el
vector de cada fragmento. Sin autorización de IA no se envía nada (CA-8): si el paciente la
retiró mientras el trabajo esperaba en la cola, el trabajo termina sin indexar.
"""

import logging

from vitalia.casos_de_uso.puertos import FragmentoNuevo, UnidadDeTrabajo, Vectorizador
from vitalia.dominio.fragmentos import partir_pagina, retirar_identificadores
from vitalia.dominio.identidad import SISTEMA

INTENTOS_MAXIMOS = 3

_registro = logging.getLogger(__name__)


class IndexarDocumentos:
    def __init__(self, unidad: UnidadDeTrabajo, vectores: Vectorizador) -> None:
        self._unidad = unidad
        self._vectores = vectores

    async def indexar_pendientes(self) -> int:
        """Indexa hasta vaciar la cola. Devuelve cuántos trabajos atendió."""
        atendidos = 0
        while await self.indexar_uno():
            atendidos += 1
        return atendidos

    async def indexar_uno(self) -> bool:
        """Toma un trabajo de la cola y lo indexa. Devuelve False si la cola estaba vacía."""
        async with self._unidad.abrir(SISTEMA) as trabajo:
            tomado = await trabajo.documentos.tomar_trabajo("indexar_documento")
            if tomado is None:
                return False
            documento = await trabajo.documentos.por_leer(tomado.documento_id)
            if not await trabajo.documentos.ia_autorizada(documento.paciente_id):
                await trabajo.documentos.terminar_trabajo(tomado.id)
                return True
            paginas = await trabajo.documentos.paginas(documento.id)
            paciente = await trabajo.fragmentos.identificadores(documento.paciente_id)

        trozos = [
            (pagina.numero, orden, trozo)
            for pagina in paginas
            for orden, trozo in enumerate(
                partir_pagina(retirar_identificadores(pagina.texto, paciente))
            )
        ]
        try:
            vectores = await self._vectores.vectorizar([trozo for _, _, trozo in trozos])
        except Exception as error:
            # Solo el tipo del error: el mensaje podría traer texto del documento.
            _registro.warning("No se pudo indexar un documento: %s", type(error).__name__)
            async with self._unidad.abrir(SISTEMA) as trabajo:
                await trabajo.documentos.terminar_trabajo(
                    tomado.id,
                    error=type(error).__name__,
                    reintentar=tomado.intentos < INTENTOS_MAXIMOS,
                )
            return True

        fragmentos = [
            FragmentoNuevo(pagina, orden, trozo, vector)
            for (pagina, orden, trozo), vector in zip(trozos, vectores, strict=True)
        ]
        async with self._unidad.abrir(SISTEMA) as trabajo:
            # Se vuelve a mirar: el paciente pudo retirar la autorización mientras se vectorizaba.
            if await trabajo.documentos.ia_autorizada(documento.paciente_id):
                await trabajo.fragmentos.reemplazar_del_documento(
                    documento.id, fragmentos, self._vectores.modelo
                )
            await trabajo.documentos.terminar_trabajo(tomado.id)
        return True
