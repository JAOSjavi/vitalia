"""Reglas de las cuentas: documento, contraseña, mayoría de edad y datos de registro."""

import re
from dataclasses import dataclass, replace
from datetime import date, timedelta, timezone
from typing import Literal

TipoDocumento = Literal["CC", "CE", "PA", "PT"]
TIPOS_DE_DOCUMENTO: tuple[TipoDocumento, ...] = ("CC", "CE", "PA", "PT")
EDAD_MINIMA = 18
LARGO_MINIMO_DE_LA_CONTRASENA = 8

# Colombia no cambia la hora en el año.
COLOMBIA = timezone(timedelta(hours=-5), "Colombia")


class DatosInvalidos(Exception):
    """Uno o varios campos no sirven. Trae un mensaje para mostrar por cada campo."""

    def __init__(self, campos: dict[str, str]) -> None:
        super().__init__("Datos inválidos: " + ", ".join(campos))
        self.campos = campos


class MenorDeEdad(Exception):
    pass


class DocumentoYaRegistrado(Exception):
    pass


class AutorizacionDesactualizada(Exception):
    """El texto que la persona aceptó ya no es el vigente."""


class YaHayMedico(Exception):
    pass


class EnlaceInvalido(Exception):
    """El enlace no existe, ya se usó o venció."""


@dataclass(frozen=True)
class Documento:
    tipo: TipoDocumento
    numero: str


@dataclass(frozen=True)
class DatosDelPaciente:
    documento: Documento
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    telefono: str
    correo: str


@dataclass(frozen=True)
class DatosDelMedico:
    documento: Documento
    nombres: str
    apellidos: str
    correo: str


def normalizar_documento(documento: Documento) -> Documento:
    """Quita espacios, puntos y guiones: 41.652.318 y 41 652 318 son el mismo documento."""
    return replace(documento, numero=re.sub(r"[\s.\-]", "", documento.numero).upper())


def falta_del_documento(documento: Documento) -> str | None:
    if documento.tipo == "CC":
        if not re.fullmatch(r"\d{3,10}", documento.numero):
            return "La cédula debe tener entre 3 y 10 números"
    elif not re.fullmatch(r"[0-9A-Z]{3,20}", documento.numero):
        return "El número debe tener entre 3 y 20 letras o números"
    return None


def faltas_de_la_contrasena(contrasena: str, documento: Documento) -> list[str]:
    faltas = []
    if len(contrasena) < LARGO_MINIMO_DE_LA_CONTRASENA:
        faltas.append(f"Debe tener al menos {LARGO_MINIMO_DE_LA_CONTRASENA} caracteres")
    if not any(caracter.isdigit() for caracter in contrasena):
        faltas.append("Debe incluir al menos un número")
    # El documento identifica a la persona; nunca hace de contraseña (D-20).
    if documento.numero and documento.numero in re.sub(r"[\s.\-]", "", contrasena).upper():
        faltas.append("No puede contener su número de documento")
    return faltas


def edad(fecha_nacimiento: date, hoy: date) -> int:
    cumplio = (hoy.month, hoy.day) >= (fecha_nacimiento.month, fecha_nacimiento.day)
    return hoy.year - fecha_nacimiento.year - (0 if cumplio else 1)


def revisar_paciente(datos: DatosDelPaciente, contrasena: str, hoy: date) -> DatosDelPaciente:
    """Normaliza y revisa el registro. Lanza DatosInvalidos o MenorDeEdad."""
    datos = replace(
        datos,
        documento=normalizar_documento(datos.documento),
        nombres=datos.nombres.strip(),
        apellidos=datos.apellidos.strip(),
        telefono=re.sub(r"[\s\-()]", "", datos.telefono),
        correo=datos.correo.strip().lower(),
    )
    campos = _faltas_comunes(datos.documento, datos.nombres, datos.apellidos, datos.correo)
    if not re.fullmatch(r"\+?\d{7,15}", datos.telefono):
        campos["telefono"] = "Escriba un teléfono de 7 a 15 números"
    if datos.fecha_nacimiento > hoy:
        campos["fecha_nacimiento"] = "La fecha de nacimiento no puede ser futura"
    if faltas := faltas_de_la_contrasena(contrasena, datos.documento):
        campos["contrasena"] = ". ".join(faltas)
    if campos:
        raise DatosInvalidos(campos)
    if edad(datos.fecha_nacimiento, hoy) < EDAD_MINIMA:
        raise MenorDeEdad()
    return datos


def revisar_medico(datos: DatosDelMedico, contrasena: str) -> DatosDelMedico:
    datos = replace(
        datos,
        documento=normalizar_documento(datos.documento),
        nombres=datos.nombres.strip(),
        apellidos=datos.apellidos.strip(),
        correo=datos.correo.strip().lower(),
    )
    campos = _faltas_comunes(datos.documento, datos.nombres, datos.apellidos, datos.correo)
    if faltas := faltas_de_la_contrasena(contrasena, datos.documento):
        campos["contrasena"] = ". ".join(faltas)
    if campos:
        raise DatosInvalidos(campos)
    return datos


def _faltas_comunes(
    documento: Documento, nombres: str, apellidos: str, correo: str
) -> dict[str, str]:
    campos: dict[str, str] = {}
    if falta := falta_del_documento(documento):
        campos["numero_documento"] = falta
    if not nombres:
        campos["nombres"] = "Escriba sus nombres"
    if not apellidos:
        campos["apellidos"] = "Escriba sus apellidos"
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
        campos["correo"] = "Escriba un correo válido"
    return campos
