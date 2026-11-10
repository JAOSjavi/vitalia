"""El médico pide que la atención se complete con los documentos del paciente (HU-047, D-36).

Es el mismo camino del asistente, con otra salida. Primero las comprobaciones de siempre, antes
de llamar al proveedor: rol, atención abierta, autorización de IA, documentos leídos y tope por
hora. Después se buscan los fragmentos: si todo el texto del paciente cabe, va todo; si no, una
búsqueda por campo. El modelo devuelve JSON y solo quedan los campos con una frase comprobada.
Nada se guarda aquí: el médico decide en la pantalla qué usa.
"""

import asyncio
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.buscar_fragmentos import POR_METODO, TOTAL
from vitalia.casos_de_uso.preguntar_al_asistente import ACCION as PREGUNTA_AL_ASISTENTE
from vitalia.casos_de_uso.preguntar_al_asistente import Limites
from vitalia.casos_de_uso.puertos import (
    FragmentoEncontrado,
    ProveedorIA,
    ProveedorNoDisponible,
    Reloj,
    UnidadDeTrabajo,
    Vectorizador,
)
from vitalia.dominio.asistente import (
    AVISO,
    Consultado,
    FragmentoParaContexto,
    SinFragmentos,
    TopeDeConsultas,
    armar_contexto,
    etiquetas_por_orden_de_subida,
    lo_consultado,
)
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.fragmentos import IANoAutorizada
from vitalia.dominio.historia_clinica import AtencionCerrada
from vitalia.dominio.identidad import Identidad
from vitalia.dominio.sugerencias import (
    CONSULTAS,
    INSTRUCCIONES,
    RespuestaIlegible,
    Sugerencia,
    leer_sugerencias,
)

ACCION = "sugerencias_para_la_historia"


@dataclass(frozen=True)
class Sugerencias:
    sugerencias: list[Sugerencia]
    consultado: list[Consultado]
    aviso: str = AVISO


class SugerirCampos:
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

    async def ejecutar(self, identidad: Identidad, atencion_id: UUID) -> Sugerencias:
        await self._autorizador.exigir(identidad, "atenciones.registrar")
        await self._autorizador.exigir(identidad, "asistente.preguntar")

        hace_una_hora = self._reloj.ahora() - timedelta(hours=1)
        async with self._unidad.abrir(identidad) as trabajo:
            atencion = await trabajo.historia.atencion(atencion_id)
            if atencion is None:
                raise NoEncontrado()
            if atencion.estado == "cerrada":
                raise AtencionCerrada()
            paciente_id = atencion.paciente_id
            if not await trabajo.documentos.ia_autorizada(paciente_id):
                raise IANoAutorizada()
            caracteres = await trabajo.fragmentos.caracteres(paciente_id)
            if caracteres == 0:
                raise SinFragmentos()
            # Las sugerencias cuentan para el mismo tope del asistente: van al mismo proveedor.
            hechas = await trabajo.bitacora.contar(
                PREGUNTA_AL_ASISTENTE, hace_una_hora
            ) + await trabajo.bitacora.contar(ACCION, hace_una_hora)
            if hechas >= self._limites.consultas_por_hora:
                raise TopeDeConsultas(self._limites.consultas_por_hora)
            todos = (
                await trabajo.fragmentos.todos(paciente_id)
                if caracteres <= self._limites.tope_contexto
                else None
            )
            documentos = await trabajo.documentos.listar_de(paciente_id)

        encontrados = todos if todos is not None else await self._buscar(identidad, paciente_id)
        contexto = armar_contexto(
            [_para_contexto(f) for f in encontrados],
            etiquetas_por_orden_de_subida([d.id for d in documentos]),
        )
        async with self._unidad.abrir(identidad) as trabajo:
            # Quién pidió, sobre quién y cuándo. Nunca lo enviado ni lo devuelto.
            await trabajo.bitacora.registrar(
                ACCION,
                paciente_id=paciente_id,
                objeto=str(atencion_id),
                detalle={"fragmentos": len(encontrados), "documentos": len(contexto.etiquetas)},
            )

        try:
            async with asyncio.timeout(self._limites.segundos_de_espera):
                respuesta = await self._ia.responder_en_json(
                    INSTRUCCIONES, f"Fragmentos del paciente:\n\n{contexto.texto}"
                )
            sugerencias = leer_sugerencias(respuesta, contexto)
        except TimeoutError as error:
            raise ProveedorNoDisponible() from error
        except RespuestaIlegible as error:
            raise ProveedorNoDisponible("respuesta_ilegible") from error
        return Sugerencias(sugerencias, lo_consultado(contexto))

    async def _buscar(self, identidad: Identidad, paciente_id: UUID) -> list[FragmentoEncontrado]:
        """Una búsqueda por campo; se reparten el tope de texto por turnos, el mejor de cada uno."""
        consultas = list(CONSULTAS.values())
        vectores = await self._vectores.vectorizar(consultas)
        async with self._unidad.abrir(identidad) as trabajo:
            resultados = [
                await trabajo.fragmentos.buscar(paciente_id, vector, consulta, POR_METODO, TOTAL)
                for consulta, vector in zip(consultas, vectores, strict=True)
            ]
        return _repartir(resultados, self._limites.tope_contexto)


def _repartir(
    resultados: Sequence[Sequence[FragmentoEncontrado]], tope: int
) -> list[FragmentoEncontrado]:
    # Por turnos: el primero de cada campo, luego el segundo... Así ningún campo se queda sin
    # fragmentos porque otro llenó el tope.
    enviados: list[FragmentoEncontrado] = []
    vistos: set[UUID] = set()
    usados = 0
    for puesto in range(max((len(r) for r in resultados), default=0)):
        for resultado in resultados:
            if puesto >= len(resultado) or resultado[puesto].id in vistos:
                continue
            fragmento = resultado[puesto]
            if usados + len(fragmento.texto) > tope and enviados:
                return enviados
            enviados.append(fragmento)
            vistos.add(fragmento.id)
            usados += len(fragmento.texto)
    return enviados


def _para_contexto(fragmento: FragmentoEncontrado) -> FragmentoParaContexto:
    return FragmentoParaContexto(
        fragmento.documento_id,
        fragmento.documento,
        fragmento.fecha_documento,
        fragmento.pagina,
        fragmento.texto,
    )
