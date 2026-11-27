"""Cobrar una cita atendida con factura electrónica (D-35; reemplaza el botón sin función HU-026).

El médico ve las citas atendidas de los últimos días, escribe el valor y cómo pagó el paciente,
y Vitalia le pide la factura a Factus. Lo que devuelve la DIAN (número y CUFE) queda guardado.
"""

from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Cita, Facturador, FacturaNueva, Reloj, UnidadDeTrabajo
from vitalia.dominio.cuentas import COLOMBIA
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.facturas import (
    Ambiente,
    CitaNoFacturable,
    Cliente,
    Factura,
    Pedido,
    concepto_de,
    revisar_cobro,
)
from vitalia.dominio.identidad import Identidad

DIAS_ATRAS = 30


@dataclass(frozen=True)
class Cobro:
    cita: Cita
    factura: Factura | None


@dataclass(frozen=True)
class ListaDeCobros:
    ambiente: Ambiente
    cobros: list[Cobro]


class Cobros:
    def __init__(
        self,
        unidad: UnidadDeTrabajo,
        autorizador: Autorizador,
        facturador: Facturador,
        reloj: Reloj,
    ) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._facturador = facturador
        self._reloj = reloj

    async def ver(self, identidad: Identidad) -> ListaDeCobros:
        """Las citas atendidas de los últimos 30 días, la más reciente primero, con su factura."""
        await self._autorizador.exigir(identidad, "facturas.ver")
        desde = self._reloj.ahora() - timedelta(days=DIAS_ATRAS)
        async with self._unidad.abrir(identidad) as trabajo:
            citas = await trabajo.agenda.citas(desde=desde, estado="atendida")
            facturas = await trabajo.facturas.de_las_citas([c.id for c in citas])
        cobros = [Cobro(c, facturas.get(c.id)) for c in reversed(citas)]
        return ListaDeCobros(self._facturador.ambiente, cobros)

    async def facturar(
        self, identidad: Identidad, cita_id: UUID, valor: Decimal, medio: str
    ) -> Factura:
        await self._autorizador.exigir(identidad, "facturas.emitir")
        assert identidad.usuario_id is not None
        medio_de_pago = revisar_cobro(valor, medio)

        async with self._unidad.abrir(identidad) as trabajo:
            cita = await trabajo.agenda.cita(cita_id)
            if cita is None:
                raise NoEncontrado()
            if cita.estado != "atendida":
                raise CitaNoFacturable()
            ya_emitida = await trabajo.facturas.de_la_cita(cita_id)
            if ya_emitida is not None:
                return ya_emitida
            ficha = await trabajo.pacientes.ficha(cita.paciente_id)
            if ficha is None:
                raise NoEncontrado()
            direccion = await trabajo.facturas.direccion_del_paciente(cita.paciente_id)

        # Factus tarda unos segundos: no se tiene la transacción abierta mientras responde.
        dia = cita.inicio.astimezone(COLOMBIA).strftime("%d/%m/%Y")
        pedido = Pedido(
            referencia=str(cita.id),
            cliente=Cliente(
                documento=ficha.documento,
                nombres=ficha.nombres,
                apellidos=ficha.apellidos,
                correo=ficha.correo,
                telefono=ficha.telefono,
                direccion=direccion,
            ),
            concepto=concepto_de(cita.tipo),
            valor=valor,
            medio=medio_de_pago,
            observacion=f"Atención del {dia}",
        )
        emitida = await self._facturador.emitir(pedido)

        async with self._unidad.abrir(identidad) as trabajo:
            factura = await trabajo.facturas.guardar(
                FacturaNueva(
                    cita_id=cita.id,
                    paciente_id=cita.paciente_id,
                    emitida_por=identidad.usuario_id,
                    concepto=pedido.concepto,
                    valor=valor,
                    medio=medio_de_pago,
                    emitida=emitida,
                    ambiente=self._facturador.ambiente,
                )
            )
            await trabajo.bitacora.registrar(
                "emision_de_factura", paciente_id=cita.paciente_id, objeto=factura.numero
            )
        return factura

    async def mias(self, identidad: Identidad) -> list[Factura]:
        """Las facturas del paciente de la sesión: la base no le deja ver otras."""
        await self._autorizador.exigir(identidad, "facturas.propias")
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.facturas.todas()

    async def pdf(self, identidad: Identidad, cita_id: UUID) -> tuple[str, bytes]:
        """El médico abre cualquiera; el paciente, solo las suyas."""
        permiso = "facturas.propias" if identidad.clase == "paciente" else "facturas.ver"
        await self._autorizador.exigir(identidad, permiso)
        async with self._unidad.abrir(identidad) as trabajo:
            factura = await trabajo.facturas.de_la_cita(cita_id)
            if factura is None:
                raise NoEncontrado()
            await trabajo.bitacora.registrar(
                "descarga_de_factura", paciente_id=factura.paciente_id, objeto=factura.numero
            )
        return await self._facturador.pdf(factura.numero)
