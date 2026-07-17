"""Configurações centralizadas da automação."""

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
NOT_FOUND_VALUE = "Não encontrado"


@dataclass(frozen=True)
class AppConfig:
    """Agrupa os caminhos e parâmetros usados pela aplicação."""

    input_pdf_dir: Path = ROOT_DIR / "input" / "pdf"
    input_images_dir: Path = ROOT_DIR / "input" / "images"
    output_dir: Path = ROOT_DIR / "output"
    template_path: Path = ROOT_DIR / "templates" / "modelo_relatorio.docx"
    log_file: Path = ROOT_DIR / "output" / "automacao.log"
    output_txt_dir: Path = ROOT_DIR / "output" / "txt"
    output_csv_dir: Path = ROOT_DIR / "output" / "csv"
    output_excel_dir: Path = ROOT_DIR / "output" / "excel"
    output_docx_dir: Path = ROOT_DIR / "output" / "docx"
    output_pdf_dir: Path = ROOT_DIR / "output" / "pdf"
    csv_output_name: str = "dados_extraidos.csv"
    excel_output_name: str = "dados_extraidos.xlsx"
    pdf_glob_pattern: str = "*.pdf"
    image_glob_patterns: tuple[str, ...] = ("*.png", "*.jpg", "*.jpeg")
    output_formats: dict[str, bool] = field(
        default_factory=lambda: {
            "txt": True,
            "csv": True,
            "xlsx": True,
            "docx": False,
            "pdf": False,
        }
    )


DEFAULT_REGEX_PATTERNS: dict[str, str] = {
    "titulo": r"Título:\s*(?P<valor>.+)",
    "cliente": r"Cliente:\s*(?P<valor>.+)",
    "data": r"Data:\s*(?P<valor>.+)",
    "resumo": r"Resumo:\s*(?P<valor>[\s\S]+)",
}


def load_config() -> AppConfig:
    """Retorna a configuração padrão da aplicação."""

    return AppConfig()
