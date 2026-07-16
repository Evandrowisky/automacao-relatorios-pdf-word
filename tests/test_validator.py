"""Testes das validações de arquivos."""

import sys
import tempfile
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))

from validator import validate_output_file, validate_required_file  # noqa: E402


class ValidatorTest(unittest.TestCase):
    """Valida cenários básicos de arquivos obrigatórios e saídas."""

    def test_validate_required_file_accepts_existing_file(self) -> None:
        with tempfile.NamedTemporaryFile() as temporary_file:
            validate_required_file(Path(temporary_file.name), "Arquivo temporário")

    def test_validate_output_file_rejects_empty_file(self) -> None:
        with tempfile.NamedTemporaryFile() as temporary_file:
            with self.assertRaises(RuntimeError):
                validate_output_file(Path(temporary_file.name))


if __name__ == "__main__":
    unittest.main()
