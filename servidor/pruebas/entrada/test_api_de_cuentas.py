"""Registro, ingreso, sesión y consultorio por la API, como los usaría una persona.

HU-001, HU-002, HU-003, HU-004, HU-006, HU-007 y la casilla de IA de HU-032.
"""

import secrets
from datetime import timedelta
from typing import Any
from uuid import UUID

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from conftest import CONTRASENA_DE_PRUEBA, DOCUMENTO_DEL_MEDICO, Cliente, RelojMovible
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.dominio.identidad import Identidad

pytestmark = pytest.mark.bd

CONTRASENA = "girasol2026"


async def _textos(cliente: Cliente) -> tuple[str, str]:
    async with cliente() as navegador:
        datos = (await navegador.get("/api/v1/autorizaciones/texto?tipo=datos")).json()
        ia = (await navegador.get("/api/v1/autorizaciones/texto?tipo=ia")).json()
    return datos["id"], ia["id"]


async def _registro(cliente: Cliente, **cambios: Any) -> dict[str, Any]:
    texto_datos, _ = await _textos(cliente)
    return {
        "tipo_documento": "CC",
        "numero_documento": str(secrets.randbelow(10**9) + 10**8),
        "nombres": "Rosa Elena",
        "apellidos": "Duarte",
        "fecha_nacimiento": "1958-03-02",
        "telefono": "318 555 0116",
        "correo": "rosa@ejemplo.test",
        "contrasena": CONTRASENA,
        "texto_datos": texto_datos,
        **cambios,
    }


def _ingreso(registro: dict[str, Any], contrasena: str = CONTRASENA) -> dict[str, str]:
    return {
        "tipo_documento": registro["tipo_documento"],
        "numero_documento": registro["numero_documento"],
        "contrasena": contrasena,
    }


async def _autorizaciones(
    unidad: UnidadPostgres, medico: UUID, usuario: str
) -> set[tuple[str, int, str]]:
    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        filas = await trabajo.conexion.execute(
            text(
                "SELECT t.tipo, t.version, a.decision FROM autorizaciones a "
                "JOIN textos_autorizacion t ON t.id = a.texto_id "
                "JOIN pacientes p ON p.id = a.paciente_id WHERE p.usuario_id = :u"
            ),
            {"u": usuario},
        )
        return {(f.tipo, f.version, f.decision) for f in filas}


# --- HU-003 y HU-032: textos de autorización


async def test_el_texto_de_datos_se_lee_sin_sesion_y_resalta_la_ia(
    cliente: Cliente, medico: UUID
) -> None:
    async with cliente() as navegador:
        respuesta = await navegador.get("/api/v1/autorizaciones/texto?tipo=datos")

    texto = respuesta.json()
    assert respuesta.status_code == 200
    assert texto["version"] == 1
    resaltados = [p["titulo"] for p in texto["puntos"] if p["resaltado"]]
    assert resaltados == ["Inteligencia artificial"]
    assert "{consultorio}" not in texto["contenido"]


# --- HU-002: registro de paciente


async def test_el_registro_crea_la_cuenta_y_entra_al_inicio(
    cliente: Cliente, unidad: UnidadPostgres, medico: UUID
) -> None:
    registro = await _registro(cliente)

    async with cliente() as navegador:
        creada = await navegador.post("/api/v1/cuentas/registro", json=registro)
        yo = await navegador.get("/api/v1/yo")

    assert creada.status_code == 201, creada.text
    assert creada.json()["rol"] == "paciente"
    assert yo.json()["nombres"] == "Rosa Elena"
    assert yo.json()["numero_documento"] == registro["numero_documento"]
    # Aceptó los datos y no marcó la IA: la IA queda sin responder (HU-003 CA-2, HU-032 CA-1).
    assert await _autorizaciones(unidad, medico, yo.json()["usuario_id"]) == {
        ("datos", 1, "aceptada")
    }


