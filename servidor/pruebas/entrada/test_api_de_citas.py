"""Horario, tipos de cita, disponibilidad y citas por la API (HU-008 a HU-023, bloque 2).

Cada prueba usa su propia semana del futuro, para que las citas de una no le quiten espacio a
otra. El reloj se pone en un momento conocido de esa semana.
"""

import asyncio
from datetime import date, datetime, timedelta
from typing import Any

import httpx
import pytest

from conftest import IngresarDoctora, NuevoPaciente, RelojMovible
from vitalia.dominio.cuentas import COLOMBIA

pytestmark = pytest.mark.bd


def a_las(dia: date, hora: int, minuto: int = 0) -> datetime:
    return datetime(dia.year, dia.month, dia.day, hora, minuto, tzinfo=COLOMBIA)


def hora_de(iso: str) -> str:
    return datetime.fromisoformat(iso).astimezone(COLOMBIA).strftime("%H:%M")


async def _agendar(
    cliente: httpx.AsyncClient, tipo: str, inicio: datetime, **mas: Any
) -> httpx.Response:
    return await cliente.post(
        "/api/v1/citas", json={"tipo_cita": tipo, "inicio": inicio.isoformat(), **mas}
    )


async def _disponibilidad(
    cliente: httpx.AsyncClient, tipo: str, dia: date | None = None
) -> dict[str, Any]:
    ruta = f"/api/v1/disponibilidad?tipo_cita={tipo}"
    if dia:
        ruta += f"&fecha={dia.isoformat()}"
    respuesta = await cliente.get(ruta)
    assert respuesta.status_code == 200, respuesta.text
    resultado: dict[str, Any] = respuesta.json()
    return resultado


async def _mis_citas(cliente: httpx.AsyncClient) -> list[dict[str, Any]]:
    citas: list[dict[str, Any]] = (await cliente.get("/api/v1/citas")).json()
    return citas


# --- HU-011 y HU-012: espacios libres y agendar


async def test_solo_se_ofrecen_los_dias_y_las_horas_libres(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 3, 3)
    # Unos minutos antes de las 7: el reloj sigue andando durante la prueba.
    reloj.poner(a_las(lunes, 6, 55))
    rosa = await nuevo_paciente()

    disponible = await _disponibilidad(rosa, consultorio_listo["Consulta general"])

    dias = [date.fromisoformat(d) for d in disponible["dias"]]
    assert dias[0] == lunes
    assert all(dia.isoweekday() <= 5 for dia in dias)
    horas = [hora_de(h) for h in disponible["horas"]]
    assert horas[:3] == ["08:00", "08:30", "09:00"]
    assert "12:00" not in horas and horas[-1] == "16:30"


async def test_agendar_deja_la_cita_confirmada_y_ese_espacio_deja_de_ofrecerse(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 3, 10)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    consulta = consultorio_listo["Consulta general"]

    creada = await _agendar(rosa, consulta, a_las(lunes, 9))
    citas = await _mis_citas(rosa)
    disponible = await _disponibilidad(rosa, consulta, lunes)

    assert creada.status_code == 201, creada.text
    assert [(c["tipo"], c["estado"], hora_de(c["inicio"])) for c in citas] == [
        ("Consulta general", "confirmada", "09:00")
    ]
    assert "09:00" not in [hora_de(h) for h in disponible["horas"]]


async def test_si_otro_tomo_el_espacio_se_ofrecen_los_mas_cercanos(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 3, 17)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa, carlos = await nuevo_paciente(), await nuevo_paciente("Carlos", "Muñoz")
    consulta = consultorio_listo["Consulta general"]

    await _agendar(rosa, consulta, a_las(lunes, 10))
    respuesta = await _agendar(carlos, consulta, a_las(lunes, 10))

    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "espacio_ocupado"
    alternativas = [hora_de(h) for h in respuesta.json()["detalle"]["alternativas"]]
    assert alternativas == ["09:30", "10:30", "09:00"]


async def test_dos_confirmaciones_al_mismo_tiempo_dejan_una_sola_cita(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 3, 24)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    pacientes = [await nuevo_paciente(f"Paciente {n}", "Simultáneo") for n in range(4)]
    consulta = consultorio_listo["Consulta general"]

    respuestas = await asyncio.gather(*(_agendar(p, consulta, a_las(lunes, 11)) for p in pacientes))

    assert sorted(r.status_code for r in respuestas) == [201, 409, 409, 409]


