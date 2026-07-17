"""Exportação de dados estruturados para CSV."""

import csv
import logging
from pathlib import Path


LOGGER = logging.getLogger(__name__)


def export_rows_to_csv(
    rows: list[dict[str, str]],
    output_path: Path,
    field_names: list[str],
) -> Path:
    """Salva os dados extraídos em CSV consolidado."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns = ["arquivo_origem", *field_names]

    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=columns,
            delimiter=";",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)

    LOGGER.info("Arquivo CSV gerado: %s", output_path)
    return output_path
