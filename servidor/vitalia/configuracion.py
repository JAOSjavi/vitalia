"""Configuración del servidor. Sale de las variables de entorno; en local, del archivo .env."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Para programar sin la nube, los archivos van a esta carpeta, que no entra al repositorio.
_CARPETA_DE_ARCHIVOS = Path(__file__).parent.parent / ".archivos"


@dataclass(frozen=True)
class Configuracion:
    bd_url: str
    sesion_secreto: str
    # Dirección de las pantallas: con ella se arman los enlaces que se entregan.
    sitio_url: str = "http://localhost:5173"
    carpeta_de_archivos: Path = _CARPETA_DE_ARCHIVOS
    # Las pruebas lo apagan y llaman al lector cuando lo necesitan.
    lector_en_segundo_plano: bool = True


def leer() -> Configuracion:
    load_dotenv()
    carpeta = os.environ.get("ARCHIVOS_CARPETA")
    return Configuracion(
        bd_url=_obligatoria("BD_URL"),
        sesion_secreto=_obligatoria("SESION_SECRETO"),
        sitio_url=os.environ.get("SITIO_URL") or Configuracion.sitio_url,
        carpeta_de_archivos=Path(carpeta) if carpeta else _CARPETA_DE_ARCHIVOS,
    )


def _obligatoria(nombre: str) -> str:
    valor = os.environ.get(nombre)
    if not valor:
        raise RuntimeError(f"Falta la variable de entorno {nombre}. Ver servidor/.env.example")
    return valor
