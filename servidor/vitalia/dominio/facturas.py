"""Factura electrónica de una consulta (D-35): qué se cobra, a quién y con qué medio."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal, get_args
from uuid import UUID

from vitalia.dominio.cuentas import DatosInvalidos, Documento

MedioDePago = Literal["efectivo", "transferencia", "tarjeta_debito", "tarjeta_credito"]
MEDIOS_DE_PAGO: tuple[MedioDePago, ...] = get_args(MedioDePago)

Ambiente = Literal["pruebas", "produccion", "de_mentira"]

# Una consulta de medicina general particular. Fuera de esto casi siempre es un error de dedo.
VALOR_MINIMO = Decimal("1000")
VALOR_MAXIMO = Decimal("5000000")


class CitaNoFacturable(Exception):
    """Solo se factura una cita atendida."""


class FacturaRechazada(Exception):
    """Factus o la DIAN rechazaron la factura. Trae los motivos tal como llegaron."""

    def __init__(self, motivos: list[str]) -> None:
        super().__init__("; ".join(motivos))
        self.motivos = motivos


class FacturadorNoDisponible(Exception):
    """Factus no respondió, tardó demasiado o no aceptó las credenciales. Se puede reintentar."""


@dataclass(frozen=True)
class Cliente:
    documento: Documento
    nombres: str
    apellidos: str
    correo: str | None
    telefono: str | None
    direccion: str | None


@dataclass(frozen=True)
class Pedido:
    """Lo que se le pide a Factus. La referencia es la cita: repetirla no crea otra factura."""

    referencia: str
    cliente: Cliente
    concepto: str
    valor: Decimal
    medio: MedioDePago
    observacion: str


@dataclass(frozen=True)
class Emitida:
    """Lo que Factus devuelve cuando la DIAN valida la factura."""

    numero: str
    cufe: str
    enlace_publico: str | None
    enlace_qr: str | None


@dataclass(frozen=True)
class Factura:
    id: UUID
    cita_id: UUID
    paciente_id: UUID
    concepto: str
    valor: Decimal
    medio: MedioDePago
    numero: str
    cufe: str
    enlace_publico: str | None
    enlace_qr: str | None
    ambiente: Ambiente
    emitida_en: datetime


def revisar_cobro(valor: Decimal, medio: str) -> MedioDePago:
    campos = {}
    if not VALOR_MINIMO <= valor <= VALOR_MAXIMO:
        campos["valor"] = "Escriba un valor entre $1.000 y $5.000.000"
    elif valor != valor.quantize(Decimal("1")):
        campos["valor"] = "Escriba el valor en pesos, sin centavos"
    if medio not in MEDIOS_DE_PAGO:
        campos["medio_pago"] = "Elija cómo pagó el paciente"
    if campos:
        raise DatosInvalidos(campos)
    return medio  # type: ignore[return-value]


def concepto_de(tipo_de_cita: str) -> str:
    """El concepto dice el tipo de cita y nunca el diagnóstico: la historia clínica es reservada."""
    return f"Consulta médica: {tipo_de_cita}"[:200]
