"""El lector en segundo plano sigue tras un error y se detiene cuando se apaga la API."""

import asyncio
from typing import cast

import pytest

from vitalia.casos_de_uso.indexar_documentos import IndexarDocumentos
from vitalia.casos_de_uso.leer_documentos import LeerDocumentos
from vitalia.entrada import lector as modulo


class LectorQueFalla:
    """Falla en el primer ciclo; en el segundo espera, y al cancelarlo responde con otro error,
    como la base cuando se la interrumpe a medio conectar."""

    def __init__(self) -> None:
        self.ciclos = 0
        self.esperando = asyncio.Event()

    async def leer_pendientes(self) -> int:
        self.ciclos += 1
        if self.ciclos == 1:
            raise RuntimeError("documento dañado")
        self.esperando.set()
        try:
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            raise ConnectionError("conexión interrumpida") from None
        return 0


class IndexadorQuieto:
    async def indexar_pendientes(self) -> int:
        return 0


async def test_sigue_despues_de_un_error_y_se_detiene_al_cancelarlo(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(modulo, "SEGUNDOS_ENTRE_REVISIONES", 0)
    falla = LectorQueFalla()
    tarea = asyncio.create_task(
        modulo.leer_en_segundo_plano(
            cast(LeerDocumentos, falla), cast(IndexarDocumentos, IndexadorQuieto())
        )
    )
    await asyncio.wait_for(falla.esperando.wait(), timeout=2)  # ya pasó el error del primero

    tarea.cancel()

    with pytest.raises(ConnectionError):
        await asyncio.wait_for(tarea, timeout=2)
