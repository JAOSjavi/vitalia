"""Reglas del registro: documento, contraseña y mayoría de edad (HU-002, HU-004)."""

from datetime import date

import pytest

from vitalia.dominio.cuentas import (
    DatosDelPaciente,
    DatosInvalidos,
    Documento,
    MenorDeEdad,
    edad,
    faltas_de_la_contrasena,
    normalizar_documento,
    revisar_paciente,
)

HOY = date(2026, 10, 14)
ROSA = DatosDelPaciente(
    documento=Documento("CC", " 41.652.318 "),
    nombres=" Rosa Elena ",
    apellidos="Duarte",
    fecha_nacimiento=date(1958, 3, 2),
    telefono="318 555 0116",
    correo="Rosa@Ejemplo.co",
)


def test_el_documento_se_escribe_de_cualquier_forma() -> None:
    for escrito in ("41652318", "41.652.318", "41 652 318", "41-652-318"):
        assert normalizar_documento(Documento("CC", escrito)).numero == "41652318"


def test_la_contrasena_necesita_ocho_caracteres_y_un_numero() -> None:
    documento = Documento("CC", "41652318")

    assert faltas_de_la_contrasena("corta1", documento) == ["Debe tener al menos 8 caracteres"]
    assert faltas_de_la_contrasena("sinnumeros", documento) == ["Debe incluir al menos un número"]
    assert faltas_de_la_contrasena("girasol2026", documento) == []


def test_el_documento_nunca_sirve_como_contrasena() -> None:
    faltas = faltas_de_la_contrasena("41652318", Documento("CC", "41652318"))

    assert "No puede contener su número de documento" in faltas


def test_la_edad_cuenta_si_ya_cumplio_anos() -> None:
    assert edad(date(2008, 10, 14), HOY) == 18
    assert edad(date(2008, 10, 15), HOY) == 17


def test_el_registro_queda_limpio() -> None:
    datos = revisar_paciente(ROSA, "girasol2026", HOY)

    assert datos.documento.numero == "41652318"
    assert datos.nombres == "Rosa Elena"
    assert datos.telefono == "3185550116"
    assert datos.correo == "rosa@ejemplo.co"


def test_el_registro_dice_que_falta_en_cada_campo() -> None:
    malo = DatosDelPaciente(Documento("CC", "12"), "", "", date(1990, 1, 1), "12", "sin-arroba")

    with pytest.raises(DatosInvalidos) as error:
        revisar_paciente(malo, "corta", HOY)

    assert set(error.value.campos) == {
        "numero_documento",
        "nombres",
        "apellidos",
        "telefono",
        "correo",
        "contrasena",
    }


def test_un_menor_de_edad_no_se_registra() -> None:
    menor = DatosDelPaciente(
        ROSA.documento, "Ana", "Ruiz", date(2010, 1, 1), ROSA.telefono, ROSA.correo
    )

    with pytest.raises(MenorDeEdad):
        revisar_paciente(menor, "girasol2026", HOY)
