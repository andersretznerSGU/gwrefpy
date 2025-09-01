import matplotlib.pyplot as plt

from src.gwrefpy.constants import tfont, afont, lfont, tifont, DEFAULT_COLORS, DEFAULT_LINE_STYLES, \
    DEFAULT_MARKER_STYLES


class Plotter:

    def __init__(self):
        self.wells = None
        self.cnt_colors = 0
        self.cnt_linestyles = 0
        self.cnt_markers = 0


    def plot(self, title="Well Data Plot", xlabel="Time", ylabel="Measurement"):
        # Placeholder for plotting logic
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(title, **tfont)
        ax.set_xlabel(xlabel, **afont)
        ax.set_ylabel(ylabel, **afont)
        for cnt, well in enumerate(self.wells):
            self._set_plot_attributes(well)
            self._plot_well(well, ax)
            print(f"Plotting data for well: {well.name}")


        self.default_plot_settings(ax)

    def _plot_well(self, well, ax):
        ax.plot(well.timeseries.index, well.timeseries.values, label=well.name, color=well.color, alpha=well.alpha,
                linestyle=well.linestyle, linewidth=well.linewidth, marker=well.marker if well.marker_vissible else None, markersize=well.markersize)
        # Placeholder for individual well plotting logic
        print(f"Plotting individual well: {well.name}")
        if well.is_reference is False:
            self._plot_fit(well, ax)

    def _plot_fit(self, well, ax):
        fits = [fit for fit, include in zip(self.fits, self.well_in_fits(well)) if include]
        for fit in fits:
            pred_const = fit.pred_const
            fit_timeseries = fit.fit_timeseries()
            x = fit_timeseries.index
            y = fit_timeseries.values
            ax.plot(x, y, linestyle='-', color='black', alpha=0.7)
            ax.fill_between(
                x,
                y - pred_const,
                y + pred_const,
                color='gray',
                alpha=0.2
            )
        print(f"Plotting fit for well: {well.name}")

    def _set_plot_attributes(self, well):
        # Set default plot attributes if not already set
        if well.color is None:
            cnt = self.cnt_colors
            well.color = DEFAULT_COLORS[cnt % len(DEFAULT_COLORS)]
            self.cnt_colors += 1
        if well.linestyle is None:
            cnt = self.cnt_linestyles
            well.linestyle = DEFAULT_LINE_STYLES[cnt % len(DEFAULT_LINE_STYLES)]
            self.cnt_linestyles += 1
        if well.marker is None:
            cnt = self.cnt_markers
            well.marker = DEFAULT_MARKER_STYLES[cnt % len(DEFAULT_MARKER_STYLES)]
            self.cnt_markers += 1
        if well.markersize is None:
            well.markersize = 6
        if well.alpha is None:
            well.alpha = 1.0


    @staticmethod
    def default_plot_settings(ax):
        # Hide the all but the bottom spines (axis lines)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")

        # Set ticks font
        xticks = ax.get_xticks()
        yticks = ax.get_yticks()
        xlabels = [item.get_text() for item in ax.get_xticklabels()]
        ylabels = [item.get_text() for item in ax.get_yticklabels()]
        ax.xaxis.set_major_locator(plt.FixedLocator(xticks)) # Needed to suppress warnings
        ax.yaxis.set_major_locator(plt.FixedLocator(yticks))
        ax.set_xticklabels(xlabels, **tifont)
        ax.set_yticklabels(ylabels, **tifont)

        # Add grid lines
        ax.grid(visible=True, which='major', color='lightgrey', linestyle='--', linewidth=0.5)
        ax.grid(visible=True, which='minor', color='lightgrey', linestyle=':', linewidth=0.5)

        # Set font sizes and styles
        ax.title.set_fontsize(16)
        ax.xaxis.label.set_fontsize(14)
        ax.yaxis.label.set_fontsize(14)
        ax.tick_params(axis='both', which='major', labelsize=12)

        # Legend
        ax.legend(prop=lfont)

