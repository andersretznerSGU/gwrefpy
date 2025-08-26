import scipy.stats as stats
import pandas as pd


class WellBase:
    """
    Base class for a well in a groundwater model.
    """

    def __init__(self, name):
        """
        Initialize a WellBase object.

        Parameters
        ----------
        name : str
            The name of the well.

        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")

        if not name:
            raise ValueError("Name cannot be an empty string.")

        # Initialize attributes
        self.name = name

        # Time and measurement attributes
        self.time = pd.Series(dtype="float64")  # Time series, can be datetime or float
        self.measurements = pd.Series(
            dtype="float64"
        )  # Measurement series, can be any numeric type

        # Plotting attributes
        self.plot_color = None
        self.plot_marker = None
        self.plot_ls = None
        self.plot_label = None

    def __repr__(self):
        return f"WellBase(name={self.name})"

    def __str__(self):
        return f"Well: {self.name}"

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
            An object containing the slope, intercept, r-value, p-value, and standard error of the regression line.
        """
        if len(self.time) != len(self.measurements):
            raise ValueError("x and y must have the same length")

        # Calculate the slope and intercept using scipy's linregress
        linreg = stats.linregress(self.time, self.measurements, **kwargs)

        return linreg

    def _datetime_to_float(self):
        """
        Convert a datetime object to a float representation.

        Parameters
        ----------
        self : WellBase
            The WellBase object containing the datetime to convert.

        Returns
        -------
        float
            The float representation of the datetime.
        """
        return self.time.timestamp() if hasattr(self.time, "timestamp") else self.time
