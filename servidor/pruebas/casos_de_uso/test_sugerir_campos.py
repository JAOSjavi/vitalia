"""Sugerencias para la historia: qué se comprueba antes, qué recibe el modelo y qué vuelve."""

import asyncio
import json
import re
from collections.abc import AsyncIterator, Sequence
from typing import Any
from uuid import UUID

import httpx
import pytest
from fastapi import FastAPI
from test_preguntar_al_asistente import FEBRERO, paciente_de, subir_y_procesar

from conftest import IngresarDoctora, NuevoPaciente, RelojMovible
from vitalia.adaptadores.ia.de_mentira import VectoresDeMentira
from vitalia.adaptadores.postgres import historia
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.preguntar_al_asistente import Limites
from vitalia.casos_de_uso.puertos import ProveedorNoDisponible, Turno
from vitalia.casos_de_uso.sugerir_campos import SugerirCampos
from vitalia.dominio.asistente import SinFragmentos, TopeDeConsultas
from vitalia.dominio.fragmentos import IANoAutorizada
from vitalia.dominio.historia_clinica import AtencionCerrada
from vitalia.dominio.identidad import Identidad

pytestmark = pytest.mark.bd


class IAQueSugiere:
    """Sugiere alergias con la primera línea que recibe y antecedentes con una frase inventada."""

    def __init__(self, demora: float = 0, respuesta: str | None = None) -> None:
        self.llamadas: list[tuple[str, str]] = []
        self._demora = demora
        self._respuesta = respuesta

    async def leer_pagina(self, imagen: bytes) -> str:
        return ""

    async def responder(self, instrucciones: str, turnos: Sequence[Turno]) -> AsyncIterator[str]:
        yield ""

    async def responder_en_json(self, instrucciones: str, texto: str) -> str:
        self.llamadas.append((instrucciones, texto))
        await asyncio.sleep(self._demora)
        if self._respuesta is not None:
            return self._respuesta
        etiqueta, pagina, linea = re.search(r"\[(D\d+), pág\. (\d+)\]\n([^\n]+)", texto).groups()  # type: ignore[union-attr]
        return json.dumps(
            {
                "campos": [
                    {
                        "campo": "alergias",
                        "valor": "Ibuprofeno con angioedema.",
                        "citas": [{"documento": etiqueta, "pagina": int(pagina), "frase": linea}],
                    },
                    {
                        "campo": "antecedentes_familiares",
                        "valor": "Madre con diabetes.",
                        "citas": [{"documento": etiqueta, "pagina": 1, "frase": "madre diabética"}],
                    },
                ]
            }
        )


def sugeridor(
    unidad: UnidadPostgres, reloj: RelojMovible, ia: IAQueSugiere, **limites: Any
) -> SugerirCampos:
    return SugerirCampos(
        unidad, Autorizador(unidad), VectoresDeMentira(), ia, reloj, Limites(**limites)
    )


async def abrir_atencion(doctora: httpx.AsyncClient, paciente: UUID) -> UUID:
    respuesta = await doctora.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})
    assert respuesta.status_code == 201, respuesta.text
    return UUID(respuesta.json()["id"])


async def test_sugiere_solo_lo_respaldado_y_sin_datos_del_paciente(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    ingresar_doctora: IngresarDoctora,
    medico: UUID,
) -> None:
    rosa = await nuevo_paciente(ia=True)
    febrero = await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    paciente = await paciente_de(unidad, rosa)
    atencion = await abrir_atencion(await ingresar_doctora(), paciente)
    ia = IAQueSugiere()

    resultado = await sugeridor(unidad, reloj, ia).ejecutar(Identidad("medico", medico), atencion)

    # Los antecedentes familiares no tienen una frase que esté en el documento: no llegan.
    [alergias] = resultado.sugerencias
    assert alergias.campo == "alergias"
    assert [(o.documento_id, o.pagina) for o in alergias.origenes] == [(febrero, 1)]
    assert [c.documento_id for c in resultado.consultado] == [febrero]
    [(instrucciones, texto)] = ia.llamadas
    assert "Rosa" not in texto and "Duarte" not in texto
    assert "JSON" in instrucciones


