"""Preguntas al asistente: qué se comprueba antes, qué recibe el modelo y qué se devuelve."""

import asyncio
import json
import re
from collections.abc import AsyncIterator, Sequence
from typing import Any
from uuid import UUID

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import text

from conftest import IngresarDoctora, NuevoPaciente, RelojMovible, pdf_con_texto
from vitalia.adaptadores.ia.de_mentira import VectoresDeMentira
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.indexar_documentos import IndexarDocumentos
from vitalia.casos_de_uso.leer_documentos import LeerDocumentos
from vitalia.casos_de_uso.preguntar_al_asistente import (
    Cierre,
    Limites,
    PreguntarAlAsistente,
)
from vitalia.casos_de_uso.puertos import ProveedorNoDisponible, Turno
from vitalia.dominio.asistente import AVISO, SinFragmentos, TopeDeConsultas
from vitalia.dominio.fragmentos import IANoAutorizada
from vitalia.dominio.identidad import SISTEMA, Identidad

pytestmark = pytest.mark.bd

FEBRERO = pdf_con_texto(
    "Paciente: Rosa Elena Duarte.\nAlergicos: medicamentoso, ibuprofeno con angioedema.",
    "Colesterol LDL: 168 mg/dL. Trigliceridos: 210 mg/dL.",
)
MAYO = pdf_con_texto("Colesterol LDL: 112 mg/dL tras atorvastatina 20 mg en la noche.")


class IAQueCita:
    """Responde citando la primera página que recibe, más una frase y un documento inventados."""

    def __init__(self, demora: float = 0) -> None:
        self.llamadas: list[tuple[str, list[Turno]]] = []
        self._demora = demora

    async def leer_pagina(self, imagen: bytes) -> str:
        return ""

    async def responder(self, instrucciones: str, turnos: Sequence[Turno]) -> AsyncIterator[str]:
        self.llamadas.append((instrucciones, list(turnos)))
        await asyncio.sleep(self._demora)
        etiqueta, pagina, primera_linea = re.search(
            r"\[(D\d+), pág\. (\d+)\]\n([^\n]+)", instrucciones
        ).groups()  # type: ignore[union-attr]
        yield f'Según el registro [{etiqueta}, pág. {pagina}: "{primera_linea}"]. '
        yield f'También [{etiqueta}, pág. {pagina}: "una frase que no está"]. '
        yield 'Y esto [D9, pág. 1: "inventado"].'


async def subir_y_procesar(
    api: FastAPI, cliente: httpx.AsyncClient, pdf: bytes, fecha: str
) -> UUID:
    respuesta = await cliente.post(
        "/api/v1/documentos",
        data={"nombre": f"Control {fecha}", "fecha_documento": fecha, "tipo": "historia_clinica"},
        files={"archivo": ("control.pdf", pdf, "application/pdf")},
    )
    assert respuesta.status_code == 201, respuesta.text
    lector: LeerDocumentos = api.state.lector
    indexador: IndexarDocumentos = api.state.indexador
    await lector.leer_pendientes()
    await indexador.indexar_pendientes()
    return UUID(respuesta.json()["id"])


async def paciente_de(unidad: UnidadPostgres, cliente: httpx.AsyncClient) -> UUID:
    usuario = (await cliente.get("/api/v1/yo")).json()["usuario_id"]
    async with unidad.abrir(SISTEMA) as trabajo:
        await trabajo.conexion.execute(
            text("SELECT set_config('vitalia.identidad', 'medico', true)")
        )
        paciente: UUID = await trabajo.conexion.scalar(
            text("SELECT id FROM pacientes WHERE usuario_id = :u"), {"u": usuario}
        )
    return paciente


@pytest.fixture
def ia() -> IAQueCita:
    return IAQueCita()


