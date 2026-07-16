"""Leitura e extração de texto de arquivos PDF."""

import logging
from pathlib import Path

import pdfplumber


LOGGER = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrai o texto de todas as páginas de um arquivo PDF."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

    LOGGER.info("Iniciando leitura do PDF: %s", pdf_path)

    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = [page.extract_text() or "" for page in pdf.pages]
    except Exception as error:
        raise RuntimeError(f"Falha ao ler o PDF '{pdf_path}'.") from error

    text = "\n".join(pages_text).strip()
    if not text:
        raise ValueError(f"O PDF '{pdf_path}' não possui texto extraível.")

    LOGGER.info("Texto extraído com sucesso de %s página(s).", len(pages_text))
    return text
