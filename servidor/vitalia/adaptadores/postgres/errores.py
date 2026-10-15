"""Traduce los rechazos de la base a los errores del dominio."""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.exc import DBAPIError

from vitalia.dominio.cuentas import (
    AutorizacionDesactualizada,
    DocumentoYaRegistrado,
    EnlaceInvalido,
    MenorDeEdad,
    YaHayMedico,
)

# Palabra que aparece en el mensaje de la base y error que le corresponde.
_TRADUCCIONES: tuple[tuple[str, type[Exception]], ...] = (
    ("menor_de_edad", MenorDeEdad),
    ("texto_desactualizado", AutorizacionDesactualizada),
    ("enlace_invalido", EnlaceInvalido),
    ("ya_hay_medico", YaHayMedico),
    ("un_solo_medico", YaHayMedico),
    ("usuarios_tipo_documento_numero_documento_key", DocumentoYaRegistrado),
)


@contextmanager
def traducir_errores() -> Iterator[None]:
    try:
        yield
    except DBAPIError as error:
        mensaje = str(error.orig)
        for palabra, traduccion in _TRADUCCIONES:
            if palabra in mensaje:
                raise traduccion() from error
        raise
