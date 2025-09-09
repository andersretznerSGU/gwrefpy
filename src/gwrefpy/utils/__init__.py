import logging

import gwrefpy.utils.logger_config

from .decorators import print_return, timed

__all__ = ["timed", "print_return"]

logger = logging.getLogger(__name__)
logger.debug("Logging is configured.")
