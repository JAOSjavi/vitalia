"""El médico le pregunta al asistente sobre los documentos de un paciente (HU-034, HU-033).

Dos tiempos. Preparar hace todas las comprobaciones antes de llamar al proveedor, en el orden de
diseno/03-api.md: rol, autorización de IA, que haya fragmentos y el tope por hora. Si algo falla,
el proveedor no se llama. Después, responder entrega el texto a medida que el modelo lo escribe
y, al final, las citas comprobadas y la lista de lo consultado.
"""

import asyncio
from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.buscar_fragmentos import POR_METODO, TOTAL
from vitalia.casos_de_uso.puertos import (
    FragmentoEncontrado,
    ProveedorIA,
    ProveedorNoDisponible,
    Reloj,
    Turno,
    UnidadDeTrabajo,
    Vectorizador,
)
from vitalia.dominio.asistente import (
    AVISO,
    INSTRUCCIONES,
    Consultado,
    Contexto,
    FragmentoParaContexto,
    OrigenComprobado,
    SinFragmentos,
    TopeDeConsultas,
    armar_contexto,
    comprobar_origenes,
    lo_consultado,
)
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.fragmentos import IANoAutorizada, Identificadores, retirar_identificadores
from vitalia.dominio.identidad import Identidad

LARGO_MAXIMO_DE_LA_PREGUNTA = 1000
TURNOS_MAXIMOS = 20
LARGO_MAXIMO_DE_UN_TURNO = 6000
ACCION = "pregunta_al_asistente"


@dataclass(frozen=True)
class Limites:
    # Máximo de texto de los fragmentos en una consulta, en caracteres (IA_TOPE_CONTEXTO).
    tope_contexto: int = 16000
    consultas_por_hora: int = 30
    segundos_de_espera: float = 60


@dataclass(frozen=True)
class PreguntaLista:
    """Lo que se le va a enviar al modelo, ya comprobado y sin identificadores."""

    instrucciones: str
    turnos: tuple[Turno, ...]
    contexto: Contexto


@dataclass(frozen=True)
class Cierre:
    origenes: list[OrigenComprobado]
    consultado: list[Consultado]
    aviso: str = AVISO


class PreguntarAlAsistente:
    def __init__(
        self,
        unidad: UnidadDeTrabajo,
        autorizador: Autorizador,
        vectores: Vectorizador,
        ia: ProveedorIA,
        reloj: Reloj,
        limites: Limites | None = None,
    ) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._vectores = vectores
        self._ia = ia
        self._reloj = reloj
        self._limites = limites or Limites()

    async def preparar(
        self,
        identidad: Identidad,
        paciente_id: UUID,
        pregunta: str,
        conversacion: Sequence[Turno] = (),
    ) -> PreguntaLista:
        await self._autorizador.exigir(identidad, "asistente.preguntar")
        pregunta = pregunta.strip()
        _revisar(pregunta, conversacion)

        hace_una_hora = self._reloj.ahora() - timedelta(hours=1)
        async with self._unidad.abrir(identidad) as trabajo:
            paciente = await trabajo.fragmentos.identificadores(paciente_id)
            if not await trabajo.documentos.ia_autorizada(paciente_id):
                raise IANoAutorizada()
            caracteres = await trabajo.fragmentos.caracteres(paciente_id)
            if caracteres == 0:
                raise SinFragmentos()
            hechas = await trabajo.bitacora.contar(ACCION, hace_una_hora)
            if hechas >= self._limites.consultas_por_hora:
                raise TopeDeConsultas(self._limites.consultas_por_hora)
            # Paciente pequeño: si todo cabe, va todo y una búsqueda fallida no deja nada afuera.
            todos = (
                await trabajo.fragmentos.todos(paciente_id)
                if caracteres <= self._limites.tope_contexto
                else None
            )

        turnos = _limpios(conversacion, paciente)
        limpia = retirar_identificadores(pregunta, paciente)
        if todos is None:
            encontrados = await self._buscar(identidad, paciente_id, limpia, turnos)
        else:
            encontrados = todos

        contexto = armar_contexto([_para_contexto(f) for f in encontrados])
        async with self._unidad.abrir(identidad) as trabajo:
            # Quién preguntó, sobre quién y cuándo. Nunca la pregunta ni la respuesta.
            await trabajo.bitacora.registrar(
                ACCION,
                paciente_id=paciente_id,
                detalle={"fragmentos": len(encontrados), "documentos": len(contexto.etiquetas)},
            )
        return PreguntaLista(
            instrucciones=f"{INSTRUCCIONES}\n\nFragmentos del paciente:\n\n{contexto.texto}",
            turnos=(*turnos, Turno("medico", limpia)),
            contexto=contexto,
        )

    async def responder(self, lista: PreguntaLista) -> AsyncIterator[str | Cierre]:
        """Entrega el texto por partes y, al final, un Cierre con las citas comprobadas."""
        partes: list[str] = []
        try:
            async with asyncio.timeout(self._limites.segundos_de_espera):
                async for parte in self._ia.responder(lista.instrucciones, lista.turnos):
                    partes.append(parte)
                    yield parte
        except TimeoutError as error:
            raise ProveedorNoDisponible() from error
        respuesta = "".join(partes)
        yield Cierre(comprobar_origenes(respuesta, lista.contexto), lo_consultado(lista.contexto))

    async def _buscar(
        self, identidad: Identidad, paciente_id: UUID, pregunta: str, turnos: Sequence[Turno]
    ) -> list[FragmentoEncontrado]:
        # "¿Y la dosis?" no se entiende sola: se busca con la pregunta anterior del médico.
        anterior = next((t.texto for t in reversed(turnos) if t.autor == "medico"), "")
        consulta = f"{anterior}\n{pregunta}".strip()
        [vector] = await self._vectores.vectorizar([consulta])
        async with self._unidad.abrir(identidad) as trabajo:
            encontrados = await trabajo.fragmentos.buscar(
                paciente_id, vector, consulta, POR_METODO, TOTAL
            )
        # Del más al menos parecido, hasta llenar el tope de texto.
        enviados: list[FragmentoEncontrado] = []
        usados = 0
        for fragmento in encontrados:
            if usados + len(fragmento.texto) > self._limites.tope_contexto and enviados:
                break
            enviados.append(fragmento)
            usados += len(fragmento.texto)
        return enviados


def _revisar(pregunta: str, conversacion: Sequence[Turno]) -> None:
    if not pregunta:
        raise DatosInvalidos({"pregunta": "Escriba la pregunta"})
    if len(pregunta) > LARGO_MAXIMO_DE_LA_PREGUNTA:
        raise DatosInvalidos({"pregunta": "La pregunta es demasiado larga"})
    if len(conversacion) > TURNOS_MAXIMOS or any(
        len(t.texto) > LARGO_MAXIMO_DE_UN_TURNO for t in conversacion
    ):
        raise DatosInvalidos({"conversacion": "La conversación es demasiado larga"})


def _limpios(conversacion: Sequence[Turno], paciente: Identificadores) -> list[Turno]:
    """La conversación la manda la pantalla: también se limpia antes de enviarla."""
    return [Turno(t.autor, retirar_identificadores(t.texto, paciente)) for t in conversacion]


def _para_contexto(fragmento: FragmentoEncontrado) -> FragmentoParaContexto:
    return FragmentoParaContexto(
        fragmento.documento_id,
        fragmento.documento,
        fragmento.fecha_documento,
        fragmento.pagina,
        fragmento.texto,
    )
