"""Único lugar que une los adaptadores con los casos de uso.

Arrancar la API:            uv run uvicorn --factory vitalia.principal:crear
Enlace de puesta en marcha: uv run python -m vitalia.principal puesta-en-marcha
"""

import argparse
import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from vitalia.adaptadores.archivos_en_disco import ArchivosEnDisco
from vitalia.adaptadores.contrasenas import ContrasenasArgon2
from vitalia.adaptadores.ia.de_mentira import IADeMentira, VectoresDeMentira
from vitalia.adaptadores.ia.qwen import IAQwen, VectoresQwen
from vitalia.adaptadores.pdf import LectorPdfium
from vitalia.adaptadores.postgres.conexion import BasePostgres, crear_motor
from vitalia.adaptadores.postgres.unidad import UnidadPostgres
from vitalia.adaptadores.reloj import RelojDelSistema
from vitalia.casos_de_uso.abrir_y_eliminar_documento import AbrirDocumento, EliminarDocumento
from vitalia.casos_de_uso.agendar_cita import AgendarCita
from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.buscar_fragmentos import BuscarFragmentos
from vitalia.casos_de_uso.buscar_pacientes import BuscarPacientes
from vitalia.casos_de_uso.cancelar_cita import CancelarCita
from vitalia.casos_de_uso.cerrar_sesion import CerrarSesion
from vitalia.casos_de_uso.consultar_disponibilidad import ConsultarDisponibilidad
from vitalia.casos_de_uso.crear_enlace_de_puesta_en_marcha import CrearEnlaceDePuestaEnMarcha
from vitalia.casos_de_uso.editar_consultorio import EditarConsultorio
from vitalia.casos_de_uso.guardar_horario import GuardarHorario
from vitalia.casos_de_uso.indexar_documentos import IndexarDocumentos
from vitalia.casos_de_uso.ingresar import Ingresar
from vitalia.casos_de_uso.leer_documentos import LeerDocumentos
from vitalia.casos_de_uso.listar_citas import ListarCitas
from vitalia.casos_de_uso.mover_cita import MoverCita
from vitalia.casos_de_uso.poner_en_marcha import PonerEnMarcha
from vitalia.casos_de_uso.preguntar_al_asistente import Limites, PreguntarAlAsistente
from vitalia.casos_de_uso.puertos import ProveedorIA, Reloj, Vectorizador
from vitalia.casos_de_uso.registrar_paciente import RegistrarPaciente
from vitalia.casos_de_uso.revisar_salud import RevisarSalud
from vitalia.casos_de_uso.subir_documento import SubirDocumento
from vitalia.casos_de_uso.tipos_de_cita import TiposDeCita
from vitalia.casos_de_uso.validar_sesion import ValidarSesion
from vitalia.casos_de_uso.ver_agenda_de_hoy import VerAgendaDeHoy
from vitalia.casos_de_uso.ver_consultorio import VerConsultorio
from vitalia.casos_de_uso.ver_ficha_del_paciente import VerFichaDelPaciente
from vitalia.casos_de_uso.ver_horario import VerHorario
from vitalia.casos_de_uso.ver_inicio_del_paciente import VerInicioDelPaciente
from vitalia.casos_de_uso.ver_mi_cuenta import VerMiCuenta
from vitalia.casos_de_uso.ver_mis_documentos import VerMisDocumentos
from vitalia.casos_de_uso.ver_texto_de_autorizacion import VerTextoDeAutorizacion
from vitalia.configuracion import Configuracion, leer
from vitalia.entrada.api import crear_api
from vitalia.entrada.casos import Ajustes, CasosDeUso
from vitalia.entrada.lector import leer_en_segundo_plano

_registro = logging.getLogger(__name__)


