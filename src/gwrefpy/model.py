import logging
from src.gwrefpy.well import WellBase

logger = logging.getLogger(__name__)

class Model:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

        self.wells = []

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
        logger.debug(f"Well '{well.name}' added to model '{self.name}'.")
