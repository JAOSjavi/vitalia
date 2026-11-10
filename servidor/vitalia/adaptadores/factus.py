"""Factus, el proveedor de factura electrónica (D-35). Documentación: developers.factus.com.co.

Se habla por HTTP directo con httpx, como con Qwen. Las credenciales nunca se escriben en el
registro ni en un mensaje de error.

- El token dura una hora: se guarda y se pide otro un minuto antes de que venza.
- La factura es la estándar (operation_type 10) a una persona natural. La del sector salud queda
  para cuando se resuelva la pregunta 6 del marco normativo.
- La consulta médica está excluida de IVA (art. 476 del Estatuto Tributario).
"""

import asyncio
import base64
import time
from typing import Any

import httpx

from vitalia.dominio.facturas import (
    Ambiente,
    Emitida,
    FacturadorNoDisponible,
    FacturaRechazada,
    MedioDePago,
    Pedido,
)

_SEGUNDOS = 60
# Códigos de la tabla "Tipos de documentos de identidad" de Factus.
_DOCUMENTOS = {"CC": "13", "CE": "22", "PA": "41", "PT": "48"}
# Códigos de la tabla "Métodos de pago".
_MEDIOS: dict[MedioDePago, str] = {
    "efectivo": "10",
    "transferencia": "47",
    "tarjeta_debito": "49",
    "tarjeta_credito": "48",
}
# "Factura de Venta" en la tabla de tipos de documento de los rangos de numeración.
_RANGO_DE_FACTURAS = "21"


