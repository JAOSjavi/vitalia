"""Los casos de uso que la entrada ofrece, ya armados por principal.py."""

from dataclasses import dataclass

from vitalia.casos_de_uso.cerrar_sesion import CerrarSesion
from vitalia.casos_de_uso.editar_consultorio import EditarConsultorio
from vitalia.casos_de_uso.ingresar import Ingresar
from vitalia.casos_de_uso.poner_en_marcha import PonerEnMarcha
from vitalia.casos_de_uso.registrar_paciente import RegistrarPaciente
from vitalia.casos_de_uso.revisar_salud import RevisarSalud
from vitalia.casos_de_uso.validar_sesion import ValidarSesion
from vitalia.casos_de_uso.ver_consultorio import VerConsultorio
from vitalia.casos_de_uso.ver_mi_cuenta import VerMiCuenta
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


@dataclass(frozen=True)
class Ajustes:
    # Con él se resume la dirección de red del equipo: se guarda el resumen, no la dirección.
    secreto_del_origen: bytes
