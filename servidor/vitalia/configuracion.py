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
    # Proveedor de IA. Sin dirección o sin clave, los vectores salen de las palabras.
    ia_direccion: str | None = None
    ia_clave: str | None = None
    ia_modelo_vectores: str = "qwen3.7-text-embedding"
    ia_dimensiones: int = 1024
    ia_modelo_respuestas: str = "qwen3.7-plus"
    ia_modelo_lectura: str = "qwen-vl-ocr-2025-11-20"
    # Máximo de texto de los fragmentos en una pregunta, en caracteres.
    ia_tope_contexto: int = 16000
    ia_tope_consultas_hora: int = 30


def leer() -> Configuracion:
    load_dotenv()
    carpeta = os.environ.get("ARCHIVOS_CARPETA")
    return Configuracion(
        bd_url=_obligatoria("BD_URL"),
        sesion_secreto=_obligatoria("SESION_SECRETO"),
        sitio_url=os.environ.get("SITIO_URL") or Configuracion.sitio_url,
        carpeta_de_archivos=Path(carpeta) if carpeta else _CARPETA_DE_ARCHIVOS,
        ia_direccion=os.environ.get("IA_DIRECCION") or None,
        ia_clave=os.environ.get("IA_CLAVE") or None,
        ia_modelo_vectores=os.environ.get("IA_MODELO_VECTORES") or Configuracion.ia_modelo_vectores,
        ia_dimensiones=int(os.environ.get("IA_DIMENSIONES") or Configuracion.ia_dimensiones),
        ia_modelo_respuestas=os.environ.get("IA_MODELO_RESPUESTAS")
        or Configuracion.ia_modelo_respuestas,
        ia_modelo_lectura=os.environ.get("IA_MODELO_LECTURA") or Configuracion.ia_modelo_lectura,
        ia_tope_contexto=int(os.environ.get("IA_TOPE_CONTEXTO") or Configuracion.ia_tope_contexto),
        ia_tope_consultas_hora=int(
            os.environ.get("IA_TOPE_CONSULTAS_HORA") or Configuracion.ia_tope_consultas_hora
        ),
    )


def _obligatoria(nombre: str) -> str:
    valor = os.environ.get(nombre)
    if not valor:
        raise RuntimeError(f"Falta la variable de entorno {nombre}. Ver servidor/.env.example")
    return valor
