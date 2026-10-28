"""Los casos de uso que la entrada ofrece, ya armados por principal.py."""

from dataclasses import dataclass

from vitalia.casos_de_uso.abrir_y_eliminar_documento import AbrirDocumento, EliminarDocumento
from vitalia.casos_de_uso.agendar_cita import AgendarCita
from vitalia.casos_de_uso.bloqueos import Bloqueos
from vitalia.casos_de_uso.buscar_fragmentos import BuscarFragmentos
from vitalia.casos_de_uso.buscar_pacientes import BuscarPacientes
from vitalia.casos_de_uso.cancelar_cita import CancelarCita
from vitalia.casos_de_uso.cerrar_sesion import CerrarSesion
from vitalia.casos_de_uso.consultar_disponibilidad import ConsultarDisponibilidad
from vitalia.casos_de_uso.editar_consultorio import EditarConsultorio
from vitalia.casos_de_uso.guardar_horario import GuardarHorario
from vitalia.casos_de_uso.ingresar import Ingresar
from vitalia.casos_de_uso.listar_citas import ListarCitas
from vitalia.casos_de_uso.mover_cita import MoverCita
from vitalia.casos_de_uso.poner_en_marcha import PonerEnMarcha
from vitalia.casos_de_uso.preguntar_al_asistente import PreguntarAlAsistente
from vitalia.casos_de_uso.registrar_asistencia import RegistrarAsistencia
from vitalia.casos_de_uso.registrar_paciente import RegistrarPaciente
from vitalia.casos_de_uso.revisar_salud import RevisarSalud
from vitalia.casos_de_uso.subir_documento import SubirDocumento
from vitalia.casos_de_uso.tipos_de_cita import TiposDeCita
from vitalia.casos_de_uso.validar_sesion import ValidarSesion
from vitalia.casos_de_uso.ver_agenda_de_hoy import VerAgendaDeHoy
from vitalia.casos_de_uso.ver_consultorio import VerConsultorio
from vitalia.casos_de_uso.ver_ficha_del_paciente import VerFichaDelPaciente
from vitalia.casos_de_uso.ver_horario import VerHorario
from vitalia.casos_de_uso.ver_inicio_del_paciente import VerInicioDelPaciente
from vitalia.casos_de_uso.ver_mi_cuenta import VerMiCuenta
from vitalia.casos_de_uso.ver_mis_documentos import VerMisDocumentos
from vitalia.casos_de_uso.ver_texto_de_autorizacion import VerTextoDeAutorizacion


@dataclass(frozen=True)
class CasosDeUso:
    revisar_salud: RevisarSalud
    validar_sesion: ValidarSesion
    ingresar: Ingresar
    cerrar_sesion: CerrarSesion
    ver_mi_cuenta: VerMiCuenta
    registrar_paciente: RegistrarPaciente
    ver_texto_de_autorizacion: VerTextoDeAutorizacion
    poner_en_marcha: PonerEnMarcha
    ver_consultorio: VerConsultorio
    editar_consultorio: EditarConsultorio
    ver_horario: VerHorario
    guardar_horario: GuardarHorario
    tipos_de_cita: TiposDeCita
    consultar_disponibilidad: ConsultarDisponibilidad
    agendar_cita: AgendarCita
    listar_citas: ListarCitas
    mover_cita: MoverCita
    cancelar_cita: CancelarCita
    registrar_asistencia: RegistrarAsistencia
    bloqueos: Bloqueos
    ver_inicio_del_paciente: VerInicioDelPaciente
    ver_agenda_de_hoy: VerAgendaDeHoy
    buscar_pacientes: BuscarPacientes
    subir_documento: SubirDocumento
    ver_mis_documentos: VerMisDocumentos
    buscar_fragmentos: BuscarFragmentos
    preguntar_al_asistente: PreguntarAlAsistente
    ver_ficha_del_paciente: VerFichaDelPaciente
    abrir_documento: AbrirDocumento
    eliminar_documento: EliminarDocumento


@dataclass(frozen=True)
class Ajustes:
    # Con él se resume la dirección de red del equipo: se guarda el resumen, no la dirección.
    secreto_del_origen: bytes
