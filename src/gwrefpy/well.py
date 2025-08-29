"""
Well Module
-----------

This module contains classes for managing wells in a groundwater model.
It includes a base class `WellBase` and two derived classes `ReferenceWell`
and `ObservationWell`.
"""

import logging
import pandas as pd
import scipy.stats as stats

logger = logging.getLogger(__name__)


class Well:
    """
    Base class for a well in a groundwater model.
    """

    def __init__(self, name, is_reference, model=None):
        """
        Initialize a WellBase object.

        Parameters
        ----------
        name : str
            The name of the well.
        is_reference : bool
            Indicates if the well is a reference well (True) or an observation well (False).
        model : Model
            The groundwater model to which the well belongs.

        """

        # Initialize attributes
        self._name = None
        self.name = name  # This will call the setter
        self.is_reference = is_reference
        self.model = []
        if model is not None:
            self.model.append(
                model
            )  # Reference to the groundwater model # Todo: allow multiple models? with for loop
            model.add_well(self)  # Add this well to the model's list of wells

        # Time and measurement attributes
        self.timeseries = None

        # Plotting attributes
        self.color = None
        self.alpha = 1.0
        self.linestyle = None
        self.linewidth = 1.0
        self.marker = None
        self.markersize = 6
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

    def add_timeseries(self, timeseries):
        """
        Add time and measurement data to the well.

        Parameters
        ----------


        """
        _validatre_timeseries(self, timeseries)
        self.timeseries = timeseries
