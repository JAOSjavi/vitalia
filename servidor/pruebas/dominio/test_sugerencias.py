"""Cómo se lee lo que devuelve el modelo para completar la historia (HU-047)."""

import json
from datetime import date
from uuid import UUID

import pytest

from vitalia.dominio.asistente import FragmentoParaContexto, armar_contexto
from vitalia.dominio.sugerencias import RespuestaIlegible, leer_sugerencias

DOCUMENTO = UUID("00000000-0000-7000-8000-000000000001")
CONTEXTO = armar_contexto(
    [
        FragmentoParaContexto(
            DOCUMENTO,
            "Control",
            date(2026, 2, 12),
            1,
            "Alergicos: medicamentoso, ibuprofeno con angioedema.\nFuma 5 cigarrillos al día.",
        )
    ]
)


def respuesta(*campos: dict[str, object]) -> str:
    return json.dumps({"campos": list(campos)})


def test_queda_el_campo_con_su_frase_comprobada() -> None:
    [sugerencia] = leer_sugerencias(
        respuesta(
            {
                "campo": "alergias",
                "valor": "Ibuprofeno: angioedema.",
                "citas": [
                    {"documento": "D1", "pagina": 1, "frase": "ibuprofeno con angioedema"},
                    {"documento": "D1", "pagina": 1, "frase": "una frase que no está"},
                ],
            }
        ),
        CONTEXTO,
    )

    assert sugerencia.campo == "alergias"
    assert sugerencia.valor == "Ibuprofeno: angioedema."
    # La frase inventada se quita; la comprobada queda.
    assert [(o.etiqueta, o.documento_id, o.frase) for o in sugerencia.origenes] == [
        ("D1", DOCUMENTO, "ibuprofeno con angioedema")
    ]


def test_se_descarta_lo_que_no_esta_respaldado_o_no_se_puede_sugerir() -> None:
    sugerencias = leer_sugerencias(
        respuesta(
            # Ninguna frase está en el documento.
            {
                "campo": "antecedentes_familiares",
                "valor": "Madre con diabetes.",
                "citas": [{"documento": "D1", "pagina": 1, "frase": "madre diabética"}],
            },
            # Documento que no se envió.
            {
                "campo": "antecedentes_personales",
                "valor": "Hipertensión.",
                "citas": [{"documento": "D9", "pagina": 1, "frase": "Fuma 5 cigarrillos"}],
            },
            # Campo que no se sugiere: el diagnóstico es del médico.
            {
                "campo": "plan",
                "valor": "Suspender ibuprofeno.",
                "citas": [{"documento": "D1", "pagina": 1, "frase": "ibuprofeno"}],
            },
            # Sin citas.
            {"campo": "enfermedad_actual", "valor": "Estable.", "citas": []},
            {
                "campo": "factores_riesgo",
                "valor": "Tabaquismo: 5 cigarrillos al día.",
                "citas": [{"documento": "D1", "pagina": "1", "frase": "Fuma 5 cigarrillos al día"}],
            },
        ),
        CONTEXTO,
    )

    assert [s.campo for s in sugerencias] == ["factores_riesgo"]


def test_acepta_el_json_envuelto_en_cercas() -> None:
    texto = "```json\n" + respuesta() + "\n```"

    assert leer_sugerencias(texto, CONTEXTO) == []


@pytest.mark.parametrize("texto", ["no es json", "[]", '{"otra": 1}'])
def test_una_respuesta_sin_la_forma_pedida_es_ilegible(texto: str) -> None:
    with pytest.raises(RespuestaIlegible):
        leer_sugerencias(texto, CONTEXTO)


def test_una_frase_recortada_con_puntos_suspensivos_se_comprueba_por_pedazos() -> None:
    [sugerencia] = leer_sugerencias(
        respuesta(
            {
                "campo": "alergias",
                "valor": "Ibuprofeno; fuma.",
                "citas": [
                    {"documento": "D1", "pagina": 1, "frase": "Alergicos: medicamentoso... Fuma 5"},
                    {"documento": "D1", "pagina": 1, "frase": "ibuprofeno… nada que ver"},
                ],
            }
        ),
        CONTEXTO,
    )

    assert [o.frase for o in sugerencia.origenes] == [
        "Alergicos: medicamentoso",
        "Fuma 5",
        "ibuprofeno",
    ]
