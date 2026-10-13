"""Los adaptadores de desarrollo cumplen su puerto: correo, IA y reloj."""

from datetime import timedelta

import pytest

from vitalia.adaptadores.correo.consola import CorreoEnConsola
from vitalia.adaptadores.ia.de_mentira import IADeMentira
from vitalia.adaptadores.reloj import RelojDelSistema
from vitalia.casos_de_uso.puertos import Correo, ProveedorIA, Reloj, Turno


async def test_correo_en_consola_muestra_el_mensaje(capsys: pytest.CaptureFixture[str]) -> None:
    correo: Correo = CorreoEnConsola()

    await correo.enviar("rosa@ejemplo.test", "Su cita", "Mañana a las 10:00")

    salida = capsys.readouterr().out
    assert "rosa@ejemplo.test" in salida
    assert "Su cita" in salida
    assert "Mañana a las 10:00" in salida


async def test_ia_de_mentira_lee_y_responde_por_partes() -> None:
    ia: ProveedorIA = IADeMentira(
        texto_de_pagina="Glucosa 92", partes_de_respuesta=("Glucosa: ", "92 [D1, pág. 1]")
    )

    assert await ia.leer_pagina(b"imagen") == "Glucosa 92"
    partes = [parte async for parte in ia.responder("Instrucciones", [Turno("medico", "¿Y?")])]
    assert partes == ["Glucosa: ", "92 [D1, pág. 1]"]


def test_el_reloj_del_sistema_da_la_hora_universal() -> None:
    reloj: Reloj = RelojDelSistema()

    assert reloj.ahora().utcoffset() == timedelta(0)
