"""
Model
-----
A class representing a groundwater model that can contain multiple wells.

"""
import logging
from src.gwrefpy.well import WellBase
from src.gwrefpy.io.io import save, load

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, name: str):
        self.name = name

        # Well attributes
        self.wells = []

        # Model attributes
        self.model_attribute = {}

    def add_well(self, well):
        """
        Add a well or a list of wells to the model.

        Parameters
        ----------
        well : WellBase or list of WellBase
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
        well : WellBase
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
        if not isinstance(well, WellBase):
            logger.error("Only WellBase instances can be added to the model.")
            raise TypeError("Only WellBase instances can be added to the model.")
        if well in self.wells:
            logger.error(f"Well '{well.name}' is already in the model.")
            raise ValueError(f"Well '{well.name}' is already in the model.")
        self.wells.append(well)
        #TODO: add model also to well
        logger.debug(f"Well '{well.name}' added to model '{self.name}'.")

    def save(self, filepath, overwrite=False):
        """
        Save the model to a file.

        Parameters
        ----------
        filepath : str
            The path to the file where the model will be saved.

        Returns
        -------
        None
            This method saves the model to a file.
        """
        # Convert model to dict before saving
        # Placeholder for actual conversion logic
        # model_dict = self.to_dict()

        # Save the model dictionary to a file
        save(self, filepath, overwrite=overwrite)
        logger.info(f"Model '{self.name}' saved to '{filepath}'.")

    def load(self, filepath):
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
        logger.info(f"Model '{self.name}' loaded from '{filepath}'.")