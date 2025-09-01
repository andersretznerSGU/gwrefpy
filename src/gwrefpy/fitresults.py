import pandas as pd

from gwrefpy.well import Well


class FitResultData:
    def __init__(
        self,
        ref_well: Well,
        obs_well: Well,
        rmse: float,
        n: int,
        fit_method: object,
        t_a: float,
        stderr: float,
        pred_const: float,
        p: float,
        offset: pd.DateOffset | pd.Timedelta | str,
        tmin: pd.Timestamp | str | None,
        tmax: pd.Timestamp | str | None,
    ):
        """
        Initialize a FitResultData object to store the results of a fit between.

        This class contains all information that is required to reproduce a fit between
        a reference well and an observation well.

        Parameters
        ----------
        ref_well : Well
            The reference well object containing the time series data.
        obs_well : Well
            The observation well object containing the time series data.
        rmse : float
            The root mean square error of the fit.
        n : int
            The number of data points used in the fit.
        fit_method : object
            The method used for fitting (e.g., linreg).
        t_a : float
            The t-value for the given confidence level and degrees of freedom.
        stderr : float
            The standard error of the regression.
        pred_const : float
            The prediction constant for the confidence interval.
        p : float
            The confidence level used in the fit.
        offset: pd.DateOffset | pd.Timedelta | str
            Allowed offset when grouping data points within time equivalents.
        tmin: pd.Timestamp | str | None
            The minimum timestamp for the calibration period.
        tmax: pd.Timestamp | str | None
            The maximum timestamp for the calibration period.
        """
        self.ref_well = ref_well
        self.obs_well = obs_well
        self.rmse = rmse
        self.n = n
        self.fit_method = fit_method
        self.t_a = t_a
        self.stderr = stderr
        self.pred_const = pred_const
        self.p = p
        self.offset = offset
        self.tmin = tmin
        self.tmax = tmax

    def __str__(self):
        return (
            f"FitResultData(ref_well={self.ref_well}, obs_well={self.obs_well}, "
            f"rmse={self.rmse:.4f}, n={self.n}, fit_method={self.fit_method})"
        )

    def __repr__(self):
        return (
            f"FitResultData(ref_well={self.ref_well}, obs_well={self.obs_well}, "
            f"rmse={self.rmse:.4f}, n={self.n}, fit_method={self.fit_method})"
        )
