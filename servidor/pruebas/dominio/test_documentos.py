"""Reglas de los documentos: qué archivo se acepta y cuándo una página quedó leída."""

from datetime import date

import pytest

from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.documentos import (
    TAMANO_MAXIMO,
    ArchivoRecibido,
    estado_final,
    legibilidad,
    tiene_texto,
    validar_archivo,
)

HOY = date(2026, 10, 28)
PDF = b"%PDF-1.4 contenido"


def recibido(**cambios: object) -> ArchivoRecibido:
    datos: dict[str, object] = {
        "nombre": "Control de octubre",
        "fecha_documento": date(2026, 10, 1),
        "tipo": "historia_clinica",
        "contenido": PDF,
    }
    datos.update(cambios)
    return ArchivoRecibido(**datos)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("contenido", "formato"),
    [
        (b"%PDF-1.7 ...", "pdf"),
        (b"\xff\xd8\xff\xe0 foto", "jpg"),
        (b"\x89PNG\r\n\x1a\n imagen", "png"),
    ],
)
def test_reconoce_el_formato_por_el_contenido(contenido: bytes, formato: str) -> None:
    valido = validar_archivo(recibido(contenido=contenido), HOY)

    assert valido.formato == formato
    assert len(valido.huella) == 64


def test_rechaza_otro_formato_aunque_el_nombre_diga_pdf() -> None:
    with pytest.raises(DatosInvalidos) as error:
        validar_archivo(recibido(nombre="examen.pdf", contenido=b"PK\x03\x04 un zip"), HOY)

    assert error.value.campos == {"archivo": "Solo se aceptan archivos PDF, JPG o PNG"}


def test_rechaza_mas_de_20_mb_y_el_archivo_vacio() -> None:
    with pytest.raises(DatosInvalidos) as grande:
        validar_archivo(recibido(contenido=PDF + b"0" * TAMANO_MAXIMO), HOY)
    with pytest.raises(DatosInvalidos) as vacio:
        validar_archivo(recibido(contenido=b""), HOY)

    assert grande.value.campos == {"archivo": "El archivo pesa más de 20 MB"}
    assert vacio.value.campos == {"archivo": "El archivo está vacío"}


def test_dice_que_falta_en_cada_campo() -> None:
    with pytest.raises(DatosInvalidos) as error:
        validar_archivo(
            recibido(nombre="  ", fecha_documento=date(2026, 10, 29), tipo="radiografia"), HOY
        )

    assert set(error.value.campos) == {"nombre", "fecha_documento", "tipo"}


def test_el_mismo_contenido_da_la_misma_huella() -> None:
    uno = validar_archivo(recibido(nombre="Uno"), HOY)
    otro = validar_archivo(recibido(nombre="Otro nombre"), HOY)

    assert uno.huella == otro.huella


def test_una_pagina_cuenta_como_leida_con_suficientes_letras() -> None:
    assert tiene_texto("Motivo de consulta: control de la presión arterial y del colesterol.")
    assert not tiene_texto("Página 2")
    assert not tiene_texto("   \n  ")


def test_el_documento_es_legible_si_alguna_pagina_trae_texto() -> None:
    texto = "Diagnóstico principal: I10 Hipertensión esencial, confirmado repetido."

    assert estado_final(["", texto]) == "legible"
    assert estado_final(["", "Firma"]) == "no_legible"


def test_la_legibilidad_cuenta_las_palabras_marcadas_ilegibles() -> None:
    assert legibilidad("Glucosa 92 mg/dL") == 1
    assert legibilidad("Glucosa [ilegible] mg/dL [ilegible]") == 0.5
    assert legibilidad("") == 0