async def test_la_casilla_de_ia_marcada_queda_como_autorizacion_aparte(
    cliente: Cliente, unidad: UnidadPostgres, medico: UUID
) -> None:
    _, texto_ia = await _textos(cliente)
    registro = await _registro(cliente, texto_ia=texto_ia)

    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)
        usuario = (await navegador.get("/api/v1/yo")).json()["usuario_id"]

    assert await _autorizaciones(unidad, medico, usuario) == {
        ("datos", 1, "aceptada"),
        ("ia", 1, "aceptada"),
    }


async def test_una_contrasena_debil_explica_que_le_falta(cliente: Cliente) -> None:
    registro = await _registro(cliente, contrasena="corta")

    async with cliente() as navegador:
        respuesta = await navegador.post("/api/v1/cuentas/registro", json=registro)

    assert respuesta.status_code == 400
    assert "8 caracteres" in respuesta.json()["detalle"]["contrasena"]
    assert "número" in respuesta.json()["detalle"]["contrasena"]


async def test_un_documento_registrado_ofrece_ingresar_sin_mostrar_la_otra_cuenta(
    cliente: Cliente,
) -> None:
    registro = await _registro(cliente)
    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)
    otra = {**registro, "nombres": "Otra", "correo": "otra@ejemplo.test"}

    async with cliente() as navegador:
        respuesta = await navegador.post("/api/v1/cuentas/registro", json=otra)

    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "documento_registrado"
    assert "rosa" not in respuesta.text.lower()


async def test_un_menor_de_edad_no_crea_la_cuenta(cliente: Cliente) -> None:
    registro = await _registro(cliente, fecha_nacimiento="2012-06-01")

    async with cliente() as navegador:
        respuesta = await navegador.post("/api/v1/cuentas/registro", json=registro)
        ingreso = await navegador.post("/api/v1/sesion", json=_ingreso(registro))

    assert respuesta.status_code == 422
    assert respuesta.json()["codigo"] == "menor_de_edad"
    assert ingreso.status_code == 401


async def test_no_se_acepta_un_texto_que_ya_no_es_el_vigente(cliente: Cliente) -> None:
    registro = await _registro(cliente, texto_datos=str(UUID(int=7)))

    async with cliente() as navegador:
        respuesta = await navegador.post("/api/v1/cuentas/registro", json=registro)

    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "autorizacion_desactualizada"


# --- HU-004: ingreso


async def test_el_ingreso_lleva_al_rol_de_cada_quien(cliente: Cliente, medico: UUID) -> None:
    registro = await _registro(cliente)
    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)

    async with cliente() as paciente, cliente() as doctora:
        como_paciente = await paciente.post("/api/v1/sesion", json=_ingreso(registro))
        como_medico = await doctora.post(
            "/api/v1/sesion", json={**DOCUMENTO_DEL_MEDICO, "contrasena": CONTRASENA_DE_PRUEBA}
        )

    assert como_paciente.json()["rol"] == "paciente"
    assert como_medico.json()["rol"] == "medico"
    cookie = como_paciente.headers["set-cookie"].lower()
    assert "httponly" in cookie and "secure" in cookie and "samesite=lax" in cookie


async def test_el_documento_se_puede_escribir_con_puntos_o_espacios(cliente: Cliente) -> None:
    registro = await _registro(cliente, numero_documento="41.652.318")
    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)

    async with cliente() as navegador:
        respuesta = await navegador.post(
            "/api/v1/sesion", json=_ingreso({**registro, "numero_documento": "41 652 318"})
        )

    assert respuesta.status_code == 200


