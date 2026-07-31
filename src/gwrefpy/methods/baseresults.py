from abc import ABC, abstractmethod

import pandas as pd


class ResultMethod(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def fit_str(self):
        pass

    @abstractmethod
    def html_fit_str(self):
        pass

    @abstractmethod
    def fit_timeseries(self, timeseries: pd.Series) -> pd.Series:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
