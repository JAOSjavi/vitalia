"""Indexar los documentos leídos y buscar en ellos, siempre dentro de un solo paciente (D-30)."""

from typing import Any
from uuid import UUID

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import text

from conftest import NuevoPaciente, pdf_con_texto
from vitalia.adaptadores.ia.de_mentira import VectoresDeMentira
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.casos_de_uso.buscar_fragmentos import BuscarFragmentos
from vitalia.casos_de_uso.indexar_documentos import IndexarDocumentos
from vitalia.casos_de_uso.leer_documentos import LeerDocumentos
from vitalia.dominio.fragmentos import IANoAutorizada
from vitalia.dominio.identidad import SISTEMA, Identidad
from vitalia.dominio.permisos import AccesoDenegado

pytestmark = pytest.mark.bd

PRESION = pdf_con_texto(
    "Paciente: Rosa Elena Duarte. Documento a nombre de la paciente.\n"
    "Motivo de consulta: control de la presion arterial.\n"
    "Tension arterial 156/94 mmHg. Losartan 50 mg cada 12 horas.",
    "Laboratorios: colesterol LDL 168 mg/dL, trigliceridos 210 mg/dL.\n"
    "Se inicia atorvastatina 20 mg en la noche.",
)
ASMA = pdf_con_texto(
    "Asma bronquial. Budesonida con formoterol dos inhalaciones cada 12 horas.\n"
    "Espirometria con obstruccion leve y respuesta al broncodilatador."
)


async def subir_y_procesar(api: FastAPI, cliente: httpx.AsyncClient, pdf: bytes) -> UUID:
    respuesta = await cliente.post(
        "/api/v1/documentos",
        data={"nombre": "Control", "fecha_documento": "2026-08-20", "tipo": "historia_clinica"},
        files={"archivo": ("control.pdf", pdf, "application/pdf")},
    )
    assert respuesta.status_code == 201, respuesta.text
    lector: LeerDocumentos = api.state.lector
    indexador: IndexarDocumentos = api.state.indexador
    await lector.leer_pendientes()
    await indexador.indexar_pendientes()
    return UUID(respuesta.json()["id"])


async def como_sistema(unidad: UnidadPostgres, consulta: str, **valores: Any) -> list[Any]:
    async with unidad.abrir(SISTEMA) as trabajo:
        return list(await trabajo.conexion.execute(text(consulta), valores))


async def paciente_del_documento(unidad: UnidadPostgres, documento: UUID) -> UUID:
    [fila] = await como_sistema(
        unidad, "SELECT paciente_id FROM documentos WHERE id = :d", d=documento
    )
    paciente: UUID = fila.paciente_id
    return paciente


def buscador(api: FastAPI) -> BuscarFragmentos:
    resultado: BuscarFragmentos = api.state.casos.buscar_fragmentos
    return resultado


async def test_indexa_por_pagina_y_sin_el_nombre_del_paciente(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente
) -> None:
    rosa = await nuevo_paciente(ia=True)

    documento = await subir_y_procesar(api, rosa, PRESION)

    fragmentos = await como_sistema(
        unidad,
        "SELECT pagina, texto, modelo FROM fragmentos WHERE documento_id = :d ORDER BY pagina",
        d=documento,
    )
    assert [f.pagina for f in fragmentos] == [1, 2]
    assert fragmentos[0].texto.startswith("Paciente: [PACIENTE].")
    assert all("Rosa" not in f.texto and "Duarte" not in f.texto for f in fragmentos)
    assert {f.modelo for f in fragmentos} == {VectoresDeMentira.modelo}


async def test_sin_autorizacion_de_ia_no_hay_fragmentos(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente
) -> None:
    luis = await nuevo_paciente("Luis", "Pardo", ia=False)

    documento = await subir_y_procesar(api, luis, PRESION)

    assert (
        await como_sistema(unidad, "SELECT id FROM fragmentos WHERE documento_id = :d", d=documento)
        == []
    )


async def test_indexar_dos_veces_no_duplica(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente
) -> None:
    rosa = await nuevo_paciente(ia=True)
    documento = await subir_y_procesar(api, rosa, PRESION)

    async with unidad.abrir(SISTEMA) as trabajo:
        await trabajo.documentos.encolar(documento, "indexar_documento")
    indexador: IndexarDocumentos = api.state.indexador
    await indexador.indexar_pendientes()

    fragmentos = await como_sistema(
        unidad, "SELECT id FROM fragmentos WHERE documento_id = :d", d=documento
    )
    assert len(fragmentos) == 2


async def test_el_medico_encuentra_el_fragmento_que_responde(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente, medico: UUID
) -> None:
    rosa = await nuevo_paciente(ia=True)
    documento = await subir_y_procesar(api, rosa, PRESION)
    paciente = await paciente_del_documento(unidad, documento)

    encontrados = await buscador(api).ejecutar(
        Identidad("medico", medico), paciente, "¿Cuánto dio el colesterol LDL?"
    )

    primero = encontrados[0]
    assert (primero.documento_id, primero.pagina) == (documento, 2)
    assert "LDL 168" in primero.texto
    assert primero.rango_palabras == 1


async def test_la_busqueda_nunca_trae_fragmentos_de_otro_paciente(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente, medico: UUID
) -> None:
    rosa = await nuevo_paciente(ia=True)
    juan = await nuevo_paciente("Juan", "Ortiz", ia=True)
    de_rosa = await subir_y_procesar(api, rosa, PRESION)
    de_juan = await subir_y_procesar(api, juan, ASMA)
    paciente_rosa = await paciente_del_documento(unidad, de_rosa)

    # La pregunta es sobre el asma, que solo está en los documentos de Juan.
    encontrados = await buscador(api).ejecutar(
        Identidad("medico", medico), paciente_rosa, "budesonida formoterol espirometria asma"
    )

    assert de_juan not in {f.documento_id for f in encontrados}
    assert {f.documento_id for f in encontrados} <= {de_rosa}


async def test_la_pregunta_se_limpia_antes_de_buscar(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente, medico: UUID
) -> None:
    rosa = await nuevo_paciente(ia=True)
    paciente = await paciente_del_documento(unidad, await subir_y_procesar(api, rosa, PRESION))

    encontrados = await buscador(api).ejecutar(
        Identidad("medico", medico), paciente, "¿Rosa Elena Duarte toma losartan?"
    )

    assert "Losartan 50 mg" in encontrados[0].texto


async def test_sin_autorizacion_de_ia_no_se_busca(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente, medico: UUID
) -> None:
    luis = await nuevo_paciente("Luis", "Pardo", ia=False)
    paciente = await paciente_del_documento(unidad, await subir_y_procesar(api, luis, PRESION))

    with pytest.raises(IANoAutorizada):
        await buscador(api).ejecutar(Identidad("medico", medico), paciente, "presión")


async def test_el_paciente_no_puede_buscar(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente
) -> None:
    rosa = await nuevo_paciente(ia=True)
    documento = await subir_y_procesar(api, rosa, PRESION)
    paciente = await paciente_del_documento(unidad, documento)
    usuario = UUID((await rosa.get("/api/v1/yo")).json()["usuario_id"])

    with pytest.raises(AccesoDenegado):
        await buscador(api).ejecutar(Identidad("paciente", usuario), paciente, "presión")
