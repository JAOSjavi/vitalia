"""Lista y búsqueda de pacientes por nombre o documento, por páginas (HU-023)."""

from dataclasses import dataclass

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import PacienteEnLista, UnidadDeTrabajo
from vitalia.dominio.identidad import Identidad

TAMANO_MAXIMO = 50


@dataclass(frozen=True)
class PaginaDePacientes:
    pacientes: list[PacienteEnLista]
    total: int
    pagina: int
    tamano: int


class BuscarPacientes:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ejecutar(
        self, identidad: Identidad, texto: str | None, pagina: int = 1, tamano: int = 20
    ) -> PaginaDePacientes:
        await self._autorizador.exigir(identidad, "pacientes.ver")
        pagina = max(pagina, 1)
        tamano = min(max(tamano, 1), TAMANO_MAXIMO)
        texto = (texto or "").strip() or None
        async with self._unidad.abrir(identidad) as trabajo:
            pacientes, total = await trabajo.pacientes.buscar(texto, pagina, tamano)
        return PaginaDePacientes(pacientes, total, pagina, tamano)