def asistente(
    unidad: UnidadPostgres, reloj: RelojMovible, ia: IAQueCita, **limites: Any
) -> PreguntarAlAsistente:
    return PreguntarAlAsistente(
        unidad, Autorizador(unidad), VectoresDeMentira(), ia, reloj, Limites(**limites)
    )


async def preguntar(caso: PreguntarAlAsistente, *args: Any) -> tuple[str, Cierre]:
    lista = await caso.preparar(*args)
    partes: list[str] = []
    cierre: Cierre | None = None
    async for evento in caso.responder(lista):
        if isinstance(evento, Cierre):
            cierre = evento
        else:
            partes.append(evento)
    assert cierre is not None
    return "".join(partes), cierre


async def test_responde_por_partes_y_comprueba_cada_cita(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    medico: UUID,
    ia: IAQueCita,
) -> None:
    rosa = await nuevo_paciente(ia=True)
    febrero = await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    await subir_y_procesar(api, rosa, MAYO, "2026-05-14")
    paciente = await paciente_de(unidad, rosa)

    respuesta, cierre = await preguntar(
        asistente(unidad, reloj, ia), Identidad("medico", medico), paciente, "¿Alergias?"
    )

    assert respuesta.startswith("Según el registro [D1, pág. 1:")
    # La cita a D9 se descarta; la frase inventada queda sin verificar.
    assert [(o.etiqueta, o.documento_id, o.pagina, o.verificado) for o in cierre.origenes] == [
        ("D1", febrero, 1, True),
        ("D1", febrero, 1, False),
    ]
    assert [(c.documento, c.paginas) for c in cierre.consultado] == [
        ("Control 2026-02-12", (1, 2)),
        ("Control 2026-05-14", (1,)),
    ]
    assert cierre.aviso == AVISO


async def test_nada_del_paciente_sale_hacia_el_modelo(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    medico: UUID,
    ia: IAQueCita,
) -> None:
    rosa = await nuevo_paciente(ia=True)
    await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    paciente = await paciente_de(unidad, rosa)

    await preguntar(
        asistente(unidad, reloj, ia),
        Identidad("medico", medico),
        paciente,
        "¿Y Rosa Elena es alérgica?",
        [Turno("medico", "¿Qué edad tiene Rosa Duarte?"), Turno("asistente", "No lo encontré.")],
    )

    [(instrucciones, turnos)] = ia.llamadas
    enviado = instrucciones + "".join(t.texto for t in turnos)
    assert "Rosa" not in enviado and "Duarte" not in enviado
    assert turnos[-1] == Turno("medico", "¿Y [PACIENTE] es alérgica?")
    assert "Responde únicamente con lo que está escrito" in instrucciones


async def test_con_mucho_texto_solo_van_los_mas_cercanos_sin_pasar_del_tope(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    medico: UUID,
    ia: IAQueCita,
) -> None:
    rosa = await nuevo_paciente(ia=True)
    await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    mayo = await subir_y_procesar(api, rosa, MAYO, "2026-05-14")
    paciente = await paciente_de(unidad, rosa)

    _, cierre = await preguntar(
        asistente(unidad, reloj, ia, tope_contexto=70),
        Identidad("medico", medico),
        paciente,
        "atorvastatina",
    )

    assert [c.documento_id for c in cierre.consultado] == [mayo]


async def test_sin_autorizacion_o_sin_documentos_no_se_llama_al_modelo(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    medico: UUID,
    ia: IAQueCita,
) -> None:
    sin_ia = await nuevo_paciente("Luis", "Pardo", ia=False)
    await subir_y_procesar(api, sin_ia, FEBRERO, "2026-02-12")
    sin_documentos = await nuevo_paciente("Juan", "Ortiz", ia=True)
    caso = asistente(unidad, reloj, ia)
    doctora = Identidad("medico", medico)

    with pytest.raises(IANoAutorizada):
        await caso.preparar(doctora, await paciente_de(unidad, sin_ia), "¿Alergias?")
    with pytest.raises(SinFragmentos):
        await caso.preparar(doctora, await paciente_de(unidad, sin_documentos), "¿Alergias?")
    assert ia.llamadas == []


