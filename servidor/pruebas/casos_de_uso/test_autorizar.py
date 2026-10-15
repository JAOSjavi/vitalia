"""El paso de autorización común a todas las operaciones (HU-006), con puertos de mentira."""

from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import cast
from uuid import UUID, uuid4

import pytest

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import UnidadDeTrabajo
from vitalia.dominio.identidad import Identidad
from vitalia.dominio.permisos import AccesoDenegado, MatrizDePermisos


@dataclass
class BitacoraEnMemoria:
    identidad: Identidad
    registros: list[tuple[Identidad, str, str | None]]

    async def registrar(
        self,
        accion: str,
        *,
        paciente_id: UUID | None = None,
        objeto: str | None = None,
        detalle: Mapping[str, object] | None = None,
    ) -> None:
        self.registros.append((self.identidad, accion, objeto))


@dataclass
class PermisosFijos:
    lecturas: list[int]

    async def matriz(self) -> MatrizDePermisos:
        self.lecturas.append(1)
        return MatrizDePermisos(frozenset({("medico", "consultorio.editar")}))


@dataclass
class TrabajoEnMemoria:
    bitacora: BitacoraEnMemoria
    permisos: PermisosFijos


@dataclass
class UnidadEnMemoria:
    registros: list[tuple[Identidad, str, str | None]] = field(default_factory=list)
    lecturas_de_matriz: list[int] = field(default_factory=list)

    @asynccontextmanager
    async def abrir(self, identidad: Identidad | None) -> AsyncIterator[TrabajoEnMemoria]:
        assert identidad is not None
        yield TrabajoEnMemoria(
            BitacoraEnMemoria(identidad, self.registros), PermisosFijos(self.lecturas_de_matriz)
        )


def _autorizador(unidad: UnidadEnMemoria) -> Autorizador:
    # El autorizador solo usa la bitácora y los permisos de la unidad de trabajo.
    return Autorizador(cast(UnidadDeTrabajo, unidad))


MEDICO = Identidad("medico", uuid4())
PACIENTE = Identidad("paciente", uuid4())


async def test_deja_pasar_lo_que_la_matriz_concede_sin_anotarlo() -> None:
    unidad = UnidadEnMemoria()

    await _autorizador(unidad).exigir(MEDICO, "consultorio.editar")

    assert unidad.registros == []


async def test_niega_al_paciente_y_anota_el_intento_a_su_nombre() -> None:
    unidad = UnidadEnMemoria()

    with pytest.raises(AccesoDenegado):
        await _autorizador(unidad).exigir(PACIENTE, "consultorio.editar")

    assert unidad.registros == [(PACIENTE, "acceso_denegado", "consultorio.editar")]


async def test_lee_la_matriz_una_sola_vez() -> None:
    unidad = UnidadEnMemoria()
    autorizador = _autorizador(unidad)

    await autorizador.exigir(MEDICO, "consultorio.editar")
    await autorizador.exigir(MEDICO, "consultorio.editar")

    assert unidad.lecturas_de_matriz == [1]
