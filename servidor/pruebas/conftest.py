"""Preparación común de las pruebas."""

import asyncio
import os
import secrets
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal
from uuid import UUID

import httpx
import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine

from vitalia.adaptadores.postgres.conexion import crear_motor
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.adaptadores.reloj import RelojDelSistema
from vitalia.casos_de_uso.crear_enlace_de_puesta_en_marcha import CrearEnlaceDePuestaEnMarcha
from vitalia.configuracion import Configuracion
from vitalia.principal import armar

SERVIDOR = Path(__file__).parent.parent
BASE_DE_PRUEBAS = "vitalia_pruebas"

load_dotenv(SERVIDOR / ".env")


def _en_la_base_de_pruebas(variable: str) -> str:
    direccion = make_url(os.environ[variable]).set(database=BASE_DE_PRUEBAS)
    return direccion.render_as_string(hide_password=False)


async def _administrar(orden: str) -> None:
    # Crear y borrar bases se hace conectado a la de desarrollo, con su dueño.
    motor = crear_motor(os.environ["BD_URL_MIGRACIONES"], reutilizar=False)
    async with motor.connect() as conexion:
        en_directo = await conexion.execution_options(isolation_level="AUTOCOMMIT")
        await en_directo.execute(text(orden))
    await motor.dispose()


@pytest.fixture(scope="session")
def url_api() -> Iterator[str]:
    """Crea la base de pruebas con sus migraciones y la borra al terminar."""
    asyncio.run(_administrar(f"DROP DATABASE IF EXISTS {BASE_DE_PRUEBAS} WITH (FORCE)"))
    asyncio.run(_administrar(f"CREATE DATABASE {BASE_DE_PRUEBAS}"))
    alembic = Config(SERVIDOR / "alembic.ini")
    alembic.attributes["url"] = _en_la_base_de_pruebas("BD_URL_MIGRACIONES")
    command.upgrade(alembic, "head")
    yield _en_la_base_de_pruebas("BD_URL")
    asyncio.run(_administrar(f"DROP DATABASE {BASE_DE_PRUEBAS} WITH (FORCE)"))


@pytest.fixture(scope="session")
async def motor_api(url_api: str) -> AsyncIterator[AsyncEngine]:
    """Motor conectado como vitalia_api, el usuario sin privilegios de la aplicación."""
    motor = crear_motor(url_api)
    yield motor
    await motor.dispose()


@pytest.fixture(scope="session")
async def motor_dueno(url_api: str) -> AsyncIterator[AsyncEngine]:
    """Motor conectado como el dueño de las tablas, el mismo usuario de las migraciones."""
    motor = crear_motor(_en_la_base_de_pruebas("BD_URL_MIGRACIONES"))
    yield motor
    await motor.dispose()


@pytest.fixture(scope="session")
def unidad(motor_api: AsyncEngine) -> UnidadPostgres:
    return UnidadPostgres(motor_api)


CrearUsuario = Callable[[Literal["paciente"]], Awaitable[UUID]]


