"""Testes da leitura de PDFs."""

import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

from pdf_reader import extract_pdf_content, extract_text_from_pdf  # noqa: E402


class PdfReaderTest(unittest.TestCase):
    """Valida a extração de texto por página e texto completo."""

    def test_extract_pdf_content_returns_pages_and_full_text(self) -> None:
        pdf_path = PROJECT_DIR / "examples" / "pdfs" / "relatorio_inspecao_01.pdf"

        extraction = extract_pdf_content(pdf_path)

        self.assertEqual(extraction["arquivo"], "relatorio_inspecao_01.pdf")
        self.assertEqual(len(extraction["paginas"]), 2)
        self.assertIn("Cliente", extraction["texto_completo"])

    def test_extract_text_from_pdf_keeps_previous_behavior(self) -> None:
        pdf_path = PROJECT_DIR / "examples" / "pdfs" / "relatorio_inspecao_01.pdf"

        text = extract_text_from_pdf(pdf_path)

        self.assertIn("10/07/2026", text)


if __name__ == "__main__":
    unittest.main()