def armar(
    configuracion: Configuracion,
    reloj: Reloj | None = None,
    ia: ProveedorIA | None = None,
) -> FastAPI:
    """El reloj y la IA solo se cambian en las pruebas.

    Sin clave de IA, el lector lee los PDF con texto y deja sin leer los escaneados; los vectores
    salen de las palabras y el asistente responde con un texto fijo.
    """
    motor = crear_motor(configuracion.bd_url)
    unidad = UnidadPostgres(motor)
    reloj = reloj or RelojDelSistema()
    contrasenas = ContrasenasArgon2()
    autorizador = Autorizador(unidad)
    archivos = ArchivosEnDisco(configuracion.carpeta_de_archivos)
    ia = ia or _ia(configuracion)
    lector = LeerDocumentos(unidad, archivos, LectorPdfium(), ia)
    vectores = _vectores(configuracion)
    limites = Limites(
        tope_contexto=configuracion.ia_tope_contexto,
        consultas_por_hora=configuracion.ia_tope_consultas_hora,
    )
    indexador = IndexarDocumentos(unidad, vectores)

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
        ver_horario=VerHorario(unidad, autorizador),
        guardar_horario=GuardarHorario(unidad, autorizador, reloj),
        tipos_de_cita=TiposDeCita(unidad, autorizador),
        consultar_disponibilidad=ConsultarDisponibilidad(unidad, autorizador, reloj),
        agendar_cita=AgendarCita(unidad, autorizador, reloj),
        listar_citas=ListarCitas(unidad, autorizador),
        mover_cita=MoverCita(unidad, autorizador, reloj),
        cancelar_cita=CancelarCita(unidad, autorizador, reloj),
        ver_inicio_del_paciente=VerInicioDelPaciente(unidad, autorizador, reloj),
        ver_agenda_de_hoy=VerAgendaDeHoy(unidad, autorizador, reloj),
        buscar_pacientes=BuscarPacientes(unidad, autorizador),
        subir_documento=SubirDocumento(unidad, autorizador, archivos, reloj),
        ver_mis_documentos=VerMisDocumentos(unidad, autorizador),
        buscar_fragmentos=BuscarFragmentos(unidad, autorizador, vectores),
        ver_ficha_del_paciente=VerFichaDelPaciente(unidad, autorizador),
        abrir_documento=AbrirDocumento(unidad, autorizador, archivos),
        eliminar_documento=EliminarDocumento(unidad, autorizador, archivos),
        preguntar_al_asistente=PreguntarAlAsistente(
            unidad, autorizador, vectores, ia or IADeMentira(), reloj, limites
        ),
    )

    @asynccontextmanager
    async def ciclo_de_vida(_: FastAPI) -> AsyncIterator[None]:
        en_segundo_plano = None
        if configuracion.lector_en_segundo_plano:
            en_segundo_plano = asyncio.create_task(leer_en_segundo_plano(lector, indexador))
        yield
        if en_segundo_plano is not None:
            en_segundo_plano.cancel()
            # Al cancelarlo puede terminar con un error de la base a medio conectar.
            with suppress(asyncio.CancelledError, Exception):
                await en_segundo_plano
        await motor.dispose()

    ajustes = Ajustes(secreto_del_origen=configuracion.sesion_secreto.encode())
    api = crear_api(casos, ajustes, ciclo_de_vida)
    # Las pruebas llaman al lector cuando lo necesitan, en vez de esperar al de segundo plano.
    api.state.lector = lector
    api.state.indexador = indexador
    return api


def _ia(configuracion: Configuracion) -> ProveedorIA | None:
    if configuracion.ia_direccion and configuracion.ia_clave:
        return IAQwen(
            configuracion.ia_direccion,
            configuracion.ia_clave,
            configuracion.ia_modelo_respuestas,
            configuracion.ia_modelo_lectura,
        )
    return None


def _vectores(configuracion: Configuracion) -> Vectorizador:
    if configuracion.ia_direccion and configuracion.ia_clave:
        return VectoresQwen(
            configuracion.ia_direccion,
            configuracion.ia_clave,
            configuracion.ia_modelo_vectores,
            configuracion.ia_dimensiones,
        )
    _registro.warning(
        "Sin IA_DIRECCION o IA_CLAVE: los vectores salen de las palabras, no de un modelo"
    )
    return VectoresDeMentira(configuracion.ia_dimensiones)


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
