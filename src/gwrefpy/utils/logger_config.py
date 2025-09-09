import logging.config

# Configure logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "minimal": {"format": "%(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "minimal",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": "gwrefpy.log",
            "mode": "w",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
logger.info("Logging is configured.")


def set_log_level(level: str) -> None:
    """Set the logging level for the gwrefpy logger.

    Args:
        level (str): Logging level as a string (e.g., 'DEBUG', 'INFO', 'WARNING',
        'ERROR', 'CRITICAL').
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logging.getLogger("gwrefpy").setLevel(numeric_level)
    logger.info(f"Log level set to {level}")
