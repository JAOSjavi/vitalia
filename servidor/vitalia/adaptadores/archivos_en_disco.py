"""Archivos en una carpeta del computador, para programar sin la nube.

Cumple el mismo puerto que el almacenamiento S3 de Cloudflare R2, que lo reemplaza al publicar.
La carpeta queda fuera del repositorio y no se sirve por ninguna ruta.
"""

import asyncio
from pathlib import Path


class ArchivosEnDisco:
    def __init__(self, carpeta: Path) -> None:
        self._carpeta = carpeta.resolve()

    def _ruta(self, clave: str) -> Path:
        ruta = (self._carpeta / clave).resolve()
        # Una clave con ".." no puede salir de la carpeta.
        if not ruta.is_relative_to(self._carpeta):
            raise ValueError("Clave de archivo inválida")
        return ruta

    async def guardar(self, clave: str, contenido: bytes) -> None:
        ruta = self._ruta(clave)

        def _escribir() -> None:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            # Primero a un archivo temporal: si algo falla, no queda un archivo a medias.
            temporal = ruta.with_suffix(ruta.suffix + ".parcial")
            temporal.write_bytes(contenido)
            temporal.replace(ruta)

        await asyncio.to_thread(_escribir)

    async def leer(self, clave: str) -> bytes:
        return await asyncio.to_thread(self._ruta(clave).read_bytes)

    async def borrar(self, clave: str) -> None:
        await asyncio.to_thread(self._ruta(clave).unlink, missing_ok=True)
