"""Ponto de entrada da ferramenta de extração e conversão de PDFs."""

import argparse
import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from config import DEFAULT_REGEX_PATTERNS, AppConfig, load_config
from csv_exporter import export_rows_to_csv
from excel_exporter import export_rows_to_excel
from image_handler import validate_images
from pdf_converter import convert_docx_to_pdf
from pdf_reader import PdfExtraction, extract_pdf_content
from regex_parser import parse_fields
from text_exporter import export_text
from utils import build_output_name, configure_logging, ensure_directories
from validator import validate_output_file, validate_required_file
from word_generator import generate_word_report


LOGGER = logging.getLogger(__name__)
CLI_FORMATS = ("txt", "csv", "xlsx", "docx", "pdf")


@dataclass(frozen=True)
class ProcessingResult:
    """Representa o resultado do processamento de um PDF."""

    source_file: Path
    success: bool
    data: dict[str, str]
    error: str = ""


def build_parser() -> argparse.ArgumentParser:
    """Cria o parser da interface de linha de comando."""

    parser = argparse.ArgumentParser(
        description="Extrai dados de PDFs e exporta para TXT, CSV, Excel, Word e PDF."
    )
    parser.add_argument("--txt", action="store_true", help="Gera TXT com texto integral.")
    parser.add_argument("--csv", action="store_true", help="Gera CSV estruturado.")
    parser.add_argument("--xlsx", action="store_true", help="Gera Excel estruturado.")
    parser.add_argument("--docx", action="store_true", help="Gera relatório Word.")
    parser.add_argument("--pdf", action="store_true", help="Gera PDF final a partir do Word.")
    parser.add_argument("--all", action="store_true", help="Gera todos os formatos disponíveis.")

    return parser


def resolve_output_formats(
    args: argparse.Namespace,
    default_formats: dict[str, bool],
) -> dict[str, bool]:
    """Define os formatos de saída a partir da CLI ou da configuração."""

    if args.all:
        return {format_name: True for format_name in CLI_FORMATS}

    selected_formats = {
        format_name: bool(getattr(args, format_name))
        for format_name in CLI_FORMATS
    }

    if any(selected_formats.values()):
        return selected_formats

    return default_formats.copy()


def run(config: AppConfig, output_formats: dict[str, bool]) -> list[ProcessingResult]:
    """Executa o fluxo principal para todos os PDFs encontrados."""

    started_at = time.perf_counter()
    prepare_directories(config)
    pdf_files = sorted(config.input_pdf_dir.glob(config.pdf_glob_pattern))

    if not pdf_files:
        raise FileNotFoundError(f"Nenhum PDF encontrado em: {config.input_pdf_dir}")

    LOGGER.info("%s PDF(s) encontrado(s).", len(pdf_files))
    results = [process_pdf(pdf_path, config, output_formats) for pdf_path in pdf_files]
    successful_rows = [result.data for result in results if result.success]
    summary = build_execution_summary(results, time.perf_counter() - started_at)

    export_structured_outputs(
        rows=successful_rows,
        config=config,
        output_formats=output_formats,
        summary=summary,
    )

    return results


def prepare_directories(config: AppConfig) -> None:
    """Cria os diretórios necessários para entrada e saída."""

    ensure_directories(
        [
            config.input_pdf_dir,
            config.input_images_dir,
            config.output_dir,
            config.output_txt_dir,
            config.output_csv_dir,
            config.output_excel_dir,
            config.output_docx_dir,
            config.output_pdf_dir,
            config.template_path.parent,
        ]
    )


def process_pdf(
    pdf_path: Path,
    config: AppConfig,
    output_formats: dict[str, bool],
) -> ProcessingResult:
    """Processa um PDF individual sem interromper a execução geral."""

    started_at = time.perf_counter()
    LOGGER.info("Processando arquivo: %s", pdf_path.name)

    try:
        extraction = extract_pdf_content(pdf_path)
        data = parse_fields(
            text=extraction["texto_completo"],
            patterns=DEFAULT_REGEX_PATTERNS,
            source_file=pdf_path.name,
        )
        data["arquivo_origem"] = pdf_path.name
        export_individual_outputs(extraction, data, pdf_path, config, output_formats)
    except Exception as error:
        LOGGER.exception("Erro ao processar arquivo %s.", pdf_path.name)
        return ProcessingResult(pdf_path, False, {}, str(error))

    elapsed_time = time.perf_counter() - started_at
    LOGGER.info("Arquivo processado com sucesso: %s em %.2fs", pdf_path.name, elapsed_time)
    return ProcessingResult(pdf_path, True, data)


