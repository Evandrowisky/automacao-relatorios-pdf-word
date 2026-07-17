"""Testes do fluxo principal e da interface de linha de comando."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

from config import AppConfig  # noqa: E402
from main import build_parser, prepare_directories, resolve_output_formats, run  # noqa: E402


class MainFlowTest(unittest.TestCase):
    """Valida processamento de múltiplos PDFs e argumentos da CLI."""

    def test_resolve_output_formats_uses_cli_selection(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--csv", "--xlsx"])

        formats = resolve_output_formats(args, {"txt": True})

        self.assertFalse(formats["txt"])
        self.assertTrue(formats["csv"])
        self.assertTrue(formats["xlsx"])

    def test_resolve_output_formats_uses_all_option(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--all"])

        formats = resolve_output_formats(args, {})

        self.assertTrue(all(formats.values()))

    def test_prepare_directories_creates_output_folders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config = build_temp_config(Path(temp_dir))

            prepare_directories(config)

            self.assertTrue(config.output_txt_dir.exists())
            self.assertTrue(config.output_csv_dir.exists())
            self.assertTrue(config.output_excel_dir.exists())

    def test_run_processes_multiple_pdfs_and_exports_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config = build_temp_config(temp_path)
            config.input_pdf_dir.mkdir(parents=True)

            copy_example_pdf("relatorio_inspecao_01.pdf", config.input_pdf_dir)
            copy_example_pdf("relatorio_inspecao_02.pdf", config.input_pdf_dir)

            results = run(
                config,
                {"txt": True, "csv": True, "xlsx": True, "docx": False, "pdf": False},
            )

            self.assertEqual(len(results), 2)
            self.assertTrue(all(result.success for result in results))
            self.assertTrue((config.output_txt_dir / "relatorio_inspecao_01.txt").exists())
            self.assertTrue((config.output_csv_dir / config.csv_output_name).exists())
            self.assertTrue((config.output_excel_dir / config.excel_output_name).exists())


def build_temp_config(root: Path) -> AppConfig:
    """Cria uma configuração isolada para testes."""

    return AppConfig(
        input_pdf_dir=root / "input" / "pdf",
        input_images_dir=root / "input" / "images",
        output_dir=root / "output",
        template_path=PROJECT_DIR / "templates" / "modelo_relatorio.docx",
        log_file=root / "output" / "automacao.log",
        output_txt_dir=root / "output" / "txt",
        output_csv_dir=root / "output" / "csv",
        output_excel_dir=root / "output" / "excel",
        output_docx_dir=root / "output" / "docx",
        output_pdf_dir=root / "output" / "pdf",
    )


def copy_example_pdf(filename: str, destination: Path) -> None:
    """Copia um PDF fictício para o diretório de entrada do teste."""

    source = PROJECT_DIR / "examples" / "pdfs" / filename
    shutil.copy(source, destination / filename)


if __name__ == "__main__":
    unittest.main()
