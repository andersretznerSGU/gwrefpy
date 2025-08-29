class FitResultData:
    def __init__(
        self,
        ref_well,
        obs_well,
        rmse,
        n,
        fit_method,
        t_a,
        stderr,
        pred_const,
        p,
        time_equivalent,
        calibration_period_start,
        calibration_period_end,
    ):
        """
        Initialize a FitResultData object to store the results of a fit between

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
        time_equivalent : float
            The time equivalent value.
        calibration_period_start : datetime
            The start date of the calibration period.
        calibration_period_end : datetime
            The end date of the calibration period.
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
        self.time_equivalent = time_equivalent
        self.calibration_period_start = calibration_period_start
        self.calibration_period_end = calibration_period_end

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
