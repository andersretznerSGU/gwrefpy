"""
Model
-----
A class representing a groundwater model that can contain multiple wells.

"""

import logging
from typing import Literal

import pandas as pd

from .fitresults import FitResultData, unpack_dict_fit_method
from .io.io import load, save
from .methods.linregressfit import linregressfit
from .plotter import Plotter
from .utils.conversions import float_to_datetime
from .well import Well

logger = logging.getLogger(__name__)


class Model(Plotter):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

        # Well attributes
        self.wells: list[Well] = []

        # Fit attributes
        self.fits: list[FitResultData] = []

    def __str__(self):
        """String representation of the Model object."""
        return f"Model(name={self.name}, wells={len(self.wells)})"

    # ======================== Well Management Methods ========================

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

    def add_well(self, well: Well | list[Well]):
        """
        Add a well or a list of wells to the model.

        Parameters
        ----------
        well : Well or list of Wells
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

    def get_wells(self, names: list[str] | str) -> Well | list[Well]:
        """
        Get wells from the model by their names.

        Parameters
        ----------
        names : list of str or str
            The name or list of names of the wells to retrieve.

        Returns
        -------
        Well | list[Well]
            The well or list of wells with the specified names.

        Raises
        ------
        ValueError
            If any of the specified well names are not found in the model.
        """
        if isinstance(names, str):
            names = [names]

        found_wells = []
        for name in names:
            if name in self.well_names:
                found_wells.append(self.wells[self.well_names.index(name)])
            else:
                logger.error(f"Well name '{name}' not found in the model.")
                raise ValueError(f"Well name '{name}' not found in the model.")

        return found_wells if len(found_wells) > 1 else found_wells[0]

    # ============================== Fit methods ==============================

    def fit(
        self,
        obs_well: Well | list[Well],
        ref_well: Well | list[Well],
        offset: pd.DateOffset | pd.Timedelta | str,
        p: float = 0.95,
        method: Literal["linearregression"] = "linearregression",
        tmin: pd.Timestamp | str | None = None,
        tmax: pd.Timestamp | str | None = None,
    ) -> FitResultData | list[FitResultData]:
        """
        Fit reference well(s) to observation well(s) using regression.

        Parameters
        ----------
        obs_well : Well | list[Well]
            The observation well(s) to use for fitting. If a list is provided,
            each well will be paired with the corresponding reference well by index.
        ref_well : Well | list[Well]
            The reference well(s) to use for fitting. If a list is provided,
            each well will be paired with the corresponding observation well by index.
        offset: pd.DateOffset | pd.Timedelta | str
            The offset to apply to the time series when grouping within time
            equivalents.
        p : float, optional
            The confidence level for the fit (default is 0.95).
        method : Literal["linearregression"]
            Method with which to perform regression. Currently only supports
            linear regression.
        tmin: pd.Timestamp | str | None = None
            Minimum time for calibration period.
        tmax: pd.Timestamp | str | None = None
            Maximum time for calibration period.

        Returns
        -------
        FitResultData | list[FitResultData]
            If single wells are provided, returns a single FitResultData object.
            If lists of wells are provided, returns a list of FitResultData objects
            for each obs_well/ref_well pair.

        Raises
        ------
        ValueError
            If lists are provided but have different lengths.
        """
        # Handle single well case (backward compatibility)
        if not isinstance(obs_well, list) and not isinstance(ref_well, list):
            result = self._fit(obs_well, ref_well, offset, p, method, tmin, tmax)
            logger.info(
                f"Fitting model '{self.name}' using reference well '{ref_well.name}' "
                f"and observation well '{obs_well.name}'."
            )
            return result

        # Handle list case
        obs_wells = obs_well if isinstance(obs_well, list) else [obs_well]
        ref_wells = ref_well if isinstance(ref_well, list) else [ref_well]

        # Validate that lists have the same length
        if len(obs_wells) != len(ref_wells):
            error_msg = (
                f"obs_well list length ({len(obs_wells)}) must match "
                f"ref_well list length ({len(ref_wells)})"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Perform fitting for each pair
        results = []
        for obs_w, ref_w in zip(obs_wells, ref_wells, strict=True):
            result = self._fit(obs_w, ref_w, offset, p, method, tmin, tmax)
            results.append(result)
            logger.info(
                f"Fitting model '{self.name}' using reference well '{ref_w.name}' "
                f"and observation well '{obs_w.name}'."
            )

        return results

    def _fit(
        self,
        obs_well: Well,
        ref_well: Well,
        offset: pd.DateOffset | pd.Timedelta | str,
        p: float = 0.95,
        method: Literal["linearregression"] = "linearregression",
        tmin: pd.Timestamp | str | None = None,
        tmax: pd.Timestamp | str | None = None,
    ) -> FitResultData:
        # Check that the ref_well is a reference well
        if not ref_well.is_reference:
            logger.error(f"The well '{ref_well.name}' is not a reference well.")
            raise ValueError(f"The well '{ref_well.name}' is not a reference well.")

        # Check that the obs_well is an observation well
        if obs_well.is_reference:
            logger.error(f"The well '{obs_well.name}' is not an observation well.")
            raise ValueError(f"The well '{obs_well.name}' is not an observation well.")

        fit = None
        if method == "linearregression":
            logger.debug("Using linear regression method for fitting.")
            fit = linregressfit(obs_well, ref_well, offset, tmin, tmax, p)
        if fit is None:
            logger.error(f"Fitting method '{method}' is not implemented.")
            raise NotImplementedError(f"Fitting method '{method}' is not implemented.")

        self.fits.append(fit)
        logger.info(f"Fit completed for model '{self.name}' with RMSE {fit.rmse}.")
        return fit

    def best_fit(
        self,
        obs_well: str | Well,
        ref_wells: list[str | Well] | None = None,
        method: Literal["linearregression"] = "linearregression",
        **kwargs,
    ) -> FitResultData:
        """
        Find the best fit for the model using the provided wells.

        Parameters
        ----------
        obs_well : Well or list of Well or None, optional
            The observation well to use for fitting.
        ref_wells : Well or list of Well or None, optional
            The reference wells to test. If None, all reference wells in the
            model will be used (default is None).
        method : Literal["linearregression"]
            Method with which to perform regression. Currently only supports
            linear regression.
        **kwargs
            Keyword arguments to pass to the fitting method. For example, you can use
            `offset`, `p`, `tmin`, and `tmax` to control

        Returns
        -------
        FitResultData
            Returns the best fit for the given observation well.
        """
        return self._best_fit(obs_well, ref_wells, method, **kwargs)

    def _best_fit(
        self,
        obs_well: str | Well,
        ref_wells: list[str | Well] | None = None,
        method: Literal["linearregression"] = "linearregression",
        **kwargs,
    ) -> FitResultData:
        """
        The internal method to find the best fit.

        Parameters
        ----------
        obs_well : Well or list of Well or None, optional
            The observation well to use for fitting.
        ref_wells : Well or list of Well or None, optional
            The reference wells to test. If None, all reference wells in the
            model will be used (default is None).
        method : Literal["linearregression"]
            Method with which to perform regression. Currently only supports
            linear regression.
        **kwargs
            Keyword arguments to pass to the fitting method. For example, you can use
            `offset`, `p`, `tmin`, and `tmax` to control

        Returns
        -------
        FitResultData
            Returns the best fit for the given arguments.
        """
        if isinstance(ref_wells, list) and len(ref_wells) < 1:
            logger.error("ref_wells list cannot be empty.")
            raise ValueError("ref_wells list cannot be empty.")

        if isinstance(obs_well, str):
            target_obs_well = self.get_wells(obs_well)
            if isinstance(target_obs_well, list):
                logger.error(
                    "obs_well parameter must resolve to a single well, not a list."
                )
                raise ValueError(
                    "obs_well parameter must resolve to a single well, not a list."
                )
        elif isinstance(obs_well, Well):
            target_obs_well = obs_well
        if ref_wells is None:
            target_ref_wells = self.ref_wells
            if len(target_ref_wells) < 1:
                logger.error("No reference wells available in the model.")
                raise ValueError("No reference wells available in the model.")
        else:
            target_ref_wells: list[Well] = []
            for rw in ref_wells:
                if isinstance(rw, str):
                    target_ref_wells.append(self.get_wells(rw))  # type: ignore
                elif isinstance(rw, Well):
                    target_ref_wells.append(rw)
                else:
                    logger.error(
                        f"Unsupported type for {rw}. Supported types are Well or str"
                    )
                    raise TypeError(
                        f"Unsupported type for {rw}. Supported types are Well or str"
                    )

        local_fits: list[FitResultData] = []
        for ref_well in target_ref_wells:
            logger.debug(
                f"Testing fit for observation well '{target_obs_well.name}' "
                f"and reference well '{ref_well.name}'."
            )
            fit = self._fit(target_obs_well, ref_well, method=method, **kwargs)
            local_fits.append(fit)
            logger.debug(
                f"Fit result for observation well '{target_obs_well.name}' and"
                f"reference well '{ref_well.name}': RMSE={fit.rmse}"
            )
        return min(local_fits, key=lambda x: x.rmse)

    def get_fits(self, well: Well | str) -> list[FitResultData] | FitResultData | None:
        """
        Get all fit results involving a specific well.

        Parameters
        ----------
        well : Well | str
            The well to check.

        Returns
        -------
        list[FitResultData] | FitResultData | None
            A list of fit results involving the specified well.
        """
        target_well: Well
        if isinstance(well, str):
            target_well = self.get_wells(well)  # type: ignore
        elif isinstance(well, Well):
            target_well = well
        else:
            logger.error("Parameter 'well' must be a Well instance or a string.")
            raise TypeError("Parameter 'well' must be a Well instance or a string.")

        fit_list = [fit for fit in self.fits if fit.has_well(target_well)]
        return (
            fit_list
            if len(fit_list) > 1
            else (fit_list[0] if len(fit_list) == 1 else None)
        )

    # ======================== Load and Save Methods ========================

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
            This method adds wells, fits, and properties to the model.
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
                rmse=fit_data.get("rmse", None),
                n=fit_data.get("n", None),
                fit_method=unpack_dict_fit_method(fit_data),
                t_a=fit_data.get("t_a", None),
                stderr=fit_data.get("stderr", None),
                pred_const=fit_data.get("pred_const", None),
                p=fit_data.get("p", None),
                offset=fit_data.get("offset", None),
                tmin=float_to_datetime(fit_data.get("tmin", None)),
                tmax=float_to_datetime(fit_data.get("tmax", None)),
            )
            self.fits.append(fit)

    def save_project(self, filename=None, overwrite=False):
        """
        Save the model to a file.

        Parameters
        ----------
        filename : str or None, optional
            The name of the file where the model will be saved. The path can be
            included.
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
