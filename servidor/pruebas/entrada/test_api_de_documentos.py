"""Subir documentos y leerlos página por página (HU-028, HU-031)."""

from collections.abc import AsyncIterator, Sequence
from pathlib import Path
from typing import Any
from uuid import UUID

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import text

from conftest import IngresarDoctora, NuevoPaciente, pdf_con_texto
from vitalia.adaptadores.archivos_en_disco import ArchivosEnDisco
from vitalia.adaptadores.pdf import LectorPdfium
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.casos_de_uso.leer_documentos import LeerDocumentos
from vitalia.casos_de_uso.puertos import Turno
from vitalia.dominio.identidad import SISTEMA

pytestmark = pytest.mark.bd

HISTORIA = pdf_con_texto(
    "IPS ARRAYANES SALUD\nMotivo de consulta: control de la presion y del colesterol.",
    "Diagnostico principal: I10 Hipertension esencial (primaria). Confirmado repetido.",
)


async def subir(
    cliente: httpx.AsyncClient,
    contenido: bytes,
    nombre: str = "Control de presión",
    fecha: str = "2026-08-20",
    tipo: str = "historia_clinica",
) -> httpx.Response:
    return await cliente.post(
        "/api/v1/documentos",
        data={"nombre": nombre, "fecha_documento": fecha, "tipo": tipo},
        files={"archivo": ("historia.pdf", contenido, "application/pdf")},
    )


def lector(api: FastAPI) -> LeerDocumentos:
    resultado: LeerDocumentos = api.state.lector
    return resultado


async def como_sistema(unidad: UnidadPostgres, consulta: str, **valores: Any) -> list[Any]:
    async with unidad.abrir(SISTEMA) as trabajo:
        return list(await trabajo.conexion.execute(text(consulta), valores))


async def test_sube_un_pdf_y_queda_en_proceso_en_la_lista(nuevo_paciente: NuevoPaciente) -> None:
    rosa = await nuevo_paciente()

    respuesta = await subir(rosa, HISTORIA)

    assert respuesta.status_code == 201, respuesta.text
    documento = respuesta.json()
    assert documento["nombre"] == "Control de presión"
    assert documento["formato"] == "pdf"
    assert documento["estado_lectura"] == "en_proceso"
    lista = (await rosa.get("/api/v1/documentos")).json()
    assert [d["id"] for d in lista] == [documento["id"]]


async def test_el_lector_guarda_el_texto_pagina_por_pagina(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente
) -> None:
    rosa = await nuevo_paciente()
    documento = (await subir(rosa, HISTORIA)).json()

    await lector(api).leer_pendientes()

    leido = (await rosa.get("/api/v1/documentos")).json()[0]
    assert leido["estado_lectura"] == "legible"
    assert leido["paginas"] == 2
    paginas = await como_sistema(
        unidad,
        "SELECT numero, texto, origen FROM paginas_documento WHERE documento_id = :d "
        "ORDER BY numero",
        d=UUID(documento["id"]),
    )
    assert [(p.numero, p.origen) for p in paginas] == [(1, "pdf"), (2, "pdf")]
    assert "I10 Hipertension esencial" in paginas[1].texto


async def test_sin_autorizacion_de_ia_no_se_indexa_aunque_sea_legible(
    api: FastAPI, unidad: UnidadPostgres, nuevo_paciente: NuevoPaciente
) -> None:
    sin_ia = await nuevo_paciente(ia=False)
    con_ia = await nuevo_paciente(ia=True)
    uno = (await subir(sin_ia, pdf_con_texto("Paciente sin IA. " * 5))).json()
    otro = (await subir(con_ia, pdf_con_texto("Paciente con IA. " * 5))).json()

    await lector(api).leer_pendientes()

    encolados = await como_sistema(
        unidad,
        "SELECT documento_id FROM trabajos_lectura WHERE tipo = 'indexar_documento' "
        "AND documento_id IN (:uno, :otro)",
        uno=UUID(uno["id"]),
        otro=UUID(otro["id"]),
    )
    assert [e.documento_id for e in encolados] == [UUID(otro["id"])]


async def test_el_mismo_archivo_dos_veces_no_deja_copias(nuevo_paciente: NuevoPaciente) -> None:
    rosa = await nuevo_paciente()
    primero = (await subir(rosa, HISTORIA)).json()

    repetido = await subir(rosa, HISTORIA, nombre="Otro nombre")

    assert repetido.status_code == 409
    assert repetido.json()["codigo"] == "documento_repetido"
    assert repetido.json()["detalle"] == {"documento_id": primero["id"]}
    assert len((await rosa.get("/api/v1/documentos")).json()) == 1


async def test_otro_paciente_puede_subir_el_mismo_archivo(nuevo_paciente: NuevoPaciente) -> None:
    rosa = await nuevo_paciente()
    luis = await nuevo_paciente("Luis", "Pardo")
    await subir(rosa, HISTORIA)

    respuesta = await subir(luis, HISTORIA)

    assert respuesta.status_code == 201
    assert len((await luis.get("/api/v1/documentos")).json()) == 1


