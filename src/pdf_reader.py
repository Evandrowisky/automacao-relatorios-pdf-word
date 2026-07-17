"""Leitura e extração de texto de arquivos PDF."""

import logging
from pathlib import Path
from typing import TypedDict

import pdfplumber


LOGGER = logging.getLogger(__name__)


class PageExtraction(TypedDict):
    """Representa o texto extraído de uma página."""

    numero: int
    texto: str


class PdfExtraction(TypedDict):
    """Representa o resultado completo da extração de um PDF."""

    arquivo: str
    paginas: list[PageExtraction]
    texto_completo: str


def extract_pdf_content(pdf_path: Path) -> PdfExtraction:
    """Extrai texto por página e também o texto completo do PDF."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

    LOGGER.info("Iniciando leitura do PDF: %s", pdf_path)

    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = [
                {"numero": index, "texto": page.extract_text() or ""}
                for index, page in enumerate(pdf.pages, start=1)
            ]
    except Exception as error:
        raise RuntimeError(f"Falha ao ler o PDF '{pdf_path}'.") from error

    full_text = "\n\n".join(page["texto"] for page in pages).strip()
    if not full_text:
        raise ValueError(f"O PDF '{pdf_path}' não possui texto extraível.")

    LOGGER.info("Texto extraído com sucesso de %s página(s).", len(pages))
    return {
        "arquivo": pdf_path.name,
        "paginas": pages,
        "texto_completo": full_text,
    }


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrai o texto completo do PDF mantendo compatibilidade anterior."""

    return extract_pdf_content(pdf_path)["texto_completo"]
