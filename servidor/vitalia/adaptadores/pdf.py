"""Lectura de PDF con pypdfium2, dentro del servidor (diseno/09-herramientas-y-entrega.md).

pdfium no se puede usar desde dos hilos a la vez: un candado deja pasar un PDF por vez, y el
trabajo corre fuera del hilo que atiende las peticiones.
"""

import asyncio
import struct
import threading
import zlib

import pypdfium2 as pdfium

_CANDADO = threading.Lock()

# 2 equivale a unos 144 puntos por pulgada: suficiente para reconocer letra impresa.
_ESCALA_DE_IMAGEN = 2


class LectorPdfium:
    async def textos(self, contenido: bytes) -> list[str]:
        return await asyncio.to_thread(_textos, contenido)

    async def imagen_de_pagina(self, contenido: bytes, numero: int) -> bytes:
        return await asyncio.to_thread(_imagen, contenido, numero)


def _textos(contenido: bytes) -> list[str]:
    with _CANDADO:
        documento = pdfium.PdfDocument(contenido)
        try:
            textos = []
            for pagina in documento:
                pagina_de_texto = pagina.get_textpage()
                textos.append(_limpio(pagina_de_texto.get_text_bounded()))
                pagina_de_texto.close()
                pagina.close()
            return textos
        finally:
            documento.close()


def _limpio(texto: str) -> str:
    # pdfium separa las líneas con \r\n y deja espacios al final.
    lineas = [linea.rstrip() for linea in texto.replace("\r\n", "\n").split("\n")]
    return "\n".join(lineas).strip()


def _imagen(contenido: bytes, numero: int) -> bytes:
    with _CANDADO:
        documento = pdfium.PdfDocument(contenido)
        try:
            pagina = documento[numero - 1]
            mapa = pagina.render(scale=_ESCALA_DE_IMAGEN, grayscale=True)
            ancho, alto, paso = mapa.width, mapa.height, mapa.stride
            datos = bytes(mapa.buffer)
            mapa.close()
            pagina.close()
        finally:
            documento.close()
    return _png_gris(datos, ancho, alto, paso)


def _png_gris(datos: bytes, ancho: int, alto: int, paso: int) -> bytes:
    """Arma un PNG en escala de grises sin depender de una biblioteca de imágenes."""
    filas = b"".join(b"\x00" + datos[fila * paso : fila * paso + ancho] for fila in range(alto))

    def bloque(tipo: bytes, cuerpo: bytes) -> bytes:
        return (
            struct.pack(">I", len(cuerpo))
            + tipo
            + cuerpo
            + struct.pack(">I", zlib.crc32(tipo + cuerpo) & 0xFFFFFFFF)
        )

    cabecera = struct.pack(">IIBBBBB", ancho, alto, 8, 0, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + bloque(b"IHDR", cabecera)
        + bloque(b"IDAT", zlib.compress(filas, 6))
        + bloque(b"IEND", b"")
    )
