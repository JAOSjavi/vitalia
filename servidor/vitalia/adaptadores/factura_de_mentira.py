"""Un facturador sin Factus: para las pruebas y para programar sin credenciales.

Las facturas que entrega dicen "de mentira" en el ambiente y no tienen validez ante la DIAN.
"""

import hashlib

from vitalia.dominio.facturas import Ambiente, Emitida, Pedido

# Un PDF mínimo de una página en blanco: basta para probar la descarga.
_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)


class FacturadorDeMentira:
    def __init__(self) -> None:
        self.pedidos: list[Pedido] = []
        self._por_referencia: dict[str, Emitida] = {}

    @property
    def ambiente(self) -> Ambiente:
        return "de_mentira"

    async def emitir(self, pedido: Pedido) -> Emitida:
        self.pedidos.append(pedido)
        # Igual que Factus: la misma referencia devuelve la misma factura.
        if pedido.referencia not in self._por_referencia:
            numero = f"PRUEBA{len(self._por_referencia) + 1:05d}"
            cufe = hashlib.sha384(pedido.referencia.encode()).hexdigest()
            self._por_referencia[pedido.referencia] = Emitida(numero, cufe, None, None)
        return self._por_referencia[pedido.referencia]

    async def pdf(self, numero: str) -> tuple[str, bytes]:
        return f"{numero}.pdf", _PDF
