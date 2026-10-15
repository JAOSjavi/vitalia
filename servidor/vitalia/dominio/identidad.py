"""Quién hace una operación."""

from dataclasses import dataclass
from typing import Literal
from uuid import UUID

Rol = Literal["medico", "paciente"]
Clase = Literal["medico", "paciente", "sistema"]


@dataclass(frozen=True)
class Identidad:
    clase: Clase
    usuario_id: UUID | None = None


# Procesos en segundo plano y arranque del servidor: no tienen usuario.
SISTEMA = Identidad("sistema")
