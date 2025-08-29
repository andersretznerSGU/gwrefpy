User guide
==========

Getting Started
----------------
To get started with gwrefpy, you can follow these steps:

**Import the package**: Start by importing the gwrefpy package in your Python script or Jupyter notebook.

   .. code-block:: python

       import gwrefpy

**Load Data**: Use the provided functions to load gravitational wave data. You can load data from files or directly from online repositories.

   .. code-block:: python

       data = gwrefpy.load_data('path_to_your_data_file')

**Process Data**: Utilize the data processing functions to clean and prepare your data for analysis.

    .. code-block:: python

         processed_data = gwrefpy.process_data(data)


.. toctree::
    :maxdepth: 1

    plotting