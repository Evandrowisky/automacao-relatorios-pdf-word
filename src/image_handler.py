"""Validação e preparação de imagens usadas no relatório."""

import logging
from pathlib import Path

from PIL import Image, UnidentifiedImageError


LOGGER = logging.getLogger(__name__)


def validate_images(image_paths: list[Path]) -> list[Path]:
    """Retorna apenas imagens válidas e legíveis."""

    valid_images: list[Path] = []

    for image_path in image_paths:
        if is_valid_image(image_path):
            valid_images.append(image_path)
        else:
            LOGGER.warning("Imagem ignorada por estar inválida: %s", image_path)

    LOGGER.info("%s imagem(ns) válida(s) encontrada(s).", len(valid_images))
    return valid_images


def is_valid_image(image_path: Path) -> bool:
    """Verifica se um arquivo pode ser aberto como imagem."""

    try:
        with Image.open(image_path) as image:
            image.verify()
    except (FileNotFoundError, UnidentifiedImageError, OSError):
        return False

    return True
