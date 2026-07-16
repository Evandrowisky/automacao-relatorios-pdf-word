"""Validações de entrada e saída da automação."""

from pathlib import Path


def validate_required_file(file_path: Path, description: str) -> None:
    """Valida se um arquivo obrigatório existe."""

    if not file_path.exists():
        raise FileNotFoundError(f"{description} não encontrado: {file_path}")


def validate_required_directory(directory: Path, description: str) -> None:
    """Valida se um diretório obrigatório existe."""

    if not directory.exists():
        raise FileNotFoundError(f"{description} não encontrado: {directory}")


def validate_output_file(file_path: Path) -> None:
    """Valida se um arquivo de saída foi criado."""

    if not file_path.exists() or file_path.stat().st_size == 0:
        raise RuntimeError(f"Arquivo de saída não foi gerado corretamente: {file_path}")
