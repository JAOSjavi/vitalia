"""El adaptador de Factus, contra un servidor de mentira que responde como el sandbox."""

import base64
import json
from decimal import Decimal

import httpx
import pytest

from vitalia.adaptadores.factus import FacturadorFactus
from vitalia.dominio.cuentas import Documento
from vitalia.dominio.facturas import (
    Cliente,
    FacturadorNoDisponible,
    FacturaRechazada,
    Pedido,
)

DIRECCION = "https://api-sandbox.factus.com.co"


def _pedido(referencia: str = "cita-1") -> Pedido:
    return Pedido(
        referencia=referencia,
        cliente=Cliente(
            documento=Documento("CC", "41652318"),
            nombres="Rosa Elena",
            apellidos="Duarte",
            correo="rosa@ejemplo.test",
            telefono="3001234567",
            direccion=None,
        ),
        concepto="Consulta médica: Consulta general",
        valor=Decimal("80000"),
        medio="transferencia",
        observacion="Atención del 04/08/2031",
    )


_VALIDADA = {
    "status": "Created",
    "data": {
        "number": "SETP990000101",
        "cufe": "cufe-de-prueba",
        "is_validated": True,
        "links": {"qr": "https://dian.test/qr", "public_url": "https://factus.test/f/1"},
    },
}


def _facturador(responder: object) -> FacturadorFactus:
    return FacturadorFactus(
        DIRECCION,
        "id",
        "secreto",
        "correo@ejemplo.test",
        "clave",
        rango_id=8,
        transporte=httpx.MockTransport(responder),  # type: ignore[arg-type]
    )


def _token(pedido: httpx.Request) -> httpx.Response | None:
    if pedido.url.path == "/oauth/token":
        return httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    return None


async def test_emite_una_factura_estandar_a_persona_natural_sin_iva() -> None:
    enviados: list[dict[str, object]] = []
    tokens = 0

    def responder(pedido: httpx.Request) -> httpx.Response:
        nonlocal tokens
        if (respuesta := _token(pedido)) is not None:
            tokens += 1
            assert b"grant_type=password" in pedido.content
            return respuesta
        assert pedido.headers["Authorization"] == "Bearer tok"
        enviados.append(json.loads(pedido.content))
        return httpx.Response(201, json=_VALIDADA)

    facturador = _facturador(responder)
    emitida = await facturador.emitir(_pedido())
    await facturador.emitir(_pedido("cita-2"))

    assert emitida.numero == "SETP990000101" and emitida.cufe == "cufe-de-prueba"
    assert emitida.enlace_publico == "https://factus.test/f/1"
    assert tokens == 1  # el token se guarda una hora
    cuerpo = enviados[0]
    assert cuerpo["reference_code"] == "cita-1" and cuerpo["numbering_range_id"] == 8
    cliente = cuerpo["customer"]
    assert cliente["identification_document_code"] == "13"  # type: ignore[index]
    assert cliente["legal_organization_code"] == "2"  # type: ignore[index]
    assert cliente["names"] == "Rosa Elena Duarte"  # type: ignore[index]
    assert "address" not in cliente  # type: ignore[operator]
    assert cliente["municipality_code"] == "11001"  # type: ignore[index]
    item = cuerpo["items"][0]  # type: ignore[index]
    assert item["price"] == "80000.00"
    assert item["taxes"] == [{"code": "01", "rate": "0.00", "is_excluded": True}]
    assert cuerpo["payment_details"][0]["payment_method_code"] == "47"  # type: ignore[index]


async def test_una_pendiente_con_la_misma_referencia_se_borra_y_se_repite() -> None:
    rutas: list[str] = []

    def responder(pedido: httpx.Request) -> httpx.Response:
        if (respuesta := _token(pedido)) is not None:
            return respuesta
        rutas.append(f"{pedido.method} {pedido.url.path}")
        if pedido.method == "POST" and rutas.count("POST /v2/bills/validate") == 1:
            return httpx.Response(409, json={"message": "Se encontró una factura pendiente"})
        if pedido.method == "DELETE":
            return httpx.Response(200, json={"message": "Eliminada"})
        return httpx.Response(201, json=_VALIDADA)

    emitida = await _facturador(responder).emitir(_pedido())

    assert rutas == [
        "POST /v2/bills/validate",
        "DELETE /v2/bills/destroy/reference/cita-1",
        "POST /v2/bills/validate",
    ]
    assert emitida.numero == "SETP990000101"


async def test_los_motivos_del_rechazo_llegan_completos() -> None:
    def responder(pedido: httpx.Request) -> httpx.Response:
        if (respuesta := _token(pedido)) is not None:
            return respuesta
        return httpx.Response(
            422,
            json={
                "message": "Validation error",
                "data": {"errors": {"customer.identification": ["Debe ser numérico"]}},
            },
        )

    with pytest.raises(FacturaRechazada) as rechazo:
        await _facturador(responder).emitir(_pedido())

    assert rechazo.value.motivos == ["customer.identification: Debe ser numérico"]


async def test_credenciales_malas_o_factus_caido_se_pueden_reintentar() -> None:
    def sin_credenciales(pedido: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "invalid_client"})

    def caido(pedido: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("sin red")

    with pytest.raises(FacturadorNoDisponible) as malas:
        await _facturador(sin_credenciales).emitir(_pedido())
    with pytest.raises(FacturadorNoDisponible):
        await _facturador(caido).emitir(_pedido())

    assert "secreto" not in str(malas.value) and "clave" not in str(malas.value)


async def test_el_pdf_llega_decodificado() -> None:
    def responder(pedido: httpx.Request) -> httpx.Response:
        if (respuesta := _token(pedido)) is not None:
            return respuesta
        assert pedido.url.path == "/v2/bills/SETP990000101/download-pdf"
        contenido = base64.b64encode(b"%PDF-1.4 factura").decode()
        return httpx.Response(
            200, json={"data": {"file_name": "SETP990000101", "pdf_base_64_encoded": contenido}}
        )

    nombre, contenido = await _facturador(responder).pdf("SETP990000101")

    assert nombre == "SETP990000101.pdf"
    assert contenido == b"%PDF-1.4 factura"


async def test_sin_rango_configurado_usa_el_primero_activo_y_vigente() -> None:
    enviados: list[dict[str, object]] = []

    def responder(pedido: httpx.Request) -> httpx.Response:
        if (respuesta := _token(pedido)) is not None:
            return respuesta
        if pedido.url.path == "/v2/numbering-ranges":
            assert pedido.url.params["filter[document]"] == "21"
            return httpx.Response(
                200,
                json={"data": {"data": [{"id": 4, "is_expired": 1}, {"id": 9, "is_expired": 0}]}},
            )
        enviados.append(json.loads(pedido.content))
        return httpx.Response(201, json=_VALIDADA)

    facturador = FacturadorFactus(
        DIRECCION, "id", "secreto", "c", "clave", transporte=httpx.MockTransport(responder)
    )
    await facturador.emitir(_pedido())

    assert enviados[0]["numbering_range_id"] == 9
    assert facturador.ambiente == "pruebas"
