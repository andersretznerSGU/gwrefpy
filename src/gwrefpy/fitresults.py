import pandas as pd

from .well import Well
from .utils.conversions import datetime_to_float


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

    def fit_timeseries(self):
        """
        Apply the fit method to a reference time series to get the fitted values.

        Parameters
        ----------
        ref_series : pd.Series
            The reference time series data.

        Returns
        -------
        pd.Series
            The fitted values based on the reference series.
        """
        if isinstance(self.fit_method, LinRegResult):
            return self.ref_well.timeseries.apply(
                lambda x: self.fit_method.slope * x + self.fit_method.intercept
            )

    def has_well(self, well):
        """
        Check if the FitResultData object involves the given well.

        Parameters
        ----------
        well : Well
            The well to check.

        Returns
        -------
        bool
            True if the well is either the reference or observation well, False otherwise.
        """
        return self.ref_well == well or self.obs_well == well

    def to_dict(self):
        """
        Convert the FitResultData object to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the FitResultData object.
        """
        dict_representation = {
            "ref_well": self.ref_well.name,
            "obs_well": self.obs_well.name,
            "rmse": self.rmse,
            "n": self.n,
            "t_a": self.t_a,
            "fit_method": str(self.fit_method.__class__.__name__),
            "stderr": self.stderr,
            "pred_const": self.pred_const,
            "p": self.p,
            "offset": self.offset,
            "tmin": datetime_to_float(self.tmin),
            "tmax": datetime_to_float(self.tmax),
        }

        if dict_representation["fit_method"] == "LinRegResult":
            dict_representation["LinRegResult"] = {
                "slope": self.fit_method.slope,
                "intercept": self.fit_method.intercept,
                "rvalue": self.fit_method.rvalue,
                "pvalue": self.fit_method.pvalue,
                "stderr": self.fit_method.stderr,
            }

        return dict_representation


def unpack_dict_fit_method(data):
    fit_method_name = data.get("fit_method", None)
    if fit_method_name == "LinRegResult":
        linreg_data = data.get("LinRegResult", {})
        return LinRegResult(
            slope=linreg_data.get("slope", 0.0),
            intercept=linreg_data.get("intercept", 0.0),
            rvalue=linreg_data.get("rvalue", 0.0),
            pvalue=linreg_data.get("pvalue", 0.0),
            stderr=linreg_data.get("stderr", 0.0),
        )
    else:
        raise ValueError(f"Unsupported fit method: {fit_method_name}")


class LinRegResult:
    def __init__(self, slope, intercept, rvalue, pvalue, stderr):
        """
        Initialize a LinRegResult object to store the results of a linear regression. This replaces the scipy
        LinregressResult object to make it serializable.

        Parameters
        ----------
        slope : float
            The slope of the regression line.
        intercept : float
            The intercept of the regression line.
        rvalue : float
            The correlation coefficient.
        pvalue : float
            The two-sided p-value for a hypothesis test whose null hypothesis is that the slope is zero.
        stderr : float
            The standard error of the estimated slope.
        """
        self.slope = slope
        self.intercept = intercept
        self.rvalue = rvalue
        self.pvalue = pvalue
        self.stderr = stderr

    def __str__(self):
        return (
            f"LinRegResult(slope={self.slope:.4f}, intercept={self.intercept:.4f}, "
            f"rvalue={self.rvalue:.4f}, pvalue={self.pvalue:.4f}, stderr={self.stderr:.4f})"
        )

    def __repr__(self):
        return (
            f"LinRegResult(slope={self.slope:.4f}, intercept={self.intercept:.4f}, "
            f"rvalue={self.rvalue:.4f}, pvalue={self.pvalue:.4f}, stderr={self.stderr:.4f})"
        )
