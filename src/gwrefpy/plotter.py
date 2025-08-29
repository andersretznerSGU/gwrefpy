

class Plotter:
    well_list = None

    def __init__(self):
        pass

    @classmethod
    def plot(cls, data):
        # Placeholder for plotting logic
        for well in cls.well_list:
            print(f"Plotting data for well: {well.name}")

    @classmethod
    def _plot_well(cls, well):
        # Placeholder for individual well plotting logic
        print(f"Plotting individual well: {well.name}")