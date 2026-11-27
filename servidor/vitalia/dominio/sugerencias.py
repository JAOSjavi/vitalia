"""Sugerencias para la historia clínica con los documentos del paciente (HU-047, D-36).

El modelo recibe los fragmentos del paciente y devuelve, en JSON, un valor por campo con las
frases en que se basa. Aquí se decide qué se le pide, cómo se lee lo que devuelve y qué se
descarta: un campo solo queda si al menos una de sus frases está tal cual en lo enviado.
"""

import json
import re
from dataclasses import dataclass

from vitalia.dominio.asistente import Contexto, OrigenComprobado, comprobar_origenes

# Lo que se puede sugerir y con qué se busca en los documentos de cada uno. Diagnóstico, plan,
# fórmula y órdenes quedan fuera: la autorización v1 dice que la IA no diagnostica ni
# recomienda tratamientos. La identificación también: se tapa antes de enviar.
CONSULTAS: dict[str, str] = {
    "antecedentes_personales": (
        "antecedentes personales patológicos, enfermedades diagnosticadas, cirugías, "
        "hospitalizaciones, medicamentos que toma"
    ),
    "antecedentes_familiares": "antecedentes familiares, enfermedades del padre, madre, hermanos",
    "alergias": "alergias a medicamentos o alimentos, reacciones adversas",
    "factores_riesgo": "tabaquismo, consumo de alcohol, sedentarismo, actividad física, exposición",
    "enfermedad_actual": "evolución, control, seguimiento, síntomas, resultados recientes",
}

LARGO_MAXIMO_DEL_VALOR = 1500

INSTRUCCIONES = """Ayudas a un médico a llenar la historia clínica de la consulta de hoy con lo \
que dicen los documentos que entregó el paciente.
1. Usa únicamente lo que está escrito en los fragmentos. No supongas ni completes.
2. Llena solo estos campos:
   - antecedentes_personales: enfermedades, cirugías, hospitalizaciones y medicamentos que toma.
   - antecedentes_familiares: enfermedades de sus familiares, diciendo el parentesco.
   - alergias: a qué y qué reacción produjo.
   - factores_riesgo: tabaco, alcohol, actividad física, exposiciones.
   - enfermedad_actual: cómo estaban sus problemas de salud en el documento más reciente, en \
dos o tres frases con la fecha de ese documento.
3. Si los fragmentos no dicen nada de un campo, no lo incluyas. No escribas "No refiere": que \
un documento no lo mencione no significa que el paciente no lo tenga.
4. Si un dato cambió con el tiempo (medicamentos, tabaco, dosis), escribe solo el más reciente \
con su fecha.
5. No des diagnósticos nuevos ni recomiendes tratamientos. No comentes sobre los fragmentos.
6. Escribe cada valor en español, breve, como lo anotaría un médico.
7. Cada campo lleva una o dos citas: la etiqueta del documento (D1, D2...), la página y una \
frase corta, de menos de 15 palabras, copiada exacta y seguida de los fragmentos, sin \
puntos suspensivos.
8. Los datos del paciente aparecen como [PACIENTE], [DOCUMENTO], [TELÉFONO] o [CORREO]; no \
intentes adivinarlos.
Responde solo con un objeto JSON con esta forma:
{"campos": [{"campo": "alergias", "valor": "texto", "citas": [{"documento": "D1", \
"pagina": 1, "frase": "frase copiada"}]}]}"""


@dataclass(frozen=True)
class Sugerencia:
    campo: str
    valor: str
    # Solo las frases comprobadas: una sugerencia sin ninguna no llega a la pantalla.
    origenes: tuple[OrigenComprobado, ...]


class RespuestaIlegible(Exception):
    """El modelo no devolvió el JSON pedido."""


def leer_sugerencias(respuesta: str, contexto: Contexto) -> list[Sugerencia]:
    """Lee el JSON del modelo y se queda con lo que está respaldado por lo enviado.

    Se descarta un campo que no está en CONSULTAS, un valor vacío y un campo sin ninguna frase
    que aparezca tal cual en el fragmento citado. Las frases que no aparecen se quitan.
    """
    try:
        datos = json.loads(_sin_cercas(respuesta))
    except ValueError as error:
        raise RespuestaIlegible() from error
    campos = datos.get("campos") if isinstance(datos, dict) else None
    if not isinstance(campos, list):
        raise RespuestaIlegible()

    sugerencias: dict[str, Sugerencia] = {}
    for item in campos:
        if not isinstance(item, dict):
            continue
        campo, valor, citas = item.get("campo"), item.get("valor"), item.get("citas")
        if campo not in CONSULTAS or campo in sugerencias or not isinstance(valor, str):
            continue
        valor = valor.strip()[:LARGO_MAXIMO_DEL_VALOR]
        if not valor or not isinstance(citas, list):
            continue
        # Se pasa al formato de cita del asistente para comprobarlas con la misma regla.
        texto = " ".join(t for c in citas if isinstance(c, dict) for t in _como_citas(c))
        comprobados = tuple(o for o in comprobar_origenes(texto, contexto) if o.verificado)
        if comprobados:
            sugerencias[campo] = Sugerencia(campo, valor, comprobados)
    return [sugerencias[c] for c in CONSULTAS if c in sugerencias]


def _como_citas(cita: dict[str, object]) -> list[str]:
    """Una cita del JSON en el formato del asistente: [D1, pág. 1: "frase"].

    Si el modelo recortó la frase con puntos suspensivos, cada pedazo va como una cita aparte:
    así cada uno se comprueba tal cual y no se descarta un dato bien citado.
    """
    documento = str(cita.get("documento", "")).strip()
    pagina = str(cita.get("pagina", "")).strip()
    if not pagina.isdigit():
        return []
    pedazos = re.split(r"\.{3}|…", str(cita.get("frase", "")))
    return [f'[{documento}, pág. {pagina}: "{p.strip()}"]' for p in pedazos if p.strip()]


def _sin_cercas(respuesta: str) -> str:
    """Algunos modelos envuelven el JSON en ```json ... ``` aunque se les pida que no."""
    texto = respuesta.strip()
    if texto.startswith("```"):
        texto = texto.split("\n", 1)[1] if "\n" in texto else ""
        texto = texto.rsplit("```", 1)[0]
    return texto
