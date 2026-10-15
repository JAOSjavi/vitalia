"""Ingresar con tipo y número de documento y contraseña (HU-004)."""

import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import NoReturn

from vitalia.casos_de_uso.fichas import nueva_ficha
from vitalia.casos_de_uso.puertos import Contrasenas, Credencial, Reloj, UnidadDeTrabajo
from vitalia.dominio.cuentas import Documento, normalizar_documento
from vitalia.dominio.identidad import Rol
from vitalia.dominio.ingreso import (
    FALLOS_PARA_BLOQUEAR_EL_EQUIPO,
    FALLOS_PARA_BLOQUEAR_LA_CUENTA,
    INACTIVIDAD_MAXIMA,
    CredencialesInvalidas,
    IngresoBloqueado,
    Intentos,
)


@dataclass(frozen=True)
class SesionNueva:
    ficha: str
    rol: Rol
    vence: datetime


class Ingresar:
    def __init__(self, unidad: UnidadDeTrabajo, contrasenas: Contrasenas, reloj: Reloj) -> None:
        self._unidad = unidad
        self._contrasenas = contrasenas
        self._reloj = reloj

    async def ejecutar(self, documento: Documento, contrasena: str, origen: str) -> SesionNueva:
        documento = normalizar_documento(documento)
        cuenta = _resumen(documento)
        async with self._unidad.abrir(None) as trabajo:
            credencial = await trabajo.cuentas.buscar_credencial(documento, cuenta, origen)

        ahora = self._reloj.ahora()
        for intentos in (credencial.intentos, credencial.intentos_del_equipo):
            if intentos.bloqueado(ahora) and intentos.bloqueado_hasta is not None:
                raise IngresoBloqueado(intentos.bloqueado_hasta)

        # Fuera de la transacción: comparar la contraseña toma su tiempo a propósito.
        correcta = await self._contrasenas.verificar(contrasena, credencial.hash_contrasena)
        usuario_id, rol = credencial.usuario_id, credencial.rol
        if not correcta or not credencial.activo or usuario_id is None or rol is None:
            await self._anotar_fallo(credencial, cuenta, origen, ahora)

        ficha, huella = nueva_ficha()
        vence = ahora + INACTIVIDAD_MAXIMA
        async with self._unidad.abrir(None) as trabajo:
            # El acierto limpia los fallos de la cuenta, no el tope del equipo.
            await trabajo.cuentas.guardar_intentos(cuenta, origen, Intentos())
            await trabajo.cuentas.abrir_sesion(usuario_id, huella, ahora, vence)
        return SesionNueva(ficha, rol, vence)

    async def _anotar_fallo(
        self, credencial: Credencial, cuenta: str, origen: str, ahora: datetime
    ) -> NoReturn:
        de_la_cuenta = credencial.intentos.con_un_fallo(ahora, FALLOS_PARA_BLOQUEAR_LA_CUENTA)
        del_equipo = credencial.intentos_del_equipo.con_un_fallo(
            ahora, FALLOS_PARA_BLOQUEAR_EL_EQUIPO
        )
        bloqueo = de_la_cuenta.bloqueado_hasta or del_equipo.bloqueado_hasta
        async with self._unidad.abrir(None) as trabajo:
            await trabajo.cuentas.guardar_intentos(cuenta, origen, de_la_cuenta)
            await trabajo.cuentas.guardar_intentos(None, origen, del_equipo)
            if credencial.usuario_id is not None:
                accion = "ingreso_bloqueado" if bloqueo else "ingreso_fallido"
                await trabajo.cuentas.anotar_sin_sesion(credencial.usuario_id, accion)
        if bloqueo is not None:
            raise IngresoBloqueado(bloqueo)
        raise CredencialesInvalidas()


def _resumen(documento: Documento) -> str:
    """Clave de los intentos: igual para una cuenta que existe y para una que no."""
    return hashlib.sha256(f"{documento.tipo}:{documento.numero}".encode()).hexdigest()
