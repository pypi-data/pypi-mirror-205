"""GoXLR Utility API: Logger"""
import logging
from typing import Final

DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
FORMAT: Final[str] = "%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s"


def setup_logger(
    log_level: str = "INFO",
) -> logging.Logger:
    """Set up logging"""

    logging.basicConfig(
        datefmt=DATE_FORMAT,
        format=FORMAT,
        level=log_level,
    )

    logger = logging.getLogger("")
    logger.setLevel(log_level)

    return logger
