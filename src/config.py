"""Configurações centralizadas da automação."""

from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppConfig:
    """Agrupa os caminhos e parâmetros usados pela aplicação."""

    input_pdf_dir: Path = ROOT_DIR / "input" / "pdf"
    input_images_dir: Path = ROOT_DIR / "input" / "images"
    output_dir: Path = ROOT_DIR / "output"
    template_path: Path = ROOT_DIR / "templates" / "modelo_relatorio.docx"
    log_file: Path = ROOT_DIR / "output" / "automacao.log"
    output_docx_name: str = "relatorio_gerado.docx"
    output_pdf_name: str = "relatorio_gerado.pdf"
    pdf_glob_pattern: str = "*.pdf"
    image_glob_patterns: tuple[str, ...] = ("*.png", "*.jpg", "*.jpeg")


DEFAULT_REGEX_PATTERNS: dict[str, str] = {
    "titulo": r"Título:\s*(?P<valor>.+)",
    "cliente": r"Cliente:\s*(?P<valor>.+)",
    "data": r"Data:\s*(?P<valor>.+)",
    "resumo": r"Resumo:\s*(?P<valor>[\s\S]+)",
}


def load_config() -> AppConfig:
    """Retorna a configuração padrão da aplicação."""

    return AppConfig()
