"""Proveedor de IA de mentira, con respuestas fijas. Para pruebas y para trabajar sin clave."""

import hashlib
import math
import re
import unicodedata
from collections.abc import AsyncIterator, Sequence

from vitalia.casos_de_uso.puertos import Turno


class VectoresDeMentira:
    """Vectores que salen de las palabras: textos con palabras en común quedan cerca.

    No entiende sinónimos, como sí lo hace un modelo de verdad, pero sirve para probar la
    búsqueda sin clave y sin enviar nada afuera.
    """

    modelo = "de-mentira"

    def __init__(self, dimensiones: int = 1024) -> None:
        self._dimensiones = dimensiones

    async def vectorizar(self, textos: Sequence[str]) -> list[list[float]]:
        return [self._vector(texto) for texto in textos]

    def _vector(self, texto: str) -> list[float]:
        vector = [0.0] * self._dimensiones
        sin_tildes = unicodedata.normalize("NFD", texto.lower())
        for palabra in re.findall(r"\w+", sin_tildes.encode("ascii", "ignore").decode()):
            if len(palabra) < 3:
                continue
            posicion = int.from_bytes(hashlib.sha256(palabra.encode()).digest()[:4], "big")
            vector[posicion % self._dimensiones] += 1.0
        norma = math.sqrt(sum(n * n for n in vector)) or 1.0
        # Un vector en cero no tiene dirección: pgvector no puede medir su distancia.
        return (
            [n / norma for n in vector] if any(vector) else [1.0] + [0.0] * (self._dimensiones - 1)
        )


class IADeMentira:
    def __init__(
        self,
        texto_de_pagina: str = "Texto de prueba de una página.",
        partes_de_respuesta: Sequence[str] = ("No aparece ", "en los documentos."),
    ) -> None:
        self._texto_de_pagina = texto_de_pagina
        self._partes_de_respuesta = partes_de_respuesta

    async def leer_pagina(self, imagen: bytes) -> str:
        return self._texto_de_pagina

    async def responder(self, instrucciones: str, turnos: Sequence[Turno]) -> AsyncIterator[str]:
        for parte in self._partes_de_respuesta:
            yield parte
