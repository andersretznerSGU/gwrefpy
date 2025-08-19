from os import path
import json

def save(filename, data, **kwargs):
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
    ext = path.splitext(filename)[1]
    if ext not in ['.gwref']:
        ext = '.gwref'
    filename = path.splitext(filename)[0] + ext

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