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


async def test_el_paciente_ve_solo_sus_facturas_y_su_pdf(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    dia = date(2032, 2, 23)
    de_rosa = await _cita_atendida(
        nuevo_paciente, consultorio_listo["Consulta general"], reloj, ingresar_doctora, dia
    )
    doctora = await ingresar_doctora()
    emitida = await doctora.post(
        f"/api/v1/citas/{de_rosa}/factura", json={"valor": 80000, "medio_pago": "efectivo"}
    )
    assert emitida.status_code == 201, emitida.text

    # Otra paciente, con su propia sesión, no ve la de Rosa ni abre su PDF.
    lucia = await nuevo_paciente(nombres="Lucía", apellidos="Mora")
    suyas = (await lucia.get("/api/v1/yo/facturas")).json()
    ajeno = await lucia.get(f"/api/v1/citas/{de_rosa}/factura/pdf")

    assert all(f["cita_id"] != de_rosa for f in suyas)
    assert ajeno.status_code == 404
    assert (await doctora.get("/api/v1/yo/facturas")).status_code == 403


# --- Cerrar la atención deja la cita atendida y lista para cobrar (D-35)


async def _cerrar_atencion_desde_la_ficha(ingresar_doctora: IngresarDoctora, apellido: str) -> None:
    from test_api_de_historia import atencion_lista, cerrar, paciente_id

    doctora = await ingresar_doctora()
    paciente = await paciente_id(doctora, apellido)
    atencion = await atencion_lista(doctora, paciente)
    cerrada = await cerrar(doctora, atencion)
    assert cerrada.status_code == 200, cerrada.text


async def _agendar(
    nuevo_paciente: NuevoPaciente, tipo: str, reloj: RelojMovible, dia: date, apellido: str
) -> str:
    reloj.poner(a_las(dia - timedelta(days=3), 9))
    paciente = await nuevo_paciente("Javier", apellido)
    agendada = await paciente.post(
        "/api/v1/citas", json={"tipo_cita": tipo, "inicio": a_las(dia, 11).isoformat()}
    )
    assert agendada.status_code == 201, agendada.text
    cita_id: str = (await paciente.get("/api/v1/citas")).json()[0]["id"]
    return cita_id


async def _estado_y_cobro(ingresar_doctora: IngresarDoctora, cita: str) -> tuple[str, int]:
    doctora = await ingresar_doctora()
    estado = next(
        c["estado"] for c in (await doctora.get("/api/v1/citas")).json() if c["id"] == cita
    )
    cobro = await doctora.post(
        f"/api/v1/citas/{cita}/factura", json={"valor": 80000, "medio_pago": "efectivo"}
    )
    return estado, cobro.status_code


async def test_cerrar_la_atencion_antes_de_la_hora_deja_la_cita_lista_para_cobrar(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    dia = date(2032, 3, 1)
    cita = await _agendar(
        nuevo_paciente, consultorio_listo["Consulta general"], reloj, dia, "Ordóñez Uno"
    )
    # La cita es a las 11; el médico atiende y cierra a las 8, desde la ficha y sin la cita.
    reloj.poner(a_las(dia, 8))
    await _cerrar_atencion_desde_la_ficha(ingresar_doctora, "Ordóñez Uno")

    assert await _estado_y_cobro(ingresar_doctora, cita) == ("atendida", 201)


async def test_sin_cita_de_hoy_se_marca_la_mas_reciente_que_quedo_sin_marcar(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    dia = date(2032, 3, 8)
    cita = await _agendar(
        nuevo_paciente, consultorio_listo["Consulta general"], reloj, dia, "Ordóñez Dos"
    )
    # Nadie la marcó ese día; la atención se cierra cinco días después.
    reloj.poner(a_las(dia + timedelta(days=5), 10))
    await _cerrar_atencion_desde_la_ficha(ingresar_doctora, "Ordóñez Dos")

    assert await _estado_y_cobro(ingresar_doctora, cita) == ("atendida", 201)
