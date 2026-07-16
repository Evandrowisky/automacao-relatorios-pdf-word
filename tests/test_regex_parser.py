"""Testes da extração de dados por regex."""

import sys
import unittest
import logging
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))

from regex_parser import extract_field, parse_fields  # noqa: E402


class RegexParserTest(unittest.TestCase):
    """Garante que os campos esperados sejam extraídos do texto."""

    def test_parse_fields_returns_expected_values(self) -> None:
        text = "Título: Relatório Mensal\nCliente: Empresa Exemplo"
        patterns = {
            "titulo": r"Título:\s*(?P<valor>.+)",
            "cliente": r"Cliente:\s*(?P<valor>.+)",
        }

        result = parse_fields(text, patterns)

        self.assertEqual(result["titulo"], "Relatório Mensal")
        self.assertEqual(result["cliente"], "Empresa Exemplo")

    def test_extract_field_returns_empty_string_when_not_found(self) -> None:
        logging.disable(logging.WARNING)
        try:
            result = extract_field("Sem o campo esperado", "data", r"Data:\s*(.+)")
        finally:
            logging.disable(logging.NOTSET)

        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
