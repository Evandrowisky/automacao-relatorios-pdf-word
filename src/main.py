"""Ponto de entrada da automação de relatórios PDF/Word."""

import logging
import sys
from pathlib import Path

from config import DEFAULT_REGEX_PATTERNS, AppConfig, load_config
from image_handler import validate_images
from pdf_converter import convert_docx_to_pdf
from pdf_reader import extract_text_from_pdf
from regex_parser import parse_fields
from utils import configure_logging, ensure_directories, find_files, find_first_file
from validator import validate_output_file, validate_required_file
from word_generator import generate_word_report


LOGGER = logging.getLogger(__name__)


def run(config: AppConfig) -> Path:
    """Executa o fluxo principal da automação."""

    ensure_directories(
        [
            config.input_pdf_dir,
            config.input_images_dir,
            config.output_dir,
            config.template_path.parent,
        ]
    )
    validate_required_file(config.template_path, "Modelo de relatório")

    input_pdf = find_first_file(config.input_pdf_dir, config.pdf_glob_pattern)
    image_paths = find_files(config.input_images_dir, config.image_glob_patterns)

    text = extract_text_from_pdf(input_pdf)
    data = parse_fields(text, DEFAULT_REGEX_PATTERNS)
    valid_images = validate_images(image_paths)

    output_docx = config.output_dir / config.output_docx_name
    output_pdf = config.output_dir / config.output_pdf_name

    generate_word_report(config.template_path, output_docx, data, valid_images)
    validate_output_file(output_docx)

    convert_docx_to_pdf(output_docx, output_pdf)
    validate_output_file(output_pdf)

    return output_pdf


def main() -> int:
    """Inicializa configurações, logs e tratamento amigável de erros."""

    config = load_config()
    configure_logging(config.log_file)

    try:
        generated_pdf = run(config)
    except Exception as error:
        LOGGER.exception("A automação foi interrompida.")
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    LOGGER.info("Automação finalizada com sucesso: %s", generated_pdf)
    print(f"Relatório gerado com sucesso: {generated_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
