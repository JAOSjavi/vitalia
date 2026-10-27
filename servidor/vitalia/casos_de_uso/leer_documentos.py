"""El lector: pasa cada documento de la cola a texto, página por página (HU-031).

Un PDF con texto se lee dentro del servidor. Un escaneado o una foto necesita que un modelo
reconozca el texto en la imagen, y eso solo se hace si el paciente autorizó la IA (CA-6).
Si el documento quedó legible y el paciente autorizó la IA, se encola su indexación (CA-7, CA-8).
"""

import logging
from dataclasses import dataclass

from vitalia.casos_de_uso.puertos import (
    Archivos,
    DocumentoPorLeer,
    LectorDePDF,
    PaginaLeida,
    ProveedorIA,
    UnidadDeTrabajo,
)
from vitalia.dominio.documentos import EstadoDeLectura, estado_final, legibilidad, tiene_texto
from vitalia.dominio.identidad import SISTEMA

INTENTOS_MAXIMOS = 3

_registro = logging.getLogger(__name__)


class SinProveedorDeLectura(Exception):
    """Hace falta reconocer el texto de una imagen y no hay un modelo configurado."""


@dataclass(frozen=True)
class Lectura:
    """Cómo terminó un documento. Sin páginas significa que espera la autorización de la IA."""

    paginas: list[PaginaLeida]
    espera_autorizacion: bool = False


class LeerDocumentos:
    def __init__(
        self,
        unidad: UnidadDeTrabajo,
        archivos: Archivos,
        pdf: LectorDePDF,
        ia: ProveedorIA | None,
    ) -> None:
        self._unidad = unidad
        self._archivos = archivos
        self._pdf = pdf
        self._ia = ia

    async def leer_pendientes(self) -> int:
        """Lee hasta vaciar la cola. Devuelve cuántos documentos procesó."""
        procesados = 0
        while await self.leer_uno():
            procesados += 1
        return procesados

    async def leer_uno(self) -> bool:
        """Toma un trabajo de la cola y lo lee. Devuelve False si la cola estaba vacía."""
        async with self._unidad.abrir(SISTEMA) as trabajo:
            tomado = await trabajo.documentos.tomar_trabajo("leer")
            if tomado is None:
                return False
            documento = await trabajo.documentos.por_leer(tomado.documento_id)
            autorizada = await trabajo.documentos.ia_autorizada(documento.paciente_id)

        try:
            lectura = await self._leer(documento, autorizada)
        except Exception as error:
            reintentar = tomado.intentos < INTENTOS_MAXIMOS and not isinstance(
                error, SinProveedorDeLectura
            )
            # Solo el tipo del error: el mensaje podría traer texto del documento.
            _registro.warning("No se pudo leer un documento: %s", type(error).__name__)
            if reintentar:
                estado: EstadoDeLectura = "en_proceso"
            elif isinstance(error, SinProveedorDeLectura):
                # No es culpa del documento: se podrá leer cuando haya un modelo configurado.
                estado = "sin_leer"
            else:
                estado = "no_legible"
            async with self._unidad.abrir(SISTEMA) as trabajo:
                await trabajo.documentos.terminar_trabajo(
                    tomado.id, error=type(error).__name__, reintentar=reintentar
                )
                await trabajo.documentos.marcar(documento.id, estado)
            return True

        async with self._unidad.abrir(SISTEMA) as trabajo:
            if lectura.espera_autorizacion:
                # Cuando el paciente autorice la IA, el documento vuelve a la cola.
                await trabajo.documentos.marcar(documento.id, "sin_leer")
            else:
                estado = estado_final([p.texto for p in lectura.paginas])
                await trabajo.documentos.guardar_paginas(documento.id, lectura.paginas)
                await trabajo.documentos.marcar(documento.id, estado, len(lectura.paginas))
                if estado == "legible" and autorizada:
                    await trabajo.documentos.encolar(documento.id, "indexar_documento")
            await trabajo.documentos.terminar_trabajo(tomado.id)
        return True

    async def _leer(self, documento: DocumentoPorLeer, autorizada: bool) -> Lectura:
        contenido = await self._archivos.leer(documento.clave_archivo)
        if documento.formato != "pdf":
            if not autorizada:
                return Lectura([], espera_autorizacion=True)
            texto = await self._reconocer(contenido)
            return Lectura([PaginaLeida(1, texto, "reconocido", legibilidad(texto))])

        textos = await self._pdf.textos(contenido)
        sin_texto = [numero for numero, texto in enumerate(textos, 1) if not tiene_texto(texto)]
        if sin_texto and not autorizada:
            if len(sin_texto) == len(textos):
                # Todo el PDF es escaneado: nada sale hacia el proveedor sin autorización.
                return Lectura([], espera_autorizacion=True)
            # Mezcla de páginas con y sin texto: se guarda lo que el PDF trae.
            sin_texto = []

        paginas = []
        for numero, texto in enumerate(textos, 1):
            if numero in sin_texto:
                imagen = await self._pdf.imagen_de_pagina(contenido, numero)
                reconocido = await self._reconocer(imagen)
                paginas.append(
                    PaginaLeida(numero, reconocido, "reconocido", legibilidad(reconocido))
                )
            else:
                paginas.append(PaginaLeida(numero, texto, "pdf", 1.0))
        return Lectura(paginas)

    async def _reconocer(self, imagen: bytes) -> str:
        if self._ia is None:
            raise SinProveedorDeLectura()
        return await self._ia.leer_pagina(imagen)
