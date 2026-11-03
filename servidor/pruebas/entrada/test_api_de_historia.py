"""Historia clínica del consultorio por la API (HU-041 a HU-045)."""

from typing import Any

import httpx
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from conftest import CONTRASENA_DE_PRUEBA, IngresarDoctora, NuevoPaciente

pytestmark = pytest.mark.bd

IDENTIFICACION = {
    "sexo": "M",
    "estado_civil": "casado",
    "ocupacion": "Docente",
    "direccion": "Calle 10 # 5-20",
    "municipio": "Tunja",
    "tipo_vinculacion": "contributivo",
    "aseguradora": "EPS de prueba",
}

CONSULTA = {
    "tipo_consulta": "control",
    "finalidad": "tratamiento",
    "causa": "enfermedad_general",
    "motivo": "Control de hipertensión arterial.",
    "enfermedad_actual": "Toma los medicamentos todos los días. Niega cefalea.",
    "antecedentes_personales": "Hipertensión arterial desde 2015.",
    "antecedentes_familiares": "Madre con diabetes tipo 2.",
    "alergias": "No refiere",
    "factores_riesgo": "No refiere",
    "revision_sistemas": "Sin hallazgos",
    "tension_sistolica": 128,
    "tension_diastolica": 82,
    "frecuencia_cardiaca": 72,
    "frecuencia_respiratoria": 16,
    "temperatura": "36,5",
    "peso": 72,
    "talla": 168,
    "examen_fisico": "Buen estado general. Ruidos cardiacos rítmicos.",
    "plan": "Continuar el tratamiento. Control en tres meses.",
    "destino": "casa",
}

DIAGNOSTICOS = [{"codigo": "I10X", "tipo": "confirmado_repetido", "principal": True}]
FORMULA = [
    {
        "nombre": "Losartán 50 mg",
        "dosis": "1 tableta",
        "via": "oral",
        "frecuencia": "cada 12 horas",
        "dias": 90,
    }
]


async def paciente_id(doctora: httpx.AsyncClient, apellido: str) -> str:
    encontrados = (await doctora.get("/api/v1/pacientes", params={"buscar": apellido})).json()
    return str(encontrados["pacientes"][0]["id"])


async def atencion_lista(doctora: httpx.AsyncClient, paciente: str) -> str:
    """Abre una atención con la identificación y la consulta completas."""
    await doctora.put(
        f"/api/v1/pacientes/{paciente}/identificacion", json={"datos": IDENTIFICACION}
    )
    abierta = await doctora.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})
    assert abierta.status_code == 201, abierta.text
    atencion = str(abierta.json()["id"])
    guardada = await doctora.patch(
        f"/api/v1/atenciones/{atencion}",
        json={"datos": CONSULTA, "diagnosticos": DIAGNOSTICOS, "medicamentos": FORMULA},
    )
    assert guardada.status_code == 200, guardada.text
    return atencion


async def cerrar(doctora: httpx.AsyncClient, atencion: str) -> httpx.Response:
    return await doctora.post(
        f"/api/v1/atenciones/{atencion}/cierre", json={"contrasena": CONTRASENA_DE_PRUEBA}
    )


async def test_abre_guarda_el_borrador_y_lo_recupera(
    ingresar_doctora: IngresarDoctora, nuevo_paciente: NuevoPaciente
) -> None:
    await nuevo_paciente("Hernando", "Castaño Ríos")
    doctora = await ingresar_doctora()
    paciente = await paciente_id(doctora, "Castaño Ríos")

    abierta = await doctora.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})
    otra = await doctora.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})
    atencion = abierta.json()["id"]
    # Una sola abierta por paciente (HU-042, CA-6).
    assert otra.json()["id"] == atencion

    guardada = await doctora.patch(
        f"/api/v1/atenciones/{atencion}", json={"datos": {"motivo": "Dolor de rodilla."}}
    )
    assert guardada.status_code == 200, guardada.text
    vista = (await doctora.get(f"/api/v1/atenciones/{atencion}")).json()
    assert vista["atencion"]["datos"]["motivo"] == "Dolor de rodilla."
    assert vista["atencion"]["estado"] == "abierta"
    assert "Sexo" in vista["faltantes"]["identificacion"]


async def test_un_signo_vital_imposible_no_se_guarda(
    ingresar_doctora: IngresarDoctora, nuevo_paciente: NuevoPaciente
) -> None:
    await nuevo_paciente("Gloria", "Mosquera Valencia")
    doctora = await ingresar_doctora()
    paciente = await paciente_id(doctora, "Mosquera Valencia")
    atencion = (await doctora.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})).json()[
        "id"
    ]

    respuesta = await doctora.patch(
        f"/api/v1/atenciones/{atencion}", json={"datos": {"temperatura": 53}}
    )

    assert respuesta.status_code == 400
    assert "temperatura" in respuesta.json()["detalle"]


async def test_no_cierra_si_faltan_datos_y_dice_cuales(
    ingresar_doctora: IngresarDoctora, nuevo_paciente: NuevoPaciente
) -> None:
    await nuevo_paciente("Martha", "Restrepo Gil")
    doctora = await ingresar_doctora()
    paciente = await paciente_id(doctora, "Restrepo Gil")
    atencion = (await doctora.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})).json()[
        "id"
    ]

    respuesta = await cerrar(doctora, atencion)

    assert respuesta.status_code == 422
    detalle = respuesta.json()["detalle"]
    assert "Ocupación" in detalle["identificacion"]
    assert "Diagnóstico principal" in detalle["atencion"]


