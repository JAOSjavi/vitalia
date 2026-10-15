"""Reglas del ingreso y de la sesión (HU-004, HU-007)."""

from dataclasses import dataclass
from datetime import datetime, timedelta

FALLOS_PARA_BLOQUEAR_LA_CUENTA = 5
# Tope por equipo, sea cual sea la cuenta: frena a quien prueba muchos documentos.
FALLOS_PARA_BLOQUEAR_EL_EQUIPO = 20
DURACION_DEL_BLOQUEO = timedelta(minutes=15)

INACTIVIDAD_MAXIMA = timedelta(minutes=30)
RENOVAR_ACTIVIDAD_CADA = timedelta(minutes=1)

VIGENCIA_DEL_ENLACE_DE_PUESTA_EN_MARCHA = timedelta(hours=24)


class CredencialesInvalidas(Exception):
    """No dice si falló el documento o la contraseña (HU-004, CA-2)."""


class IngresoBloqueado(Exception):
    def __init__(self, hasta: datetime) -> None:
        super().__init__(f"Ingreso bloqueado hasta {hasta.isoformat()}")
        self.hasta = hasta


@dataclass(frozen=True)
class Intentos:
    """Fallos seguidos de una cuenta desde un equipo, o de un equipo con cualquier cuenta."""

    fallos: int = 0
    ultimo_fallo: datetime | None = None
    bloqueado_hasta: datetime | None = None

    def vigentes(self, ahora: datetime) -> "Intentos":
        """Pasado el bloqueo, o 15 minutos sin fallar, se cuenta de nuevo desde cero."""
        if self.bloqueado_hasta is not None:
            return self if ahora < self.bloqueado_hasta else Intentos()
        if self.ultimo_fallo is None or ahora - self.ultimo_fallo >= DURACION_DEL_BLOQUEO:
            return Intentos()
        return self

    def bloqueado(self, ahora: datetime) -> bool:
        return self.bloqueado_hasta is not None and ahora < self.bloqueado_hasta

    def con_un_fallo(self, ahora: datetime, tope: int) -> "Intentos":
        fallos = self.vigentes(ahora).fallos + 1
        hasta = ahora + DURACION_DEL_BLOQUEO if fallos >= tope else None
        return Intentos(fallos, ahora, hasta)
