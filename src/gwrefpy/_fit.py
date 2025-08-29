from scipy.stats import stats


class Fit():
    def __init__(self, model, data):
        self.model = model
        self.data = data

    def run(self):
        # Placeholder for fitting logic
        print("Running fit...")
        # Here you would implement the actual fitting algorithm
        return {"status": "success", "model": self.model, "data": self.data}

    def _get_linear_regression(self, **kwargs):
        """
        Perform linear regression on the given data points.

        Parameters
        ----------
        x : array-like
            The independent variable data points.
        y : array-like
            The dependent variable data points.

        Returns
        -------
        linreg : LinregressResult
            An object containing the slope, intercept, r-value, p-value,
            and standard error of the regression line.
        """
        if len(self.time) != len(self.measurements):
            raise ValueError("x and y must have the same length")

        # Calculate the slope and intercept using scipy's linregress
        linreg = stats.linregress(self.time, self.measurements, **kwargs)

        return linreg