"""Proveedor de IA de mentira, con respuestas fijas. Para pruebas y para trabajar sin clave."""

from collections.abc import AsyncIterator, Sequence

from vitalia.casos_de_uso.puertos import Turno


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
