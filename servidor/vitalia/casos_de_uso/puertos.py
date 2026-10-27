"""Puertos: lo que los casos de uso necesitan de afuera, sin decir quién lo hace."""

from collections.abc import AsyncIterator, Mapping, Sequence
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, Protocol
from uuid import UUID

from vitalia.dominio.agenda import EstadoDeCita, Franja, Intervalo, TipoDeCita
from vitalia.dominio.cuentas import DatosDelMedico, DatosDelPaciente, Documento
from vitalia.dominio.documentos import (
    ArchivoValido,
    EstadoDeLectura,
    Formato,
    TipoDeDocumento,
)
from vitalia.dominio.fragmentos import Identificadores
from vitalia.dominio.identidad import Identidad, Rol
from vitalia.dominio.ingreso import Intentos
from vitalia.dominio.permisos import MatrizDePermisos


class BaseDeDatos(Protocol):
    async def responde(self) -> bool:
        """Dice si la base atiende una consulta."""
        ...


class Bitacora(Protocol):
    async def registrar(
        self,
        accion: str,
        *,
        paciente_id: UUID | None = None,
        objeto: str | None = None,
        detalle: Mapping[str, object] | None = None,
    ) -> None:
        """Anota quién hizo qué. El detalle nunca lleva contenido clínico."""
        ...


class Permisos(Protocol):
    async def matriz(self) -> MatrizDePermisos: ...


@dataclass(frozen=True)
class Credencial:
    """Lo que la base entrega para verificar un ingreso. Sin cuenta, usuario_id es None."""

    usuario_id: UUID | None
    hash_contrasena: str | None
    rol: Rol | None
    activo: bool
    intentos: Intentos
    intentos_del_equipo: Intentos


@dataclass(frozen=True)
class PuntoDelTexto:
    titulo: str
    texto: str
    resaltado: bool = False


@dataclass(frozen=True)
class TextoDeAutorizacion:
    id: UUID
    tipo: Literal["datos", "ia"]
    version: int
    puntos: Sequence[PuntoDelTexto]
    contenido: str
    vigente_desde: datetime


@dataclass(frozen=True)
class Cuenta:
    usuario_id: UUID
    rol: Rol
    documento: Documento
    nombres: str
    apellidos: str
    correo: str | None


class Cuentas(Protocol):
    """Lo de las cuentas. Lo que ocurre sin sesión pasa por funciones de la base."""

    async def buscar_credencial(
        self, documento: Documento, resumen_de_la_cuenta: str, origen: str
    ) -> Credencial: ...

    async def guardar_intentos(
        self, resumen_de_la_cuenta: str | None, origen: str, intentos: Intentos
    ) -> None:
        """Sin resumen de cuenta, guarda el tope del equipo. Sin fallos, borra la fila."""
        ...

    async def anotar_sin_sesion(self, usuario_id: UUID | None, accion: str) -> None: ...

    async def abrir_sesion(
        self, usuario_id: UUID, huella: str, ahora: datetime, vence: datetime
    ) -> None: ...

    async def sesion_vigente(self, huella: str, ahora: datetime) -> Identidad | None: ...

    async def anular_sesion(self, huella: str, ahora: datetime) -> None: ...

    async def texto_vigente(self, tipo: Literal["datos", "ia"]) -> TextoDeAutorizacion: ...

    async def registrar_paciente(
        self,
        datos: DatosDelPaciente,
        hash_contrasena: str,
        texto_datos: UUID,
        texto_ia: UUID | None,
        hoy: date,
    ) -> UUID:
        """Lanza DocumentoYaRegistrado, MenorDeEdad o AutorizacionDesactualizada."""
        ...

    async def crear_enlace_de_puesta_en_marcha(self, huella: str, vence: datetime) -> None:
        """Lanza YaHayMedico."""
        ...

    async def usar_enlace_de_puesta_en_marcha(
        self, huella: str, ahora: datetime, datos: DatosDelMedico, hash_contrasena: str
    ) -> UUID:
        """Lanza EnlaceInvalido, YaHayMedico o DocumentoYaRegistrado."""
        ...

    async def cuenta(self, usuario_id: UUID) -> Cuenta: ...


@dataclass(frozen=True)
class ConsultorioPublico:
    nombre: str | None
    telefono: str | None
    medico: str | None


@dataclass(frozen=True)
class DatosDelConsultorio:
    nombre: str | None
    direccion: str | None
    telefono: str | None
    correo: str | None
    medico_nombres: str
    medico_apellidos: str
    registro_profesional: str | None


@dataclass(frozen=True)
class ReglasDelConsultorio:
    anticipacion_horas: int
    margen_agenda_minutos: int
    telefono: str | None
    direccion: str | None


class Consultorios(Protocol):
    async def publico(self) -> ConsultorioPublico: ...

    async def reglas(self) -> ReglasDelConsultorio: ...

    async def datos(self) -> DatosDelConsultorio: ...

    async def guardar(self, medico_id: UUID, datos: DatosDelConsultorio) -> None: ...


