"""Cobro de la consulta con factura electrónica (D-35)."""

from datetime import datetime
from decimal import Decimal
from urllib.parse import quote
from uuid import UUID

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel, Field

from vitalia.dominio.facturas import Ambiente, MedioDePago
from vitalia.dominio.facturas import Factura as FacturaDelDominio
from vitalia.entrada.rutas_citas import Cita
from vitalia.entrada.sesion import Sesion, casos

rutas = APIRouter(prefix="/api/v1")


class Factura(BaseModel):
    numero: str
    cufe: str
    concepto: str
    valor: int
    medio_pago: MedioDePago
    enlace_publico: str | None
    enlace_qr: str | None
    ambiente: Ambiente
    emitida_en: datetime

    @classmethod
    def de(cls, factura: FacturaDelDominio) -> "Factura":
        return cls(
            numero=factura.numero,
            cufe=factura.cufe,
            concepto=factura.concepto,
            valor=int(factura.valor),
            medio_pago=factura.medio,
            enlace_publico=factura.enlace_publico,
            enlace_qr=factura.enlace_qr,
            ambiente=factura.ambiente,
            emitida_en=factura.emitida_en,
        )


class Cobro(BaseModel):
    cita: Cita
    factura: Factura | None


class ListaDeCobros(BaseModel):
    ambiente: Ambiente
    cobros: list[Cobro]


class PedidoDeFactura(BaseModel):
    valor: int = Field(description="En pesos, sin centavos")
    medio_pago: str


@rutas.get("/cobros")
async def ver_cobros(identidad: Sesion, request: Request) -> ListaDeCobros:
    lista = await casos(request).cobros.ver(identidad)
    return ListaDeCobros(
        ambiente=lista.ambiente,
        cobros=[
            Cobro(cita=Cita.de(c.cita), factura=Factura.de(c.factura) if c.factura else None)
            for c in lista.cobros
        ],
    )


@rutas.post("/citas/{cita_id}/factura", status_code=status.HTTP_201_CREATED)
async def facturar(
    cita_id: UUID, pedido: PedidoDeFactura, identidad: Sesion, request: Request
) -> Factura:
    factura = await casos(request).cobros.facturar(
        identidad, cita_id, Decimal(pedido.valor), pedido.medio_pago
    )
    return Factura.de(factura)


@rutas.get("/citas/{cita_id}/factura/pdf")
async def pdf_de_la_factura(cita_id: UUID, identidad: Sesion, request: Request) -> Response:
    nombre, contenido = await casos(request).cobros.pdf(identidad, cita_id)
    return Response(
        contenido,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename*=UTF-8''{quote(nombre)}",
            "X-Content-Type-Options": "nosniff",
        },
    )