async def test_no_se_ofrece_lo_que_empieza_en_menos_de_una_hora(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    martes = date(2031, 4, 1)
    reloj.poner(a_las(martes, 8, 10))
    rosa = await nuevo_paciente()
    consulta = consultorio_listo["Consulta general"]

    disponible = await _disponibilidad(rosa, consulta, martes)
    muy_pronto = await _agendar(rosa, consulta, a_las(martes, 8, 30))

    assert hora_de(disponible["horas"][0]) == "09:30"
    assert muy_pronto.status_code == 422
    assert muy_pronto.json()["codigo"] == "espacio_no_disponible"


async def test_el_paciente_no_puede_agendar_por_fuera_del_horario(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    sabado = date(2031, 4, 12)
    reloj.poner(a_las(sabado - timedelta(days=4), 9))
    rosa = await nuevo_paciente()

    respuesta = await _agendar(rosa, consultorio_listo["Consulta general"], a_las(sabado, 9))

    assert respuesta.status_code == 422


async def test_una_segunda_cita_del_mismo_tipo_pide_confirmar(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 4, 14)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    control = consultorio_listo["Control"]

    await _agendar(rosa, control, a_las(lunes, 8))
    sin_confirmar = await _agendar(rosa, control, a_las(lunes, 14))
    confirmada = await _agendar(rosa, control, a_las(lunes, 14), confirmar_repetida=True)

    assert sin_confirmar.status_code == 409
    assert sin_confirmar.json()["codigo"] == "cita_repetida"
    assert confirmada.status_code == 201


# --- HU-013 y HU-020: mis citas e inicio


async def test_cada_paciente_ve_solo_sus_citas_proximas_primero(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 4, 21)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa, carlos = await nuevo_paciente(), await nuevo_paciente("Carlos", "Muñoz")
    consulta, control = consultorio_listo["Consulta general"], consultorio_listo["Control"]

    await _agendar(rosa, control, a_las(lunes + timedelta(days=2), 15))
    await _agendar(rosa, consulta, a_las(lunes, 8))
    await _agendar(carlos, consulta, a_las(lunes, 9))
    inicio = (await rosa.get("/api/v1/yo/inicio")).json()

    citas = await _mis_citas(rosa)
    assert [(c["tipo"], hora_de(c["inicio"])) for c in citas] == [
        ("Consulta general", "08:00"),
        ("Control", "15:00"),
    ]
    assert inicio["proxima"]["tipo"] == "Consulta general"
    assert inicio["puede_cambiarla"] is True


async def test_sin_citas_el_inicio_invita_a_agendar(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente
) -> None:
    rosa = await nuevo_paciente()

    inicio = (await rosa.get("/api/v1/yo/inicio")).json()

    assert inicio["proxima"] is None


# --- HU-014 y HU-015: mover y cancelar como paciente


async def test_mover_con_tiempo_libera_el_espacio_anterior(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
) -> None:
    lunes = date(2031, 5, 5)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    consulta = consultorio_listo["Consulta general"]
    await _agendar(rosa, consulta, a_las(lunes, 8))
    cita = (await _mis_citas(rosa))[0]

    movida = await rosa.post(
        f"/api/v1/citas/{cita['id']}/mover", json={"inicio": a_las(lunes, 10).isoformat()}
    )
    disponible = await _disponibilidad(rosa, consulta, lunes)

    assert movida.status_code == 204, movida.text
    assert hora_de((await _mis_citas(rosa))[0]["inicio"]) == "10:00"
    assert "08:00" in [hora_de(h) for h in disponible["horas"]]


async def test_con_menos_de_24_horas_no_se_mueve_ni_se_cancela(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    martes = date(2031, 5, 13)
    reloj.poner(a_las(martes - timedelta(days=1), 9))
    rosa = await nuevo_paciente()
    await _agendar(rosa, consultorio_listo["Consulta general"], a_las(martes, 8))
    cita = (await _mis_citas(rosa))[0]

    mover = await rosa.post(
        f"/api/v1/citas/{cita['id']}/mover", json={"inicio": a_las(martes, 10).isoformat()}
    )
    cancelar = await rosa.post(f"/api/v1/citas/{cita['id']}/cancelar", json={})

    assert mover.status_code == cancelar.status_code == 422
    assert mover.json()["codigo"] == "falta_anticipacion"
    assert (await _mis_citas(rosa))[0]["estado"] == "confirmada"


async def test_si_el_nuevo_espacio_se_ocupa_la_cita_original_se_conserva(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 5, 19)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa, carlos = await nuevo_paciente(), await nuevo_paciente("Carlos", "Muñoz")
    consulta = consultorio_listo["Consulta general"]
    await _agendar(rosa, consulta, a_las(lunes, 8))
    await _agendar(carlos, consulta, a_las(lunes, 10))
    cita = (await _mis_citas(rosa))[0]

    respuesta = await rosa.post(
        f"/api/v1/citas/{cita['id']}/mover", json={"inicio": a_las(lunes, 10).isoformat()}
    )

    assert respuesta.status_code == 409
    assert hora_de((await _mis_citas(rosa))[0]["inicio"]) == "08:00"


async def test_cancelar_deja_la_cita_en_el_historial_y_libera_el_espacio(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 5, 26)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    consulta = consultorio_listo["Consulta general"]
    await _agendar(rosa, consulta, a_las(lunes, 9))
    cita = (await _mis_citas(rosa))[0]

    cancelada = await rosa.post(f"/api/v1/citas/{cita['id']}/cancelar", json={})
    disponible = await _disponibilidad(rosa, consulta, lunes)

    assert cancelada.status_code == 204
    assert (await _mis_citas(rosa))[0]["estado"] == "cancelada"
    assert "09:00" in [hora_de(h) for h in disponible["horas"]]


async def test_un_paciente_no_toca_la_cita_de_otro(
    consultorio_listo: dict[str, str], nuevo_paciente: NuevoPaciente, reloj: RelojMovible
) -> None:
    lunes = date(2031, 6, 2)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa, carlos = await nuevo_paciente(), await nuevo_paciente("Carlos", "Muñoz")
    await _agendar(rosa, consultorio_listo["Consulta general"], a_las(lunes, 9))
    cita = (await _mis_citas(rosa))[0]

    respuesta = await carlos.post(f"/api/v1/citas/{cita['id']}/cancelar", json={})

    assert respuesta.status_code == 404
    assert (await _mis_citas(rosa))[0]["estado"] == "confirmada"


# --- HU-016 y HU-017: el médico agenda, mueve y cancela


async def _id_de(doctora: httpx.AsyncClient, nombre: str) -> str:
    pagina = (await doctora.get("/api/v1/pacientes", params={"buscar": nombre})).json()
    assert pagina["total"] >= 1, pagina
    paciente_id: str = pagina["pacientes"][0]["id"]
    return paciente_id


async def test_el_medico_agenda_para_un_paciente_y_este_la_ve(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 6, 9)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    lucia = await nuevo_paciente("Lucía Fernanda", "Quintero Agendada")
    doctora = await ingresar_doctora()
    paciente = await _id_de(doctora, "lucia fernanda quintero agendada")

    creada = await _agendar(
        doctora, consultorio_listo["Control"], a_las(lunes, 15), paciente=paciente
    )

    assert creada.status_code == 201, creada.text
    assert [c["tipo"] for c in await _mis_citas(lucia)] == ["Control"]


async def test_por_fuera_del_horario_el_medico_confirma_y_nunca_cruza_citas(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 6, 16)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    await nuevo_paciente("Mario", "Fuera De Horario")
    doctora = await ingresar_doctora()
    paciente = await _id_de(doctora, "mario fuera de horario")
    consulta = consultorio_listo["Consulta general"]

    sin_confirmar = await _agendar(doctora, consulta, a_las(lunes, 18), paciente=paciente)
    confirmada = await _agendar(
        doctora, consulta, a_las(lunes, 18), paciente=paciente, confirmar_fuera_de_horario=True
    )
    cruzada = await _agendar(
        doctora,
        consulta,
        a_las(lunes, 18, 15),
        paciente=paciente,
        confirmar_fuera_de_horario=True,
    )

    assert sin_confirmar.status_code == 409
    assert sin_confirmar.json()["codigo"] == "fuera_de_horario"
    assert confirmada.status_code == 201
    assert cruzada.status_code == 409
    assert cruzada.json()["codigo"] == "espacio_ocupado"


async def test_el_medico_mueve_sin_las_24_horas_y_cancela_con_motivo(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    martes = date(2031, 6, 24)
    reloj.poner(a_las(martes, 7))
    rosa = await nuevo_paciente()
    await _agendar(rosa, consultorio_listo["Consulta general"], a_las(martes, 9))
    cita = (await _mis_citas(rosa))[0]

    doctora = await ingresar_doctora()
    movida = await doctora.post(
        f"/api/v1/citas/{cita['id']}/mover", json={"inicio": a_las(martes, 10).isoformat()}
    )
    sin_motivo = await doctora.post(f"/api/v1/citas/{cita['id']}/cancelar", json={})
    cancelada = await doctora.post(
        f"/api/v1/citas/{cita['id']}/cancelar",
        json={"motivo": "La doctora estuvo en una urgencia."},
    )

    assert movida.status_code == 204
    assert sin_motivo.status_code == 400
    assert cancelada.status_code == 204
    vista_por_rosa = (await _mis_citas(rosa))[0]
    assert vista_por_rosa["estado"] == "cancelada"
    assert vista_por_rosa["motivo"] == "La doctora estuvo en una urgencia."


async def test_una_cita_atendida_no_se_mueve_ni_se_cancela(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 6, 30)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    await _agendar(rosa, consultorio_listo["Consulta general"], a_las(lunes, 9))
    cita = (await _mis_citas(rosa))[0]
    reloj.poner(a_las(lunes, 9, 40))
    doctora = await ingresar_doctora()
    await doctora.post(f"/api/v1/citas/{cita['id']}/asistencia", json={"estado": "atendida"})

    respuesta = await doctora.post(
        f"/api/v1/citas/{cita['id']}/cancelar", json={"motivo": "Prueba"}
    )

    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "cita_no_modificable"


# --- HU-018: asistencia


async def _cita_de(
    rosa: httpx.AsyncClient, tipo: str, reloj: RelojMovible, inicio: datetime
) -> str:
    """Rosa agenda tres días antes; devuelve el número de la cita."""
    await _agendar(rosa, tipo, inicio)
    cita_id: str = (await _mis_citas(rosa))[0]["id"]
    return cita_id


async def _marcar(ingresar_doctora: IngresarDoctora, cita_id: str, estado: str) -> httpx.Response:
    # Cada salto del reloj vence la sesión anterior: la doctora vuelve a ingresar.
    doctora = await ingresar_doctora()
    return await doctora.post(f"/api/v1/citas/{cita_id}/asistencia", json={"estado": estado})


async def _estado(ingresar_doctora: IngresarDoctora, cita_id: str) -> str:
    doctora = await ingresar_doctora()
    citas = (await doctora.get("/api/v1/citas")).json()
    estado: str = next(c["estado"] for c in citas if c["id"] == cita_id)
    return estado


async def test_la_asistencia_se_marca_el_dia_de_la_cita(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 8, 4)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    cita = await _cita_de(rosa, consultorio_listo["Consulta general"], reloj, a_las(lunes, 9))

    antes_de_tiempo = await _marcar(ingresar_doctora, cita, "atendida")
    reloj.poner(a_las(lunes, 8, 30))
    no_asistio_antes = await _marcar(ingresar_doctora, cita, "no_asistio")
    atendida = await _marcar(ingresar_doctora, cita, "atendida")

    assert antes_de_tiempo.status_code == 400
    assert no_asistio_antes.status_code == 400
    assert atendida.status_code == 204
    assert await _estado(ingresar_doctora, cita) == "atendida"


async def test_la_asistencia_se_corrige_solo_el_mismo_dia(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 8, 11)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    cita = await _cita_de(rosa, consultorio_listo["Consulta general"], reloj, a_las(lunes, 9))

    reloj.poner(a_las(lunes, 10))
    await _marcar(ingresar_doctora, cita, "no_asistio")
    corregida = await _marcar(ingresar_doctora, cita, "atendida")
    reloj.poner(a_las(lunes + timedelta(days=1), 8))
    al_otro_dia = await _marcar(ingresar_doctora, cita, "no_asistio")

    assert corregida.status_code == 204
    assert al_otro_dia.status_code == 400
    assert await _estado(ingresar_doctora, cita) == "atendida"


async def test_un_paciente_no_marca_asistencia(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
) -> None:
    lunes = date(2031, 8, 18)
    reloj.poner(a_las(lunes, 8))
    rosa = await nuevo_paciente()
    cita = await _cita_de(rosa, consultorio_listo["Consulta general"], reloj, a_las(lunes, 9, 30))

    respuesta = await rosa.post(f"/api/v1/citas/{cita}/asistencia", json={"estado": "atendida"})

    assert respuesta.status_code == 403


# --- HU-021 y HU-001 CA-4: agenda de hoy y lo que falta por configurar


async def test_la_agenda_de_hoy_va_por_hora_con_paciente_tipo_y_estado(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    jueves = date(2031, 7, 10)
    reloj.poner(a_las(jueves - timedelta(days=3), 9))
    rosa, carlos = await nuevo_paciente(), await nuevo_paciente("Carlos", "Muñoz Hoy")
    await _agendar(carlos, consultorio_listo["Control"], a_las(jueves, 15))
    await _agendar(rosa, consultorio_listo["Consulta general"], a_las(jueves, 8, 30))

    reloj.poner(a_las(jueves, 7, 40))
    doctora = await ingresar_doctora()
    agenda = (await doctora.get("/api/v1/agenda/hoy")).json()

    assert [(c["paciente"], c["tipo"], c["estado"]) for c in agenda["citas"]] == [
        ("Rosa Elena Duarte", "Consulta general", "confirmada"),
        ("Carlos Muñoz Hoy", "Control", "confirmada"),
    ]
    assert agenda["pendientes"] == []
    # La que sigue es la de Rosa: la tarjeta trae su edad y sus documentos, sin abrir la ficha.
    assert agenda["sigue"]["cita_id"] == agenda["citas"][0]["id"]
    assert agenda["sigue"]["documentos"] == 0
    assert agenda["sigue"]["ia_autorizada"] is False


async def test_un_dia_sin_citas_muestra_la_proxima(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    domingo = date(2031, 7, 20)
    reloj.poner(a_las(domingo - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    await _agendar(rosa, consultorio_listo["Control"], a_las(domingo + timedelta(days=1), 8))

    reloj.poner(a_las(domingo, 9))
    doctora = await ingresar_doctora()
    agenda = (await doctora.get("/api/v1/agenda/hoy")).json()

    assert agenda["citas"] == []
    assert hora_de(agenda["proxima"]["inicio"]) == "08:00"


async def test_sin_tipos_activos_la_agenda_no_esta_disponible(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    ingresar_doctora: IngresarDoctora,
) -> None:
    rosa = await nuevo_paciente()
    doctora = await ingresar_doctora()
    for tipo in consultorio_listo.values():
        await doctora.patch(f"/api/v1/tipos-cita/{tipo}", json={"activo": False})
    try:
        agenda = (await doctora.get("/api/v1/agenda/hoy")).json()
        tipos_del_paciente = (await rosa.get("/api/v1/tipos-cita")).json()
        consulta = await rosa.get(
            f"/api/v1/disponibilidad?tipo_cita={consultorio_listo['Consulta general']}"
        )
    finally:
        for tipo in consultorio_listo.values():
            await doctora.patch(f"/api/v1/tipos-cita/{tipo}", json={"activo": True})

    assert "tipos_cita" in agenda["pendientes"]
    assert tipos_del_paciente == []
    assert consulta.status_code == 400


# --- HU-008 y HU-010: horario y tipos de cita


async def test_un_horario_con_franjas_cruzadas_se_rechaza(
    ingresar_doctora: IngresarDoctora,
) -> None:
    doctora = await ingresar_doctora()
    respuesta = await doctora.put(
        "/api/v1/horario",
        json={
            "franjas": [
                {"dia_semana": 2, "hora_inicio": "08:00", "hora_fin": "12:00"},
                {"dia_semana": 2, "hora_inicio": "11:00", "hora_fin": "13:00"},
            ]
        },
    )

    assert respuesta.status_code == 400
    assert "martes" in respuesta.json()["detalle"]["franjas.1"]


async def test_cambiar_el_horario_lista_las_citas_que_quedan_por_fuera(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    viernes = date(2031, 8, 1)
    reloj.poner(a_las(viernes - timedelta(days=3), 9))
    rosa = await nuevo_paciente("Rosa", "Afectada Por Horario")
    await _agendar(rosa, consultorio_listo["Consulta general"], a_las(viernes, 15))
    doctora = await ingresar_doctora()
    actual = (await doctora.get("/api/v1/horario")).json()

    sin_tardes = [f for f in actual["franjas"] if f["hora_inicio"] < "12:00"]
    try:
        guardado = (await doctora.put("/api/v1/horario", json={"franjas": sin_tardes})).json()
    finally:
        await doctora.put("/api/v1/horario", json=actual)

    afectadas = [c["paciente"] for c in guardado["citas_afectadas"]]
    assert "Rosa Afectada Por Horario" in afectadas
    assert (await _mis_citas(rosa))[0]["estado"] == "confirmada"


async def test_cambiar_la_duracion_de_un_tipo_no_cambia_las_citas_ya_agendadas(
    nuevo_paciente: NuevoPaciente, reloj: RelojMovible, ingresar_doctora: IngresarDoctora
) -> None:
    lunes = date(2031, 8, 11)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    doctora = await ingresar_doctora()
    tipo = (
        await doctora.post(
            "/api/v1/tipos-cita", json={"nombre": "Revisión de exámenes", "duracion_minutos": 20}
        )
    ).json()["id"]
    rosa = await nuevo_paciente()
    await _agendar(rosa, tipo, a_las(lunes, 8))

    await doctora.patch(f"/api/v1/tipos-cita/{tipo}", json={"duracion_minutos": 40})
    await doctora.patch(f"/api/v1/tipos-cita/{tipo}", json={"activo": False})

    cita = (await _mis_citas(rosa))[0]
    assert cita["duracion_minutos"] == 20
    assert cita["estado"] == "confirmada"
    assert tipo not in [t["id"] for t in (await rosa.get("/api/v1/tipos-cita")).json()]


# --- HU-023: pacientes


async def test_buscar_pacientes_sin_tildes_o_por_documento(
    nuevo_paciente: NuevoPaciente, ingresar_doctora: IngresarDoctora
) -> None:
    await nuevo_paciente("Ángela María", "Peñaloza Búsqueda")
    doctora = await ingresar_doctora()

    por_nombre = (
        await doctora.get("/api/v1/pacientes", params={"buscar": "angela penaloza"})
    ).json()
    numero = por_nombre["pacientes"][0]["numero_documento"]
    con_puntos = f"{numero[:3]}.{numero[3:6]}.{numero[6:]}"
    por_documento = (await doctora.get("/api/v1/pacientes", params={"buscar": con_puntos})).json()

    assert [p["apellidos"] for p in por_nombre["pacientes"]] == ["Peñaloza Búsqueda"]
    assert [p["numero_documento"] for p in por_documento["pacientes"]] == [numero]


async def test_la_lista_de_pacientes_va_por_paginas_y_en_orden(
    nuevo_paciente: NuevoPaciente, ingresar_doctora: IngresarDoctora
) -> None:
    for apellido in ("Zuluaga Orden", "Álvarez Orden", "Mejía Orden"):
        await nuevo_paciente("Ana", apellido)
    doctora = await ingresar_doctora()

    primera = (
        await doctora.get("/api/v1/pacientes", params={"buscar": "orden", "tamano": 2})
    ).json()
    segunda = (
        await doctora.get("/api/v1/pacientes", params={"buscar": "orden", "tamano": 2, "pagina": 2})
    ).json()

    assert primera["total"] == 3
    assert [p["apellidos"] for p in primera["pacientes"] + segunda["pacientes"]] == [
        "Álvarez Orden",
        "Mejía Orden",
        "Zuluaga Orden",
    ]


async def test_un_paciente_no_puede_ver_la_lista_de_pacientes(
    nuevo_paciente: NuevoPaciente,
) -> None:
    rosa = await nuevo_paciente()

    respuesta = await rosa.get("/api/v1/pacientes")

    assert respuesta.status_code == 403


# --- HU-009: bloqueos del horario


async def _bloquear(
    doctora: httpx.AsyncClient, inicio: datetime, fin: datetime, motivo: str = "Congreso médico"
) -> httpx.Response:
    return await doctora.post(
        "/api/v1/bloqueos",
        json={"inicio": inicio.isoformat(), "fin": fin.isoformat(), "motivo": motivo},
    )


async def test_lo_bloqueado_deja_de_ofrecerse_y_vuelve_al_eliminarlo(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 9, 1)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    doctora = await ingresar_doctora()
    consulta = consultorio_listo["Consulta general"]

    creado = await _bloquear(doctora, a_las(lunes, 9), a_las(lunes, 10))
    horas = [hora_de(h) for h in (await _disponibilidad(rosa, consulta, lunes))["horas"]]
    encima = await _agendar(rosa, consulta, a_las(lunes, 9))

    assert creado.status_code == 201, creado.text
    assert "09:00" not in horas and "09:30" not in horas
    assert "08:30" in horas and "10:00" in horas
    assert encima.status_code == 422

    eliminado = await doctora.delete(f"/api/v1/bloqueos/{creado.json()['id']}")
    horas = [hora_de(h) for h in (await _disponibilidad(rosa, consulta, lunes))["horas"]]

    assert eliminado.status_code == 204
    assert "09:00" in horas


async def test_un_bloqueo_que_tapa_citas_las_lista_y_no_se_guarda(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 9, 8)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    await _agendar(rosa, consultorio_listo["Control"], a_las(lunes, 15))
    cita = (await _mis_citas(rosa))[0]
    doctora = await ingresar_doctora()

    con_citas = await _bloquear(doctora, a_las(lunes, 14), a_las(lunes, 17))
    await doctora.post(f"/api/v1/citas/{cita['id']}/cancelar", json={"motivo": "Congreso"})
    despues = await _bloquear(doctora, a_las(lunes, 14), a_las(lunes, 17))

    assert con_citas.status_code == 409
    assert con_citas.json()["codigo"] == "bloqueo_con_citas"
    assert [c["id"] for c in con_citas.json()["detalle"]["citas"]] == [cita["id"]]
    assert despues.status_code == 201


async def test_un_bloqueo_de_varios_dias_tapa_cada_dia(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 9, 15)
    reloj.poner(a_las(lunes - timedelta(days=3), 9))
    rosa = await nuevo_paciente()
    doctora = await ingresar_doctora()

    await _bloquear(doctora, a_las(lunes, 0), a_las(lunes + timedelta(days=2), 0), "Vacaciones")
    dias = (await _disponibilidad(rosa, consultorio_listo["Control"]))["dias"]

    assert lunes.isoformat() not in dias
    assert (lunes + timedelta(days=1)).isoformat() not in dias
    assert (lunes + timedelta(days=2)).isoformat() in dias


async def test_el_medico_no_da_citas_sobre_un_bloqueo_y_hoy_lo_muestra(
    consultorio_listo: dict[str, str],
    nuevo_paciente: NuevoPaciente,
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 9, 22)
    reloj.poner(a_las(lunes, 7))
    rosa = await nuevo_paciente()
    doctora = await ingresar_doctora()
    paciente = await _id_de(doctora, "rosa elena duarte")
    await _bloquear(doctora, a_las(lunes, 14), a_las(lunes, 17))

    encima = await _agendar(
        doctora, consultorio_listo["Control"], a_las(lunes, 15), paciente=paciente
    )
    agenda = (await doctora.get("/api/v1/agenda/hoy")).json()
    del_paciente = await rosa.get(
        "/api/v1/bloqueos",
        params={"desde": a_las(lunes, 0).isoformat(), "hasta": a_las(lunes, 23).isoformat()},
    )

    assert encima.status_code == 409
    assert encima.json()["codigo"] == "espacio_bloqueado"
    assert [b["motivo"] for b in agenda["bloqueos"]] == ["Congreso médico"]
    assert del_paciente.status_code == 403


async def test_un_bloqueo_pide_motivo_y_uno_pasado_no_se_elimina(
    consultorio_listo: dict[str, str],
    reloj: RelojMovible,
    ingresar_doctora: IngresarDoctora,
) -> None:
    lunes = date(2031, 9, 29)
    reloj.poner(a_las(lunes, 7))
    doctora = await ingresar_doctora()

    sin_motivo = await _bloquear(doctora, a_las(lunes, 9), a_las(lunes, 10), "  ")
    creado = await _bloquear(doctora, a_las(lunes, 9), a_las(lunes, 10))
    reloj.poner(a_las(lunes, 11))
    doctora = await ingresar_doctora()
    pasado = await doctora.delete(f"/api/v1/bloqueos/{creado.json()['id']}")

    assert sin_motivo.status_code == 400
    assert pasado.status_code == 400
