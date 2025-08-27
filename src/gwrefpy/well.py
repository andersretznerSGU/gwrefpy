import logging

import pandas as pd
import scipy.stats as stats

logger = logging.getLogger(__name__)


class WellBase:
    """
    Base class for a well in a groundwater model.
    """

    def __init__(self, name, model):
        """
        Initialize a WellBase object.

        Parameters
        ----------
        name : str
            The name of the well.
        model : Model
            The groundwater model to which the well belongs.

        """

        # Initialize attributes
        self._name = None
        self.name = name  # This will call the setter
        self.model = model  # Reference to the groundwater model
        model.add_well(self)  # Add this well to the model's list of wells

        # Time and measurement attributes
        self.time = pd.Series(dtype="datetime")  # Time series, as datetime
        self._time = pd.Series(dtype="float64")  # Internal time series as float
        self.measurements = pd.Series(
            dtype="float64"
        )  # Measurement series, can be any numeric type

        # Plotting attributes
        self.color = None
        self.alpha = 1.0
        self.linestyle = None
        self.linewidth = None
        self.marker = None
        self.markerstyle = None

        # Geographic attributes
        self.latitude = None
        self.longitude = None
        self.elevation = None

        # Well attributes
        self.well_attribute = {}

    @property
    def name(self):
        """The name of the well."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name of the well."""
        if not value:
            logger.error("Name cannot be an empty string.")
            raise ValueError("Name cannot be an empty string.")
        if not isinstance(value, str):
            logger.error("Name must be a string.")
            raise TypeError("Name must be a string.")
        self._name = value

    def set_kwargs(self, **kwargs):
        """
        Set attributes of the WellBase object using keyword arguments.

        Parameters
        ----------
        **kwargs : dict
            The attributes to set. The keys should be the names of the attributes and
            the values should be the new values.

        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                logger.warning(f"{self.__class__.__name__} has no attribute '{key}'")
                raise AttributeError(
                    f"{self.__class__.__name__} has no attribute '{key}'"
                )

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
            An object containing the slope, intercept, r-value, p-value,
            and standard error of the regression line.
        """
        if len(self.time) != len(self.measurements):
            raise ValueError("x and y must have the same length")

        # Calculate the slope and intercept using scipy's linregress
        linreg = stats.linregress(self.time, self.measurements, **kwargs)

        return linreg

    @staticmethod
    def _datetime_to_float(date_time):
        """
        Convert a datetime object to a float representation.

        Parameters
        ----------
        date_time : datetime
            The datetime object to convert.

        Returns
        -------
        float
            The float representation of the datetime.
        """
        return date_time.timestamp() if hasattr(date_time, "timestamp") else date_time

    def add_well_data(self, time, measurements):
        """
        Add time and measurement data to the well.

        Parameters
        ----------
        time : array-like
            The time data points.
        measurements : array-like
            The measurement data points.

        """
        if len(time) != len(measurements):
            logger.warning("Time and measurements must have the same length")
            raise ValueError("Time and measurements must have the same length")

        logger.info(f"Adding {len(time)} data points to well '{self.name}'")

        self.time = pd.Series(time)
        self.measurements = pd.Series(measurements)


class ReferenceWell(WellBase):
    """
    Class for a reference well in a groundwater model.
    """

    def __init__(self, name):
        """
        Initialize a ReferenceWell object.

        Parameters
        ----------
        name : str
            The name of the reference well.

        """
        super().__init__(name)


class ObservationWell(WellBase):
    """
    Class for an observation well in a groundwater model.
    """

    def __init__(self, name):
        """
        Initialize an ObservationWell object.

        Parameters
        ----------
        name : str
            The name of the observation well.

        """
        super().__init__(name)
