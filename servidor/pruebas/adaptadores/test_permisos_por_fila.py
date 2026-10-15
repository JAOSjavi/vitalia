"""La base misma filtra lo que cada quien puede ver (HU-036)."""

from uuid import UUID

import pytest
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncEngine

from conftest import CrearUsuario
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.dominio.identidad import Identidad

pytestmark = pytest.mark.bd

# Catálogos que todo el que tenga identidad puede leer (última fila de la sección 3.3).
CATALOGOS = {"roles", "permisos", "rol_permiso"}


async def test_sin_identidad_no_sale_ninguna_fila(
    motor_api: AsyncEngine, crear_usuario: CrearUsuario
) -> None:
    await crear_usuario("paciente")

    async with motor_api.connect() as conexion:
        for tabla in ("roles", "rol_permiso", "usuarios", "pacientes", "consultorio"):
            filas = await conexion.scalar(text(f"SELECT count(*) FROM {tabla}"))
            assert filas == 0, tabla


async def test_un_paciente_solo_ve_sus_propias_filas_aunque_no_filtre(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario
) -> None:
    rosa = await crear_usuario("paciente")
    await crear_usuario("paciente")

    async with unidad.abrir(Identidad("paciente", rosa)) as trabajo:
        usuarios = list(await trabajo.conexion.scalars(text("SELECT id FROM usuarios")))
        pacientes = list(await trabajo.conexion.scalars(text("SELECT usuario_id FROM pacientes")))

    assert usuarios == [rosa]
    assert pacientes == [rosa]


async def test_el_medico_ve_a_todos_los_pacientes(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario, medico: UUID
) -> None:
    rosa = await crear_usuario("paciente")
    carlos = await crear_usuario("paciente")

    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        pacientes = set(await trabajo.conexion.scalars(text("SELECT usuario_id FROM pacientes")))

    assert {rosa, carlos} <= pacientes


async def test_la_aplicacion_no_puede_leer_las_contrasenas(
    unidad: UnidadPostgres, medico: UUID
) -> None:
    with pytest.raises(ProgrammingError, match="permission denied"):
        async with unidad.abrir(Identidad("medico", medico)) as trabajo:
            await trabajo.conexion.execute(text("SELECT hash_contrasena FROM usuarios"))


async def test_el_paciente_no_puede_editar_el_consultorio(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario
) -> None:
    rosa = await crear_usuario("paciente")

    async with unidad.abrir(Identidad("paciente", rosa)) as trabajo:
        resultado = await trabajo.conexion.execute(text("UPDATE consultorio SET nombre = 'Otro'"))

    assert resultado.rowcount == 0


async def test_el_dueno_conectado_directamente_tampoco_ve_filas(
    motor_dueno: AsyncEngine, medico: UUID
) -> None:
    async with motor_dueno.connect() as conexion:
        assert await conexion.scalar(text("SELECT count(*) FROM usuarios")) == 0


async def test_toda_tabla_tiene_permisos_forzados_y_ninguna_politica_abierta(
    motor_dueno: AsyncEngine,
) -> None:
    """Es la prueba que hace fallar el despliegue (HU-036, CA-4)."""
    async with motor_dueno.connect() as conexion:
        tablas = (
            await conexion.execute(
                text(
                    "SELECT relname, relrowsecurity, relforcerowsecurity, "
                    "has_table_privilege('vitalia_api', oid, 'SELECT, INSERT, UPDATE, DELETE') "
                    "AS con_acceso FROM pg_class "
                    "WHERE relnamespace = 'public'::regnamespace AND relkind IN ('r', 'p') "
                    "AND relname <> 'alembic_version'"
                )
            )
        ).all()
        politicas = (
            await conexion.execute(
                text(
                    "SELECT tablename, policyname, cmd, qual, with_check FROM pg_policies "
                    "WHERE schemaname = 'public' AND 'vitalia_api' = ANY (roles)"
                )
            )
        ).all()

    assert tablas, "No hay tablas que revisar"
    sin_forzar = [t.relname for t in tablas if not (t.relrowsecurity and t.relforcerowsecurity)]
    assert sin_forzar == [], f"Tablas sin permisos por fila forzados: {sin_forzar}"

    # Una tabla a la que la aplicación no tiene ningún acceso queda cerrada sin política.
    con_politica = {p.tablename for p in politicas}
    sin_politica = sorted({t.relname for t in tablas if t.con_acceso} - con_politica)
    assert sin_politica == [], f"Tablas abiertas a la aplicación sin política: {sin_politica}"

    # Toda política de la aplicación depende de la identidad: sin ella no pasa ninguna fila.
    abiertas = [
        f"{p.tablename}.{p.policyname}"
        for p in politicas
        if "identidad()" not in f"{p.qual or ''} {p.with_check or ''}"
    ]
    assert abiertas == [], f"Políticas que no dependen de la identidad: {abiertas}"

    # Solo los catálogos se leen con cualquier identidad.
    para_todos = [
        p.tablename
        for p in politicas
        if p.qual == "(identidad() IS NOT NULL)" and p.tablename not in CATALOGOS
    ]
    assert para_todos == [], f"Tablas abiertas a cualquier identidad: {para_todos}"


async def test_la_aplicacion_no_toca_la_tabla_de_migraciones(motor_api: AsyncEngine) -> None:
    with pytest.raises(ProgrammingError, match="permission denied"):
        async with motor_api.connect() as conexion:
            await conexion.execute(text("SELECT * FROM alembic_version"))
