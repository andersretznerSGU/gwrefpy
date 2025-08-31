"""
Model
-----
A class representing a groundwater model that can contain multiple wells.

"""

import logging

from .fitresults import FitResultData, unpack_dict_fit_method
from .io.io import load, save
from .methods.linregressfit import linregressfit
from .well import Well

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, name: str):
        self.name = name

        # Well attributes
        self.wells = []

        # Fit attributes
        self.fits = []

    def __str__(self):
        """String representation of the Model object."""
        return f"Model(name={self.name}, wells={len(self.wells)})"

    # ============================== Well Management Methods ==============================

    @property
    def obs_wells(self):
        """List of observation wells in the model."""
        return [well for well in self.wells if not well.is_reference]

    @property
    def ref_wells(self):
        """List of reference wells in the model."""
        return [well for well in self.wells if well.is_reference]

    @property
    def well_names(self):
        """List of all well names in the model."""
        return [well.name for well in self.wells]

    def add_well(self, well):
        """
        Add a well or a list of wells to the model.

        Parameters
        ----------
        well : Well or list of WellBase
            The well or list of wells to add to the model.

        Returns
        -------
        None
            This method modifies the model in place.
        """
        if isinstance(well, list):
            for w in well:
                self._add_well(w)
            logger.info(f"Added {len(well)} wells to model '{self.name}'.")
        else:
            self._add_well(well)
            logger.info(f"Added one well to model '{self.name}'.")

    def _add_well(self, well):
        """
        The internal method to add a well to the model.

        Parameters
        ----------
        well : Well
            The well to add to the model.

        Raises
        ------
        TypeError
            If the well is not an instance of WellBase.
        ValueError
            If the well is already in the model.

        Returns
        -------
        None
            This method modifies the model in place.
        """

        # Check if the well is an instance of Well
        if not isinstance(well, Well):
            logger.error("Only Well instances can be added to the model.")
            raise TypeError("Only Well instances can be added to the model.")

        # Check if the well is already in the model
        if well in self.wells:
            logger.error(f"Well '{well.name}' is already in the model.")
            raise ValueError(f"Well '{well.name}' is already in the model.")

        # Check if the well name already exists in the model
        if well.name in self.well_names:
            logger.error(f"Well name '{well.name}' already exists in the model.")
            raise ValueError(f"Well name '{well.name}' already exists in the model.")

        # Add the well to the model
        self.wells.append(well)
        well.model.append(self)
        logger.debug(f"Well '{well.name}' added to model '{self.name}'.")

    # ============================== Load and Save Methods ==============================

    def fit(self, ref_well, obs_well, time_equivalent, calibration_period_start, calibration_period_end, p=0.95, method="linearregression"):
        """
        Fit the model using a reference well and an observation well.

        Parameters
        ----------
        ref_well : Well
            The reference well to use for fitting.
        obs_well : Well
            The observation well to use for fitting.
        time_equivalent : float
            The time equivalent value.
        calibration_period_start : datetime
            The start date of the calibration period.
        calibration_period_end : datetime
            The end date of the calibration period.
        p : float, optional
            The confidence level for the fit (default is 0.95).
        method : str, optional
            The fitting method to use (default is 'linearregression').

        Returns
        -------
        None
            This method modifies the model in place.
        """
        self._fit(ref_well, obs_well, time_equivalent, calibration_period_start, calibration_period_end, p, method)
        logger.info(
            f"Fitting model '{self.name}' using reference well '{ref_well.name}' and observation well '{obs_well.name}'."
        )

    def _fit(self, ref_well, obs_well, time_equivalent, calibration_period_start, calibration_period_end, p, method):
        """
        The internal method to perform the fitting.

        Parameters
        ----------
        ref_well : Well
            The reference well to use for fitting.
        obs_well : Well
            The observation well to use for fitting.
        p : float, optional
            The confidence level for the fit (default is 0.95).
        method : str, optional
            The fitting method to use (default is 'linearregression').

        Returns
        -------
        None
            This method modifies the model in place.
        """
        # Check that the ref_well is a reference well
        if not ref_well.is_reference:
            logger.error(f"The well '{ref_well.name}' is not a reference well.")
            raise ValueError(f"The well '{ref_well.name}' is not a reference well.")

        # Check that the obs_well is an observation well
        if obs_well.is_reference:
            logger.error(f"The well '{obs_well.name}' is not an observation well.")
            raise ValueError(f"The well '{obs_well.name}' is not an observation well.")

        # Placeholder for internal fit logic
        logger.debug(
            f"Internal fitting logic for model '{self.name}' with reference well '{ref_well.name}' and observation well '{obs_well.name}'."
        )

        # Validate and adjust wells
        ref_timeseries = ref_well.timeseries
        obs_timeseries = obs_well.timeseries

        fit = None
        if method == "linearregression":
            logger.debug("Using linear regression method for fitting.")
            fit = linregressfit(ref_well, obs_well, time_equivalent, calibration_period_start, calibration_period_end, p=p)

        if fit is None:
            logger.error(f"Fitting method '{method}' is not implemented.")
            raise NotImplementedError(f"Fitting method '{method}' is not implemented.")

        self.fits.append(fit)
        logger.info(f"Fit completed for model '{self.name}'.")

    def best_fit(self, ref_well=None, obs_well=None):
        """
        Find the best fit for the model using the provided wells.

        Parameters
        ----------
        ref_well : Well or list of Well or None, optional
            The reference well to use for fitting (default is None).
        obs_well : Well or list of Well or None, optional
            The observation well to use for fitting (default is None).

        Returns
        -------
        None
            This method modifies the model in place.
        """
        # Placeholder for best fit logic
        logger.info(f"Finding best fit for model '{self.name}'.")

    def _best_fit(self, ref_well=None, obs_well=None):
        """
        The internal method to find the best fit.

        Parameters
        ----------
        ref_well : Well or list of Well or None, optional
            The reference well to use for fitting (default is None).
        obs_well : Well or list of Well or None, optional
            The observation well to use for fitting (default is None).

        Returns
        -------
        None
            This method modifies the model in place.
        """
        # Placeholder for internal best fit logic
        logger.debug(f"Internal best fit logic for model '{self.name}'.")
        # best_fit = BestFitResults(ref_well, obs_well)
        best_fit = "h"
        self.fits.append(best_fit)
        logger.info(f"Best fit completed for model '{self.name}'.")

    # ============================== Load and Save Methods ==============================

    def to_dict(self):
        """
        Convert the model to a dictionary representation.

        Returns
        -------
        dict
            A dictionary representation of the model.
        """
        # Create a dictionary representation of the model
        model_dict = {
            "name": self.name,
            "wells": [well.name for well in self.wells],
        }

        # Create a dictionary representation of each well
        wells_dict = {}
        for well in self.wells:
            wells_dict[well.name] = well.to_dict()
        model_dict["wells_dict"] = wells_dict

        # Add fits if they exist
        if self.fits:
            model_dict["fits"] = [fit.to_dict() for fit in self.fits]

        return model_dict

    def unpack_dict(self, data):
        """
        Unpack a dictionary representation of the model and set the model's attributes.

        Parameters
        ----------
        data : dict
            A dictionary representation of the model.

        Returns
        -------
        None
            This method modifies the model in place.
        """
        self.name = data.get("name", self.name)

        # Unpack wells
        wells_dict = data.get("wells_dict", {})
        for w in wells_dict.items():
            well_obj = w[1]
            well = Well(name=well_obj["name"], is_reference=well_obj["is_reference"])
            well.unpack_dict(well_obj)
            self.add_well(well)

        # Unpack fits
        fits_list = data.get("fits", [])
        for fit_data in fits_list:
            fit = FitResultData(
                ref_well=self.wells[self.well_names.index(fit_data["ref_well"])],
                obs_well=self.wells[self.well_names.index(fit_data["obs_well"])],
                rmse = fit_data.get("rmse", None),
                n = fit_data.get("n", None),
                fit_method = unpack_dict_fit_method(fit_data),
                t_a = fit_data.get("t_a", None),
                stderr = fit_data.get("stderr", None),
                pred_const = fit_data.get("pred_const", None),
                p = fit_data.get("p", None),
                time_equivalent = fit_data.get("time_equivalent", None),
                calibration_period_start = fit_data.get("calibration_period_start", None),
                calibration_period_end = fit_data.get("calibration_period_end", None),
            )
            self.fits.append(fit)

    def save_project(self, filename=None, overwrite=False):
        """
        Save the model to a file.

        Parameters
        ----------
        filename : str or None, optional
            The name of the file where the model will be saved. The path can be included.
        overwrite : bool, optional
            Whether to overwrite the file if it already exists (default is False).

        Returns
        -------
        None
            This method saves the model to a file.
        """

        # Convert the model to a dictionary
        model_dict = self.to_dict()

        # Set default filename if not provided
        if filename is None:
            filename = f"{self.name}.gwref"

        # Save the model dictionary to a file
        save(filename, model_dict, overwrite=overwrite)
        logger.info(f"Model '{self.name}' saved to '{filename}'.")

    def open_project(self, filepath):
        """
        Load the model from a file.

        Parameters
        ----------
        filepath : str
            The path to the file from which the model will be loaded.

        Returns
        -------
        None
            This method loads the model from a file.
        """
        # Placeholder for load logic
        data = load(filepath)
        self.unpack_dict(data)
        logger.info(f"Model '{self.name}' loaded from '{filepath}'.")
