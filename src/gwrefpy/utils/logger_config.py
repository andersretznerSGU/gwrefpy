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
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.debug("Logging is configured.")


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


def enable_file_logging(name: str = "gwrefpy.log", filemode: str = "w") -> None:
    """Enable logging to a file named 'gwrefpy.log' in the current directory.

    Parameters
    ----------
    name : str
        The name of the log file. Default is 'gwrefpy.log'.
    filemode : str
        The mode to open the log file. Default is 'w' (write mode).
        Other common mode is 'a' (append mode).
    """
    root_logger = logging.getLogger()
    # check if the name has an extension, if not add .log
    if not name.endswith(".log"):
        name += ".log"
    # Check if file handler already exists
    if not any(isinstance(h, logging.FileHandler) for h in root_logger.handlers):
        file_handler = logging.FileHandler(name, mode=filemode, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
