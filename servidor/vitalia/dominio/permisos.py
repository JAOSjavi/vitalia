"""Matriz de permisos: qué rol puede hacer qué operación. Lo que no está, queda denegado."""

from dataclasses import dataclass


class AccesoDenegado(Exception):
    def __init__(self, permiso: str) -> None:
        super().__init__(f"Acceso denegado a la operación {permiso}")
        self.permiso = permiso


@dataclass(frozen=True)
class MatrizDePermisos:
    concedidos: frozenset[tuple[str, str]]

    def permite(self, rol: str, permiso: str) -> bool:
        return (rol, permiso) in self.concedidos
