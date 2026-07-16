"""Funções utilitárias compartilhadas pela automação."""

import logging
from pathlib import Path


def configure_logging(log_file: Path) -> None:
    """Configura logs em arquivo e no console."""

    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def ensure_directories(paths: list[Path]) -> None:
    """Cria os diretórios informados quando eles ainda não existem."""

    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def find_first_file(directory: Path, pattern: str) -> Path:
    """Localiza o primeiro arquivo de um diretório usando um padrão glob."""

    files = sorted(directory.glob(pattern))
    if not files:
        raise FileNotFoundError(
            f"Nenhum arquivo encontrado em '{directory}' com o padrão '{pattern}'."
        )

    return files[0]


def find_files(directory: Path, patterns: tuple[str, ...]) -> list[Path]:
    """Localiza arquivos que correspondem a um ou mais padrões glob."""

    files: list[Path] = []
    for pattern in patterns:
        files.extend(directory.glob(pattern))

    return sorted(set(files))
