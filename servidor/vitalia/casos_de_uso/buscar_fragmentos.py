"""El médico busca en los documentos de un paciente los fragmentos que responden una pregunta.

Es el primer paso de cada pregunta al asistente (diseno/04-asistente-ia.md, sección 5.1): la
pregunta se limpia de identificadores, se vectoriza y se busca por significado y por palabras,
siempre dentro de un solo paciente. La bitácora anota quién buscó sobre quién, sin la pregunta.
"""

from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import FragmentoEncontrado, UnidadDeTrabajo, Vectorizador
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.fragmentos import IANoAutorizada, retirar_identificadores
from vitalia.dominio.identidad import Identidad

# Punto de partida del diseño; se ajustan con el conjunto de prueba.
POR_METODO = 20
TOTAL = 12
LARGO_MAXIMO_DE_LA_PREGUNTA = 1000


class BuscarFragmentos:
    def __init__(
        self, unidad: UnidadDeTrabajo, autorizador: Autorizador, vectores: Vectorizador
    ) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._vectores = vectores

    async def ejecutar(
        self,
        identidad: Identidad,
        paciente_id: UUID,
        pregunta: str,
        por_metodo: int = POR_METODO,
        total: int = TOTAL,
    ) -> list[FragmentoEncontrado]:
        await self._autorizador.exigir(identidad, "asistente.preguntar")
        pregunta = pregunta.strip()
        if not pregunta:
            raise DatosInvalidos({"pregunta": "Escriba la pregunta"})
        if len(pregunta) > LARGO_MAXIMO_DE_LA_PREGUNTA:
            raise DatosInvalidos({"pregunta": "La pregunta es demasiado larga"})

        async with self._unidad.abrir(identidad) as trabajo:
            paciente = await trabajo.fragmentos.identificadores(paciente_id)
            if not await trabajo.documentos.ia_autorizada(paciente_id):
                raise IANoAutorizada()

        limpia = retirar_identificadores(pregunta, paciente)
        [vector] = await self._vectores.vectorizar([limpia])

        async with self._unidad.abrir(identidad) as trabajo:
            encontrados = await trabajo.fragmentos.buscar(
                paciente_id, vector, limpia, por_metodo, total
            )
            await trabajo.bitacora.registrar(
                "busqueda_del_asistente",
                paciente_id=paciente_id,
                detalle={"fragmentos": len(encontrados)},
            )
        return encontrados
