import numpy as np
import scipy as sp
import pandas as pd
import logging

from gwrefpy.well import Well
from gwrefpy.fitresults import FitResultData
from gwrefpy.methods.timeseries import groupby_time_equivalents


logger = logging.getLogger(__name__)


def linregressfit(
    ref_well: Well,
    obs_well: Well,
    offset: pd.DateOffset | pd.Timedelta | str,
    tmin: pd.Timestamp | str | None = None,
    tmax: pd.Timestamp | str | None = None,
    p=0.95,
):
    """
    Perform linear regression fit between reference and observation well time series.

    Parameters
    ----------
    ref_well : Well
        The reference well object containing the time series data.
    obs_well : Well
        The observation well object containing the time series data.
    offset: pd.DateOffset | pd.Timedelta | str
        The offset to apply when grouping the time series into time equivalents.
    tmin: pd.Timestamp | str | None = None
        The minimum timestamp for the calibration period.
    tmax: pd.Timestamp | str | None = None
        The maximum timestamp for the calibration period.
    p : float, optional
        The confidence level for the prediction interval (default is 0.95).

    Returns
    -------
    fit_result : FitResultData
        A `FitResultData` object containing the results of the linear regression fit.
    """

    def _t_inv(probability, degrees_freedom):
        """
        Mimics Excel's T.INV function.
        Returns the t-value for the given probability and degrees of freedom.
        """
        return -sp.stats.t.ppf(probability, degrees_freedom)

    def _get_gwrefs_stats(p, n, stderr):
        ta = _t_inv((1 - p) / 2, n - 1)
        pc = ta * stderr * np.sqrt(1 + 1 / n)
        return pc, ta

    def compute_residual_std_error(x, y, a, b, n):
        y_pred = a * x + b
        residuals = y - y_pred

        stderr = np.sum(residuals**2) - np.sum(
            residuals * (x - np.mean(x))
        ) ** 2 / np.sum((x - np.mean(x)) ** 2)
        stderr *= 1 / (n - 2)
        stderr = np.sqrt(stderr)

        return stderr

    # Groupby time equivalents with given offset
    if ref_well.timeseries is None or obs_well.timeseries is None:
        logger.critical(f"Missing time series data for for either ref or obs well")
        return None

    ref_timeseries, obs_timeseries, n = groupby_time_equivalents(
        ref_well.timeseries.loc[tmin:tmax], obs_well.timeseries.loc[tmin:tmax], offset
    )

    linreg = sp.stats.linregress(ref_timeseries, obs_timeseries)

    stderr = compute_residual_std_error(
        ref_timeseries, obs_timeseries, linreg.slope, linreg.intercept, n
    )

    pred_const, t_a = _get_gwrefs_stats(p, n, stderr)

    # Create and return a FitResultData object with the regression results
    fit_result = FitResultData(
        ref_well=ref_well,
        obs_well=obs_well,
        rmse=linreg.rvalue,
        n=n,
        fit_method=linreg,
        t_a=t_a,
        stderr=stderr,
        pred_const=pred_const,
        p=p,
        offset=offset,
        tmin=tmin,
        tmax=tmax,
    )
    return fit_result