async def test_el_error_no_dice_si_fallo_el_documento_o_la_contrasena(cliente: Cliente) -> None:
    registro = await _registro(cliente)
    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)

    async with cliente("10.0.1.1") as navegador:
        mala_contrasena = await navegador.post(
            "/api/v1/sesion", json=_ingreso(registro, "otra2026x")
        )
        sin_cuenta = await navegador.post(
            "/api/v1/sesion", json=_ingreso({**registro, "numero_documento": "999999999"})
        )

    assert mala_contrasena.status_code == sin_cuenta.status_code == 401
    assert mala_contrasena.json() == sin_cuenta.json()


async def test_cinco_fallos_bloquean_esa_cuenta_desde_ese_equipo(cliente: Cliente) -> None:
    registro = await _registro(cliente)
    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)

    async with cliente("10.0.2.2") as intruso:
        fallos = [
            (await intruso.post("/api/v1/sesion", json=_ingreso(registro, "otra2026x"))).status_code
            for _ in range(5)
        ]
        con_la_correcta = await intruso.post("/api/v1/sesion", json=_ingreso(registro))
    async with cliente("10.0.2.3") as su_dueno:
        desde_su_equipo = await su_dueno.post("/api/v1/sesion", json=_ingreso(registro))

    assert fallos == [401, 401, 401, 401, 429]
    assert con_la_correcta.status_code == 429
    assert con_la_correcta.json()["codigo"] == "ingreso_bloqueado"
    # Un tercero no deja por fuera al dueño de la cuenta (arquitectura, sección 3.7).
    assert desde_su_equipo.status_code == 200


async def test_una_cuenta_que_no_existe_tambien_se_bloquea(cliente: Cliente) -> None:
    falsa = {"tipo_documento": "CC", "numero_documento": "123123123", "contrasena": "otra2026x"}

    async with cliente("10.0.3.3") as navegador:
        estados = [
            (await navegador.post("/api/v1/sesion", json=falsa)).status_code for _ in range(5)
        ]

    assert estados == [401, 401, 401, 401, 429]


# --- HU-007: cierre y vencimiento de la sesión


async def test_cerrar_sesion_la_anula_en_el_servidor(cliente: Cliente) -> None:
    registro = await _registro(cliente)

    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)
        ficha = navegador.cookies["vitalia_sesion"]
        cerrada = await navegador.delete("/api/v1/sesion")
    async with cliente() as copia:
        copia.cookies.set("vitalia_sesion", ficha, domain="vitalia.prueba", path="/api")
        despues = await copia.get("/api/v1/yo")

    assert cerrada.status_code == 204
    assert despues.status_code == 401


async def test_media_hora_sin_uso_pide_ingresar_de_nuevo(
    cliente: Cliente, reloj: RelojMovible
) -> None:
    registro = await _registro(cliente)

    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)
        reloj.adelanto = timedelta(minutes=29)
        a_tiempo = await navegador.get("/api/v1/yo")
        reloj.adelanto = timedelta(minutes=29 + 31)
        tarde = await navegador.get("/api/v1/yo")

    assert a_tiempo.status_code == 200
    assert tarde.status_code == 401
    assert tarde.json()["codigo"] == "sin_sesion"


async def test_nada_de_la_api_queda_guardado_en_el_navegador(cliente: Cliente) -> None:
    async with cliente() as navegador:
        respuesta = await navegador.get("/api/v1/autorizaciones/texto?tipo=ia")

    assert respuesta.headers["cache-control"] == "no-store"


async def test_una_peticion_que_no_sale_de_la_aplicacion_no_modifica_nada(
    cliente: Cliente,
) -> None:
    registro = await _registro(cliente)

    async with cliente() as navegador:
        del navegador.headers["X-Vitalia"]
        respuesta = await navegador.post("/api/v1/cuentas/registro", json=registro)

    assert respuesta.status_code == 403
    assert respuesta.json()["codigo"] == "falta_encabezado"


# --- HU-001: médico y consultorio; HU-006: acceso denegado


