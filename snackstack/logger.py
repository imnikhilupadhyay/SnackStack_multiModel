
import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()

logger_level = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    level = getattr(logging, logger_level, logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(name)-18s | %(levelname)-7s | %(message)s",
                datefmt="%H:%M:%S"
            )
        )
        logger.addHandler(handler)

        logger.setLevel(level)
    
    return logger
