"""Extração de dados estruturados a partir de texto usando regex."""

import logging
import re


LOGGER = logging.getLogger(__name__)


def parse_fields(text: str, patterns: dict[str, str]) -> dict[str, str]:
    """Extrai campos nomeados a partir de padrões regex configurados."""

    extracted_data: dict[str, str] = {}

    for field_name, pattern in patterns.items():
        extracted_data[field_name] = extract_field(text, field_name, pattern)

    return extracted_data


def extract_field(text: str, field_name: str, pattern: str) -> str:
    """Extrai um único campo do texto com base em um padrão regex."""

    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not match:
        LOGGER.warning("Campo '%s' não encontrado no texto do PDF.", field_name)
        return ""

    if "valor" in match.groupdict():
        return match.group("valor").strip()

    return match.group(1).strip() if match.groups() else match.group(0).strip()