def export_individual_outputs(
    extraction: PdfExtraction,
    data: dict[str, str],
    pdf_path: Path,
    config: AppConfig,
    output_formats: dict[str, bool],
) -> None:
    """Gera saídas individuais de um PDF quando configuradas."""

    if output_formats.get("txt"):
        export_text(extraction, config.output_txt_dir)

    if output_formats.get("docx") or output_formats.get("pdf"):
        docx_path = generate_docx(pdf_path, config, data)
        validate_output_file(docx_path)

        if output_formats.get("pdf"):
            pdf_output_path = config.output_pdf_dir / build_output_name(
                pdf_path,
                "relatorio",
                "pdf",
            )
            convert_docx_to_pdf(docx_path, pdf_output_path)
            validate_output_file(pdf_output_path)


def generate_docx(pdf_path: Path, config: AppConfig, data: dict[str, str]) -> Path:
    """Gera um relatório DOCX para um PDF de origem."""

    validate_required_file(config.template_path, "Modelo de relatório")
    image_paths = validate_images(
        [
            path
            for pattern in config.image_glob_patterns
            for path in config.input_images_dir.glob(pattern)
        ]
    )
    output_docx = config.output_docx_dir / build_output_name(pdf_path, "relatorio", "docx")

    return generate_word_report(config.template_path, output_docx, data, image_paths)


def export_structured_outputs(
    rows: list[dict[str, str]],
    config: AppConfig,
    output_formats: dict[str, bool],
    summary: dict[str, str | int | float],
) -> None:
    """Gera arquivos consolidados de dados estruturados."""

    field_names = list(DEFAULT_REGEX_PATTERNS.keys())

    if output_formats.get("csv"):
        export_rows_to_csv(
            rows=rows,
            output_path=config.output_csv_dir / config.csv_output_name,
            field_names=field_names,
        )

    if output_formats.get("xlsx"):
        export_rows_to_excel(
            rows=rows,
            output_path=config.output_excel_dir / config.excel_output_name,
            field_names=field_names,
            execution_summary=summary,
        )


def build_execution_summary(
    results: list[ProcessingResult],
    elapsed_time: float | None = None,
) -> dict[str, str | int | float]:
    """Monta o resumo consolidado da execução."""

    success_count = sum(result.success for result in results)
    error_count = len(results) - success_count
    summary: dict[str, str | int | float] = {
        "PDFs processados": len(results),
        "Arquivos com sucesso": success_count,
        "Arquivos com erro": error_count,
        "Data e hora da execução": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }

    if elapsed_time is not None:
        summary["Tempo total de processamento (s)"] = round(elapsed_time, 2)

    return summary


def print_execution_summary(results: list[ProcessingResult], output_dir: Path) -> None:
    """Exibe um resumo amigável da execução."""

    success_count = sum(result.success for result in results)
    error_count = len(results) - success_count

    print(f"{len(results)} PDF(s) encontrado(s).")
    print(f"{success_count} processado(s) com sucesso.")
    print(f"{error_count} apresentou(aram) erro.")
    print(f"Arquivos gerados em: {output_dir}")

    for result in results:
        if not result.success:
            print(f"- Erro em {result.source_file.name}: {result.error}")


def main(argv: list[str] | None = None) -> int:
    """Inicializa argumentos, configurações, logs e tratamento de erros."""

    config = load_config()
    configure_logging(config.log_file)
    parser = build_parser()
    args = parser.parse_args(argv)
    output_formats = resolve_output_formats(args, config.output_formats)

    started_at = time.perf_counter()

    try:
        results = run(config, output_formats)
    except Exception as error:
        LOGGER.exception("A automação foi interrompida.")
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    elapsed_time = time.perf_counter() - started_at
    LOGGER.info("Automação finalizada em %.2fs.", elapsed_time)
    print_execution_summary(results, config.output_dir)

    return 0 if all(result.success for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
