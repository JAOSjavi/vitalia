"""Historia clínica del consultorio en PostgreSQL (E9).

Los nombres de columna salen de CAMPOS_DE_LA_ATENCION y CAMPOS_DE_IDENTIFICACION, nunca de la
petición: por eso se pueden escribir en el texto de la consulta.
"""

import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from datetime import datetime
from typing import Any, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from vitalia.adaptadores.postgres.errores import traducir_errores
from vitalia.casos_de_uso.puertos import AtencionGuardada, Firma, NotaAclaratoria
from vitalia.dominio.historia_clinica import (
    CAMPOS_DE_IDENTIFICACION,
    CAMPOS_DE_LA_ATENCION,
    Diagnostico,
    Medicamento,
    Valor,
)


def _valor(dato: Any) -> Valor:
    return cast(Valor, dato)


class HistoriaPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def abierta_de(self, paciente_id: UUID) -> UUID | None:
        abierta: UUID | None = await self._conexion.scalar(
            text("SELECT id FROM atenciones WHERE paciente_id = :p AND estado = 'abierta'"),
            {"p": paciente_id},
        )
        return abierta

    async def abrir(
        self,
        paciente_id: UUID,
        medico_id: UUID,
        cita_id: UUID | None,
        antecedentes: Mapping[str, Valor],
    ) -> UUID:
        columnas = ["paciente_id", "medico_id", "cita_id", *antecedentes]
        valores = {"paciente_id": paciente_id, "medico_id": medico_id, "cita_id": cita_id}
        valores.update(antecedentes)  # type: ignore[arg-type]
        with traducir_errores():
            atencion_id: UUID = await self._conexion.scalar(
                text(
                    f"INSERT INTO atenciones ({', '.join(columnas)}) "
                    f"VALUES ({', '.join(':' + c for c in columnas)}) RETURNING id"
                ),
                valores,
            )
        return atencion_id

    async def atencion(self, atencion_id: UUID) -> AtencionGuardada | None:
        fila = (
            await self._conexion.execute(
                text("SELECT * FROM atenciones WHERE id = :id"), {"id": atencion_id}
            )
        ).one_or_none()
        return None if fila is None else _guardada(dict(fila._mapping))

    async def de_paciente(self, paciente_id: UUID) -> list[AtencionGuardada]:
        filas = await self._conexion.execute(
            text("SELECT * FROM atenciones WHERE paciente_id = :p ORDER BY inicio DESC"),
            {"p": paciente_id},
        )
        return [_guardada(dict(f._mapping)) for f in filas]

    async def guardar(
        self,
        atencion_id: UUID,
        datos: Mapping[str, Valor],
        diagnosticos: Sequence[Diagnostico] | None,
        medicamentos: Sequence[Medicamento] | None,
        ahora: datetime,
    ) -> None:
        asignaciones = [f"{c} = :{c}" for c in datos]
        valores: dict[str, object] = {"id": atencion_id, "ahora": ahora, **datos}
        if diagnosticos is not None:
            asignaciones.append("diagnosticos = CAST(:diagnosticos AS jsonb)")
            valores["diagnosticos"] = json.dumps([asdict(d) for d in diagnosticos])
        if medicamentos is not None:
            asignaciones.append("medicamentos = CAST(:medicamentos AS jsonb)")
            valores["medicamentos"] = json.dumps([asdict(m) for m in medicamentos])
        asignaciones.append("guardada_en = :ahora")
        with traducir_errores():
            await self._conexion.execute(
                text(f"UPDATE atenciones SET {', '.join(asignaciones)} WHERE id = :id"), valores
            )

    async def cerrar(self, atencion_id: UUID, fin: datetime, firma: Firma) -> None:
        with traducir_errores():
            await self._conexion.execute(
                text(
                    "UPDATE atenciones SET estado = 'cerrada', fin = :fin, guardada_en = :fin, "
                    "firma_nombre = :nombre, firma_registro = :registro, "
                    "firma_documento = :documento WHERE id = :id"
                ),
                {
                    "id": atencion_id,
                    "fin": fin,
                    "nombre": firma.nombre,
                    "registro": firma.registro,
                    "documento": firma.documento,
                },
            )

    async def agregar_nota(
        self, atencion_id: UUID, medico_id: UUID, texto: str, firma: Firma
    ) -> None:
        await self._conexion.execute(
            text(
                "INSERT INTO notas_aclaratorias "
                "(atencion_id, medico_id, texto, firma_nombre, firma_registro) "
                "VALUES (:atencion, :medico, :texto, :nombre, :registro)"
            ),
            {
                "atencion": atencion_id,
                "medico": medico_id,
                "texto": texto,
                "nombre": firma.nombre,
                "registro": firma.registro,
            },
        )

    async def notas(self, atenciones: Sequence[UUID]) -> list[NotaAclaratoria]:
        if not atenciones:
            return []
        filas = await self._conexion.execute(
            text(
                "SELECT atencion_id, texto, fecha, firma_nombre, firma_registro "
                "FROM notas_aclaratorias WHERE atencion_id = ANY(:ids) ORDER BY fecha"
            ),
            {"ids": list(atenciones)},
        )
        return [
            NotaAclaratoria(f.atencion_id, f.texto, f.fecha, f.firma_nombre, f.firma_registro)
            for f in filas
        ]

    async def identificacion(self, paciente_id: UUID) -> dict[str, Valor] | None:
        fila = (
            await self._conexion.execute(
                text(f"SELECT {', '.join(CAMPOS_DE_IDENTIFICACION)} FROM pacientes WHERE id = :id"),
                {"id": paciente_id},
            )
        ).one_or_none()
        return None if fila is None else {k: _valor(v) for k, v in fila._mapping.items()}

    async def guardar_identificacion(self, paciente_id: UUID, datos: Mapping[str, Valor]) -> None:
        if not datos:
            return
        await self._conexion.execute(
            text(f"UPDATE pacientes SET {', '.join(f'{c} = :{c}' for c in datos)} WHERE id = :id"),
            {"id": paciente_id, **datos},
        )

    async def nombres_cie10(self, codigos: Sequence[str]) -> dict[str, str]:
        if not codigos:
            return {}
        filas = await self._conexion.execute(
            text("SELECT codigo, nombre FROM cie10 WHERE codigo = ANY(:codigos)"),
            {"codigos": list(codigos)},
        )
        return {f.codigo: f.nombre for f in filas}

    async def buscar_cie10(self, texto: str, limite: int) -> list[tuple[str, str]]:
        # Por el comienzo del código ("I10") o por palabras del nombre, sin tildes.
        filas = await self._conexion.execute(
            text(
                "SELECT codigo, nombre FROM cie10 "
                "WHERE codigo LIKE upper(:texto) || '%' "
                "OR NOT EXISTS (SELECT 1 FROM regexp_split_to_table(sin_tildes(trim(:texto)), "
                "'\\s+') AS palabra WHERE sin_tildes(nombre) NOT LIKE '%' || palabra || '%') "
                "ORDER BY (codigo LIKE upper(:texto) || '%') DESC, codigo LIMIT :limite"
            ),
            {"texto": texto, "limite": limite},
        )
        return [(f.codigo, f.nombre) for f in filas]

    async def firma_del_medico(self) -> tuple[Firma, str | None]:
        fila = (
            await self._conexion.execute(
                text(
                    "SELECT m.nombres, m.apellidos, m.registro_profesional, u.tipo_documento, "
                    "u.numero_documento, hash_del_medico_actual() AS hash "
                    "FROM medicos m JOIN usuarios u ON u.id = m.usuario_id "
                    "WHERE m.usuario_id = usuario_actual()"
                )
            )
        ).one()
        firma = Firma(
            nombre=f"{fila.nombres} {fila.apellidos}".strip(),
            registro=fila.registro_profesional,
            documento=f"{fila.tipo_documento} {fila.numero_documento}",
        )
        return firma, fila.hash


def _lista(dato: Any) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], json.loads(dato) if isinstance(dato, str) else dato)


def _guardada(fila: Mapping[str, Any]) -> AtencionGuardada:
    return AtencionGuardada(
        id=fila["id"],
        paciente_id=fila["paciente_id"],
        cita_id=fila["cita_id"],
        estado=fila["estado"],
        inicio=fila["inicio"],
        fin=fila["fin"],
        guardada_en=fila["guardada_en"],
        datos={c: _valor(fila[c]) for c in CAMPOS_DE_LA_ATENCION},
        diagnosticos=[Diagnostico(**d) for d in _lista(fila["diagnosticos"])],
        medicamentos=[Medicamento(**m) for m in _lista(fila["medicamentos"])],
        firma_nombre=fila["firma_nombre"],
        firma_registro=fila["firma_registro"],
        firma_documento=fila["firma_documento"],
    )
