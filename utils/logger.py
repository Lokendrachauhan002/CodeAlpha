"""Application and conversation logging helpers."""
import logging
from pathlib import Path


def configure_logging(log_path: Path) -> logging.Logger:
    """Configure a file and console logger only once."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("faq_chatbot")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        for handler in (logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler()):
            handler.setFormatter(formatter)
            logger.addHandler(handler)
    return logger
