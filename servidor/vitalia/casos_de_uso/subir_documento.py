"""El paciente sube un documento suyo (HU-028). La lectura sigue después, por la cola (HU-031)."""

from uuid import uuid4

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import Archivos, DocumentoSubido, Reloj, UnidadDeTrabajo
from vitalia.dominio.agenda import dia_en_colombia
from vitalia.dominio.documentos import ArchivoRecibido, DocumentoRepetido, validar_archivo
from vitalia.dominio.identidad import Identidad


class SubirDocumento:
    def __init__(
        self, unidad: UnidadDeTrabajo, autorizador: Autorizador, archivos: Archivos, reloj: Reloj
    ) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._archivos = archivos
        self._reloj = reloj

    async def ejecutar(self, identidad: Identidad, recibido: ArchivoRecibido) -> DocumentoSubido:
        await self._autorizador.exigir(identidad, "documentos.subir")
        archivo = validar_archivo(recibido, dia_en_colombia(self._reloj.ahora()))

        async with self._unidad.abrir(identidad) as trabajo:
            repetido = await trabajo.documentos.por_huella(archivo.huella)
        if repetido is not None:
            raise DocumentoRepetido(repetido)

        # La clave no dice de quién es el archivo ni qué contiene.
        clave = f"documentos/{uuid4()}.{archivo.formato}"
        await self._archivos.guardar(clave, archivo.contenido)
        try:
            async with self._unidad.abrir(identidad) as trabajo:
                documento = await trabajo.documentos.crear(archivo, clave)
                await trabajo.documentos.encolar(documento.id, "leer")
                await trabajo.bitacora.registrar("documento_subido", objeto=str(documento.id))
        except BaseException:
            # Sin fila en la base, el archivo no le sirve a nadie: no se deja a medias (CA-5).
            await self._archivos.borrar(clave)
            raise
        return documento
