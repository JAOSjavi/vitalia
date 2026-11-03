"""Reglas de la historia clínica de medicina general (HU-041 a HU-045).

Cada campo de la atención y de la identificación del paciente se describe una vez aquí: su tipo,
sus valores válidos y si hace falta para cerrar. De esa descripción salen la revisión del
borrador, la lista de lo que falta al cerrar y las listas que muestran las pantallas. De dónde
sale cada campo en la norma está en diseno/10-historia-clinica.md.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Literal

from vitalia.dominio.cuentas import DatosInvalidos

Clase = Literal["texto", "entero", "decimal", "opcion", "si_no"]

# "No refiere" y "Sin hallazgos" cuentan como escritos: la norma no admite espacios en blanco,
# pero sí dejar constancia de que no hay nada (HU-043, CA-3).
NO_REFIERE = "No refiere"
SIN_HALLAZGOS = "Sin hallazgos"

LARGO_DE_TEXTO = 4000
LARGO_DE_DATO_CORTO = 200

LISTAS: dict[str, dict[str, str]] = {
    "sexo": {"H": "Hombre", "M": "Mujer", "I": "Indeterminado o intersexual"},
    "estado_civil": {
        "soltero": "Soltero(a)",
        "casado": "Casado(a)",
        "union_libre": "Unión libre",
        "separado": "Separado(a)",
        "divorciado": "Divorciado(a)",
        "viudo": "Viudo(a)",
    },
    "nivel_escolar": {
        "ninguno": "Ninguno",
        "primaria": "Primaria",
        "secundaria": "Secundaria",
        "tecnica": "Técnica",
        "tecnologica": "Tecnológica",
        "universitaria": "Universitaria",
        "posgrado": "Posgrado",
    },
    "pertenencia_etnica": {
        "indigena": "Indígena",
        "rom": "Rom (gitano)",
        "raizal": "Raizal",
        "palenquero": "Palenquero",
        "afrocolombiano": "Negro, mulato o afrocolombiano",
        "ninguna": "Ninguna",
    },
    "zona": {"urbana": "Urbana", "rural": "Rural"},
    "tipo_vinculacion": {
        "contributivo": "Contributivo",
        "subsidiado": "Subsidiado",
        "especial": "Especial o de excepción",
        "particular": "Particular",
    },
    "tipo_consulta": {"primera_vez": "Primera vez", "control": "Control"},
    "finalidad": {
        "diagnostico": "Diagnóstico",
        "tratamiento": "Tratamiento",
        "promocion_prevencion": "Promoción y prevención",
        "rehabilitacion": "Rehabilitación",
    },
    "causa": {
        "enfermedad_general": "Enfermedad general",
        "enfermedad_laboral": "Enfermedad laboral",
        "accidente_trabajo": "Accidente de trabajo",
        "accidente_transito": "Accidente de tránsito",
        "otro_accidente": "Otro tipo de accidente",
        "lesion_por_agresion": "Lesión por agresión",
        "otra": "Otra",
    },
    "tipo_diagnostico": {
        "impresion_diagnostica": "Impresión diagnóstica",
        "confirmado_nuevo": "Confirmado nuevo",
        "confirmado_repetido": "Confirmado repetido",
    },
    "destino": {"casa": "A casa", "remitido": "Remitido a otro prestador"},
    "via": {
        "oral": "Oral",
        "sublingual": "Sublingual",
        "topica": "Tópica",
        "inhalada": "Inhalada",
        "nasal": "Nasal",
        "oftalmica": "Oftálmica",
        "otica": "Ótica",
        "intramuscular": "Intramuscular",
        "intravenosa": "Intravenosa",
        "subcutanea": "Subcutánea",
        "rectal": "Rectal",
        "vaginal": "Vaginal",
        "transdermica": "Transdérmica",
    },
}


@dataclass(frozen=True)
class Campo:
    nombre: str
    clase: Clase = "texto"
    obligatorio: bool = False
    lista: str | None = None
    minimo: Decimal | None = None
    maximo: Decimal | None = None
    largo: int = LARGO_DE_TEXTO
    unidad: str | None = None


def _signo(nombre: str, minimo: str, maximo: str, unidad: str, clase: Clase = "entero") -> Campo:
    return Campo(nombre, clase, True, minimo=Decimal(minimo), maximo=Decimal(maximo), unidad=unidad)


# Los datos de la atención, en el orden del formulario (diseno/05-pantallas.md, M-15).
CAMPOS_DE_LA_ATENCION: dict[str, Campo] = {
    "tipo_consulta": Campo("Tipo de consulta", "opcion", True, "tipo_consulta"),
    "finalidad": Campo("Finalidad", "opcion", True, "finalidad"),
    "causa": Campo("Causa que motiva la atención", "opcion", True, "causa"),
    "acompanante_nombre": Campo("Acompañante", largo=LARGO_DE_DATO_CORTO),
    "acompanante_telefono": Campo("Teléfono del acompañante", largo=30),
    "acompanante_parentesco": Campo("Parentesco del acompañante", largo=60),
    "motivo": Campo("Motivo de consulta", obligatorio=True),
    "enfermedad_actual": Campo("Enfermedad actual", obligatorio=True),
    "antecedentes_personales": Campo("Antecedentes personales", obligatorio=True),
    "antecedentes_familiares": Campo("Antecedentes familiares", obligatorio=True),
    "alergias": Campo("Alergias", obligatorio=True),
    "factores_riesgo": Campo("Factores de riesgo", obligatorio=True),
    "revision_sistemas": Campo("Revisión por sistemas", obligatorio=True),
    "sintomatico_respiratorio": Campo("Sintomático respiratorio", "si_no"),
    "sintomatico_piel": Campo("Sintomático de piel", "si_no"),
    "tension_sistolica": _signo("Tensión arterial sistólica", "50", "260", "mmHg"),
    "tension_diastolica": _signo("Tensión arterial diastólica", "30", "160", "mmHg"),
    "frecuencia_cardiaca": _signo("Frecuencia cardiaca", "20", "250", "lat/min"),
    "frecuencia_respiratoria": _signo("Frecuencia respiratoria", "5", "60", "resp/min"),
    "temperatura": _signo("Temperatura", "30", "45", "°C", "decimal"),
    "saturacion": Campo(
        "Saturación de oxígeno", "entero", minimo=Decimal(50), maximo=Decimal(100), unidad="%"
    ),
    "peso": _signo("Peso", "1", "350", "kg", "decimal"),
    "talla": _signo("Talla", "30", "250", "cm"),
    "examen_fisico": Campo("Examen físico", obligatorio=True),
    "analisis": Campo("Análisis"),
    "plan": Campo("Plan de manejo", obligatorio=True),
    "recomendaciones": Campo("Recomendaciones y signos de alarma"),
    "ordenes": Campo("Órdenes de exámenes o procedimientos"),
    "incapacidad_dias": Campo(
        "Incapacidad", "entero", minimo=Decimal(0), maximo=Decimal(180), unidad="días"
    ),
    "destino": Campo("Cómo termina la atención", "opcion", True, "destino"),
    "remitido_a": Campo("Remitido a", largo=LARGO_DE_DATO_CORTO),
}

# Lo que el artículo 9 de la Resolución 1995 pide para identificar al paciente y el registro no
# pregunta (HU-041). La pertenencia étnica, la zona y el nivel escolar los pide la 866 y no
# frenan el cierre: se exigirán cuando se envíe el resumen de atención.
CAMPOS_DE_IDENTIFICACION: dict[str, Campo] = {
    "sexo": Campo("Sexo", "opcion", True, "sexo"),
    "estado_civil": Campo("Estado civil", "opcion", True, "estado_civil"),
    "ocupacion": Campo("Ocupación", obligatorio=True, largo=120),
    "nivel_escolar": Campo("Nivel escolar", "opcion", lista="nivel_escolar"),
    "pertenencia_etnica": Campo("Pertenencia étnica", "opcion", lista="pertenencia_etnica"),
    "direccion": Campo("Dirección", obligatorio=True, largo=LARGO_DE_DATO_CORTO),
    "municipio": Campo("Municipio de residencia", obligatorio=True, largo=120),
    "zona": Campo("Zona", "opcion", lista="zona"),
    "tipo_vinculacion": Campo("Tipo de vinculación", "opcion", True, "tipo_vinculacion"),
    "aseguradora": Campo("Aseguradora", largo=120),
    "responsable_nombre": Campo("Persona responsable", largo=120),
    "responsable_telefono": Campo("Teléfono del responsable", largo=30),
    "responsable_parentesco": Campo("Parentesco del responsable", largo=60),
}

Valor = str | int | Decimal | bool | None


def revisar(cambios: Mapping[str, object], campos: Mapping[str, Campo]) -> dict[str, Valor]:
    """Revisa un borrador: cada valor con su tipo y su rango. Vacío es válido mientras está abierto.

    Lanza DatosInvalidos con un mensaje por cada campo que no sirve, como "revise la temperatura"
    ante un valor imposible (HU-043, CA-4).
    """
    errores: dict[str, str] = {}
    limpios: dict[str, Valor] = {}
    for clave, crudo in cambios.items():
        campo = campos.get(clave)
        if campo is None:
            errores[clave] = "Ese dato no existe en la historia clínica"
            continue
        try:
            limpios[clave] = _limpio(campo, crudo)
        except ValueError as error:
            errores[clave] = str(error)
    if errores:
        raise DatosInvalidos(errores)
    return limpios


def _limpio(campo: Campo, crudo: object) -> Valor:
    if crudo is None or (isinstance(crudo, str) and not crudo.strip()):
        return None
    if campo.clase == "si_no":
        if not isinstance(crudo, bool):
            raise ValueError("Elija sí o no")
        return crudo
    if campo.clase == "opcion":
        assert campo.lista is not None
        if crudo not in LISTAS[campo.lista]:
            raise ValueError("Elija una de las opciones")
        return str(crudo)
    if campo.clase == "texto":
        if not isinstance(crudo, str):
            raise ValueError("Escriba un texto")
        texto = crudo.strip()
        if len(texto) > campo.largo:
            raise ValueError(f"Máximo {campo.largo} caracteres")
        return texto
    try:
        numero = Decimal(str(crudo).replace(",", "."))
    except InvalidOperation:
        raise ValueError("Escriba un número") from None
    if campo.clase == "entero" and numero != numero.to_integral_value():
        raise ValueError("Escriba un número entero")
    if (campo.minimo is not None and numero < campo.minimo) or (
        campo.maximo is not None and numero > campo.maximo
    ):
        unidad = f" {campo.unidad}" if campo.unidad else ""
        rango = f"{campo.minimo} y {campo.maximo}{unidad}"
        raise ValueError(f"Revise el valor: debe estar entre {rango}")
    return int(numero) if campo.clase == "entero" else numero.quantize(Decimal("0.1"))


def indice_de_masa_corporal(peso: Decimal | None, talla: int | None) -> Decimal | None:
    """Se calcula, no se guarda (HU-043, CA-4)."""
    if not peso or not talla:
        return None
    metros = Decimal(talla) / 100
    return (Decimal(peso) / (metros * metros)).quantize(Decimal("0.1"))


@dataclass(frozen=True)
class Diagnostico:
    codigo: str
    nombre: str
    tipo: str
    principal: bool


@dataclass(frozen=True)
class Medicamento:
    nombre: str
    dosis: str
    via: str
    frecuencia: str
    dias: int
    indicaciones: str | None = None


def revisar_diagnosticos(
    crudos: Sequence[Mapping[str, object]], nombres: Mapping[str, str]
) -> list[Diagnostico]:
    """Cada uno de la lista CIE-10, con su tipo; uno solo es el principal (HU-043, CA-2).

    `nombres` trae el nombre oficial de los códigos pedidos: el nombre no lo escribe la pantalla.
    """
    errores: dict[str, str] = {}
    diagnosticos: list[Diagnostico] = []
    vistos: set[str] = set()
    for posicion, crudo in enumerate(crudos):
        codigo = str(crudo.get("codigo") or "").strip().upper()
        tipo = str(crudo.get("tipo") or "")
        if codigo not in nombres:
            errores[f"diagnosticos.{posicion}"] = "Elija un diagnóstico de la lista CIE-10"
            continue
        if tipo not in LISTAS["tipo_diagnostico"]:
            errores[f"diagnosticos.{posicion}"] = "Elija el tipo de diagnóstico"
            continue
        if codigo in vistos:
            errores[f"diagnosticos.{posicion}"] = "Ese diagnóstico ya está en la lista"
            continue
        vistos.add(codigo)
        diagnosticos.append(
            Diagnostico(codigo, nombres[codigo], tipo, bool(crudo.get("principal")))
        )
    if sum(d.principal for d in diagnosticos) > 1:
        errores["diagnosticos"] = "Solo un diagnóstico puede ser el principal"
    if errores:
        raise DatosInvalidos(errores)
    return diagnosticos


def revisar_medicamentos(crudos: Sequence[Mapping[str, object]]) -> list[Medicamento]:
    """La fórmula con lo que pide la Resolución 866: dosis, vía, frecuencia y duración (CA-6)."""
    errores: dict[str, str] = {}
    medicamentos: list[Medicamento] = []
    for posicion, crudo in enumerate(crudos):
        clave = f"medicamentos.{posicion}"
        partes = {k: str(crudo.get(k) or "").strip() for k in ("nombre", "dosis", "frecuencia")}
        faltan = [k for k, v in partes.items() if not v]
        via = str(crudo.get("via") or "")
        if faltan:
            errores[clave] = "Falta " + ", ".join(faltan)
            continue
        if via not in LISTAS["via"]:
            errores[clave] = "Elija la vía de administración"
            continue
        try:
            dias = int(str(crudo.get("dias")))
        except ValueError:
            errores[clave] = "Escriba los días de tratamiento"
            continue
        if not 1 <= dias <= 365:
            errores[clave] = "Los días van de 1 a 365"
            continue
        if any(len(v) > LARGO_DE_DATO_CORTO for v in partes.values()):
            errores[clave] = f"Máximo {LARGO_DE_DATO_CORTO} caracteres por dato"
            continue
        indicaciones = str(crudo.get("indicaciones") or "").strip() or None
        medicamentos.append(
            Medicamento(
                partes["nombre"], partes["dosis"], via, partes["frecuencia"], dias, indicaciones
            )
        )
    if errores:
        raise DatosInvalidos(errores)
    return medicamentos


@dataclass(frozen=True)
class Faltantes:
    """Lo que impide cerrar, con el nombre que ve el médico (HU-041, CA-3; HU-044, CA-2)."""

    identificacion: list[str] = field(default_factory=list)
    atencion: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self.identificacion or self.atencion)


class FaltanDatos(Exception):
    def __init__(self, faltantes: Faltantes) -> None:
        super().__init__("Faltan datos para cerrar la atención")
        self.faltantes = faltantes


def faltantes(
    atencion: Mapping[str, object],
    diagnosticos: Sequence[Diagnostico],
    identificacion: Mapping[str, object],
) -> Faltantes:
    def vacios(datos: Mapping[str, object], campos: Mapping[str, Campo]) -> list[str]:
        return [
            c.nombre
            for clave, c in campos.items()
            if c.obligatorio and datos.get(clave) in (None, "")
        ]

    de_la_atencion = vacios(atencion, CAMPOS_DE_LA_ATENCION)
    if not any(d.principal for d in diagnosticos):
        de_la_atencion.append("Diagnóstico principal")
    if atencion.get("destino") == "remitido" and not atencion.get("remitido_a"):
        de_la_atencion.append("Remitido a")

    de_identificacion = vacios(identificacion, CAMPOS_DE_IDENTIFICACION)
    # Un paciente particular no tiene aseguradora (HU-041, CA-4).
    if identificacion.get("tipo_vinculacion") not in (
        None,
        "particular",
    ) and not identificacion.get("aseguradora"):
        de_identificacion.append("Aseguradora")
    return Faltantes(de_identificacion, de_la_atencion)


# Los antecedentes pasan de la última atención cerrada a la nueva para confirmarlos (CA-5).
ANTECEDENTES = ("antecedentes_personales", "antecedentes_familiares", "alergias", "factores_riesgo")


class AtencionYaAbierta(Exception):
    """El paciente ya tiene una atención abierta: se sigue en esa (HU-042, CA-6)."""


class AtencionCerrada(Exception):
    """Una atención cerrada no se modifica: se corrige con una nota aclaratoria."""


class ContrasenaIncorrecta(Exception):
    """La contraseña con que se quiso firmar no es la del médico."""
