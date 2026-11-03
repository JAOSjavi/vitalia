"""Historia clínica del consultorio: atender, registrar, cerrar y consultar (HU-041 a HU-045).

Una atención abierta es el borrador: se guarda por partes mientras el médico escribe. Al cerrarla
el médico confirma su contraseña, queda firmada con su nombre, su registro y la hora, y ya no
cambia. El paciente ve sus atenciones cerradas.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from vitalia.casos_de_uso.autorizar import Autorizador
from vitalia.casos_de_uso.puertos import (
    AtencionGuardada,
    Contrasenas,
    NotaAclaratoria,
    Reloj,
    Trabajo,
    UnidadDeTrabajo,
)
from vitalia.dominio.cuentas import DatosInvalidos
from vitalia.dominio.errores import NoEncontrado
from vitalia.dominio.historia_clinica import (
    ANTECEDENTES,
    CAMPOS_DE_IDENTIFICACION,
    CAMPOS_DE_LA_ATENCION,
    AtencionCerrada,
    AtencionYaAbierta,
    ContrasenaIncorrecta,
    FaltanDatos,
    Faltantes,
    Valor,
    faltantes,
    indice_de_masa_corporal,
    revisar,
    revisar_diagnosticos,
    revisar_medicamentos,
)
from vitalia.dominio.identidad import Identidad

LARGO_MAXIMO_DE_LA_NOTA = 4000
RESULTADOS_CIE10 = 20


@dataclass(frozen=True)
class VistaDeAtencion:
    atencion: AtencionGuardada
    notas: list[NotaAclaratoria]
    imc: Decimal | None


@dataclass(frozen=True)
class AtencionParaEscribir:
    """Lo que necesita la pantalla de atención (M-15)."""

    vista: VistaDeAtencion
    identificacion: dict[str, Valor]
    faltantes: Faltantes


class Atenciones:
    def __init__(
        self,
        unidad: UnidadDeTrabajo,
        autorizador: Autorizador,
        contrasenas: Contrasenas,
        reloj: Reloj,
    ) -> None:
        self._unidad = unidad
        self._autorizador = autorizador
        self._contrasenas = contrasenas
        self._reloj = reloj

    async def abrir(
        self, identidad: Identidad, paciente_id: UUID, cita_id: UUID | None = None
    ) -> UUID:
        """Desde una cita o desde la ficha. Si ya hay una abierta, se sigue en esa (HU-042, CA-6).

        Los antecedentes de la última atención cerrada llegan para confirmarlos (HU-043, CA-5).
        """
        await self._autorizador.exigir(identidad, "atenciones.registrar")
        assert identidad.usuario_id is not None
        async with self._unidad.abrir(identidad) as trabajo:
            if not await trabajo.pacientes.existe(paciente_id):
                raise NoEncontrado()
            abierta = await trabajo.historia.abierta_de(paciente_id)
            if abierta is not None:
                return abierta
            if cita_id is not None:
                cita = await trabajo.agenda.cita(cita_id)
                if cita is None or cita.paciente_id != paciente_id:
                    raise DatosInvalidos({"cita_id": "Esa cita no es de este paciente"})
            anteriores = await trabajo.historia.de_paciente(paciente_id)
            ultima = next((a for a in anteriores if a.estado == "cerrada"), None)
            antecedentes = {c: ultima.datos[c] for c in ANTECEDENTES} if ultima else {}
            try:
                atencion_id = await trabajo.historia.abrir(
                    paciente_id, identidad.usuario_id, cita_id, antecedentes
                )
            except AtencionYaAbierta:
                # Otra pestaña la abrió al mismo tiempo: se usa esa.
                abierta = await trabajo.historia.abierta_de(paciente_id)
                assert abierta is not None
                return abierta
            await trabajo.bitacora.registrar(
                "apertura_de_atencion", paciente_id=paciente_id, objeto=str(atencion_id)
            )
        return atencion_id

    async def para_escribir(self, identidad: Identidad, atencion_id: UUID) -> AtencionParaEscribir:
        await self._autorizador.exigir(identidad, "atenciones.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            atencion = await self._atencion(trabajo, atencion_id)
            identificacion = await trabajo.historia.identificacion(atencion.paciente_id) or {}
            notas = await trabajo.historia.notas([atencion.id])
            if atencion.estado == "cerrada":
                await trabajo.bitacora.registrar(
                    "consulta_de_historia",
                    paciente_id=atencion.paciente_id,
                    objeto=str(atencion.id),
                )
        return AtencionParaEscribir(
            _vista(atencion, notas),
            identificacion,
            faltantes(atencion.datos, atencion.diagnosticos, identificacion),
        )

    async def guardar(
        self,
        identidad: Identidad,
        atencion_id: UUID,
        cambios: Mapping[str, object],
        diagnosticos: Sequence[Mapping[str, object]] | None = None,
        medicamentos: Sequence[Mapping[str, object]] | None = None,
    ) -> datetime:
        """Guarda el borrador con lo que cambió. Devuelve la hora en que quedó guardado (CA-5)."""
        await self._autorizador.exigir(identidad, "atenciones.registrar")
        datos = revisar(cambios, CAMPOS_DE_LA_ATENCION)
        revisados_med = None if medicamentos is None else revisar_medicamentos(medicamentos)
        ahora = self._reloj.ahora()
        async with self._unidad.abrir(identidad) as trabajo:
            atencion = await self._atencion(trabajo, atencion_id)
            if atencion.estado == "cerrada":
                raise AtencionCerrada()
            revisados_dx = None
            if diagnosticos is not None:
                codigos = [str(d.get("codigo") or "").strip().upper() for d in diagnosticos]
                nombres = await trabajo.historia.nombres_cie10(codigos)
                revisados_dx = revisar_diagnosticos(diagnosticos, nombres)
            await trabajo.historia.guardar(atencion_id, datos, revisados_dx, revisados_med, ahora)
        return ahora

    async def guardar_identificacion(
        self, identidad: Identidad, paciente_id: UUID, cambios: Mapping[str, object]
    ) -> None:
        """Los datos que el registro no pide; se completan una vez (HU-041, CA-1 y CA-2)."""
        await self._autorizador.exigir(identidad, "pacientes.identificacion")
        datos = revisar(cambios, CAMPOS_DE_IDENTIFICACION)
        async with self._unidad.abrir(identidad) as trabajo:
            if not await trabajo.pacientes.existe(paciente_id):
                raise NoEncontrado()
            await trabajo.historia.guardar_identificacion(paciente_id, datos)
            await trabajo.bitacora.registrar(
                "identificacion_del_paciente",
                paciente_id=paciente_id,
                detalle={"campos": list(datos)},
            )

    async def cerrar(self, identidad: Identidad, atencion_id: UUID, contrasena: str) -> datetime:
        """Revisa la contraseña, la identificación y la consulta, en ese orden (diseno/03-api.md).

        Si falta algo no cierra y dice qué. Al cerrar, la cita queda como atendida.
        """
        await self._autorizador.exigir(identidad, "atenciones.registrar")
        assert identidad.usuario_id is not None
        async with self._unidad.abrir(identidad) as trabajo:
            firma, hash_contrasena = await trabajo.historia.firma_del_medico()
        if not await self._contrasenas.verificar(contrasena, hash_contrasena):
            async with self._unidad.abrir(identidad) as trabajo:
                await trabajo.bitacora.registrar("firma_rechazada", objeto=str(atencion_id))
            raise ContrasenaIncorrecta()

        fin = self._reloj.ahora()
        async with self._unidad.abrir(identidad) as trabajo:
            atencion = await self._atencion(trabajo, atencion_id)
            if atencion.estado == "cerrada":
                raise AtencionCerrada()
            identificacion = await trabajo.historia.identificacion(atencion.paciente_id) or {}
            pendientes = faltantes(atencion.datos, atencion.diagnosticos, identificacion)
            if pendientes:
                raise FaltanDatos(pendientes)
            await trabajo.historia.cerrar(atencion_id, fin, firma)
            if atencion.cita_id is not None:
                cita = await trabajo.agenda.cita(atencion.cita_id)
                if cita is not None and cita.estado == "confirmada":
                    await trabajo.agenda.marcar_asistencia(cita.id, "atendida")
                    await trabajo.agenda.anotar_cambio(cita.id, identidad.usuario_id, "asistencia")
            await trabajo.bitacora.registrar(
                "cierre_de_atencion", paciente_id=atencion.paciente_id, objeto=str(atencion_id)
            )
        return fin

    async def agregar_nota(self, identidad: Identidad, atencion_id: UUID, texto: str) -> None:
        """La única forma de corregir una atención cerrada (Resolución 1995, art. 18)."""
        await self._autorizador.exigir(identidad, "atenciones.registrar")
        assert identidad.usuario_id is not None
        texto = texto.strip()
        if not texto or len(texto) > LARGO_MAXIMO_DE_LA_NOTA:
            raise DatosInvalidos(
                {"texto": f"Escriba la nota, hasta {LARGO_MAXIMO_DE_LA_NOTA} caracteres"}
            )
        async with self._unidad.abrir(identidad) as trabajo:
            atencion = await self._atencion(trabajo, atencion_id)
            if atencion.estado != "cerrada":
                raise DatosInvalidos({"texto": "Mientras está abierta, corríjala directamente"})
            firma, _ = await trabajo.historia.firma_del_medico()
            await trabajo.historia.agregar_nota(atencion_id, identidad.usuario_id, texto, firma)
            await trabajo.bitacora.registrar(
                "nota_aclaratoria", paciente_id=atencion.paciente_id, objeto=str(atencion_id)
            )

    async def historia_del_paciente(
        self, identidad: Identidad, paciente_id: UUID
    ) -> list[VistaDeAtencion]:
        """Las atenciones en orden, la abierta incluida, con sus notas (HU-045)."""
        await self._autorizador.exigir(identidad, "atenciones.ver")
        async with self._unidad.abrir(identidad) as trabajo:
            if not await trabajo.pacientes.existe(paciente_id):
                raise NoEncontrado()
            vistas = await _con_notas(trabajo, await trabajo.historia.de_paciente(paciente_id))
            await trabajo.bitacora.registrar("consulta_de_historia", paciente_id=paciente_id)
        return vistas

    async def mi_historia(self, identidad: Identidad) -> list[VistaDeAtencion]:
        """El paciente ve sus atenciones cerradas; la base no le entrega las abiertas."""
        await self._autorizador.exigir(identidad, "historia.propia")
        async with self._unidad.abrir(identidad) as trabajo:
            paciente_id = await trabajo.agenda.paciente_de_la_sesion()
            if paciente_id is None:
                raise NoEncontrado()
            vistas = await _con_notas(trabajo, await trabajo.historia.de_paciente(paciente_id))
            await trabajo.bitacora.registrar("consulta_de_historia", paciente_id=paciente_id)
        return vistas

    async def buscar_cie10(self, identidad: Identidad, texto: str) -> list[tuple[str, str]]:
        await self._autorizador.exigir(identidad, "atenciones.registrar")
        texto = texto.strip()
        if len(texto) < 2:
            return []
        async with self._unidad.abrir(identidad) as trabajo:
            return await trabajo.historia.buscar_cie10(texto[:60], RESULTADOS_CIE10)

    @staticmethod
    async def _atencion(trabajo: Trabajo, atencion_id: UUID) -> AtencionGuardada:
        atencion = await trabajo.historia.atencion(atencion_id)
        if atencion is None:
            raise NoEncontrado()
        return atencion


def _vista(atencion: AtencionGuardada, notas: list[NotaAclaratoria]) -> VistaDeAtencion:
    peso = atencion.datos.get("peso")
    talla = atencion.datos.get("talla")
    return VistaDeAtencion(
        atencion,
        notas,
        indice_de_masa_corporal(
            peso if isinstance(peso, Decimal) else None, talla if isinstance(talla, int) else None
        ),
    )


async def _con_notas(trabajo: Trabajo, atenciones: list[AtencionGuardada]) -> list[VistaDeAtencion]:
    notas = await trabajo.historia.notas([a.id for a in atenciones])
    return [_vista(a, [n for n in notas if n.atencion_id == a.id]) for a in atenciones]
