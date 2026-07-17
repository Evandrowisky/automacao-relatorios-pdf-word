"""Extração de dados estruturados a partir de texto usando regex."""

import logging
import re

from config import NOT_FOUND_VALUE


LOGGER = logging.getLogger(__name__)


def parse_fields(
    text: str,
    patterns: dict[str, str],
    source_file: str = "",
) -> dict[str, str]:
    """Extrai campos nomeados a partir de padrões regex configurados."""

    extracted_data: dict[str, str] = {}

    for field_name, pattern in patterns.items():
        extracted_data[field_name] = extract_field(
            text=text,
            field_name=field_name,
            pattern=pattern,
            source_file=source_file,
        )

    return extracted_data


def extract_field(
    text: str,
    field_name: str,
    pattern: str,
    source_file: str = "",
) -> str:
    """Extrai um único campo do texto com base em um padrão regex."""

    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not match:
        if source_file:
            LOGGER.warning(
                "Campo '%s' não encontrado no arquivo %s.",
                field_name,
                source_file,
            )
        else:
            LOGGER.warning("Campo '%s' não encontrado no texto do PDF.", field_name)
        return NOT_FOUND_VALUE

    if "valor" in match.groupdict():
        return match.group("valor").strip()

    return match.group(1).strip() if match.groups() else match.group(0).strip()
