import os
from os import path
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

def save(filename, data, overwrite=False, **kwargs):
    """
    Save an object to a file.

    Parameters
    ----------
    filename : str
        The name of the file where the object will be saved.
    data : dict
        The data to save, typically a dictionary containing the object and its metadata.
    **kwargs : dict
        Additional keyword arguments that may be used for saving options.

    Returns
    -------
    Message
        A message indicating the success or failure of the save operation.
    """
    # Check the filename extension
    ext = os.path.splitext(filename)[1]
    if ext == "":
        filename += ".gwref"
    elif ext not in ['.gwref']:
        raise ValueError(f"Unsupported file extension: {ext}. Expected '.gwref'.")
    filename = path.splitext(filename)[0] + ext

    # Check if the file already exists
    if os.path.exists(f"{filename}") and not overwrite:
        # If the file exists and overwrite is False, log a warning and return
        logger.warning(
            f"The file {filename} already exists. To overwrite the existing file set the argument 'overwrite' to True."
        )
        return

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    return f"Object saved to {filename}"

def load(filename):
    """
    Load an object from a file.

    Parameters
    ----------
    filename : str
        The name of the file from which the object will be loaded.

    Returns
    -------
    object
        The loaded object.
    """
    ext = path.splitext(filename)[1]
    if ext not in ['.gwref']:
        raise ValueError(f"Unsupported file extension: {ext}. Expected '.gwref'.")

    with open(filename, 'r') as file:
        data = json.load(file)

    return data