class FacturadorFactus:
    def __init__(
        self,
        direccion: str,
        client_id: str,
        client_secret: str,
        usuario: str,
        contrasena: str,
        rango_id: int | None = None,
        transporte: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._direccion = direccion.rstrip("/")
        self._credenciales = {
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            "username": usuario,
            "password": contrasena,
        }
        self._rango_id = rango_id
        self._transporte = transporte
        self._token: str | None = None
        self._vence = 0.0
        self._candado = asyncio.Lock()

    @property
    def ambiente(self) -> Ambiente:
        return "pruebas" if "sandbox" in self._direccion else "produccion"

    async def emitir(self, pedido: Pedido) -> Emitida:
        async with self._cliente() as cliente:
            cuerpo = _cuerpo(pedido, await self._rango(cliente))
            respuesta = await self._pedir(cliente, "POST", "/v2/bills/validate", json=cuerpo)
            if respuesta.status_code == 409:
                # Quedó una pendiente con esta referencia sin validar: se borra y se repite.
                await self._pedir(
                    cliente, "DELETE", f"/v2/bills/destroy/reference/{pedido.referencia}"
                )
                respuesta = await self._pedir(cliente, "POST", "/v2/bills/validate", json=cuerpo)
        datos = _datos(respuesta)
        factura = datos.get("bill", datos)
        enlaces = factura.get("links") or {}
        if not factura.get("number") or not factura.get("cufe"):
            raise FacturaRechazada(["Factus no devolvió el número ni el CUFE de la factura"])
        return Emitida(
            numero=str(factura["number"]),
            cufe=str(factura["cufe"]),
            enlace_publico=enlaces.get("public_url") or factura.get("public_url"),
            enlace_qr=enlaces.get("qr") or factura.get("qr"),
        )

    async def pdf(self, numero: str) -> tuple[str, bytes]:
        async with self._cliente() as cliente:
            respuesta = await self._pedir(cliente, "GET", f"/v2/bills/{numero}/download-pdf")
        datos = _datos(respuesta)
        nombre = str(datos.get("file_name") or numero)
        if not nombre.lower().endswith(".pdf"):
            nombre += ".pdf"
        return nombre, base64.b64decode(datos["pdf_base_64_encoded"])

    async def probar(self) -> int | None:
        """Pide un token y busca el rango de facturas. Sirve para revisar las credenciales."""
        async with self._cliente() as cliente:
            await self._token_vigente(cliente, renovar=True)
            return await self._rango(cliente)

    # --- Conexión

    def _cliente(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._direccion,
            timeout=_SEGUNDOS,
            transport=self._transporte,
            headers={"Accept": "application/json"},
        )

    async def _pedir(
        self, cliente: httpx.AsyncClient, metodo: str, ruta: str, **mas: Any
    ) -> httpx.Response:
        for intento in range(2):
            token = await self._token_vigente(cliente, renovar=intento > 0)
            try:
                respuesta = await cliente.request(
                    metodo, ruta, headers={"Authorization": f"Bearer {token}"}, **mas
                )
            except httpx.HTTPError as error:
                raise FacturadorNoDisponible("Factus no respondió") from error
            # Un token que Factus ya no acepta se cambia una vez.
            if respuesta.status_code != 401:
                return respuesta
        raise FacturadorNoDisponible("Factus no aceptó las credenciales")

    async def _token_vigente(self, cliente: httpx.AsyncClient, renovar: bool) -> str:
        async with self._candado:
            if self._token and not renovar and time.monotonic() < self._vence:
                return self._token
            try:
                respuesta = await cliente.post("/oauth/token", data=self._credenciales)
            except httpx.HTTPError as error:
                raise FacturadorNoDisponible("Factus no respondió") from error
            if respuesta.status_code != 200:
                raise FacturadorNoDisponible(
                    f"Factus no aceptó las credenciales ({respuesta.status_code})"
                )
            cuerpo = respuesta.json()
            self._token = str(cuerpo["access_token"])
            self._vence = time.monotonic() + int(cuerpo.get("expires_in", 3600)) - 60
            return self._token

    async def _rango(self, cliente: httpx.AsyncClient) -> int | None:
        """El rango de numeración de facturas: el configurado o el primero activo y vigente."""
        if self._rango_id is not None:
            return self._rango_id
        respuesta = await self._pedir(
            cliente,
            "GET",
            "/v2/numbering-ranges",
            params={"filter[document]": _RANGO_DE_FACTURAS, "filter[is_active]": "1"},
        )
        if respuesta.status_code != 200:
            return None
        datos = respuesta.json().get("data")
        rangos = datos.get("data", []) if isinstance(datos, dict) else (datos or [])
        vigentes = [r for r in rangos if not int(r.get("is_expired") or 0)]
        if vigentes:
            self._rango_id = int(vigentes[0]["id"])
        return self._rango_id


def _datos(respuesta: httpx.Response) -> dict[str, Any]:
    if respuesta.status_code >= 500:
        raise FacturadorNoDisponible(f"Factus respondió {respuesta.status_code}")
    try:
        cuerpo = respuesta.json()
    except ValueError as error:
        raise FacturadorNoDisponible("Factus respondió algo que no se entiende") from error
    if respuesta.status_code >= 400:
        raise FacturaRechazada(_motivos(cuerpo))
    datos: dict[str, Any] = cuerpo.get("data") or {}
    return datos


def _motivos(cuerpo: Any) -> list[str]:
    """Factus pone los errores en data.errors (por campo o como lista) o en message."""
    motivos: list[str] = []
    datos = cuerpo.get("data") if isinstance(cuerpo, dict) else None
    errores = datos.get("errors") if isinstance(datos, dict) else None
    if isinstance(errores, dict):
        for campo, lista in errores.items():
            for texto in lista if isinstance(lista, list) else [lista]:
                motivos.append(f"{campo}: {texto}")
    elif isinstance(errores, list):
        motivos += [str(e) for e in errores]
    if not motivos and isinstance(cuerpo, dict) and cuerpo.get("message"):
        motivos.append(str(cuerpo["message"]))
    return motivos or ["Factus rechazó la factura sin decir por qué"]


def _cuerpo(pedido: Pedido, rango_id: int | None) -> dict[str, Any]:
    cliente = pedido.cliente
    valor = f"{pedido.valor:.2f}"
    datos_cliente: dict[str, Any] = {
        "identification_document_code": _DOCUMENTOS[cliente.documento.tipo],
        "identification": cliente.documento.numero,
        "legal_organization_code": "2",
        "names": f"{cliente.nombres} {cliente.apellidos}",
        "tribute_code": "ZZ",
        "responsibilities": ["R-99-PN"],
        "country_code": "CO",
    }
    for campo, dato in (
        ("email", cliente.correo),
        ("phone", cliente.telefono),
        ("address", cliente.direccion),
    ):
        if dato:
            datos_cliente[campo] = dato
    cuerpo: dict[str, Any] = {
        "reference_code": pedido.referencia,
        "document": "01",
        "operation_type": "10",
        "observation": pedido.observacion[:250],
        "payment_details": [
            {
                "payment_form": "1",
                "payment_method_code": _MEDIOS[pedido.medio],
                "amount": valor,
            }
        ],
        "customer": datos_cliente,
        "items": [
            {
                "code_reference": "CONSULTA",
                "name": pedido.concepto,
                "quantity": "1.00",
                "discount_rate": "0.00",
                "price": valor,
                "unit_measure_code": "94",
                "standard_code": "999",
                "taxes": [{"code": "01", "rate": "0.00", "is_excluded": True}],
            }
        ],
    }
    if rango_id is not None:
        cuerpo["numbering_range_id"] = rango_id
    return cuerpo