@pytest.mark.parametrize(
    ("contenido", "datos", "campo"),
    [
        (b"PK\x03\x04 un zip", {}, "archivo"),
        (b"%PDF-" + b"0" * (20 * 1024 * 1024), {}, "archivo"),
        (HISTORIA, {"nombre": "  "}, "nombre"),
        (HISTORIA, {"fecha": "2099-01-01"}, "fecha_documento"),
        (HISTORIA, {"tipo": "radiografia"}, "tipo"),
    ],
    ids=["formato", "mas_de_20_mb", "sin_nombre", "fecha_futura", "tipo"],
)
async def test_rechaza_el_archivo_y_dice_por_que(
    nuevo_paciente: NuevoPaciente, contenido: bytes, datos: dict[str, str], campo: str
) -> None:
    rosa = await nuevo_paciente()

    respuesta = await subir(rosa, contenido, **datos)

    assert respuesta.status_code == 400, respuesta.text
    assert campo in respuesta.json()["detalle"]
    assert (await rosa.get("/api/v1/documentos")).json() == []


async def test_el_medico_no_sube_documentos(ingresar_doctora: IngresarDoctora) -> None:
    doctora = await ingresar_doctora()

    respuesta = await subir(doctora, HISTORIA)

    assert respuesta.status_code == 403


async def test_cada_paciente_ve_solo_sus_documentos(nuevo_paciente: NuevoPaciente) -> None:
    rosa = await nuevo_paciente()
    luis = await nuevo_paciente("Luis", "Pardo")
    await subir(rosa, HISTORIA)

    assert (await luis.get("/api/v1/documentos")).json() == []


async def test_un_pdf_danado_queda_no_legible_tras_los_reintentos(
    api: FastAPI, nuevo_paciente: NuevoPaciente
) -> None:
    rosa = await nuevo_paciente()
    await subir(rosa, b"%PDF-1.4 esto no es un pdf de verdad")

    await lector(api).leer_pendientes()

    assert (await rosa.get("/api/v1/documentos")).json()[0]["estado_lectura"] == "no_legible"


class IAEspia:
    """Cuenta cuántas imágenes le llegan y responde un texto fijo."""

    def __init__(self) -> None:
        self.imagenes: list[bytes] = []

    async def leer_pagina(self, imagen: bytes) -> str:
        self.imagenes.append(imagen)
        return "Hemoglobina glicosilada 6,9 % del 10/09/2026. Glucemia en ayunas 118 mg/dL."

    async def responder(self, instrucciones: str, turnos: Sequence[Turno]) -> AsyncIterator[str]:
        yield ""


@pytest.fixture
def espia() -> IAEspia:
    return IAEspia()


@pytest.fixture
def lector_con_ia(
    unidad: UnidadPostgres, carpeta_de_archivos: Path, espia: IAEspia
) -> LeerDocumentos:
    return LeerDocumentos(unidad, ArchivosEnDisco(carpeta_de_archivos), LectorPdfium(), espia)


ESCANEADO = pdf_con_texto("", "")


async def test_un_escaneado_sin_autorizacion_no_sale_hacia_la_ia(
    nuevo_paciente: NuevoPaciente, lector_con_ia: LeerDocumentos, espia: IAEspia
) -> None:
    rosa = await nuevo_paciente(ia=False)
    await subir(rosa, ESCANEADO)
    await subir(rosa, b"\x89PNG\r\n\x1a\n una foto", nombre="Foto del examen")

    await lector_con_ia.leer_pendientes()

    assert espia.imagenes == []
    estados = {d["estado_lectura"] for d in (await rosa.get("/api/v1/documentos")).json()}
    assert estados == {"sin_leer"}


async def test_un_escaneado_con_autorizacion_se_reconoce_pagina_por_pagina(
    unidad: UnidadPostgres,
    nuevo_paciente: NuevoPaciente,
    lector_con_ia: LeerDocumentos,
    espia: IAEspia,
) -> None:
    gloria = await nuevo_paciente(ia=True)
    documento = (await subir(gloria, ESCANEADO, nombre="Laboratorios escaneados")).json()

    await lector_con_ia.leer_pendientes()

    assert len(espia.imagenes) == 2
    assert all(imagen.startswith(b"\x89PNG") for imagen in espia.imagenes)
    leido = (await gloria.get("/api/v1/documentos")).json()[0]
    assert (leido["estado_lectura"], leido["paginas"]) == ("legible", 2)
    paginas = await como_sistema(
        unidad,
        "SELECT origen, legibilidad FROM paginas_documento WHERE documento_id = :d",
        d=UUID(documento["id"]),
    )
    assert {(p.origen, p.legibilidad) for p in paginas} == {("reconocido", 1.0)}


async def test_sin_modelo_configurado_el_escaneado_queda_sin_leer(
    api: FastAPI, nuevo_paciente: NuevoPaciente
) -> None:
    gloria = await nuevo_paciente(ia=True)
    await subir(gloria, ESCANEADO)

    await lector(api).leer_pendientes()  # el de la API no tiene proveedor de IA

    assert (await gloria.get("/api/v1/documentos")).json()[0]["estado_lectura"] == "sin_leer"
