"""El adaptador de Qwen, contra un servidor de mentira que responde como el de Alibaba."""

import json

import httpx
import pytest

from vitalia.adaptadores.ia.qwen import ErrorDelProveedor, IAQwen, VectoresQwen
from vitalia.casos_de_uso.puertos import ProveedorIA, ProveedorNoDisponible, Turno, Vectorizador

DIRECCION = "https://espacio.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"


def servidor(responder: object) -> httpx.MockTransport:
    return httpx.MockTransport(responder)  # type: ignore[arg-type]


async def test_vectoriza_de_a_diez_textos_y_en_orden() -> None:
    peticiones: list[dict[str, object]] = []

    def responder(pedido: httpx.Request) -> httpx.Response:
        cuerpo = json.loads(pedido.content)
        peticiones.append(cuerpo)
        assert pedido.headers["Authorization"] == "Bearer clave-de-prueba"
        # El proveedor puede devolverlos desordenados: cada uno trae su índice.
        datos = [
            {"index": i, "embedding": [float(len(t)), 1.0]} for i, t in enumerate(cuerpo["input"])
        ]
        return httpx.Response(200, json={"data": list(reversed(datos))})

    vectores: Vectorizador = VectoresQwen(
        DIRECCION, "clave-de-prueba", "qwen3.7-text-embedding", 2, servidor(responder)
    )
    textos = [f"texto {'x' * n}" for n in range(12)]

    resultado = await vectores.vectorizar(textos)

    assert [len(p["input"]) for p in peticiones] == [10, 2]  # type: ignore[arg-type]
    assert peticiones[0]["dimensions"] == 2
    assert [v[0] for v in resultado] == [float(len(t)) for t in textos]


async def test_responde_por_partes_con_las_instrucciones_y_la_conversacion() -> None:
    recibido: dict[str, object] = {}

    def responder(pedido: httpx.Request) -> httpx.Response:
        recibido.update(json.loads(pedido.content))
        eventos = [
            {"choices": [{"delta": {"role": "assistant"}}]},
            {"choices": [{"delta": {"content": "El LDL "}}]},
            {"choices": [{"delta": {"content": "fue 168."}}]},
            {"choices": [], "usage": {"total_tokens": 20}},
        ]
        cuerpo = "".join(f"data: {json.dumps(e)}\n\n" for e in eventos) + "data: [DONE]\n\n"
        return httpx.Response(200, text=cuerpo, headers={"content-type": "text/event-stream"})

    ia: ProveedorIA = IAQwen(DIRECCION, "clave", "qwen3.7-plus", "lector", servidor(responder))
    turnos = [Turno("medico", "¿LDL?"), Turno("asistente", "168."), Turno("medico", "¿Y antes?")]

    partes = [p async for p in ia.responder("Instrucciones fijas", turnos)]

    assert partes == ["El LDL ", "fue 168."]
    assert recibido["stream"] is True
    assert recibido["temperature"] == 0
    assert recibido["messages"] == [
        {"role": "system", "content": "Instrucciones fijas"},
        {"role": "user", "content": "¿LDL?"},
        {"role": "assistant", "content": "168."},
        {"role": "user", "content": "¿Y antes?"},
    ]


async def test_un_rechazo_del_proveedor_se_vuelve_proveedor_no_disponible() -> None:
    def responder(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            json={"error": {"code": "AccessDenied.Unpurchased", "message": "Access denied"}},
        )

    ia = IAQwen(DIRECCION, "clave-secreta", "qwen3.7-plus", "lector", servidor(responder))

    with pytest.raises(ErrorDelProveedor) as error:
        _ = [p async for p in ia.responder("x", [Turno("medico", "hola")])]

    assert isinstance(error.value, ProveedorNoDisponible)
    assert (error.value.estado, error.value.codigo) == (403, "AccessDenied.Unpurchased")
    assert "clave-secreta" not in str(error.value)


async def test_sin_conexion_tambien_es_proveedor_no_disponible() -> None:
    def responder(pedido: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("sin red", request=pedido)

    vectores = VectoresQwen(DIRECCION, "clave", "modelo", 2, servidor(responder))

    with pytest.raises(ProveedorNoDisponible):
        await vectores.vectorizar(["texto"])


async def test_lee_una_pagina_enviando_la_imagen() -> None:
    recibido: dict[str, object] = {}

    def responder(pedido: httpx.Request) -> httpx.Response:
        recibido.update(json.loads(pedido.content))
        return httpx.Response(
            200, json={"choices": [{"message": {"content": "  Glucemia 118 mg/dL \n"}}]}
        )

    ia = IAQwen(DIRECCION, "clave", "respuestas", "qwen-vl-ocr-2025-11-20", servidor(responder))

    texto = await ia.leer_pagina(b"\x89PNG\r\n\x1a\n imagen")

    assert texto == "Glucemia 118 mg/dL"
    assert recibido["model"] == "qwen-vl-ocr-2025-11-20"
    contenido = recibido["messages"][0]["content"]  # type: ignore[index]
    assert contenido[0]["image_url"]["url"].startswith("data:image/png;base64,")