async def test_cerrar_pide_la_contrasena_del_medico(
    ingresar_doctora: IngresarDoctora, nuevo_paciente: NuevoPaciente
) -> None:
    await nuevo_paciente("Juan Sebastián", "Ortiz Bermúdez")
    doctora = await ingresar_doctora()
    atencion = await atencion_lista(doctora, await paciente_id(doctora, "Ortiz Bermúdez"))

    respuesta = await doctora.post(
        f"/api/v1/atenciones/{atencion}/cierre", json={"contrasena": "otra"}
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["codigo"] == "contrasena_incorrecta"


async def test_cerrada_queda_firmada_no_cambia_y_se_corrige_con_una_nota(
    ingresar_doctora: IngresarDoctora, nuevo_paciente: NuevoPaciente, motor_dueno: AsyncEngine
) -> None:
    await nuevo_paciente("Inés", "Quintero Lozada")
    doctora = await ingresar_doctora()
    atencion = await atencion_lista(doctora, await paciente_id(doctora, "Quintero Lozada"))

    cerrada = await cerrar(doctora, atencion)
    assert cerrada.status_code == 200, cerrada.text

    vista = (await doctora.get(f"/api/v1/atenciones/{atencion}")).json()["atencion"]
    assert vista["estado"] == "cerrada"
    assert vista["firma"]["nombre"] == "Camila Ríos"
    assert vista["firma"]["documento"] == "CC 52345678"
    assert vista["imc"] == 25.5
    assert vista["diagnosticos"][0]["nombre"] == "Hipertensión esencial (primaria)"

    # Lo cerrado no cambia por la API (HU-044, CA-3)...
    cambio = await doctora.patch(f"/api/v1/atenciones/{atencion}", json={"datos": {"plan": "X"}})
    assert cambio.status_code == 409
    # ...ni siquiera para el dueño de las tablas.
    with pytest.raises(Exception, match="no se modifica"):
        async with motor_dueno.begin() as conexion:
            # Sin esto el dueño no ve la fila; la transacción fallida lo deshace.
            await conexion.execute(text("ALTER TABLE atenciones NO FORCE ROW LEVEL SECURITY"))
            await conexion.execute(
                text("UPDATE atenciones SET plan = 'X' WHERE id = :id"), {"id": atencion}
            )

    nota = await doctora.post(
        f"/api/v1/atenciones/{atencion}/notas", json={"texto": "La talla correcta es 170 cm."}
    )
    assert nota.status_code == 201, nota.text
    vista = (await doctora.get(f"/api/v1/atenciones/{atencion}")).json()["atencion"]
    assert vista["notas"][0]["texto"] == "La talla correcta es 170 cm."


async def test_la_siguiente_atencion_trae_los_antecedentes_de_la_anterior(
    ingresar_doctora: IngresarDoctora, nuevo_paciente: NuevoPaciente
) -> None:
    await nuevo_paciente("Ana María", "Mejía Arango")
    doctora = await ingresar_doctora()
    paciente = await paciente_id(doctora, "Mejía Arango")
    primera = await atencion_lista(doctora, paciente)
    assert (await cerrar(doctora, primera)).status_code == 200

    segunda = (await doctora.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})).json()["id"]
    datos = (await doctora.get(f"/api/v1/atenciones/{segunda}")).json()["atencion"]["datos"]

    assert datos["antecedentes_personales"] == "Hipertensión arterial desde 2015."
    assert datos["alergias"] == "No refiere"
    assert datos["motivo"] is None


async def test_el_paciente_ve_solo_sus_atenciones_cerradas(
    ingresar_doctora: IngresarDoctora, nuevo_paciente: NuevoPaciente
) -> None:
    luis = await nuevo_paciente("Álvaro", "Villamizar Peña")
    otra = await nuevo_paciente("Beatriz", "Cárdenas Ruiz")
    doctora = await ingresar_doctora()
    paciente = await paciente_id(doctora, "Villamizar Peña")
    cerrada = await atencion_lista(doctora, paciente)
    assert (await cerrar(doctora, cerrada)).status_code == 200
    await doctora.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})

    suyas: list[dict[str, Any]] = (await luis.get("/api/v1/mi-historia")).json()
    ajenas = (await otra.get("/api/v1/mi-historia")).json()

    assert [a["id"] for a in suyas] == [cerrada]
    assert suyas[0]["medicamentos"][0]["nombre"] == "Losartán 50 mg"
    assert ajenas == []
    # El paciente no abre atenciones ni ve la de otro.
    assert (await luis.post(f"/api/v1/pacientes/{paciente}/atenciones", json={})).status_code == 403
    assert (await otra.get(f"/api/v1/atenciones/{cerrada}")).status_code == 403


async def test_busca_diagnosticos_por_codigo_y_por_nombre(
    ingresar_doctora: IngresarDoctora,
) -> None:
    doctora = await ingresar_doctora()

    por_codigo = (await doctora.get("/api/v1/cie10", params={"buscar": "i10"})).json()
    por_nombre = (await doctora.get("/api/v1/cie10", params={"buscar": "hipertension"})).json()

    assert por_codigo[0]["codigo"] == "I10X"
    assert "I10X" in [d["codigo"] for d in por_nombre]
