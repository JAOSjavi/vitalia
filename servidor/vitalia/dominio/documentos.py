"""Reglas de los documentos que sube el paciente (HU-028) y de su lectura (HU-031)."""

import hashlib
from dataclasses import dataclass
from datetime import date
from typing import Literal
from uuid import UUID

from vitalia.dominio.cuentas import DatosInvalidos

Formato = Literal["pdf", "jpg", "png"]
TipoDeDocumento = Literal["historia_clinica", "examen", "formula", "imagen", "otro"]
EstadoDeLectura = Literal["sin_leer", "en_proceso", "legible", "no_legible"]

TIPOS: tuple[TipoDeDocumento, ...] = ("historia_clinica", "examen", "formula", "imagen", "otro")
TAMANO_MAXIMO = 20 * 1024 * 1024
LARGO_MAXIMO_DEL_NOMBRE = 120

# Una página con menos letras que esto no cuenta como leída: suele ser un escaneado, una
# página en blanco o solo un sello. El valor se ajusta en la prueba de concepto.
LETRAS_MINIMAS_POR_PAGINA = 40


class DocumentoRepetido(Exception):
    """El paciente ya subió ese mismo archivo. Reintentar una carga no deja copias."""

    def __init__(self, documento_id: UUID) -> None:
        super().__init__("El documento ya existe")
        self.documento_id = documento_id


@dataclass(frozen=True)
class ArchivoRecibido:
    nombre: str
    fecha_documento: date
    tipo: TipoDeDocumento
    contenido: bytes


@dataclass(frozen=True)
class ArchivoValido:
    nombre: str
    fecha_documento: date
    tipo: TipoDeDocumento
    contenido: bytes
    formato: Formato
    huella: str


def formato_por_contenido(contenido: bytes) -> Formato | None:
    """Se mira el contenido y no la extensión del nombre, que cualquiera puede cambiar."""
    if contenido.startswith(b"%PDF-"):
        return "pdf"
    if contenido.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if contenido.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    return None


def validar_archivo(archivo: ArchivoRecibido, hoy: date) -> ArchivoValido:
    """Lanza DatosInvalidos con el motivo de cada campo rechazado (HU-028, CA-2)."""
    campos: dict[str, str] = {}
    nombre = archivo.nombre.strip()
    if not nombre:
        campos["nombre"] = "Escriba el nombre del documento"
    elif len(nombre) > LARGO_MAXIMO_DEL_NOMBRE:
        campos["nombre"] = f"El nombre puede tener hasta {LARGO_MAXIMO_DEL_NOMBRE} letras"
    if archivo.fecha_documento > hoy:
        campos["fecha_documento"] = "La fecha del documento no puede ser futura"
    if archivo.tipo not in TIPOS:
        campos["tipo"] = "Elija el tipo de documento"

    formato = formato_por_contenido(archivo.contenido)
    if not archivo.contenido:
        campos["archivo"] = "El archivo está vacío"
    elif len(archivo.contenido) > TAMANO_MAXIMO:
        campos["archivo"] = "El archivo pesa más de 20 MB"
    elif formato is None:
        campos["archivo"] = "Solo se aceptan archivos PDF, JPG o PNG"

    if campos:
        raise DatosInvalidos(campos)
    assert formato is not None
    return ArchivoValido(
        nombre=nombre,
        fecha_documento=archivo.fecha_documento,
        tipo=archivo.tipo,
        contenido=archivo.contenido,
        formato=formato,
        huella=hashlib.sha256(archivo.contenido).hexdigest(),
    )


def tiene_texto(texto: str) -> bool:
    """Si una página trae texto suficiente para no tener que reconocerlo en la imagen."""
    return sum(caracter.isalnum() for caracter in texto) >= LETRAS_MINIMAS_POR_PAGINA


def legibilidad(texto: str) -> float:
    """De 0 a 1: qué parte de las palabras se pudo leer. El modelo marca las demás [ilegible]."""
    palabras = texto.split()
    if not palabras:
        return 0.0
    ilegibles = sum("[ilegible]" in palabra for palabra in palabras)
    return 1 - ilegibles / len(palabras)


def estado_final(paginas: list[str]) -> EstadoDeLectura:
    """Legible si al menos una página trae texto; si ninguna, no legible (HU-031, CA-3)."""
    return "legible" if any(tiene_texto(texto) for texto in paginas) else "no_legible"