async def test_tope_de_preguntas_por_hora(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    medico: UUID,
    ia: IAQueCita,
) -> None:
    rosa = await nuevo_paciente(ia=True)
    await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    paciente = await paciente_de(unidad, rosa)
    doctora = Identidad("medico", medico)
    async with unidad.abrir(doctora) as trabajo:
        hechas = await trabajo.bitacora.contar(
            "pregunta_al_asistente", reloj.ahora().replace(year=2000)
        )
    caso = asistente(unidad, reloj, ia, consultas_por_hora=hechas + 1)

    await caso.preparar(doctora, paciente, "¿Alergias?")
    with pytest.raises(TopeDeConsultas):
        await caso.preparar(doctora, paciente, "¿Y el LDL?")


async def test_si_el_modelo_tarda_demasiado_se_avisa(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    medico: UUID,
) -> None:
    rosa = await nuevo_paciente(ia=True)
    await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    paciente = await paciente_de(unidad, rosa)
    caso = asistente(unidad, reloj, IAQueCita(demora=1), segundos_de_espera=0.1)

    with pytest.raises(ProveedorNoDisponible):
        await preguntar(caso, Identidad("medico", medico), paciente, "¿Alergias?")


async def test_la_ruta_responde_por_partes_y_cierra_con_las_listas(
    api: FastAPI,
    unidad: UnidadPostgres,
    nuevo_paciente: NuevoPaciente,
    ingresar_doctora: IngresarDoctora,
) -> None:
    rosa = await nuevo_paciente(ia=True)
    await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    paciente = await paciente_de(unidad, rosa)
    doctora = await ingresar_doctora()

    respuesta = await doctora.post(
        f"/api/v1/pacientes/{paciente}/asistente/preguntas", json={"pregunta": "¿Alergias?"}
    )

    assert respuesta.status_code == 200, respuesta.text
    assert respuesta.headers["content-type"].startswith("application/x-ndjson")
    eventos = [json.loads(linea) for linea in respuesta.text.splitlines()]
    assert {e["tipo"] for e in eventos[:-1]} == {"texto"}
    fin = eventos[-1]
    assert fin["tipo"] == "fin"
    assert fin["aviso"] == AVISO
    assert [c["paginas"] for c in fin["consultado"]] == [[1, 2]]
    # La bitácora anota quién preguntó sobre quién, sin la pregunta.
    async with unidad.abrir(SISTEMA) as trabajo:
        await trabajo.conexion.execute(
            text("SELECT set_config('vitalia.identidad', 'medico', true)")
        )
        detalle = await trabajo.conexion.scalar(
            text(
                "SELECT detalle FROM bitacora WHERE accion = 'pregunta_al_asistente' "
                "AND paciente_id = :p"
            ),
            {"p": paciente},
        )
    assert detalle == {"fragmentos": 2, "documentos": 1}


async def test_la_ruta_rechaza_antes_de_llamar_al_modelo(
    api: FastAPI,
    unidad: UnidadPostgres,
    nuevo_paciente: NuevoPaciente,
    ingresar_doctora: IngresarDoctora,
) -> None:
    luis = await nuevo_paciente("Luis", "Pardo", ia=False)
    paciente = await paciente_de(unidad, luis)
    doctora = await ingresar_doctora()

    sin_ia = await doctora.post(
        f"/api/v1/pacientes/{paciente}/asistente/preguntas", json={"pregunta": "¿Alergias?"}
    )
    del_paciente = await luis.post(
        f"/api/v1/pacientes/{paciente}/asistente/preguntas", json={"pregunta": "¿Alergias?"}
    )

    assert (sin_ia.status_code, sin_ia.json()["codigo"]) == (422, "ia_no_autorizada")
    assert del_paciente.status_code == 403
