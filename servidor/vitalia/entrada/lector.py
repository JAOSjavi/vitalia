"""El lector en segundo plano: corre dentro del servicio de la API (arquitectura, sección 3.5).

Revisa la cola cada pocos segundos: primero lee lo que se subió y después indexa lo que quedó
legible. Si un ciclo falla, lo anota y sigue: un documento dañado no detiene a los demás.
"""

import asyncio
import logging

from vitalia.casos_de_uso.indexar_documentos import IndexarDocumentos
from vitalia.casos_de_uso.leer_documentos import LeerDocumentos

SEGUNDOS_ENTRE_REVISIONES = 3

_registro = logging.getLogger(__name__)


async def leer_en_segundo_plano(lector: LeerDocumentos, indexador: IndexarDocumentos) -> None:
    while True:
        try:
            await lector.leer_pendientes()
            await indexador.indexar_pendientes()
        except Exception as error:
            # Al apagar la API la cancelación puede llegar envuelta en un error de la base:
            # si la tarea se está cancelando, se deja salir en vez de seguir el ciclo.
            tarea = asyncio.current_task()
            if tarea is not None and tarea.cancelling():
                raise
            _registro.warning("El lector falló en un ciclo: %s", type(error).__name__)
        await asyncio.sleep(SEGUNDOS_ENTRE_REVISIONES)
