Plotting
========

The gwrefpy package has several plotting capabilities to visualize groundwater data. Below are some examples of how to use these plotting functions.

Setting plotting style
----------------------
You can set the individual plotting styles of each well object by assigning the plotting attributes to that object. The available attributes are: ``color``, ``linestyle``, ``linewidth``, ``label``, ``alpha``, ``marker``, and ``markersize``

.. code-block:: python

    import gwrefpy
    import matplotlib.pyplot as plt

    # Create the model
    model = gwrefpy.Model()
    well1 = gwrefpy.Well(name='Well 1', x=0, y=0, depth=100, model=model)

    # The plotting atribute can either be set in the well initialization or after
    well1.set_kwargs(color='blue', linestyle='--')

    # Plot the well with default style
    model.plot_wells(show=True)

Plotting kwargs
---------------
The plotting functions in gwrefpy accept additional keyword arguments (kwargs) that can be used to customize the appearance of the plots. These kwargs are passed directly to the underlying matplotlib functions. Currently kwargs are passed to the following functions: ``plt.subplot()`` and ``plt.savefig()``.

