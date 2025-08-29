import numpy as np
import scipy as sp

from gwrefpy.fitresults import FitResultData


def linregressfit(ref_well, obs_well, p=0.95):
    """
    Perform linear regression fit between reference and observation well time series.

    Parameters
    ----------
    ref_well : Well
        The reference well object containing the time series data.
    obs_well : Well
        The observation well object containing the time series data.
    p : float, optional
        The confidence level for the prediction interval (default is 0.95).

    Returns
    -------
    fit_result : FitResultData
        An object containing the results of the linear regression fit.
    """

    def _get_linear_regression(timeseries_ref, timeseries_obs):
        """
        Perform linear regression on the given data points.

        Parameters
        ----------
        timeseries : pd.Series
            A pandas Series with a datetime index and numerical values.

        Returns
        -------
        linreg : LinregressResult
            An object containing the slope, intercept, r-value, p-value,
            and standard error of the regression line.
        """
        # Calculate the slope and intercept using scipy's linregress
        return sp.stats.linregress(timeseries_ref, timeseries_obs)

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

    n = len(ref_well.timeseries)

    linreg = _get_linear_regression(ref_well.timeseries, obs_well.timeseries)

    stderr = compute_residual_std_error(
        ref_well.timeseries, obs_well.timeseries, linreg.slope, linreg.intercept, n
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
    )
    return fit_result
