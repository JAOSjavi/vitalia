"""Cómo se parte una página en fragmentos y qué se tapa antes de enviarla al proveedor."""

import itertools

from vitalia.dominio.fragmentos import (
    REPETIDO,
    TOPE,
    Identificadores,
    partir_pagina,
    retirar_identificadores,
)

HERNANDO = Identificadores(
    nombres="Hernando",
    apellidos="Castaño Ríos",
    numero_documento="79482615",
    telefono="3104827713",
    correo="hernando.castano@ejemplo.test",
)


def pagina_larga() -> str:
    frases = [
        f"Frase número {n} de la historia, con tensión arterial de 1{n:02d}/80 mmHg."
        for n in range(60)
    ]
    return "\n".join(frases)


def test_una_pagina_corta_es_un_solo_fragmento() -> None:
    assert partir_pagina("  Motivo de consulta: control.  ") == ["Motivo de consulta: control."]
    assert partir_pagina("   ") == []


def test_ningun_fragmento_pasa_del_tope_y_cortan_en_fin_de_frase() -> None:
    trozos = partir_pagina(pagina_larga())

    assert len(trozos) > 1
    assert all(len(t) <= TOPE for t in trozos)
    assert all(t.endswith("mmHg.") for t in trozos)


def test_cada_fragmento_repite_el_final_del_anterior() -> None:
    trozos = partir_pagina(pagina_larga())

    for anterior, siguiente in itertools.pairwise(trozos):
        # Las frases miden menos que lo que se repite: la última pasa entera al siguiente.
        ultima_frase = anterior.split("\n")[-1]
        assert len(ultima_frase) < REPETIDO
        assert ultima_frase in siguiente


def test_no_se_pierde_ninguna_frase() -> None:
    texto = pagina_larga()
    trozos = partir_pagina(texto)

    for frase in texto.split("\n"):
        assert any(frase in t for t in trozos), frase


def test_una_frase_mas_larga_que_el_tope_se_parte_en_palabras() -> None:
    trozos = partir_pagina("palabra " * 400)

    assert all(len(t) <= TOPE for t in trozos)


def test_tapa_el_nombre_con_o_sin_tildes_y_en_mayusculas() -> None:
    texto = (
        "Nombres y apellidos: Hernando Castaño Ríos\n"
        "PACIENTE HERNANDO CASTANO RIOS, 58 años.\n"
        "El señor Castaño refiere cefalea."
    )

    limpio = retirar_identificadores(texto, HERNANDO)

    assert "Hernando" not in limpio and "HERNANDO" not in limpio
    assert "Castaño" not in limpio and "CASTANO" not in limpio
    assert limpio.count("[PACIENTE]") == 3
    assert "Nombres y apellidos: [PACIENTE]" in limpio
    assert "refiere cefalea" in limpio


def test_tapa_documento_telefono_y_correo_aunque_lleven_puntos_o_espacios() -> None:
    texto = (
        "Documento: Cédula de ciudadanía 79.482.615\n"
        "Teléfono: 310 482 7713 · Correo: Hernando.Castano@ejemplo.test"
    )

    limpio = retirar_identificadores(texto, HERNANDO)

    assert limpio == (
        "Documento: Cédula de ciudadanía [DOCUMENTO]\nTeléfono: [TELÉFONO] · Correo: [CORREO]"
    )


def test_no_toca_otros_numeros_ni_otras_personas() -> None:
    texto = (
        "Colesterol LDL: 168 mg/dL. Registro médico 11-4417-18. NIT 900.000.111-1.\n"
        "Persona responsable: Luz Marina Peña Duarte · 311 905 2284\n"
        "Documento del médico 80.214.637; número 794826150 no es el suyo."
    )

    assert retirar_identificadores(texto, HERNANDO) == texto
