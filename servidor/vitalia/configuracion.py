"""Configuración del servidor. Sale de las variables de entorno; en local, del archivo .env."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Configuracion:
    bd_url: str
    sesion_secreto: str
    # Dirección de las pantallas: con ella se arman los enlaces que se entregan.
    sitio_url: str = "http://localhost:5173"


def leer() -> Configuracion:
    load_dotenv()
    return Configuracion(
        bd_url=_obligatoria("BD_URL"),
        sesion_secreto=_obligatoria("SESION_SECRETO"),
        sitio_url=os.environ.get("SITIO_URL") or Configuracion.sitio_url,
    )


def _obligatoria(nombre: str) -> str:
    valor = os.environ.get(nombre)
    if not valor:
        raise RuntimeError(f"Falta la variable de entorno {nombre}. Ver servidor/.env.example")
    return valor
