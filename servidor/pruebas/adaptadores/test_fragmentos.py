"""Lo que la base garantiza sobre documentos y fragmentos del asistente (D-30, HU-031 a HU-033)."""

from uuid import UUID

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from conftest import CrearUsuario
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.dominio.identidad import SISTEMA, Identidad

pytestmark = pytest.mark.bd


def vector(*primeros: float) -> str:
    """Un vector de 1.024 números con los primeros dados y el resto en cero, como texto."""
    numeros = list(primeros) + [0.0] * (1024 - len(primeros))
    return "[" + ",".join(str(n) for n in numeros) + "]"


async def subir_documento(unidad: UnidadPostgres, paciente: UUID, huella: str = "h1") -> UUID:
    async with unidad.abrir(Identidad("paciente", paciente)) as trabajo:
        documento: UUID = await trabajo.conexion.scalar(
            text(
                "INSERT INTO documentos (paciente_id, nombre, fecha_documento, tipo, formato, "
                "tamano, huella, clave_archivo) VALUES (paciente_actual(), 'Control', "
                "'2026-09-01', 'examen', 'pdf', 1000, :huella, gen_random_uuid()::text) "
                "RETURNING id"
            ),
            {"huella": huella},
        )
    return documento


async def indexar(unidad: UnidadPostgres, documento: UUID, textos: list[tuple[str, str]]) -> None:
    """Hace lo que hará el lector: guarda la página 1 y sus fragmentos con su vector."""
    async with unidad.abrir(SISTEMA) as trabajo:
        await trabajo.conexion.execute(
            text(
                "INSERT INTO paginas_documento (documento_id, numero, texto, origen) "
                "VALUES (:d, 1, 'página completa', 'pdf')"
            ),
            {"d": documento},
        )
        for orden, (texto, su_vector) in enumerate(textos):
            await trabajo.conexion.execute(
                text(
                    "INSERT INTO fragmentos (paciente_id, documento_id, pagina, orden, texto, "
                    "vector, modelo) SELECT paciente_id, id, 1, :orden, :texto, "
                    "CAST(:vector AS vector), 'de-prueba' FROM documentos WHERE id = :d"
                ),
                {"d": documento, "orden": orden, "texto": texto, "vector": su_vector},
            )


async def contar_fragmentos(unidad: UnidadPostgres, medico: UUID) -> int:
    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        total: int = await trabajo.conexion.scalar(text("SELECT count(*) FROM fragmentos"))
    return total


async def test_busca_por_palabras_sin_tildes_y_por_cercania(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario, medico: UUID
) -> None:
    rosa = await crear_usuario("paciente")
    documento = await subir_documento(unidad, rosa)
    await indexar(
        unidad,
        documento,
        [
            ("Paciente DIABÉTICA en control con metformina.", vector(1, 0)),
            ("Radiografía de tórax sin hallazgos.", vector(0, 1)),
        ],
    )

    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        por_palabras = list(
            await trabajo.conexion.scalars(
                text(
                    "SELECT texto FROM fragmentos WHERE documento_id = :d "
                    "AND lexico @@ websearch_to_tsquery('vitalia_es', 'diabetica')"
                ),
                {"d": documento},
            )
        )
        por_cercania = list(
            await trabajo.conexion.scalars(
                text(
                    "SELECT texto FROM fragmentos WHERE documento_id = :d "
                    "ORDER BY vector <=> CAST(:pregunta AS vector)"
                ),
                {"d": documento, "pregunta": vector(0.1, 0.9)},
            )
        )

    assert por_palabras == ["Paciente DIABÉTICA en control con metformina."]
    assert por_cercania[0] == "Radiografía de tórax sin hallazgos."


async def test_un_fragmento_no_puede_quedar_con_otro_paciente(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario, medico: UUID
) -> None:
    rosa = await crear_usuario("paciente")
    carlos = await crear_usuario("paciente")
    documento = await subir_documento(unidad, rosa)
    await indexar(unidad, documento, [])
    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        paciente_carlos = await trabajo.conexion.scalar(
            text("SELECT id FROM pacientes WHERE usuario_id = :u"), {"u": carlos}
        )

    with pytest.raises(IntegrityError, match="fragmentos_documento_id_paciente_id_fkey"):
        async with unidad.abrir(SISTEMA) as trabajo:
            await trabajo.conexion.execute(
                text(
                    "INSERT INTO fragmentos (paciente_id, documento_id, pagina, orden, texto, "
                    "vector, modelo) VALUES (:p, :d, 1, 0, 'dato', CAST(:v AS vector), 'x')"
                ),
                {"p": paciente_carlos, "d": documento, "v": vector(1)},
            )


async def test_el_paciente_no_ve_documentos_ajenos_ni_fragmentos(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario
) -> None:
    rosa = await crear_usuario("paciente")
    carlos = await crear_usuario("paciente")
    documento = await subir_documento(unidad, rosa)
    await indexar(unidad, documento, [("Dato de Rosa.", vector(1))])

    async with unidad.abrir(Identidad("paciente", carlos)) as trabajo:
        documentos = await trabajo.conexion.scalar(text("SELECT count(*) FROM documentos"))
    async with unidad.abrir(Identidad("paciente", rosa)) as trabajo:
        fragmentos = await trabajo.conexion.scalar(text("SELECT count(*) FROM fragmentos"))

    assert documentos == 0
    assert fragmentos == 0


async def test_al_eliminar_el_documento_se_van_sus_paginas_y_fragmentos(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario, medico: UUID
) -> None:
    rosa = await crear_usuario("paciente")
    documento = await subir_documento(unidad, rosa)
    await indexar(unidad, documento, [("Dato.", vector(1))])
    antes = await contar_fragmentos(unidad, medico)

    async with unidad.abrir(Identidad("paciente", rosa)) as trabajo:
        await trabajo.conexion.execute(
            text("DELETE FROM documentos WHERE id = :d"), {"d": documento}
        )

    assert await contar_fragmentos(unidad, medico) == antes - 1


async def test_al_retirar_la_autorizacion_de_ia_se_borran_sus_fragmentos(
    unidad: UnidadPostgres, crear_usuario: CrearUsuario, medico: UUID
) -> None:
    rosa = await crear_usuario("paciente")
    carlos = await crear_usuario("paciente")
    await indexar(unidad, await subir_documento(unidad, rosa), [("De Rosa.", vector(1))])
    await indexar(unidad, await subir_documento(unidad, carlos), [("De Carlos.", vector(1))])
    antes = await contar_fragmentos(unidad, medico)

    async with unidad.abrir(Identidad("paciente", rosa)) as trabajo:
        await trabajo.conexion.execute(
            text(
                "INSERT INTO autorizaciones (paciente_id, texto_id, decision) "
                "SELECT paciente_actual(), id, 'retirada' FROM textos_autorizacion "
                "WHERE tipo = 'ia' AND version = 1"
            )
        )

    # Solo se van los de Rosa; los de Carlos siguen.
    assert await contar_fragmentos(unidad, medico) == antes - 1