@dataclass(frozen=True)
class Cita:
    id: UUID
    paciente_id: UUID
    paciente: str
    tipo_id: UUID
    tipo: str
    inicio: datetime
    fin: datetime
    estado: EstadoDeCita
    fuera_de_horario: bool
    # El último motivo que dio quien la movió o la canceló (HU-017, CA-3).
    motivo: str | None


class Agenda(Protocol):
    async def franjas(self) -> list[Franja]: ...

    async def reemplazar_franjas(self, franjas: Sequence[Franja]) -> None: ...

    async def tipos(self, solo_activos: bool) -> list[TipoDeCita]: ...

    async def tipo(self, tipo_id: UUID) -> TipoDeCita | None: ...

    async def crear_tipo(self, nombre: str, duracion_minutos: int) -> TipoDeCita: ...

    async def guardar_tipo(self, tipo: TipoDeCita) -> None: ...

    async def ocupados(self, desde: datetime, hasta: datetime) -> list[tuple[UUID, Intervalo]]:
        """Lo ocupado en el rango, sin decir de quién. Sirve también al paciente."""
        ...

    async def citas(
        self,
        *,
        desde: datetime | None = None,
        hasta: datetime | None = None,
        paciente_id: UUID | None = None,
        estado: EstadoDeCita | None = None,
        limite: int | None = None,
    ) -> list[Cita]:
        """Las citas en orden de inicio. Los permisos por fila dejan al paciente solo las suyas."""
        ...

    async def cita(self, cita_id: UUID) -> Cita | None: ...

    async def crear_cita(
        self,
        paciente_id: UUID,
        tipo_id: UUID,
        intervalo: Intervalo,
        creada_por: UUID,
        fuera_de_horario: bool,
    ) -> UUID:
        """Lanza EspacioOcupado si se cruza con otra cita: lo impide la base."""
        ...

    async def mover_cita(self, cita_id: UUID, intervalo: Intervalo, fuera_de_horario: bool) -> None:
        """Lanza EspacioOcupado si se cruza con otra cita: lo impide la base."""
        ...

    async def cancelar_cita(self, cita_id: UUID) -> None: ...

    async def anotar_cambio(
        self,
        cita_id: UUID,
        usuario_id: UUID,
        tipo: Literal["creada", "movida", "cancelada"],
        inicio_anterior: datetime | None = None,
        inicio_nuevo: datetime | None = None,
        motivo: str | None = None,
    ) -> None: ...

    async def paciente_de_la_sesion(self) -> UUID | None: ...


@dataclass(frozen=True)
class PacienteEnLista:
    id: UUID
    nombres: str
    apellidos: str
    documento: Documento
    telefono: str


class Pacientes(Protocol):
    async def buscar(
        self, texto: str | None, pagina: int, tamano: int
    ) -> tuple[list[PacienteEnLista], int]:
        """Una página en orden alfabético y el total de pacientes que coinciden."""
        ...

    async def existe(self, paciente_id: UUID) -> bool: ...


@dataclass(frozen=True)
class DocumentoSubido:
    id: UUID
    nombre: str
    fecha_documento: date
    tipo: TipoDeDocumento
    formato: Formato
    tamano: int
    estado_lectura: EstadoDeLectura
    paginas: int | None
    subido_en: datetime


@dataclass(frozen=True)
class DocumentoPorLeer:
    id: UUID
    paciente_id: UUID
    formato: Formato
    clave_archivo: str


@dataclass(frozen=True)
class TrabajoDeLectura:
    id: UUID
    documento_id: UUID
    intentos: int


@dataclass(frozen=True)
class PaginaLeida:
    numero: int
    texto: str
    origen: Literal["pdf", "reconocido"]
    legibilidad: float


TipoDeTrabajo = Literal["leer", "indexar_documento"]


class Documentos(Protocol):
    """Documentos del paciente y la cola del lector. Los permisos por fila dicen quién ve qué."""

    async def por_huella(self, huella: str) -> UUID | None:
        """El documento del paciente de la sesión con ese mismo contenido, si ya lo subió."""
        ...

    async def crear(self, archivo: ArchivoValido, clave_archivo: str) -> DocumentoSubido:
        """Lo guarda a nombre del paciente de la sesión, ya en proceso de lectura."""
        ...

    async def listar(self) -> list[DocumentoSubido]:
        """Los del paciente de la sesión, del más reciente al más antiguo."""
        ...

    async def encolar(self, documento_id: UUID, tipo: TipoDeTrabajo) -> None: ...

    # Lo que sigue lo usa el lector, con la identidad sistema.

    async def tomar_trabajo(self, tipo: TipoDeTrabajo) -> TrabajoDeLectura | None:
        """El trabajo pendiente más antiguo, ya marcado en curso. Dos lectores no toman el mismo."""
        ...

    async def terminar_trabajo(
        self, trabajo_id: UUID, *, error: str | None = None, reintentar: bool = False
    ) -> None:
        """Sin error queda hecho; con error, pendiente otra vez o fallido."""
        ...

    async def por_leer(self, documento_id: UUID) -> DocumentoPorLeer: ...

    async def ia_autorizada(self, paciente_id: UUID) -> bool:
        """Si la última decisión del paciente sobre la IA es aceptarla."""
        ...

    async def guardar_paginas(self, documento_id: UUID, paginas: Sequence[PaginaLeida]) -> None: ...

    async def paginas(self, documento_id: UUID) -> list[PaginaLeida]: ...

    async def marcar(
        self, documento_id: UUID, estado: EstadoDeLectura, paginas: int | None = None
    ) -> None: ...


