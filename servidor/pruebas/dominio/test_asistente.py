"""Lo que recibe el modelo y cómo se comprueba lo que cita (diseño del asistente, 5.2 a 5.4)."""

from datetime import date
from uuid import uuid4

from vitalia.dominio.asistente import (
    FragmentoParaContexto,
    armar_contexto,
    comprobar_origenes,
    etiquetas_por_orden_de_subida,
    extraer_citas,
    lo_consultado,
)

FEBRERO, MAYO = uuid4(), uuid4()


def fragmento(documento: object, pagina: int, texto: str) -> FragmentoParaContexto:
    if documento is FEBRERO:
        return FragmentoParaContexto(
            FEBRERO, "Control de febrero", date(2026, 2, 12), pagina, texto
        )
    return FragmentoParaContexto(MAYO, "Control de mayo", date(2026, 5, 14), pagina, texto)


# Llegan en el orden de la búsqueda, no en el de las fechas.
ENCONTRADOS = [
    fragmento(MAYO, 2, "Colesterol LDL: 112 mg/dL. Transaminasa ALT: 31 U/L."),
    fragmento(FEBRERO, 3, "Colesterol LDL: 168 mg/dL.\nGlucemia en ayunas: 98 mg/dL."),
    fragmento(FEBRERO, 1, "Alérgicos: Medicamentoso: ibuprofeno. Presentó angioedema."),
]


def test_cada_documento_lleva_su_etiqueta_en_orden_de_fecha() -> None:
    contexto = armar_contexto(ENCONTRADOS)

    assert contexto.etiquetas == {"D1": FEBRERO, "D2": MAYO}
    texto = contexto.texto
    assert texto.index("=== D1 · Control de febrero · 12/02/2026 ===") < texto.index("=== D2")
    # Dentro de un documento, por página.
    assert texto.index("[D1, pág. 1]") < texto.index("[D1, pág. 3]")
    assert "[D2, pág. 2]\nColesterol LDL: 112 mg/dL." in texto


def test_reconoce_las_citas_con_su_frase() -> None:
    respuesta = (
        'LDL de 168 [D1, pág. 3: "Colesterol LDL: 168 mg/dL"] y luego 112 '
        "[d2, pag 2: “Colesterol LDL: 112 mg/dL”]. Alergia [D1, página 1]."
    )

    citas = extraer_citas(respuesta)

    assert [(c.etiqueta, c.pagina, c.frase) for c in citas] == [
        ("D1", 3, "Colesterol LDL: 168 mg/dL"),
        ("D2", 2, "Colesterol LDL: 112 mg/dL"),
        ("D1", 1, ""),
    ]


def test_comprueba_cada_cita_contra_lo_que_se_envio() -> None:
    contexto = armar_contexto(ENCONTRADOS)
    respuesta = (
        'El LDL fue 168 [D1, pág. 3: "colesterol  LDL: 168 mg/dL"]. '  # bien, aunque cambie
        'Toma losartán [D1, pág. 1: "losartán 50 mg"]. '  # la página se envió; la frase no está
        'Glucemia 98 [D1, pág. 2: "Glucemia en ayunas: 98"]. '  # esa página no se envió
        'Peso 84 kg [D7, pág. 1: "Peso: 84,0 kg"]. '  # ese documento no existe
        'Otra vez [D1, pág. 3: "Colesterol LDL: 168 mg/dL"].'  # repetida
    )

    origenes = comprobar_origenes(respuesta, contexto)

    assert [(o.etiqueta, o.pagina, o.verificado) for o in origenes] == [
        ("D1", 3, True),
        ("D1", 1, False),
    ]
    assert origenes[0].documento_id == FEBRERO
    assert origenes[0].documento == "Control de febrero"


def test_una_cita_sin_frase_no_queda_verificada() -> None:
    origenes = comprobar_origenes("Alergia [D1, pág. 1].", armar_contexto(ENCONTRADOS))

    assert [(o.etiqueta, o.verificado) for o in origenes] == [("D1", False)]


def test_lo_consultado_lista_documentos_y_paginas() -> None:
    consultado = lo_consultado(armar_contexto(ENCONTRADOS))

    assert [(c.documento, c.paginas) for c in consultado] == [
        ("Control de febrero", (1, 3)),
        ("Control de mayo", (2,)),
    ]


def test_las_etiquetas_siguen_el_orden_de_subida_y_no_el_de_la_busqueda() -> None:
    primero, segundo = sorted([FEBRERO, MAYO])
    etiquetas = etiquetas_por_orden_de_subida([segundo, primero])

    contexto = armar_contexto([f for f in ENCONTRADOS if f.documento_id == segundo], etiquetas)

    assert etiquetas == {primero: "D1", segundo: "D2"}
    assert contexto.etiquetas == {"D2": segundo}
    assert "=== D2 ·" in contexto.texto
