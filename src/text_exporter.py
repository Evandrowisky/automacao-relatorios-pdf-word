"""Exportação do texto integral extraído dos PDFs."""

import logging
from pathlib import Path

from pdf_reader import PdfExtraction


LOGGER = logging.getLogger(__name__)


def export_text(extraction: PdfExtraction, output_dir: Path) -> Path:
    """Salva todo o texto extraído de um PDF em arquivo TXT."""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{Path(extraction['arquivo']).stem}.txt"
    content = build_text_content(extraction)

    output_path.write_text(content, encoding="utf-8")
    LOGGER.info("Arquivo TXT gerado: %s", output_path)

    return output_path


def build_text_content(extraction: PdfExtraction) -> str:
    """Monta o conteúdo textual com separação clara entre páginas."""

    sections = [f"ARQUIVO DE ORIGEM: {extraction['arquivo']}", ""]

    for page in extraction["paginas"]:
        sections.extend(
            [
                f"================ PÁGINA {page['numero']} ================",
                "",
                page["texto"].strip(),
                "",
            ]
        )

    return "\n".join(sections).strip() + "\n"
