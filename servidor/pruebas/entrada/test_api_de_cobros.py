"""Cobro de una cita atendida con factura electrónica por la API (D-35).

Las pruebas usan el facturador de mentira: el de Factus se prueba aparte, contra su formato.
"""

from datetime import date, datetime, timedelta

import pytest

from conftest import IngresarDoctora, NuevoPaciente, RelojMovible
from vitalia.dominio.cuentas import COLOMBIA

pytestmark = pytest.mark.bd


def a_las(dia: date, hora: int) -> datetime:
    return datetime(dia.year, dia.month, dia.day, hora, tzinfo=COLOMBIA)


async def _cita_atendida(
    nuevo_paciente: NuevoPaciente,
    tipo: str,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
    dia: date,
    atender: bool = True,
) -> str:
    reloj.poner(a_las(dia - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    agendada = await rosa.post(
        "/api/v1/citas", json={"tipo_cita": tipo, "inicio": a_las(dia, 9).isoformat()}
    )
    assert agendada.status_code == 201, agendada.text
    cita_id: str = (await rosa.get("/api/v1/citas")).json()[0]["id"]
    reloj.poner(a_las(dia, 10))
    if atender:
        doctora = await ingresar_doctora()
        marcada = await doctora.post(
            f"/api/v1/citas/{cita_id}/asistencia", json={"estado": "atendida"}
        )
        assert marcada.status_code == 204, marcada.text
    return cita_id


async def test_la_cita_atendida_se_factura_una_sola_vez(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    cita = await _cita_atendida(
        nuevo_paciente,
        consultorio_listo["Consulta general"],
        reloj,
        ingresar_doctora,
        date(2032, 2, 2),
    )
    doctora = await ingresar_doctora()

    antes = (await doctora.get("/api/v1/cobros")).json()
    primera = await doctora.post(
        f"/api/v1/citas/{cita}/factura", json={"valor": 80000, "medio_pago": "efectivo"}
    )
    segunda = await doctora.post(
        f"/api/v1/citas/{cita}/factura", json={"valor": 95000, "medio_pago": "transferencia"}
    )
    despues = (await doctora.get("/api/v1/cobros")).json()
    pdf = await doctora.get(f"/api/v1/citas/{cita}/factura/pdf")

    assert antes["ambiente"] == "de_mentira"
    assert next(c for c in antes["cobros"] if c["cita"]["id"] == cita)["factura"] is None
    assert primera.status_code == 201, primera.text
    factura = primera.json()
    assert factura["valor"] == 80000 and factura["medio_pago"] == "efectivo"
    assert factura["concepto"] == "Consulta médica: Consulta general"
    assert factura["numero"] and factura["cufe"]
    # Repetir no crea otra ni cambia la emitida.
    assert segunda.status_code == 201 and segunda.json()["numero"] == factura["numero"]
    assert segunda.json()["valor"] == 80000
    cobro = next(c for c in despues["cobros"] if c["cita"]["id"] == cita)
    assert cobro["factura"]["numero"] == factura["numero"]
    assert pdf.status_code == 200 and pdf.content.startswith(b"%PDF")


async def test_solo_se_factura_lo_atendido_con_un_valor_razonable(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    cita = await _cita_atendida(
        nuevo_paciente,
        consultorio_listo["Consulta general"],
        reloj,
        ingresar_doctora,
        date(2032, 2, 9),
        atender=False,
    )
    doctora = await ingresar_doctora()

    sin_atender = await doctora.post(
        f"/api/v1/citas/{cita}/factura", json={"valor": 80000, "medio_pago": "efectivo"}
    )
    await doctora.post(f"/api/v1/citas/{cita}/asistencia", json={"estado": "atendida"})
    muy_poco = await doctora.post(
        f"/api/v1/citas/{cita}/factura", json={"valor": 50, "medio_pago": "bitcoin"}
    )

    assert sin_atender.status_code == 409
    assert sin_atender.json()["codigo"] == "cita_no_facturable"
    assert muy_poco.status_code == 400
    assert set(muy_poco.json()["detalle"]) == {"valor", "medio_pago"}


async def test_el_paciente_no_cobra_ni_ve_los_cobros(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    cita = await _cita_atendida(
        nuevo_paciente,
        consultorio_listo["Consulta general"],
        reloj,
        ingresar_doctora,
        date(2032, 2, 16),
    )

    # La sesión de antes venció con el salto del reloj: ingresa otra paciente.
    rosa = await nuevo_paciente(nombres="Lucía", apellidos="Mora")
    lista = await rosa.get("/api/v1/cobros")
    cobro = await rosa.post(
        f"/api/v1/citas/{cita}/factura", json={"valor": 80000, "medio_pago": "efectivo"}
    )

    assert lista.status_code == 403
    assert cobro.status_code == 403
