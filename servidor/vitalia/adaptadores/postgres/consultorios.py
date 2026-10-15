"""El consultorio y los datos del médico en PostgreSQL."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from vitalia.casos_de_uso.puertos import ConsultorioPublico, DatosDelConsultorio


class ConsultoriosPostgres:
    def __init__(self, conexion: AsyncConnection) -> None:
        self._conexion = conexion

    async def publico(self) -> ConsultorioPublico:
        fila = (await self._conexion.execute(text("SELECT * FROM consultorio_publico()"))).one()
        return ConsultorioPublico(fila.nombre, fila.telefono, fila.medico)

    async def datos(self) -> DatosDelConsultorio:
        fila = (
            await self._conexion.execute(
                text(
                    "SELECT c.nombre, c.direccion, c.telefono, c.correo, "
                    "m.nombres, m.apellidos, m.registro_profesional "
                    "FROM consultorio c LEFT JOIN medicos m ON true"
                )
            )
        ).one()
        return DatosDelConsultorio(
            nombre=fila.nombre,
            direccion=fila.direccion,
            telefono=fila.telefono,
            correo=fila.correo,
            medico_nombres=fila.nombres or "",
            medico_apellidos=fila.apellidos or "",
            registro_profesional=fila.registro_profesional,
        )

    async def guardar(self, medico_id: UUID, datos: DatosDelConsultorio) -> None:
        await self._conexion.execute(
            text(
                "UPDATE consultorio SET nombre = :nombre, direccion = :direccion, "
                "telefono = :telefono, correo = :correo"
            ),
            {
                "nombre": datos.nombre,
                "direccion": datos.direccion,
                "telefono": datos.telefono,
                "correo": datos.correo,
            },
        )
        await self._conexion.execute(
            text(
                "UPDATE medicos SET nombres = :nombres, apellidos = :apellidos, "
                "registro_profesional = :registro WHERE usuario_id = :medico"
            ),
            {
                "nombres": datos.medico_nombres,
                "apellidos": datos.medico_apellidos,
                "registro": datos.registro_profesional,
                "medico": medico_id,
            },
        )
