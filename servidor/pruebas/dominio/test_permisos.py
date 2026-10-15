"""La matriz de permisos niega todo lo que no concede (HU-006)."""

from vitalia.dominio.permisos import MatrizDePermisos

MATRIZ = MatrizDePermisos(frozenset({("medico", "consultorio.editar"), ("paciente", "cuenta.ver")}))


def test_permite_lo_concedido_al_rol() -> None:
    assert MATRIZ.permite("medico", "consultorio.editar")


def test_niega_al_paciente_una_operacion_del_medico() -> None:
    assert not MATRIZ.permite("paciente", "consultorio.editar")


def test_niega_una_operacion_nueva_hasta_que_se_asigne() -> None:
    assert not MATRIZ.permite("medico", "operacion.recien_creada")


def test_niega_todo_a_un_rol_que_no_existe() -> None:
    assert not MATRIZ.permite("sin_rol", "cuenta.ver")
