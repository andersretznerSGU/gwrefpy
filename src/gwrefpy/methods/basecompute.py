from abc import ABC, abstractmethod

from src.gwrefpy.fitresults import FitResultData


class ComputeMethod(ABC):
    @staticmethod
    @abstractmethod
    def compute_fit(common_kwargs: dict, fit_kwargs: dict) -> FitResultData:
        pass
