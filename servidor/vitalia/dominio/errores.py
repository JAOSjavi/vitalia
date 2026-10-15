"""Errores del dominio que no son de una regla en particular."""


class NoEncontrado(Exception):
    """No existe, o no es de quien pregunta. No se distingue, para no revelar que existe."""
