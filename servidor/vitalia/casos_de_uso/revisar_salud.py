"""Revisa si el servidor puede atender: hoy, si la base responde."""

from dataclasses import dataclass

from vitalia.casos_de_uso.puertos import BaseDeDatos


@dataclass(frozen=True)
class Salud:
    base_responde: bool


class RevisarSalud:
    def __init__(self, base: BaseDeDatos) -> None:
        self._base = base

    async def ejecutar(self) -> Salud:
        return Salud(base_responde=await self._base.responde())
