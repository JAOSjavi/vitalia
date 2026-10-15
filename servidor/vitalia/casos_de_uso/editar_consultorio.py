"""El médico registra los datos del consultorio, su nombre y su registro (HU-001, CA-2)."""

from dataclasses import replace

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import DatosDelConsultorio, UnidadDeTrabajo
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.identidad import Identidad


class EditarConsultorio:
    def __init__(self, unidad: UnidadDeTrabajo, autorizador: Autorizador) -> None:
        self._unidad = unidad
        self._autorizador = autorizador

    async def ejecutar(self, identidad: Identidad, datos: DatosDelConsultorio) -> None:
        await self._autorizador.exigir(identidad, "consultorio.editar")
        assert identidad.usuario_id is not None
        datos = _sin_espacios(datos)
        campos = {}
        if not datos.nombre:
            campos["nombre"] = "Escriba el nombre del consultorio"
        if not datos.medico_nombres:
            campos["medico_nombres"] = "Escriba sus nombres"
        if not datos.medico_apellidos:
            campos["medico_apellidos"] = "Escriba sus apellidos"
        if campos:
            raise DatosInvalidos(campos)
        async with self._unidad.abrir(identidad) as trabajo:
            await trabajo.consultorios.guardar(identidad.usuario_id, datos)
            await trabajo.bitacora.registrar("edicion_del_consultorio")


def _sin_espacios(datos: DatosDelConsultorio) -> DatosDelConsultorio:
    def limpio(valor: str | None) -> str | None:
        return (valor or "").strip() or None

    return replace(
        datos,
        nombre=limpio(datos.nombre),
        direccion=limpio(datos.direccion),
        telefono=limpio(datos.telefono),
        correo=limpio(datos.correo),
        medico_nombres=datos.medico_nombres.strip(),
        medico_apellidos=datos.medico_apellidos.strip(),
        registro_profesional=limpio(datos.registro_profesional),
    )
