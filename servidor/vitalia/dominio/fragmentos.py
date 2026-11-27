"""Fragmentos que busca el asistente (D-30): cómo se parte una página y qué se tapa antes.

Un fragmento sale de una sola página, para saber siempre de dónde salió. Se corta en un fin de
párrafo o de frase, y repite el final del anterior para no partir un dato en dos.
"""

import re
import unicodedata
from dataclasses import dataclass

TOPE = 1000
REPETIDO = 150


class IANoAutorizada(Exception):
    """El paciente no ha autorizado el uso de IA: el asistente no trabaja con sus datos."""


# Un fin de frase: punto, signo de cierre o salto de línea, seguido de espacio o de otra línea.
# Va entre paréntesis para conservar el separador y volver a unir las frases como estaban.
_FIN_DE_FRASE = re.compile(r"((?<=[.!?:;])\s+|\n+)")


def partir_pagina(texto: str, tope: int = TOPE, repetido: int = REPETIDO) -> list[str]:
    """Trozos de hasta `tope` caracteres, sin cruzar de página. Se llama una vez por página."""
    texto = texto.strip()
    if not texto:
        return []
    if len(texto) <= tope:
        return [texto]

    trozos: list[str] = []
    actual = ""
    for union, frase in _frases(texto, tope):
        if actual and len(actual) + 1 + len(frase) > tope:
            trozos.append(actual)
            cola = _cola(actual, repetido)
            # Si la frase siguiente es muy larga, no se repite nada: ningún trozo pasa del tope.
            actual = cola if len(cola) + 1 + len(frase) <= tope else ""
        actual = f"{actual}{union}{frase}" if actual else frase
    if actual:
        trozos.append(actual)
    return trozos


def _frases(texto: str, tope: int) -> list[tuple[str, str]]:
    """Cada frase con lo que la unía a la anterior: un salto de línea o un espacio."""
    piezas = _FIN_DE_FRASE.split(texto)
    resultado: list[tuple[str, str]] = []
    union = ""
    for posicion, pieza in enumerate(piezas):
        if posicion % 2:  # separador
            union = "\n" if "\n" in pieza else " "
            continue
        frase = pieza.strip()
        # Una frase más larga que el tope se parte en palabras, para que ningún trozo se pase.
        while len(frase) > tope:
            corte = frase.rfind(" ", 0, tope)
            corte = corte if corte > 0 else tope
            resultado.append((union, frase[:corte].strip()))
            frase, union = frase[corte:].strip(), " "
        if frase:
            resultado.append((union, frase))
    return resultado


def _cola(trozo: str, repetido: int) -> str:
    """El final del trozo que se repite al comienzo del siguiente, empezando en una palabra."""
    if len(trozo) <= repetido:
        return trozo
    cola = trozo[-repetido:]
    espacio = cola.find(" ")
    return cola[espacio + 1 :] if espacio >= 0 else cola


@dataclass(frozen=True)
class Identificadores:
    """Lo que identifica al paciente directamente. Nunca sale hacia el proveedor (A.8.11)."""

    nombres: str
    apellidos: str
    numero_documento: str
    telefono: str | None
    correo: str | None


ROTULO_PACIENTE = "[PACIENTE]"
ROTULO_DOCUMENTO = "[DOCUMENTO]"
ROTULO_TELEFONO = "[TELÉFONO]"
ROTULO_CORREO = "[CORREO]"


def retirar_identificadores(texto: str, paciente: Identificadores) -> str:
    """Reemplaza por rótulos el nombre, el documento, el teléfono y el correo del paciente.

    Encuentra el nombre con o sin tildes y en mayúsculas o minúsculas, y los números aunque
    estén escritos con puntos o espacios: "79.482.615" o "310 482 7713".
    """
    if paciente.correo:
        texto = re.sub(re.escape(paciente.correo), ROTULO_CORREO, texto, flags=re.IGNORECASE)
    texto = _tapar_numero(texto, paciente.numero_documento, ROTULO_DOCUMENTO)
    if paciente.telefono:
        texto = _tapar_numero(texto, paciente.telefono, ROTULO_TELEFONO)

    completo = f"{paciente.nombres} {paciente.apellidos}"
    # Del más largo al más corto: primero el nombre completo, luego cada parte suelta.
    partes = sorted(
        {completo, paciente.nombres, paciente.apellidos, *completo.split()},
        key=len,
        reverse=True,
    )
    for parte in partes:
        if len(parte) >= 3:
            texto = _patron_de_nombre(parte).sub(ROTULO_PACIENTE, texto)
    # "[PACIENTE] [PACIENTE]" queda de tapar nombres y apellidos por separado.
    return re.sub(r"\[PACIENTE\](?:\s+\[PACIENTE\])+", ROTULO_PACIENTE, texto)


def _tapar_numero(texto: str, numero: str, rotulo: str) -> str:
    digitos = re.sub(r"\D", "", numero)
    if len(digitos) < 6:
        return texto
    separador = r"[\s.\-]?"
    patron = r"(?<!\d)" + separador.join(re.escape(d) for d in digitos) + r"(?!\d)"
    return re.sub(patron, rotulo, texto)


def _sin_tilde(letra: str) -> str:
    return unicodedata.normalize("NFD", letra)[0]


def _patron_de_nombre(nombre: str) -> re.Pattern[str]:
    """Cada letra acepta su versión con o sin tilde; las palabras se separan con espacios."""
    piezas = []
    for letra in nombre:
        if letra.isspace():
            piezas.append(r"\s+")
            continue
        base = _sin_tilde(letra.lower())
        variantes = {letra.lower(), base} | {
            c for c in "áéíóúüñ" if _sin_tilde(c) == base and c != base
        }
        if base == "n":
            variantes.add("ñ")
        piezas.append("[" + "".join(sorted(re.escape(v) for v in variantes)) + "]")
    return re.compile(r"(?<!\w)" + "".join(piezas) + r"(?!\w)", re.IGNORECASE)
