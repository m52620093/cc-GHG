from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

logging.addLevelName(logging.WARNING, "WARN")

LOGGER_NAME = "cc_ghg"


def setup_logger(base_dir: Path, file_name: str, max_bytes: int, backup_count: int) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        base_dir / file_name,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    return logger
