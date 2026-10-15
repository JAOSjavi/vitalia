"""Bitácora de solo inserción en la misma transacción (HU-037) y accesos negados (HU-006)."""

from uuid import UUID, uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, IntegrityError, ProgrammingError
from sqlalchemy.ext.asyncio import AsyncEngine

from conftest import CrearUsuario
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.dominio.identidad import Identidad
from vitalia.dominio.permisos import AccesoDenegado

pytestmark = pytest.mark.bd


async def _registros_de(
    unidad: UnidadPostgres, medico: UUID, usuario: UUID
) -> list[tuple[str, ...]]:
    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        filas = await trabajo.conexion.execute(
            text("SELECT rol, accion, objeto FROM bitacora WHERE usuario_id = :u ORDER BY id"),
            {"u": usuario},
        )
        return [tuple(fila) for fila in filas]


async def test_cada_quien_registra_a_su_nombre_y_el_medico_lo_lee(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario, medico: UUID
) -> None:
    rosa = await crear_usuario("paciente")

    async with unidad.abrir(Identidad("paciente", rosa)) as trabajo:
        await trabajo.bitacora.registrar("apertura_de_documento", objeto="documento")

    assert await _registros_de(unidad, medico, rosa) == [
        ("paciente", "apertura_de_documento", "documento")
    ]


async def test_nadie_registra_a_nombre_de_otro(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario
) -> None:
    rosa = await crear_usuario("paciente")

    with pytest.raises(ProgrammingError, match="row-level security"):
        async with unidad.abrir(Identidad("paciente", rosa)) as trabajo:
            await trabajo.conexion.execute(
                text("INSERT INTO bitacora (usuario_id, rol, accion) VALUES (:u, 'medico', 'x')"),
                {"u": rosa},
            )


async def test_el_paciente_no_lee_la_bitacora(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario
) -> None:
    rosa = await crear_usuario("paciente")

    async with unidad.abrir(Identidad("paciente", rosa)) as trabajo:
        await trabajo.bitacora.registrar("ingreso")
        visibles = await trabajo.conexion.scalar(text("SELECT count(*) FROM bitacora"))

    assert visibles == 0


@pytest.mark.parametrize("orden", ["UPDATE bitacora SET accion = 'otra'", "DELETE FROM bitacora"])
async def test_la_aplicacion_no_modifica_ni_borra_la_bitacora(
    unidad: UnidadPostgres, medico: UUID, orden: str
) -> None:
    with pytest.raises(ProgrammingError, match="permission denied"):
        async with unidad.abrir(Identidad("medico", medico)) as trabajo:
            await trabajo.conexion.execute(text(orden))


@pytest.mark.parametrize(
    "orden",
    [
        "ALTER TABLE bitacora NO FORCE ROW LEVEL SECURITY; UPDATE bitacora SET accion = 'otra'",
        "ALTER TABLE bitacora NO FORCE ROW LEVEL SECURITY; DELETE FROM bitacora",
        "TRUNCATE bitacora",
    ],
)
async def test_ni_el_dueno_de_las_tablas_cambia_la_bitacora(
    unidad: UnidadPostgres, motor_dueno: AsyncEngine, medico: UUID, orden: str
) -> None:
    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        await trabajo.bitacora.registrar("ingreso")

    with pytest.raises(DBAPIError, match="solo admite inserciones"):
        async with motor_dueno.begin() as conexion:
            for parte in orden.split("; "):
                await conexion.execute(text(parte))


async def test_si_la_bitacora_falla_la_operacion_no_se_confirma(
    unidad: UnidadPostgres, medico: UUID
) -> None:
    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        antes = await trabajo.conexion.scalar(text("SELECT nombre FROM consultorio"))

    with pytest.raises(IntegrityError):
        async with unidad.abrir(Identidad("medico", medico)) as trabajo:
            await trabajo.conexion.execute(text("UPDATE consultorio SET nombre = 'Cambiado'"))
            # Un paciente que no existe hace fallar el registro.
            await trabajo.bitacora.registrar("correccion", paciente_id=uuid4())

    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        assert await trabajo.conexion.scalar(text("SELECT nombre FROM consultorio")) == antes


async def test_un_paciente_que_pide_una_operacion_del_medico_queda_en_la_bitacora(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario, medico: UUID
) -> None:
    rosa = await crear_usuario("paciente")
    autorizador = Autorizador(unidad)

    await autorizador.exigir(Identidad("paciente", rosa), "consultorio.ver")
    with pytest.raises(AccesoDenegado):
        await autorizador.exigir(Identidad("paciente", rosa), "consultorio.editar")

    assert await _registros_de(unidad, medico, rosa) == [
        ("paciente", "acceso_denegado", "consultorio.editar")
    ]
