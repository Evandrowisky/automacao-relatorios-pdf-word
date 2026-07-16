"""Conversão de documentos Word para PDF."""

import logging
from pathlib import Path

from docx2pdf import convert


LOGGER = logging.getLogger(__name__)


def convert_docx_to_pdf(docx_path: Path, pdf_path: Path) -> Path:
    """Converte um arquivo DOCX para PDF."""

    if not docx_path.exists():
        raise FileNotFoundError(f"DOCX não encontrado: {docx_path}")

    LOGGER.info("Convertendo DOCX para PDF: %s", pdf_path)

    try:
        convert(str(docx_path), str(pdf_path))
    except Exception as error:
        raise RuntimeError(
            "Falha ao converter DOCX para PDF. Verifique se o Microsoft Word "
            "está instalado e disponível neste ambiente."
        ) from error

    LOGGER.info("PDF gerado com sucesso.")
    return pdf_path
