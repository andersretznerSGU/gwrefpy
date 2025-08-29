from .model import Model
from .well import Well

__name__ = "gwrefpy"
__version__ = "0.1.0"
__all__ = ["Model", "Well"]


def hello() -> str:
    return "Hello from gwrefpy!"
