"""Único lugar que une los adaptadores con los casos de uso.

Arrancar la API:            uv run uvicorn --factory vitalia.principal:crear
Enlace de puesta en marcha: uv run python -m vitalia.principal puesta-en-marcha
"""

import argparse
import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from vitalia.adaptadores.contrasenas import ContrasenasArgon2
from vitalia.adaptadores.postgres.conexion import BasePostgres, crear_motor
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.adaptadores.reloj import RelojDelSistema
from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.cerrar_sesion import CerrarSesion
from vitalia.casos_de_uso.crear_enlace_de_puesta_en_marcha import CrearEnlaceDePuestaEnMarcha
from vitalia.casos_de_uso.editar_consultorio import EditarConsultorio
from vitalia.casos_de_uso.ingresar import Ingresar
from vitalia.casos_de_uso.poner_en_marcha import PonerEnMarcha
from vitalia.casos_de_uso.puertos import Reloj
from vitalia.casos_de_uso.registrar_paciente import RegistrarPaciente
from vitalia.casos_de_uso.revisar_salud import RevisarSalud
from vitalia.casos_de_uso.validar_sesion import ValidarSesion
from vitalia.casos_de_uso.ver_consultorio import VerConsultorio
from vitalia.casos_de_uso.ver_mi_cuenta import VerMiCuenta
from vitalia.casos_de_uso.ver_texto_de_autorizacion import VerTextoDeAutorizacion
from vitalia.configuracion import Configuracion, leer
from vitalia.entrada.api import crear_api
from vitalia.entrada.casos import Ajustes, CasosDeUso


def armar(configuracion: Configuracion, reloj: Reloj | None = None) -> FastAPI:
    """El reloj solo se cambia en las pruebas, para simular el paso del tiempo."""
    motor = crear_motor(configuracion.bd_url)
    unidad = UnidadPostgres(motor)
    reloj = reloj or RelojDelSistema()
    contrasenas = ContrasenasArgon2()
    autorizador = Autorizador(unidad)

    casos = CasosDeUso(
        revisar_salud=RevisarSalud(BasePostgres(motor)),
        validar_sesion=ValidarSesion(unidad, reloj),
        ingresar=Ingresar(unidad, contrasenas, reloj),
        cerrar_sesion=CerrarSesion(unidad, autorizador, reloj),
        ver_mi_cuenta=VerMiCuenta(unidad, autorizador),
        registrar_paciente=RegistrarPaciente(unidad, contrasenas, reloj),
        ver_texto_de_autorizacion=VerTextoDeAutorizacion(unidad),
        poner_en_marcha=PonerEnMarcha(unidad, contrasenas, reloj),
        ver_consultorio=VerConsultorio(unidad, autorizador),
        editar_consultorio=EditarConsultorio(unidad, autorizador),
    )

    @asynccontextmanager
    async def ciclo_de_vida(_: FastAPI) -> AsyncIterator[None]:
        yield
        await motor.dispose()

    ajustes = Ajustes(secreto_del_origen=configuracion.sesion_secreto.encode())
    return crear_api(casos, ajustes, ciclo_de_vida)


def crear() -> FastAPI:
    return armar(leer())


async def crear_enlace_de_puesta_en_marcha(configuracion: Configuracion) -> str:
    motor = crear_motor(configuracion.bd_url, reutilizar=False)
    try:
        caso = CrearEnlaceDePuestaEnMarcha(UnidadPostgres(motor), RelojDelSistema())
        ficha = await caso.ejecutar()
    finally:
        await motor.dispose()
    return f"{configuracion.sitio_url}/puesta-en-marcha?enlace={ficha}"


def main() -> None:
    ordenes = argparse.ArgumentParser(prog="vitalia")
    ordenes.add_argument(
        "orden",
        choices=["puesta-en-marcha"],
        help="puesta-en-marcha: crea el enlace de un solo uso para la cuenta del médico",
    )
    ordenes.parse_args()
    enlace = asyncio.run(crear_enlace_de_puesta_en_marcha(leer()))
    print("Enlace para crear la cuenta del médico. Sirve una sola vez y vence en 24 horas:")
    print(enlace)


if __name__ == "__main__":
    main()
