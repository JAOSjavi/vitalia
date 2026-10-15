"""Cinco fallos seguidos bloquean 15 minutos (HU-004, CA-3)."""

from datetime import UTC, datetime, timedelta

from vitalia.dominio.ingreso import Intentos

AHORA = datetime(2026, 10, 14, 15, 0, tzinfo=UTC)


def _fallar(veces: int, tope: int = 5) -> Intentos:
    intentos = Intentos()
    for minuto in range(veces):
        intentos = intentos.con_un_fallo(AHORA + timedelta(minutes=minuto), tope)
    return intentos


def test_cuatro_fallos_no_bloquean() -> None:
    assert not _fallar(4).bloqueado(AHORA + timedelta(minutes=4))


def test_el_quinto_fallo_bloquea_quince_minutos() -> None:
    intentos = _fallar(5)

    assert intentos.bloqueado(AHORA + timedelta(minutes=5))
    assert intentos.bloqueado_hasta == AHORA + timedelta(minutes=19)


def test_pasado_el_bloqueo_se_cuenta_desde_cero() -> None:
    despues = _fallar(5).con_un_fallo(AHORA + timedelta(minutes=30), 5)

    assert despues.fallos == 1
    assert not despues.bloqueado(AHORA + timedelta(minutes=30))


def test_quince_minutos_sin_fallar_borran_la_cuenta() -> None:
    despues = _fallar(4).con_un_fallo(AHORA + timedelta(minutes=20), 5)

    assert despues.fallos == 1