async def test_no_se_llama_al_modelo_si_algo_falta_antes(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    ingresar_doctora: IngresarDoctora,
    medico: UUID,
) -> None:
    doctora = await ingresar_doctora()
    sin_ia = await nuevo_paciente("Luis", "Pardo", ia=False)
    await subir_y_procesar(api, sin_ia, FEBRERO, "2026-02-12")
    sin_documentos = await nuevo_paciente("Juan", "Ortiz", ia=True)
    ia = IAQueSugiere()
    caso = sugeridor(unidad, reloj, ia)
    medica = Identidad("medico", medico)

    with pytest.raises(IANoAutorizada):
        await caso.ejecutar(
            medica, await abrir_atencion(doctora, await paciente_de(unidad, sin_ia))
        )
    with pytest.raises(SinFragmentos):
        await caso.ejecutar(
            medica, await abrir_atencion(doctora, await paciente_de(unidad, sin_documentos))
        )
    assert ia.llamadas == []


async def test_una_atencion_cerrada_no_recibe_sugerencias(
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    medico: UUID,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Cerrada:
        estado = "cerrada"

    async def atencion(*_: object) -> Cerrada:
        return Cerrada()

    monkeypatch.setattr(historia.HistoriaPostgres, "atencion", atencion)
    with pytest.raises(AtencionCerrada):
        await sugeridor(unidad, reloj, IAQueSugiere()).ejecutar(
            Identidad("medico", medico), UUID(int=1)
        )


async def test_cuenta_para_el_tope_del_asistente(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    ingresar_doctora: IngresarDoctora,
    medico: UUID,
) -> None:
    rosa = await nuevo_paciente(ia=True)
    await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    atencion = await abrir_atencion(await ingresar_doctora(), await paciente_de(unidad, rosa))
    medica = Identidad("medico", medico)
    desde = reloj.ahora().replace(year=2000)
    async with unidad.abrir(medica) as trabajo:
        hechas = await trabajo.bitacora.contar(
            "pregunta_al_asistente", desde
        ) + await trabajo.bitacora.contar("sugerencias_para_la_historia", desde)
    caso = sugeridor(unidad, reloj, IAQueSugiere(), consultas_por_hora=hechas + 1)

    await caso.ejecutar(medica, atencion)
    with pytest.raises(TopeDeConsultas):
        await caso.ejecutar(medica, atencion)


@pytest.mark.parametrize(
    ("ia", "limites"),
    [(IAQueSugiere(demora=1), {"segundos_de_espera": 0.1}), (IAQueSugiere(respuesta="hola"), {})],
)
async def test_si_el_modelo_tarda_o_no_responde_json_se_avisa(
    api: FastAPI,
    unidad: UnidadPostgres,
    reloj: RelojMovible,
    nuevo_paciente: NuevoPaciente,
    ingresar_doctora: IngresarDoctora,
    medico: UUID,
    ia: IAQueSugiere,
    limites: dict[str, Any],
) -> None:
    rosa = await nuevo_paciente(ia=True)
    await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    atencion = await abrir_atencion(await ingresar_doctora(), await paciente_de(unidad, rosa))

    with pytest.raises(ProveedorNoDisponible):
        await sugeridor(unidad, reloj, ia, **limites).ejecutar(
            Identidad("medico", medico), atencion
        )


async def test_la_ruta_devuelve_las_sugerencias_y_rechaza_sin_autorizacion(
    api: FastAPI,
    unidad: UnidadPostgres,
    nuevo_paciente: NuevoPaciente,
    ingresar_doctora: IngresarDoctora,
) -> None:
    doctora = await ingresar_doctora()
    rosa = await nuevo_paciente(ia=True)
    await subir_y_procesar(api, rosa, FEBRERO, "2026-02-12")
    luis = await nuevo_paciente("Luis", "Pardo", ia=False)
    con_ia = await abrir_atencion(doctora, await paciente_de(unidad, rosa))
    sin_ia = await abrir_atencion(doctora, await paciente_de(unidad, luis))

    respuesta = await doctora.post(f"/api/v1/atenciones/{con_ia}/sugerencias")
    rechazo = await doctora.post(f"/api/v1/atenciones/{sin_ia}/sugerencias")

    assert respuesta.status_code == 200, respuesta.text
    # La IA de mentira de la API no sugiere nada; lo que importa es la forma.
    cuerpo = respuesta.json()
    assert cuerpo["sugerencias"] == []
    assert [c["paginas"] for c in cuerpo["consultado"]] == [[1, 2]]
    assert rechazo.status_code == 422
    assert rechazo.json()["codigo"] == "ia_no_autorizada"
    # El paciente no puede pedirlas.
    assert (await rosa.post(f"/api/v1/atenciones/{con_ia}/sugerencias")).status_code == 403
