"""Reglas del asistente: qué se le dice al modelo y cómo se comprueba lo que cita (D-30).

Diseño en diseno/04-asistente-ia.md, secciones 5.2 a 5.4. El modelo recibe los fragmentos
encontrados con una etiqueta por documento (D1, D2...) y debe citar así:
[D2, pág. 1: "frase copiada del fragmento"]. El servidor revisa cada cita antes de mostrarla.
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from uuid import UUID

INSTRUCCIONES = """Eres un asistente que ayuda a un médico a consultar los documentos que entregó \
un paciente.
1. Responde únicamente con lo que está escrito en los fragmentos que recibes.
2. Después de cada dato indica su origen con la etiqueta del documento, la página y la frase \
exacta en que te basas, copiada entre comillas, así: [D2, pág. 1: "frase copiada"].
3. Si la información no aparece en los fragmentos, responde "No lo encontré en los documentos \
ni en las atenciones". No supongas ni completes.
4. No des diagnósticos ni recomiendes tratamientos. Si te lo piden, aclara que solo resumes lo \
registrado.
5. Si dos fragmentos se contradicen, muestra ambos datos con su origen.
6. Responde en español, de forma breve y en orden de fecha.
7. Los datos del paciente aparecen como [PACIENTE], [DOCUMENTO], [TELÉFONO] o [CORREO]; \
no intentes adivinarlos."""

AVISO = (
    "El asistente es un apoyo: resume lo que está escrito y puede equivocarse. "
    "No reemplaza la lectura del documento."
)

NO_ENCONTRADO = "No lo encontré en los documentos ni en las atenciones"


class SinFragmentos(Exception):
    """El paciente todavía no tiene documentos indexados: no hay sobre qué preguntar."""


class TopeDeConsultas(Exception):
    """Se llegó al máximo de preguntas por hora."""

    def __init__(self, tope: int) -> None:
        super().__init__(f"Máximo {tope} preguntas por hora")
        self.tope = tope


@dataclass(frozen=True)
class FragmentoParaContexto:
    documento_id: UUID
    documento: str
    fecha_documento: date
    pagina: int
    texto: str


@dataclass(frozen=True)
class Contexto:
    texto: str
    # Etiqueta que vio el modelo (D1, D2...) y documento al que corresponde.
    etiquetas: dict[str, UUID]
    fragmentos: tuple[FragmentoParaContexto, ...]


def armar_contexto(fragmentos: Sequence[FragmentoParaContexto]) -> Contexto:
    """Agrupa por documento en orden de fecha; dentro de cada uno, por página (sección 5.2)."""
    por_documento: dict[UUID, list[FragmentoParaContexto]] = {}
    for fragmento in fragmentos:
        por_documento.setdefault(fragmento.documento_id, []).append(fragmento)
    ordenados = sorted(
        por_documento.values(), key=lambda grupo: (grupo[0].fecha_documento, grupo[0].documento)
    )

    bloques: list[str] = []
    etiquetas: dict[str, UUID] = {}
    for numero, grupo in enumerate(ordenados, 1):
        etiqueta = f"D{numero}"
        primero = grupo[0]
        etiquetas[etiqueta] = primero.documento_id
        partes = [f"=== {etiqueta} · {primero.documento} · {primero.fecha_documento:%d/%m/%Y} ==="]
        partes += [
            f"[{etiqueta}, pág. {f.pagina}]\n{f.texto}"
            for f in sorted(grupo, key=lambda f: f.pagina)
        ]
        bloques.append("\n\n".join(partes))
    return Contexto("\n\n".join(bloques), etiquetas, tuple(fragmentos))


@dataclass(frozen=True)
class Cita:
    etiqueta: str
    pagina: int
    frase: str


# [D2, pág. 1: "frase"]. Acepta "pag", comillas tipográficas y la frase vacía.
_CITA = re.compile(
    r"\[\s*(D\d+)\s*,\s*p[áa]g(?:ina)?\.?\s*(\d+)\s*(?::\s*[\"“«](.*?)[\"”»]\s*)?\]",
    re.IGNORECASE | re.DOTALL,
)


def extraer_citas(respuesta: str) -> list[Cita]:
    return [
        Cita(m.group(1).upper(), int(m.group(2)), (m.group(3) or "").strip())
        for m in _CITA.finditer(respuesta)
    ]


@dataclass(frozen=True)
class OrigenComprobado:
    etiqueta: str
    documento_id: UUID
    documento: str
    pagina: int
    frase: str
    # False: el documento y la página se enviaron, pero la frase no aparece tal cual.
    verificado: bool


def _plano(texto: str) -> str:
    # Las comillas tipográficas valen como comillas rectas.
    texto = texto.translate({0x201C: '"', 0x201D: '"', 0x2019: "'"})
    return re.sub(r"\s+", " ", texto).strip().casefold()


def comprobar_origenes(respuesta: str, contexto: Contexto) -> list[OrigenComprobado]:
    """Revisa cada cita contra lo que se envió en esta consulta (sección 5.4).

    Una cita a un documento o una página que no se envió se descarta. Si se envió pero la frase
    no aparece en el texto de esa página, queda como origen sin verificar.
    """
    origenes: list[OrigenComprobado] = []
    vistos: set[tuple[str, int, str]] = set()
    for cita in extraer_citas(respuesta):
        documento_id = contexto.etiquetas.get(cita.etiqueta)
        enviados = [
            f
            for f in contexto.fragmentos
            if f.documento_id == documento_id and f.pagina == cita.pagina
        ]
        clave = (cita.etiqueta, cita.pagina, _plano(cita.frase))
        if not enviados or clave in vistos:
            continue
        vistos.add(clave)
        verificado = bool(cita.frase) and any(
            _plano(cita.frase) in _plano(f.texto) for f in enviados
        )
        origenes.append(
            OrigenComprobado(
                cita.etiqueta,
                enviados[0].documento_id,
                enviados[0].documento,
                cita.pagina,
                cita.frase,
                verificado,
            )
        )
    return origenes


@dataclass(frozen=True)
class Consultado:
    """Un documento que recibió el asistente y las páginas que se le enviaron (HU-034, CA-7)."""

    documento_id: UUID
    documento: str
    fecha_documento: date
    paginas: tuple[int, ...]


def lo_consultado(contexto: Contexto) -> list[Consultado]:
    paginas: dict[UUID, set[int]] = {}
    datos: dict[UUID, FragmentoParaContexto] = {}
    for f in contexto.fragmentos:
        paginas.setdefault(f.documento_id, set()).add(f.pagina)
        datos.setdefault(f.documento_id, f)
    return sorted(
        (
            Consultado(d, datos[d].documento, datos[d].fecha_documento, tuple(sorted(p)))
            for d, p in paginas.items()
        ),
        key=lambda c: (c.fecha_documento, c.documento),
    )