@pytest.fixture(scope="session")
def crear_usuario(motor_dueno: AsyncEngine) -> CrearUsuario:
    """Crea un paciente inventado sin contraseña, directo en la base, para probar permisos.

    Como dueño, quita por un momento los permisos forzados. Las cuentas que ingresan se crean
    por la API, como lo haría una persona.
    """

    async def _crear(rol: Literal["paciente"]) -> UUID:
        tablas = ("usuarios", "pacientes", "medicos")
        async with motor_dueno.begin() as conexion:
            for tabla in tablas:
                await conexion.execute(text(f"ALTER TABLE {tabla} NO FORCE ROW LEVEL SECURITY"))
            usuario_id: UUID = await conexion.scalar(
                text(
                    "INSERT INTO usuarios (tipo_documento, numero_documento, rol) "
                    "VALUES ('CC', :numero, :rol) RETURNING id"
                ),
                {"numero": str(secrets.randbelow(10**10)), "rol": rol},
            )
            await conexion.execute(
                text(
                    "INSERT INTO pacientes (usuario_id, nombres, apellidos, fecha_nacimiento, "
                    "telefono) VALUES (:id, 'Paciente', 'De prueba', '1980-05-17', '3000000000')"
                ),
                {"id": usuario_id},
            )
            for tabla in tablas:
                await conexion.execute(text(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY"))
        return usuario_id

    return _crear


class RelojMovible:
    """Reloj de las pruebas: marca la hora real más lo que se le adelante."""

    def __init__(self) -> None:
        self.adelanto = timedelta()

    def ahora(self) -> datetime:
        return datetime.now(UTC) + self.adelanto

    def poner(self, momento: datetime) -> None:
        """Deja el reloj en ese momento; desde ahí sigue andando."""
        self.adelanto = momento - datetime.now(UTC)


@pytest.fixture(scope="session")
def reloj() -> RelojMovible:
    return RelojMovible()


@pytest.fixture(autouse=True)
def reloj_en_hora(reloj: RelojMovible) -> Iterator[None]:
    yield
    reloj.adelanto = timedelta()


@pytest.fixture(scope="session")
def carpeta_de_archivos(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Donde las pruebas guardan los documentos subidos. Se borra sola."""
    return tmp_path_factory.mktemp("archivos")


@pytest.fixture(scope="session")
async def api(
    url_api: str, reloj: RelojMovible, carpeta_de_archivos: Path
) -> AsyncIterator[FastAPI]:
    configuracion = Configuracion(
        bd_url=url_api,
        sesion_secreto="pruebas",
        carpeta_de_archivos=carpeta_de_archivos,
        lector_en_segundo_plano=False,
    )
    aplicacion = armar(configuracion, reloj)
    async with aplicacion.router.lifespan_context(aplicacion):
        yield aplicacion


Cliente = Callable[..., httpx.AsyncClient]


@pytest.fixture
def cliente(api: FastAPI) -> Cliente:
    """Un navegador de mentira. Cada equipo tiene su propia dirección de red."""

    def _cliente(equipo: str = "10.0.0.1") -> httpx.AsyncClient:
        transporte = httpx.ASGITransport(app=api, client=(equipo, 50000))
        return httpx.AsyncClient(
            transport=transporte, base_url="https://vitalia.prueba", headers={"X-Vitalia": "1"}
        )

    return _cliente


DOCUMENTO_DEL_MEDICO = {"tipo_documento": "CC", "numero_documento": "52345678"}
CONTRASENA_DE_PRUEBA = "consultorio2026"


@pytest.fixture(scope="session")
async def medico(api: FastAPI, url_api: str) -> UUID:
    """El único médico del consultorio (supuesto S-01), creado con la puesta en marcha."""
    motor = crear_motor(url_api, reutilizar=False)
    try:
        caso = CrearEnlaceDePuestaEnMarcha(UnidadPostgres(motor), RelojDelSistema())
        enlace = await caso.ejecutar()
    finally:
        await motor.dispose()

    transporte = httpx.ASGITransport(app=api, client=("10.0.0.9", 50000))
    async with httpx.AsyncClient(
        transport=transporte, base_url="https://vitalia.prueba", headers={"X-Vitalia": "1"}
    ) as navegador:
        creada = await navegador.post(
            "/api/v1/puesta-en-marcha",
            json={
                "enlace": enlace,
                **DOCUMENTO_DEL_MEDICO,
                "nombres": "Camila",
                "apellidos": "Ríos",
                "correo": "camila@ejemplo.test",
                "contrasena": CONTRASENA_DE_PRUEBA,
            },
        )
        assert creada.status_code == 201, creada.text
        yo = await navegador.get("/api/v1/yo")
    return UUID(yo.json()["usuario_id"])


def navegador(api: FastAPI, equipo: str = "10.0.0.1") -> httpx.AsyncClient:
    transporte = httpx.ASGITransport(app=api, client=(equipo, 50000))
    return httpx.AsyncClient(
        transport=transporte, base_url="https://vitalia.prueba", headers={"X-Vitalia": "1"}
    )


IngresarDoctora = Callable[[], Awaitable[httpx.AsyncClient]]


@pytest.fixture
async def ingresar_doctora(api: FastAPI, medico: UUID) -> AsyncIterator[IngresarDoctora]:
    """Abre la sesión de la médica. Se llama después de poner el reloj, o la sesión vencería."""
    abiertos: list[httpx.AsyncClient] = []

    async def _ingresar() -> httpx.AsyncClient:
        cliente = navegador(api, "10.0.0.9")
        abiertos.append(cliente)
        respuesta = await cliente.post(
            "/api/v1/sesion", json={**DOCUMENTO_DEL_MEDICO, "contrasena": CONTRASENA_DE_PRUEBA}
        )
        assert respuesta.status_code == 200, respuesta.text
        return cliente

    yield _ingresar
    for cliente in abiertos:
        await cliente.aclose()


NuevoPaciente = Callable[..., Awaitable[httpx.AsyncClient]]


@pytest.fixture
async def nuevo_paciente(api: FastAPI) -> AsyncIterator[NuevoPaciente]:
    """Registra pacientes inventados por la API y entrega su navegador con la sesión abierta."""
    abiertos: list[httpx.AsyncClient] = []

    async def _registrar(
        nombres: str = "Rosa Elena", apellidos: str = "Duarte", ia: bool = False
    ) -> httpx.AsyncClient:
        cliente = navegador(api)
        abiertos.append(cliente)
        texto = (await cliente.get("/api/v1/autorizaciones/texto?tipo=datos")).json()
        texto_ia = None
        if ia:
            texto_ia = (await cliente.get("/api/v1/autorizaciones/texto?tipo=ia")).json()["id"]
        respuesta = await cliente.post(
            "/api/v1/cuentas/registro",
            json={
                "tipo_documento": "CC",
                "numero_documento": str(secrets.randbelow(10**9) + 10**8),
                "nombres": nombres,
                "apellidos": apellidos,
                "fecha_nacimiento": "1958-03-02",
                "telefono": "3185550116",
                "correo": "paciente@ejemplo.test",
                "contrasena": "girasol2026",
                "texto_datos": texto["id"],
                "texto_ia": texto_ia,
            },
        )
        assert respuesta.status_code == 201, respuesta.text
        return cliente

    yield _registrar
    for cliente in abiertos:
        await cliente.aclose()


@pytest.fixture(scope="session")
async def consultorio_listo(api: FastAPI, medico: UUID) -> dict[str, str]:
    """Datos del consultorio, horario de lunes a viernes de 8 a 12 y de 2 a 5, y dos tipos de cita.

    Devuelve el id de cada tipo de cita.
    """
    async with navegador(api, "10.0.0.9") as cliente:
        await cliente.post(
            "/api/v1/sesion", json={**DOCUMENTO_DEL_MEDICO, "contrasena": CONTRASENA_DE_PRUEBA}
        )
        franjas = [
            {"dia_semana": dia, "hora_inicio": inicio, "hora_fin": fin}
            for dia in range(1, 6)
            for inicio, fin in (("08:00", "12:00"), ("14:00", "17:00"))
        ]
        datos = await cliente.put(
            "/api/v1/consultorio",
            json={
                "nombre": "Consultorio Dra. Camila Ríos",
                "direccion": "Calle 10 # 5-20, Tunja",
                "telefono": "608 742 1100",
                "correo": None,
                "medico_nombres": "Camila",
                "medico_apellidos": "Ríos",
                "registro_profesional": "RM 15-2031",
            },
        )
        assert datos.status_code == 204, datos.text
        guardado = await cliente.put("/api/v1/horario", json={"franjas": franjas})
        assert guardado.status_code == 200, guardado.text
        tipos = {}
        for nombre, minutos in (("Consulta general", 30), ("Control", 20)):
            creado = await cliente.post(
                "/api/v1/tipos-cita", json={"nombre": nombre, "duracion_minutos": minutos}
            )
            assert creado.status_code == 201, creado.text
            tipos[nombre] = creado.json()["id"]
    return tipos


def pdf_con_texto(*paginas: str) -> bytes:
    """Arma un PDF de verdad, con una página por texto.

    Una cadena vacía da una página sin texto, como la de un escaneado.
    """
    objetos = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    hijas = " ".join(f"{4 + 2 * i} 0 R" for i in range(len(paginas)))
    objetos.append(f"<< /Type /Pages /Kids [{hijas}] /Count {len(paginas)} >>".encode())
    objetos.append(
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    )
    for i, texto in enumerate(paginas):
        ordenes = ["BT /F1 11 Tf 50 760 Td 14 TL"]
        for linea in texto.split("\n") if texto else []:
            escapada = linea.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            ordenes.append(f"({escapada}) Tj T*")
        ordenes.append("ET")
        flujo = "\n".join(ordenes).encode("cp1252")
        objetos.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>".encode()
        )
        objetos.append(b"<< /Length %d >>\nstream\n" % len(flujo) + flujo + b"\nendstream")

    salida = bytearray(b"%PDF-1.4\n")
    posiciones = []
    for numero, cuerpo in enumerate(objetos, 1):
        posiciones.append(len(salida))
        salida += f"{numero} 0 obj\n".encode() + cuerpo + b"\nendobj\n"
    indice = len(salida)
    salida += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode()
    for posicion in posiciones:
        salida += f"{posicion:010d} 00000 n \n".encode()
    salida += (
        f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{indice}\n%%EOF\n"
    ).encode()
    return bytes(salida)
