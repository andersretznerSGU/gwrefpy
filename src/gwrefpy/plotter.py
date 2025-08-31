import matplotlib.pyplot as plt

class Plotter:

    def __init__(self):
        self.wells = None


    def plot(self):
        # Placeholder for plotting logic
        fig, ax = plt.subplots(figsize=(10, 6))
        self.default_plot_settings(ax)
        ax.set_title("Well Data Plot")
        ax.set_xlabel("Time")
        ax.set_ylabel("Measurement")
        for well in self.wells:
            self._plot_well(well, ax)
            print(f"Plotting data for well: {well.name}")


    def _plot_well(self, well, ax):
        ax.plot(well.timeseries.index, well.timeseries.values, label=well.name, color=well.color, alpha=well.alpha,
                linestyle=well.linestyle, linewidth=well.linewidth, marker=well.marker, markersize=well.markersize)
        # Placeholder for individual well plotting logic
        print(f"Plotting individual well: {well.name}")
        if well.is_reference is False:
            self._plot_fit(well, ax)

    def _plot_fit(self, well, ax):
        fits = [fit for fit, include in zip(self.fits, self.well_in_fits(well)) if include]
        for fit in fits:
            pred_const = fit.pred_const
            well_ref = fit.ref_well
            vals = well_ref.timeseries.apply(lambda x: fit.fit_method.slope * x + fit.fit_method.intercept)
            ax.plot(well_ref.timeseries.index, vals, linestyle='-', color='black', alpha=0.7)
            ax.plot(well.timeseries.index, well.timeseries.values + pred_const, linestyle='--', color='gray', alpha=0.7)
            ax.plot(well.timeseries.index, well.timeseries.values - pred_const, linestyle='--', color='gray', alpha=0.7)
            ax.fill_between(
                well.timeseries.index,
                well.timeseries.values - pred_const,
                well.timeseries.values + pred_const,
                color='gray',
                alpha=0.2
            )
        print(f"Plotting fit for well: {well.name}")


    @staticmethod
    def default_plot_settings(ax):
        # Hide the all but the bottom spines (axis lines)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")

        # Add grid lines
        ax.grid(visible=True, which='major', color='lightgrey', linestyle='--', linewidth=0.5)
        ax.grid(visible=True, which='minor', color='lightgrey', linestyle=':', linewidth=0.5)

