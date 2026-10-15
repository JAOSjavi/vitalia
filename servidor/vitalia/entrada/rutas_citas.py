"""Horario, tipos de cita, disponibilidad, citas, agenda de hoy y pacientes (diseno/03-api.md)."""

from datetime import date, datetime, time
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Request, status
from pydantic import AwareDatetime, BaseModel, Field

from vitalia.casos_de_uso.puertos import Cita as CitaDelDominio
from vitalia.dominio.agenda import EstadoDeCita, Franja, TipoDeCita
from vitalia.dominio.cuentas import TipoDocumento
from vitalia.entrada.sesion import Sesion, casos

rutas = APIRouter(prefix="/api/v1")


class Cita(BaseModel):
    id: UUID
    paciente_id: UUID
    paciente: str
    tipo_id: UUID
    tipo: str
    inicio: datetime
    fin: datetime
    duracion_minutos: int
    estado: EstadoDeCita
    fuera_de_horario: bool
    motivo: str | None

    @classmethod
    def de(cls, cita: CitaDelDominio) -> "Cita":
        return cls(
            id=cita.id,
            paciente_id=cita.paciente_id,
            paciente=cita.paciente,
            tipo_id=cita.tipo_id,
            tipo=cita.tipo,
            inicio=cita.inicio,
            fin=cita.fin,
            duracion_minutos=int((cita.fin - cita.inicio).total_seconds() // 60),
            estado=cita.estado,
            fuera_de_horario=cita.fuera_de_horario,
            motivo=cita.motivo,
        )


class FranjaDeHorario(BaseModel):
    dia_semana: int = Field(ge=1, le=7)
    hora_inicio: time
    hora_fin: time


class Horario(BaseModel):
    franjas: list[FranjaDeHorario] = Field(max_length=70)


class HorarioGuardado(BaseModel):
    citas_afectadas: list[Cita]


class Tipo(BaseModel):
    id: UUID
    nombre: str
    duracion_minutos: int
    activo: bool

    @classmethod
    def de(cls, tipo: TipoDeCita) -> "Tipo":
        return cls(
            id=tipo.id,
            nombre=tipo.nombre,
            duracion_minutos=tipo.duracion_minutos,
            activo=tipo.activo,
        )


class TipoNuevo(BaseModel):
    nombre: str = Field(max_length=80)
    duracion_minutos: int


class CambioDeTipo(BaseModel):
    nombre: str | None = Field(default=None, max_length=80)
    duracion_minutos: int | None = None
    activo: bool | None = None


class Disponibilidad(BaseModel):
    tipo: Tipo
    dias: list[date]
    dia: date | None
    horas: list[datetime]


class CitaNueva(BaseModel):
    tipo_cita: UUID
    inicio: AwareDatetime
    # Solo el médico indica el paciente; el paciente agenda para sí mismo.
    paciente: UUID | None = None
    confirmar_repetida: bool = False
    confirmar_fuera_de_horario: bool = False


class CitaCreada(BaseModel):
    id: UUID


class Movimiento(BaseModel):
    inicio: AwareDatetime
    motivo: str | None = Field(default=None, max_length=300)
    confirmar_fuera_de_horario: bool = False


class Cancelacion(BaseModel):
    motivo: str | None = Field(default=None, max_length=300)


class InicioDelPaciente(BaseModel):
    proxima: Cita | None
    puede_cambiarla: bool
    anticipacion_horas: int
    telefono: str | None
    direccion: str | None


class AgendaDeHoy(BaseModel):
    dia: datetime
    citas: list[Cita]
    proxima: Cita | None
    pendientes: list[Literal["horario", "tipos_cita", "consultorio"]]


class Paciente(BaseModel):
    id: UUID
    nombres: str
    apellidos: str
    tipo_documento: TipoDocumento
    numero_documento: str
    telefono: str


class PaginaDePacientes(BaseModel):
    pacientes: list[Paciente]
    total: int
    pagina: int
    tamano: int


# --- Horario (HU-008)


@rutas.get("/horario")
async def ver_horario(identidad: Sesion, request: Request) -> Horario:
    franjas = await casos(request).ver_horario.ejecutar(identidad)
    return Horario(
        franjas=[
            FranjaDeHorario(dia_semana=f.dia_semana, hora_inicio=f.inicio, hora_fin=f.fin)
            for f in franjas
        ]
    )


@rutas.put("/horario")
async def guardar_horario(horario: Horario, identidad: Sesion, request: Request) -> HorarioGuardado:
    afectadas = await casos(request).guardar_horario.ejecutar(
        identidad, [Franja(f.dia_semana, f.hora_inicio, f.hora_fin) for f in horario.franjas]
    )
    return HorarioGuardado(citas_afectadas=[Cita.de(c) for c in afectadas])


# --- Tipos de cita (HU-010)


@rutas.get("/tipos-cita")
async def ver_tipos(identidad: Sesion, request: Request) -> list[Tipo]:
    return [Tipo.de(t) for t in await casos(request).tipos_de_cita.ver(identidad)]


@rutas.post("/tipos-cita", status_code=status.HTTP_201_CREATED)
async def crear_tipo(tipo: TipoNuevo, identidad: Sesion, request: Request) -> Tipo:
    creado = await casos(request).tipos_de_cita.crear(identidad, tipo.nombre, tipo.duracion_minutos)
    return Tipo.de(creado)


@rutas.patch("/tipos-cita/{tipo_id}")
async def editar_tipo(
    tipo_id: UUID, cambio: CambioDeTipo, identidad: Sesion, request: Request
) -> Tipo:
    editado = await casos(request).tipos_de_cita.editar(
        identidad, tipo_id, cambio.nombre, cambio.duracion_minutos, cambio.activo
    )
    return Tipo.de(editado)


# --- Disponibilidad y citas (HU-011 a HU-017)


@rutas.get("/disponibilidad")
async def disponibilidad(
    tipo_cita: UUID,
    identidad: Sesion,
    request: Request,
    fecha: date | None = None,
    cita: UUID | None = None,
) -> Disponibilidad:
    """Con "cita", calcula para moverla: su propio espacio cuenta como libre."""
    resultado = await casos(request).consultar_disponibilidad.ejecutar(
        identidad, tipo_cita, fecha, cita
    )
    return Disponibilidad(
        tipo=Tipo.de(resultado.tipo), dias=resultado.dias, dia=resultado.dia, horas=resultado.horas
    )


@rutas.post("/citas", status_code=status.HTTP_201_CREATED)
async def crear_cita(nueva: CitaNueva, identidad: Sesion, request: Request) -> CitaCreada:
    cita_id = await casos(request).agendar_cita.ejecutar(
        identidad,
        nueva.tipo_cita,
        nueva.inicio,
        nueva.paciente,
        nueva.confirmar_repetida,
        nueva.confirmar_fuera_de_horario,
    )
    return CitaCreada(id=cita_id)


@rutas.get("/citas")
async def listar_citas(
    identidad: Sesion,
    request: Request,
    desde: AwareDatetime | None = None,
    hasta: AwareDatetime | None = None,
    estado: EstadoDeCita | None = None,
) -> list[Cita]:
    citas = await casos(request).listar_citas.ejecutar(identidad, desde, hasta, estado)
    return [Cita.de(c) for c in citas]


@rutas.post("/citas/{cita_id}/mover", status_code=status.HTTP_204_NO_CONTENT)
async def mover_cita(
    cita_id: UUID, movimiento: Movimiento, identidad: Sesion, request: Request
) -> None:
    await casos(request).mover_cita.ejecutar(
        identidad,
        cita_id,
        movimiento.inicio,
        movimiento.motivo,
        movimiento.confirmar_fuera_de_horario,
    )


@rutas.post("/citas/{cita_id}/cancelar", status_code=status.HTTP_204_NO_CONTENT)
async def cancelar_cita(
    cita_id: UUID, cancelacion: Cancelacion, identidad: Sesion, request: Request
) -> None:
    await casos(request).cancelar_cita.ejecutar(identidad, cita_id, cancelacion.motivo)


@rutas.get("/yo/inicio")
async def inicio_del_paciente(identidad: Sesion, request: Request) -> InicioDelPaciente:
    inicio = await casos(request).ver_inicio_del_paciente.ejecutar(identidad)
    return InicioDelPaciente(
        proxima=Cita.de(inicio.proxima) if inicio.proxima else None,
        puede_cambiarla=inicio.puede_cambiarla,
        anticipacion_horas=inicio.reglas.anticipacion_horas,
        telefono=inicio.reglas.telefono,
        direccion=inicio.reglas.direccion,
    )


# --- Panel del médico (HU-021, HU-023)


@rutas.get("/agenda/hoy")
async def agenda_de_hoy(identidad: Sesion, request: Request) -> AgendaDeHoy:
    agenda = await casos(request).ver_agenda_de_hoy.ejecutar(identidad)
    return AgendaDeHoy(
        dia=agenda.dia,
        citas=[Cita.de(c) for c in agenda.citas],
        proxima=Cita.de(agenda.proxima) if agenda.proxima else None,
        pendientes=agenda.pendientes,
    )


@rutas.get("/pacientes")
async def buscar_pacientes(
    identidad: Sesion,
    request: Request,
    buscar: str | None = None,
    pagina: int = 1,
    tamano: int = 20,
) -> PaginaDePacientes:
    resultado = await casos(request).buscar_pacientes.ejecutar(identidad, buscar, pagina, tamano)
    return PaginaDePacientes(
        pacientes=[
            Paciente(
                id=p.id,
                nombres=p.nombres,
                apellidos=p.apellidos,
                tipo_documento=p.documento.tipo,
                numero_documento=p.documento.numero,
                telefono=p.telefono,
            )
            for p in resultado.pacientes
        ],
        total=resultado.total,
        pagina=resultado.pagina,
        tamano=resultado.tamano,
    )
