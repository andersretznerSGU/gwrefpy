import numpy as np
import scipy.stats as stats
from dataclasses import dataclass, field

@dataclass
class FitResultData:
    pred_const: float
    obs_well: dict
    ref_well: dict
    RMSE: float = field(init=False)
    Std: float = field(init=False)
    t_a: tuple = field(init=False)
    n: int = field(init=False)


    def __post_init__(self):
        predictions = self.obs_well['predictions']
        actuals = self.ref_well['actuals']
        self.n = len(actuals)
        self.RMSE = np.sqrt(np.mean(np.square(np.array(predictions) - np.array(actuals))))
        residuals = np.array(actuals) - np.array(predictions)
        self.Std = np.std(residuals)
        self.t_a = stats.t.fit(residuals)

