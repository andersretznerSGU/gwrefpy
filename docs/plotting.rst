Plotting
========

The gwrefpy package has several plotting capabilities to visualize groundwaer data. Below are some examples of how to use these plotting functions.

Setting plotting style
----------------------
You can set the indivudual plotting syles of each well object by assigning the plotting attributes to that object. The available attributes are:
- color
- linestyle
- linewidth
- label
- alpha
- marker
- markersize

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
