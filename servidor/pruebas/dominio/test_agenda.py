"""Reglas de la agenda: horario, espacios libres y anticipación (HU-008, HU-011, HU-014)."""

from datetime import date, datetime, time, timedelta

import pytest

from vitalia.dominio.agenda import (
    Franja,
    Intervalo,
    alternativas,
    dias_con_espacio,
    en_horario,
    espacios_del_dia,
    puede_cambiarla_el_paciente,
    revisar_horario,
)
from vitalia.dominio.cuentas import COLOMBIA, DatosInvalidos

LUNES = date(2031, 3, 3)
MANANA_Y_TARDE = [
    Franja(dia, inicio, fin)
    for dia in range(1, 6)
    for inicio, fin in ((time(8), time(12)), (time(14), time(17)))
]
MEDIA_HORA = timedelta(minutes=30)


def a_las(dia: date, hora: int, minuto: int = 0) -> datetime:
    return datetime(dia.year, dia.month, dia.day, hora, minuto, tzinfo=COLOMBIA)


def horas(espacios: list[datetime]) -> list[str]:
    return [e.astimezone(COLOMBIA).strftime("%H:%M") for e in espacios]


def test_una_franja_que_termina_antes_de_empezar_se_rechaza() -> None:
    with pytest.raises(DatosInvalidos) as error:
        revisar_horario([Franja(1, time(12), time(8))])

    assert error.value.campos == {"franjas.0": "La franja del lunes termina antes de empezar"}


def test_dos_franjas_del_mismo_dia_no_se_cruzan() -> None:
    with pytest.raises(DatosInvalidos) as error:
        revisar_horario([Franja(2, time(8), time(12)), Franja(2, time(11), time(13))])

    assert set(error.value.campos) == {"franjas.0", "franjas.1"}


def test_franjas_seguidas_o_de_otro_dia_si_sirven() -> None:
    revisar_horario(
        [Franja(2, time(8), time(12)), Franja(2, time(12), time(13)), Franja(3, time(8), time(12))]
    )


def test_los_espacios_van_uno_tras_otro_en_cada_franja() -> None:
    libres = espacios_del_dia(LUNES, MANANA_Y_TARDE, [], MEDIA_HORA, a_las(LUNES, 0))

    assert horas(libres)[:3] == ["08:00", "08:30", "09:00"]
    assert horas(libres)[-2:] == ["16:00", "16:30"]
    assert len(libres) == 14


def test_lo_ocupado_no_se_ofrece() -> None:
    ocupado = [Intervalo(a_las(LUNES, 8, 30), a_las(LUNES, 9, 10))]

    libres = horas(espacios_del_dia(LUNES, MANANA_Y_TARDE, ocupado, MEDIA_HORA, a_las(LUNES, 0)))

    assert "08:30" not in libres
    assert "09:00" not in libres
    assert "09:30" in libres


def test_lo_que_ya_paso_o_empieza_antes_del_margen_no_se_ofrece() -> None:
    desde = a_las(LUNES, 8, 10) + timedelta(hours=1)

    libres = horas(espacios_del_dia(LUNES, MANANA_Y_TARDE, [], MEDIA_HORA, desde))

    assert libres[0] == "09:30"


def test_un_tipo_mas_largo_que_lo_que_queda_de_la_franja_no_cabe() -> None:
    libres = espacios_del_dia(
        LUNES, [Franja(1, time(8), time(12))], [], timedelta(minutes=45), a_las(LUNES, 0)
    )

    assert horas(libres) == ["08:00", "08:45", "09:30", "10:15", "11:00"]


def test_un_dia_sin_franjas_no_ofrece_nada() -> None:
    sabado = LUNES + timedelta(days=5)

    assert espacios_del_dia(sabado, MANANA_Y_TARDE, [], MEDIA_HORA, a_las(LUNES, 0)) == []


def test_solo_se_listan_los_dias_con_espacio() -> None:
    lleno = [Intervalo(a_las(LUNES, 0), a_las(LUNES, 23))]

    dias = dias_con_espacio(a_las(LUNES, 6), MANANA_Y_TARDE, lleno, MEDIA_HORA)

    assert dias[0] == LUNES + timedelta(days=1)
    assert all(dia.isoweekday() <= 5 for dia in dias)
    assert len(dias) == 6


def test_las_alternativas_son_las_mas_cercanas() -> None:
    ocupado = [Intervalo(a_las(LUNES, 10), a_las(LUNES, 10, 30))]

    cercanas = alternativas(a_las(LUNES, 10), MANANA_Y_TARDE, ocupado, MEDIA_HORA, a_las(LUNES, 6))

    assert horas(cercanas) == ["09:30", "10:30", "09:00"]


def test_en_horario_exige_que_la_cita_quepa_completa() -> None:
    assert en_horario(Intervalo(a_las(LUNES, 11, 30), a_las(LUNES, 12)), MANANA_Y_TARDE)
    assert not en_horario(Intervalo(a_las(LUNES, 11, 45), a_las(LUNES, 12, 15)), MANANA_Y_TARDE)


def test_el_paciente_cambia_su_cita_solo_con_mas_de_24_horas() -> None:
    cita = a_las(LUNES, 10)

    assert puede_cambiarla_el_paciente(cita, cita - timedelta(hours=25), 24)
    assert not puede_cambiarla_el_paciente(cita, cita - timedelta(hours=23), 24)