async def test_el_enlace_de_puesta_en_marcha_no_sirve_dos_veces(
    cliente: Cliente, medico: UUID
) -> None:
    async with cliente() as navegador:
        respuesta = await navegador.post(
            "/api/v1/puesta-en-marcha",
            json={
                "enlace": "uno-que-no-existe",
                "tipo_documento": "CC",
                "numero_documento": "80123456",
                "nombres": "Otro",
                "apellidos": "Médico",
                "correo": "otro@ejemplo.test",
                "contrasena": "otro2026x",
            },
        )

    assert respuesta.status_code == 422
    assert respuesta.json()["codigo"] == "enlace_invalido"


async def test_no_se_crea_un_segundo_enlace_si_ya_hay_medico(url_api: str, medico: UUID) -> None:
    from vitalia.adaptadores.postgres.conexion import crear_motor
    from vitalia.adaptadores.reloj import RelojDelSistema
    from vitalia.casos_de_uso.crear_enlace_de_puesta_en_marcha import (
        CrearEnlaceDePuestaEnMarcha,
    )
    from vitalia.dominio.cuentas import YaHayMedico

    motor = crear_motor(url_api, reutilizar=False)
    try:
        with pytest.raises(YaHayMedico):
            await CrearEnlaceDePuestaEnMarcha(UnidadPostgres(motor), RelojDelSistema()).ejecutar()
    finally:
        await motor.dispose()


async def test_el_medico_registra_su_consultorio_y_el_paciente_lo_ve(
    cliente: Cliente, medico: UUID
) -> None:
    consultorio = {
        "nombre": "Consultorio Dra. Camila Ríos",
        "direccion": "Calle 10 # 5-20, Tunja",
        "telefono": "608 742 1100",
        "correo": "consultorio@ejemplo.test",
        "medico_nombres": "Camila",
        "medico_apellidos": "Ríos",
        "registro_profesional": "RM 15-2031",
    }

    async with cliente() as doctora:
        await doctora.post(
            "/api/v1/sesion", json={**DOCUMENTO_DEL_MEDICO, "contrasena": CONTRASENA_DE_PRUEBA}
        )
        guardado = await doctora.put("/api/v1/consultorio", json=consultorio)
        leido = await doctora.get("/api/v1/consultorio")
    async with cliente() as cualquiera:
        publico = await cualquiera.get("/api/v1/consultorio/publico")

    assert guardado.status_code == 204
    assert leido.json() == consultorio
    assert publico.json() == {
        "nombre": "Consultorio Dra. Camila Ríos",
        "telefono": "608 742 1100",
        "medico": "Camila Ríos",
    }


async def test_un_paciente_no_edita_el_consultorio_y_queda_en_la_bitacora(
    cliente: Cliente, unidad: UnidadPostgres, motor_api: AsyncEngine, medico: UUID
) -> None:
    registro = await _registro(cliente)

    async with cliente() as navegador:
        await navegador.post("/api/v1/cuentas/registro", json=registro)
        usuario = (await navegador.get("/api/v1/yo")).json()["usuario_id"]
        respuesta = await navegador.put(
            "/api/v1/consultorio",
            json={
                "nombre": "Mío",
                "direccion": None,
                "telefono": None,
                "correo": None,
                "medico_nombres": "Yo",
                "medico_apellidos": "Mismo",
                "registro_profesional": None,
            },
        )

    assert respuesta.status_code == 403
    async with unidad.abrir(Identidad("medico", medico)) as trabajo:
        acciones = list(
            await trabajo.conexion.scalars(
                text("SELECT accion FROM bitacora WHERE usuario_id = :u ORDER BY id"),
                {"u": usuario},
            )
        )
    assert acciones == ["registro", "ingreso", "acceso_denegado"]


async def test_sin_sesion_no_hay_cuenta_que_ver(cliente: Cliente) -> None:
    async with cliente() as navegador:
        respuesta = await navegador.get("/api/v1/yo")

    assert respuesta.status_code == 401
    assert set(respuesta.json()) == {"codigo", "mensaje", "detalle"}
