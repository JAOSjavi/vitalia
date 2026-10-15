"""Cuentas en PostgreSQL. Lo que ocurre sin sesión llama a las funciones de la base."""

import json
from datetime import date, datetime
from typing import Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from vitalia.adaptadores.postgres.errores import traducir_errores
from vitalia.casos_de_uso.puertos import Credencial, Cuenta, PuntoDelTexto, TextoDeAutorizacion
from vitalia.dominio.cuentas import DatosDelMedico, DatosDelPaciente, Documento, TipoDocumento
from vitalia.dominio.identidad import Identidad, Rol
from vitalia.dominio.ingreso import INACTIVIDAD_MAXIMA, RENOVAR_ACTIVIDAD_CADA, Intentos


class CuentasPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def buscar_credencial(
        self, documento: Documento, resumen_de_la_cuenta: str, origen: str
    ) -> Credencial:
        fila = (
            await self._conexion.execute(
                text("SELECT * FROM buscar_credencial(:tipo, :numero, :cuenta, :origen)"),
                {
                    "tipo": documento.tipo,
                    "numero": documento.numero,
                    "cuenta": resumen_de_la_cuenta,
                    "origen": origen,
                },
            )
        ).one()
        return Credencial(
            usuario_id=fila.usuario_id,
            hash_contrasena=fila.hash_contrasena,
            rol=cast(Rol | None, fila.rol),
            activo=fila.activo,
            intentos=Intentos(fila.fallos or 0, fila.ultimo_fallo, fila.bloqueado_hasta),
            intentos_del_equipo=Intentos(
                fila.fallos_equipo or 0, fila.ultimo_fallo_equipo, fila.equipo_bloqueado_hasta
            ),
        )

    async def guardar_intentos(
        self, resumen_de_la_cuenta: str | None, origen: str, intentos: Intentos
    ) -> None:
        await self._conexion.execute(
            text("SELECT guardar_intentos(:cuenta, :origen, :fallos, :ultimo, :hasta)"),
            {
                "cuenta": resumen_de_la_cuenta,
                "origen": origen,
                "fallos": intentos.fallos,
                "ultimo": intentos.ultimo_fallo,
                "hasta": intentos.bloqueado_hasta,
            },
        )

    async def anotar_sin_sesion(self, usuario_id: UUID | None, accion: str) -> None:
        await self._conexion.execute(
            text("SELECT anotar_sin_sesion(:usuario, :accion)"),
            {"usuario": usuario_id, "accion": accion},
        )

    async def abrir_sesion(
        self, usuario_id: UUID, huella: str, ahora: datetime, vence: datetime
    ) -> None:
        await self._conexion.execute(
            text("SELECT abrir_sesion(:usuario, :huella, :ahora, :vence)"),
            {"usuario": usuario_id, "huella": huella, "ahora": ahora, "vence": vence},
        )

    async def sesion_vigente(self, huella: str, ahora: datetime) -> Identidad | None:
        fila = (
            await self._conexion.execute(
                text(
                    "SELECT usuario_id, rol "
                    "FROM sesion_vigente(:huella, :ahora, :inactividad, :renovar)"
                ),
                {
                    "huella": huella,
                    "ahora": ahora,
                    "inactividad": INACTIVIDAD_MAXIMA,
                    "renovar": RENOVAR_ACTIVIDAD_CADA,
                },
            )
        ).one_or_none()
        if fila is None:
            return None
        return Identidad(cast(Rol, fila.rol), fila.usuario_id)

    async def anular_sesion(self, huella: str, ahora: datetime) -> None:
        await self._conexion.execute(
            text(
                "UPDATE sesiones SET anulada_en = :ahora "
                "WHERE hash_identificador = :huella AND anulada_en IS NULL"
            ),
            {"huella": huella, "ahora": ahora},
        )

    async def texto_vigente(self, tipo: Literal["datos", "ia"]) -> TextoDeAutorizacion:
        fila = (
            await self._conexion.execute(text("SELECT * FROM texto_vigente(:tipo)"), {"tipo": tipo})
        ).one()
        puntos = json.loads(fila.puntos) if isinstance(fila.puntos, str) else fila.puntos
        return TextoDeAutorizacion(
            id=fila.id,
            tipo=tipo,
            version=fila.version,
            puntos=[
                PuntoDelTexto(p["titulo"], p["texto"], p.get("resaltado", False)) for p in puntos
            ],
            contenido=fila.contenido,
            vigente_desde=fila.vigente_desde,
        )

    async def registrar_paciente(
        self,
        datos: DatosDelPaciente,
        hash_contrasena: str,
        texto_datos: UUID,
        texto_ia: UUID | None,
        hoy: date,
    ) -> UUID:
        with traducir_errores():
            usuario_id: UUID = await self._conexion.scalar(
                text(
                    "SELECT registrar_paciente(:tipo, :numero, :nombres, :apellidos, "
                    ":nacimiento, :telefono, :correo, :hash, :texto_datos, :texto_ia, :hoy)"
                ),
                {
                    "tipo": datos.documento.tipo,
                    "numero": datos.documento.numero,
                    "nombres": datos.nombres,
                    "apellidos": datos.apellidos,
                    "nacimiento": datos.fecha_nacimiento,
                    "telefono": datos.telefono,
                    "correo": datos.correo,
                    "hash": hash_contrasena,
                    "texto_datos": texto_datos,
                    "texto_ia": texto_ia,
                    "hoy": hoy,
                },
            )
        return usuario_id

    async def crear_enlace_de_puesta_en_marcha(self, huella: str, vence: datetime) -> None:
        with traducir_errores():
            await self._conexion.execute(
                text("SELECT crear_enlace_puesta_en_marcha(:huella, :vence)"),
                {"huella": huella, "vence": vence},
            )

    async def usar_enlace_de_puesta_en_marcha(
        self, huella: str, ahora: datetime, datos: DatosDelMedico, hash_contrasena: str
    ) -> UUID:
        with traducir_errores():
            usuario_id: UUID = await self._conexion.scalar(
                text(
                    "SELECT usar_enlace_puesta_en_marcha(:huella, :ahora, :tipo, :numero, "
                    ":correo, :hash, :nombres, :apellidos)"
                ),
                {
                    "huella": huella,
                    "ahora": ahora,
                    "tipo": datos.documento.tipo,
                    "numero": datos.documento.numero,
                    "correo": datos.correo,
                    "hash": hash_contrasena,
                    "nombres": datos.nombres,
                    "apellidos": datos.apellidos,
                },
            )
        return usuario_id

    async def cuenta(self, usuario_id: UUID) -> Cuenta:
        fila = (
            await self._conexion.execute(
                text(
                    "SELECT u.id, u.rol, u.tipo_documento, u.numero_documento, u.correo, "
                    "coalesce(p.nombres, m.nombres) AS nombres, "
                    "coalesce(p.apellidos, m.apellidos) AS apellidos "
                    "FROM usuarios u "
                    "LEFT JOIN pacientes p ON p.usuario_id = u.id "
                    "LEFT JOIN medicos m ON m.usuario_id = u.id "
                    "WHERE u.id = :id"
                ),
                {"id": usuario_id},
            )
        ).one()
        return Cuenta(
            usuario_id=fila.id,
            rol=cast(Rol, fila.rol),
            documento=Documento(cast(TipoDocumento, fila.tipo_documento), fila.numero_documento),
            nombres=fila.nombres,
            apellidos=fila.apellidos,
            correo=fila.correo,
        )