@dataclass(frozen=True)
class FragmentoNuevo:
    pagina: int
    orden: int
    texto: str
    vector: Sequence[float]


@dataclass(frozen=True)
class FragmentoEncontrado:
    id: UUID
    documento_id: UUID
    documento: str
    fecha_documento: date
    pagina: int
    texto: str
    puntaje: float
    # Puesto en cada búsqueda; None si esa búsqueda no lo trajo.
    rango_significado: int | None
    rango_palabras: int | None


class Fragmentos(Protocol):
    """Lo que busca el asistente. Siempre de un solo paciente."""

    async def identificadores(self, paciente_id: UUID) -> Identificadores:
        """Lo que hay que tapar antes de enviar texto del paciente al proveedor."""
        ...

    async def reemplazar_del_documento(
        self, documento_id: UUID, fragmentos: Sequence[FragmentoNuevo], modelo: str
    ) -> None:
        """Borra los que tenga el documento y guarda estos: indexar dos veces da lo mismo."""
        ...

    async def buscar(
        self,
        paciente_id: UUID,
        vector: Sequence[float],
        consulta: str,
        por_metodo: int,
        total: int,
    ) -> list[FragmentoEncontrado]:
        """Por significado y por palabras, combinadas, del más al menos parecido."""
        ...


class Vectorizador(Protocol):
    """Convierte textos en vectores: números que representan lo que significan."""

    @property
    def modelo(self) -> str: ...

    async def vectorizar(self, textos: Sequence[str]) -> list[list[float]]:
        """Un vector por texto, en el mismo orden."""
        ...


class Archivos(Protocol):
    """Donde se guardan los archivos: privados, sin ninguna ruta pública (HU-027)."""

    async def guardar(self, clave: str, contenido: bytes) -> None: ...

    async def leer(self, clave: str) -> bytes: ...

    async def borrar(self, clave: str) -> None:
        """No falla si el archivo ya no existe."""
        ...


class LectorDePDF(Protocol):
    """Lee un PDF dentro del servidor: nada sale a un proveedor externo."""

    async def textos(self, contenido: bytes) -> list[str]:
        """El texto de cada página, en orden. Una página sin texto da una cadena vacía."""
        ...

    async def imagen_de_pagina(self, contenido: bytes, numero: int) -> bytes:
        """La página dibujada como imagen PNG, para reconocer su texto. Empieza en 1."""
        ...


class Trabajo(Protocol):
    """Una transacción abierta a nombre de alguien. Sus repositorios la comparten."""

    @property
    def bitacora(self) -> Bitacora: ...

    @property
    def permisos(self) -> Permisos: ...

    @property
    def cuentas(self) -> Cuentas: ...

    @property
    def consultorios(self) -> Consultorios: ...

    @property
    def agenda(self) -> Agenda: ...

    @property
    def pacientes(self) -> Pacientes: ...

    @property
    def documentos(self) -> Documentos: ...

    @property
    def fragmentos(self) -> Fragmentos: ...


class UnidadDeTrabajo(Protocol):
    def abrir(self, identidad: Identidad | None) -> AbstractAsyncContextManager[Trabajo]:
        """Abre la transacción y le dice a la base quién es; sin identidad no ve ninguna fila.

        Confirma al salir y deshace si algo falla.
        """
        ...


class Contrasenas(Protocol):
    async def cifrar(self, contrasena: str) -> str: ...

    async def verificar(self, contrasena: str, hash_contrasena: str | None) -> bool:
        """Sin hash tarda lo mismo y responde que no: así no se sabe si la cuenta existe."""
        ...


class Correo(Protocol):
    async def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None: ...


@dataclass(frozen=True)
class Turno:
    autor: Literal["medico", "asistente"]
    texto: str


class ProveedorIA(Protocol):
    async def leer_pagina(self, imagen: bytes) -> str:
        """Transcribe el texto de la imagen de una página."""
        ...

    def responder(self, instrucciones: str, turnos: Sequence[Turno]) -> AsyncIterator[str]:
        """Entrega la respuesta por partes, a medida que el proveedor la escribe."""
        ...


class Reloj(Protocol):
    def ahora(self) -> datetime: ...
