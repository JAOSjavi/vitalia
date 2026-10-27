"""El lector en segundo plano: corre dentro del servicio de la API (arquitectura, sección 3.5).

Revisa la cola cada pocos segundos. Si un ciclo falla, lo anota y sigue: un documento dañado
no puede detener la lectura de los demás.
"""

import asyncio
import logging

from vitalia.casos_de_uso.leer_documentos import LeerDocumentos

SEGUNDOS_ENTRE_REVISIONES = 3

_registro = logging.getLogger(__name__)


async def leer_en_segundo_plano(lector: LeerDocumentos) -> None:
    while True:
        try:
            await lector.leer_pendientes()
        except Exception as error:
            _registro.warning("El lector falló en un ciclo: %s", type(error).__name__)
        await asyncio.sleep(SEGUNDOS_ENTRE_REVISIONES)
