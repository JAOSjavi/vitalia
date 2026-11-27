"""Reglas de la historia clínica (HU-041, HU-043)."""

from decimal import Decimal

import pytest

from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.historia_clinica import (
    CAMPOS_DE_IDENTIFICACION,
    CAMPOS_DE_LA_ATENCION,
    NO_REFIERE,
    Diagnostico,
    faltantes,
    indice_de_masa_corporal,
    revisar,
    revisar_diagnosticos,
    revisar_medicamentos,
)


def test_un_signo_vital_imposible_pide_revisarlo() -> None:
    with pytest.raises(DatosInvalidos) as error:
        revisar({"temperatura": "53", "frecuencia_cardiaca": 72}, CAMPOS_DE_LA_ATENCION)
    assert error.value.campos == {"temperatura": "Revise el valor: debe estar entre 30 y 45 °C"}


def test_acepta_decimales_con_coma_y_deja_vacio_lo_que_no_se_ha_escrito() -> None:
    limpios = revisar(
        {"temperatura": "36,8", "peso": 72.35, "motivo": "  ", "talla": "168"},
        CAMPOS_DE_LA_ATENCION,
    )
    assert limpios == {
        "temperatura": Decimal("36.8"),
        "peso": Decimal("72.4"),
        "motivo": None,
        "talla": 168,
    }


def test_rechaza_campos_que_no_existen_y_opciones_fuera_de_la_lista() -> None:
    with pytest.raises(DatosInvalidos) as error:
        revisar({"agudeza_visual": "20/40", "causa": "picadura"}, CAMPOS_DE_LA_ATENCION)
    assert set(error.value.campos) == {"agudeza_visual", "causa"}


def test_el_indice_de_masa_corporal_se_calcula_con_peso_y_talla() -> None:
    assert indice_de_masa_corporal(Decimal("72.0"), 168) == Decimal("25.5")
    assert indice_de_masa_corporal(None, 168) is None


def test_diagnosticos_de_la_lista_con_un_solo_principal() -> None:
    nombres = {"I10X": "Hipertensión esencial (primaria)", "E119": "Diabetes mellitus"}
    diagnosticos = revisar_diagnosticos(
        [
            {"codigo": "i10x", "tipo": "confirmado_repetido", "principal": True},
            {"codigo": "E119", "tipo": "impresion_diagnostica"},
        ],
        nombres,
    )
    assert diagnosticos[0] == Diagnostico(
        "I10X", "Hipertensión esencial (primaria)", "confirmado_repetido", True
    )
    with pytest.raises(DatosInvalidos):
        revisar_diagnosticos(
            [
                {"codigo": "I10X", "tipo": "confirmado_nuevo", "principal": True},
                {"codigo": "E119", "tipo": "confirmado_nuevo", "principal": True},
            ],
            nombres,
        )
    with pytest.raises(DatosInvalidos):
        revisar_diagnosticos([{"codigo": "ZZZZ", "tipo": "confirmado_nuevo"}], nombres)


def test_la_formula_pide_dosis_via_frecuencia_y_dias() -> None:
    formula = revisar_medicamentos(
        [
            {
                "nombre": "Losartán 50 mg",
                "dosis": "1 tableta",
                "via": "oral",
                "frecuencia": "cada 12 horas",
                "dias": "90",
            }
        ]
    )
    assert formula[0].dias == 90
    with pytest.raises(DatosInvalidos) as error:
        revisar_medicamentos([{"nombre": "Losartán", "dosis": "1", "frecuencia": "diaria"}])
    assert error.value.campos == {"medicamentos.0": "Elija la vía de administración"}


def _consulta_completa() -> dict[str, object]:
    datos: dict[str, object] = {
        c: "escrito" for c, campo in CAMPOS_DE_LA_ATENCION.items() if campo.obligatorio
    }
    datos.update(
        tipo_consulta="control",
        finalidad="tratamiento",
        causa="enfermedad_general",
        destino="casa",
        alergias=NO_REFIERE,
    )
    return datos


def _identificacion_completa() -> dict[str, object]:
    return {
        "sexo": "M",
        "estado_civil": "casado",
        "ocupacion": "Docente",
        "direccion": "Calle 10 # 5-20",
        "municipio": "Tunja",
        "tipo_vinculacion": "particular",
    }


def test_no_refiere_cuenta_como_escrito_y_el_particular_no_necesita_aseguradora() -> None:
    principal = [Diagnostico("I10X", "Hipertensión", "confirmado_repetido", True)]
    assert not faltantes(_consulta_completa(), principal, _identificacion_completa())


def test_dice_que_falta_para_cerrar() -> None:
    consulta = _consulta_completa() | {"motivo": None, "destino": "remitido"}
    identificacion = _identificacion_completa() | {"tipo_vinculacion": "contributivo"}
    pendientes = faltantes(consulta, [], identificacion)
    assert pendientes.atencion == ["Motivo de consulta", "Diagnóstico principal", "Remitido a"]
    assert pendientes.identificacion == ["Aseguradora"]
    assert set(CAMPOS_DE_IDENTIFICACION) >= {"sexo", "aseguradora", "responsable_nombre"}
