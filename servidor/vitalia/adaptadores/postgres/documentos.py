"""Documentos del paciente, sus páginas leídas y la cola del lector en PostgreSQL."""

from collections.abc import Sequence
from typing import Any, Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from vitalia.adaptadores.postgres.errores import traducir_errores
from vitalia.casos_de_uso.puertos import (
    DocumentoParaAbrir,
    DocumentoPorLeer,
    DocumentoSubido,
    PaginaLeida,
    TipoDeTrabajo,
    TrabajoDeLectura,
)
from vitalia.dominio.documentos import ArchivoValido, EstadoDeLectura, Formato, TipoDeDocumento

_COLUMNAS = "id, nombre, fecha_documento, tipo, formato, tamano, estado_lectura, paginas, subido_en"


def _documento(fila: Any) -> DocumentoSubido:
    return DocumentoSubido(
        id=fila.id,
        nombre=fila.nombre,
        fecha_documento=fila.fecha_documento,
        tipo=cast(TipoDeDocumento, fila.tipo),
        formato=cast(Formato, fila.formato),
        tamano=fila.tamano,
        estado_lectura=cast(EstadoDeLectura, fila.estado_lectura),
        paginas=fila.paginas,
        subido_en=fila.subido_en,
    )


class DocumentosPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def por_huella(self, huella: str) -> UUID | None:
        resultado: UUID | None = await self._conexion.scalar(
            text("SELECT id FROM documentos WHERE paciente_id = paciente_actual() AND huella = :h"),
            {"h": huella},
        )
        return resultado

    async def crear(self, archivo: ArchivoValido, clave_archivo: str) -> DocumentoSubido:
        with traducir_errores():
            fila = (
                await self._conexion.execute(
                    text(
                        "INSERT INTO documentos (paciente_id, nombre, fecha_documento, tipo, "
                        "formato, tamano, huella, clave_archivo, estado_lectura) VALUES "
                        "(paciente_actual(), :nombre, :fecha, :tipo, :formato, :tamano, "
                        f":huella, :clave, 'en_proceso') RETURNING {_COLUMNAS}"
                    ),
                    {
                        "nombre": archivo.nombre,
                        "fecha": archivo.fecha_documento,
                        "tipo": archivo.tipo,
                        "formato": archivo.formato,
                        "tamano": len(archivo.contenido),
                        "huella": archivo.huella,
                        "clave": clave_archivo,
                    },
                )
            ).one()
        return _documento(fila)

    async def listar(self) -> list[DocumentoSubido]:
        filas = await self._conexion.execute(
            text(
                f"SELECT {_COLUMNAS} FROM documentos WHERE paciente_id = paciente_actual() "
                "ORDER BY fecha_documento DESC, subido_en DESC"
            )
        )
        return [_documento(f) for f in filas]

    async def listar_de(self, paciente_id: UUID) -> list[DocumentoSubido]:
        filas = await self._conexion.execute(
            text(
                f"SELECT {_COLUMNAS} FROM documentos WHERE paciente_id = :p "
                "ORDER BY fecha_documento DESC, subido_en DESC"
            ),
            {"p": paciente_id},
        )
        return [_documento(f) for f in filas]

    async def encolar(self, documento_id: UUID, tipo: TipoDeTrabajo) -> None:
        await self._conexion.execute(
            text("INSERT INTO trabajos_lectura (tipo, documento_id) VALUES (:tipo, :documento)"),
            {"tipo": tipo, "documento": documento_id},
        )

    async def para_abrir(self, documento_id: UUID) -> DocumentoParaAbrir | None:
        fila = (
            await self._conexion.execute(
                text(
                    "SELECT id, paciente_id, nombre, formato, clave_archivo FROM documentos "
                    "WHERE id = :id"
                ),
                {"id": documento_id},
            )
        ).one_or_none()
        if fila is None:
            return None
        return DocumentoParaAbrir(
            fila.id, fila.paciente_id, fila.nombre, cast(Formato, fila.formato), fila.clave_archivo
        )

    async def eliminar(self, documento_id: UUID) -> str | None:
        clave: str | None = await self._conexion.scalar(
            text("DELETE FROM documentos WHERE id = :id RETURNING clave_archivo"),
            {"id": documento_id},
        )
        return clave

    async def tomar_trabajo(self, tipo: TipoDeTrabajo) -> TrabajoDeLectura | None:
        # SKIP LOCKED: si hay otro lector, cada uno toma un trabajo distinto sin esperar.
        fila = (
            await self._conexion.execute(
                text(
                    "UPDATE trabajos_lectura SET estado = 'en_curso', intentos = intentos + 1 "
                    "WHERE id = (SELECT id FROM trabajos_lectura "
                    "WHERE estado = 'pendiente' AND tipo = :tipo "
                    "ORDER BY creado_en LIMIT 1 FOR UPDATE SKIP LOCKED) "
                    "RETURNING id, documento_id, intentos"
                ),
                {"tipo": tipo},
            )
        ).one_or_none()
        if fila is None:
            return None
        return TrabajoDeLectura(fila.id, fila.documento_id, fila.intentos)

    async def terminar_trabajo(
        self, trabajo_id: UUID, *, error: str | None = None, reintentar: bool = False
    ) -> None:
        estado = "hecho" if error is None else ("pendiente" if reintentar else "fallido")
        await self._conexion.execute(
            text("UPDATE trabajos_lectura SET estado = :estado, error = :error WHERE id = :id"),
            {"estado": estado, "error": error, "id": trabajo_id},
        )

    async def por_leer(self, documento_id: UUID) -> DocumentoPorLeer:
        fila = (
            await self._conexion.execute(
                text(
                    "SELECT id, paciente_id, formato, clave_archivo FROM documentos WHERE id = :id"
                ),
                {"id": documento_id},
            )
        ).one()
        return DocumentoPorLeer(
            fila.id, fila.paciente_id, cast(Formato, fila.formato), fila.clave_archivo
        )

    async def ia_autorizada(self, paciente_id: UUID) -> bool:
        decision: str | None = await self._conexion.scalar(
            text(
                "SELECT a.decision FROM autorizaciones a "
                "JOIN textos_autorizacion t ON t.id = a.texto_id "
                "WHERE a.paciente_id = :paciente AND t.tipo = 'ia' "
                "ORDER BY a.fecha DESC LIMIT 1"
            ),
            {"paciente": paciente_id},
        )
        return decision == "aceptada"

    async def guardar_paginas(self, documento_id: UUID, paginas: Sequence[PaginaLeida]) -> None:
        if not paginas:
            return
        await self._conexion.execute(
            text(
                "INSERT INTO paginas_documento (documento_id, numero, texto, origen, legibilidad) "
                "VALUES (:documento, :numero, :texto, :origen, :legibilidad)"
            ),
            [
                {
                    "documento": documento_id,
                    "numero": p.numero,
                    "texto": p.texto,
                    "origen": p.origen,
                    "legibilidad": p.legibilidad,
                }
                for p in paginas
            ],
        )

    async def paginas(self, documento_id: UUID) -> list[PaginaLeida]:
        filas = await self._conexion.execute(
            text(
                "SELECT numero, texto, origen, legibilidad FROM paginas_documento "
                "WHERE documento_id = :d ORDER BY numero"
            ),
            {"d": documento_id},
        )
        return [
            PaginaLeida(
                f.numero,
                f.texto,
                cast(Literal["pdf", "reconocido"], f.origen),
                f.legibilidad if f.legibilidad is not None else 1.0,
            )
            for f in filas
        ]

    async def marcar(
        self, documento_id: UUID, estado: EstadoDeLectura, paginas: int | None = None
    ) -> None:
        await self._conexion.execute(
            text(
                "UPDATE documentos SET estado_lectura = :estado, "
                "paginas = coalesce(:paginas, paginas) WHERE id = :id"
            ),
            {"estado": estado, "paginas": paginas, "id": documento_id},
        )
