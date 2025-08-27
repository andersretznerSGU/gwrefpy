from .model import Model
from .well import ReferenceWell, ObservationWell

__name__ = "gwrefpy"
__version__ = "0.1.0"
__all__ = ["Model", "ReferenceWell", "ObservationWell"]


def hello() -> str:
    return "Hello from gwrefpy!"
