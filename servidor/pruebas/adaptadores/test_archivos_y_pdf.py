"""Guardar archivos en la carpeta local y leer PDF con pypdfium2."""

from pathlib import Path

import pytest

from conftest import pdf_con_texto
from vitalia.adaptadores.archivos_en_disco import ArchivosEnDisco
from vitalia.adaptadores.pdf import LectorPdfium
from vitalia.casos_de_uso.puertos import Archivos, LectorDePDF


async def test_guarda_lee_y_borra_un_archivo(tmp_path: Path) -> None:
    archivos: Archivos = ArchivosEnDisco(tmp_path)

    await archivos.guardar("documentos/a.pdf", b"%PDF-1.4 contenido")
    assert await archivos.leer("documentos/a.pdf") == b"%PDF-1.4 contenido"

    await archivos.borrar("documentos/a.pdf")
    await archivos.borrar("documentos/a.pdf")  # borrar dos veces no falla
    assert not (tmp_path / "documentos" / "a.pdf").exists()
    assert list((tmp_path / "documentos").iterdir()) == []  # sin temporales a medias


async def test_una_clave_no_puede_salir_de_la_carpeta(tmp_path: Path) -> None:
    archivos = ArchivosEnDisco(tmp_path / "archivos")

    with pytest.raises(ValueError):
        await archivos.guardar("../fuera.pdf", b"x")


async def test_lee_el_texto_de_cada_pagina_en_orden() -> None:
    pdf: LectorDePDF = LectorPdfium()

    textos = await pdf.textos(
        pdf_con_texto("Motivo de consulta: control.\nTensión arterial 128/80 mmHg", "", "Fin")
    )

    assert textos == ["Motivo de consulta: control.\nTensión arterial 128/80 mmHg", "", "Fin"]


async def test_dibuja_una_pagina_como_imagen_png() -> None:
    imagen = await LectorPdfium().imagen_de_pagina(pdf_con_texto("Uno", "Dos"), 2)

    assert imagen.startswith(b"\x89PNG\r\n\x1a\n")
    assert imagen.endswith(b"IEND\xaeB`\x82")


async def test_un_pdf_danado_lanza_un_error() -> None:
    with pytest.raises(Exception):  # noqa: B017  # pdfium usa su propio tipo de error
        await LectorPdfium().textos(b"%PDF-1.4 esto no es un pdf")
