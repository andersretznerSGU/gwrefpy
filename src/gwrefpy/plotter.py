import matplotlib.pyplot as plt
import logging

from .constants import (
    DEFAULT_COLORS,
    DEFAULT_LINE_STYLES,
    DEFAULT_MARKER_STYLES,
    afont,
    lfont,
    tfont,
    tifont,
)

logger = logging.getLogger(__name__)

class Plotter:
    def __init__(self):
        self.wells = None
        self.cnt_colors = 0
        self.cnt_linestyles = 0
        self.cnt_markers = 0

    def plot(self, title: str="Well Data Plot", xlabel: str="Time", ylabel: str="Measurement"):
        """
        This method plots the time series data for all wells in the model.
        It also overlays the fitted models if available.

        Parameters
        ----------
        title : str
            The title of the plot.
        xlabel : str
            The label for the x-axis.
        ylabel : str
            The label for the y-axis.

        Returns
        -------
        fig : matplotlib.figure.Figure
            The figure object containing the plot.
        ax : matplotlib.axes.Axes
            The axes object of the plot.
        """
        # Placeholder for plotting logic
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(title, **tfont)
        ax.set_xlabel(xlabel, **afont)
        ax.set_ylabel(ylabel, **afont)
        for _cnt, well in enumerate(self.wells):
            logger.info(f"Plotting well: {well.name}")
            self._set_plot_attributes(well)
            self._plot_well(well, ax)
            if well.is_reference is False:
                self._mark_outliers(well, ax)
        self._default_plot_settings(ax)

        return fig, ax

    def _plot_well(self, well, ax):
        ax.plot(
            well.timeseries.index,
            well.timeseries.values,
            label=well.name,
            color=well.color,
            alpha=well.alpha,
            linestyle=well.linestyle,
            linewidth=well.linewidth,
            marker=well.marker if well.marker_visible else None,
            markersize=well.markersize,
        )
        ax.text(
            well.timeseries.index[-1],
            well.timeseries.values[-1],
            f" {well.name}",
            color=well.color,
            horizontalalignment="left",
            verticalalignment="center",
            **lfont,
        )
        if well.is_reference is False:
            self._plot_fit(well, ax)

    def _plot_fit(self, well, ax):
        fits = self.get_fits(well)
        if isinstance(fits, list) is False:
            fits = [fits]
        for fit in fits:
            pred_const = fit.pred_const
            fit_timeseries = fit.fit_timeseries()
            x = fit_timeseries.index
            y = fit_timeseries.values
            ax.plot(x, y, linestyle="-", color="gray", alpha=0.2)
            ax.fill_between(x, y - pred_const, y + pred_const, color="gray", alpha=0.2)
        logger.info(f"Plotting fit for well: {well.name}")

    def _mark_outliers(self, well, ax):
        fit = self.get_fits(well)
        if isinstance(fit, list):
            fit = fit[0]
        outliers = fit.fit_outliers()
        well_outliers = well.timeseries[outliers]
        if well_outliers is not None and not well_outliers.empty:
            ax.scatter(
                well_outliers.index,
                well_outliers.values,
                edgecolor="red",
                facecolors='none',
                marker="o",
                s=50,
                label=f"{well.name} Outliers",
                zorder=5,
            )
            logger.info(f"Marking outliers for well: {well.name}")

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
    def _default_plot_settings(ax):
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
        ax.xaxis.set_major_locator(
            plt.FixedLocator(xticks)
        )  # Needed to suppress warnings
        ax.yaxis.set_major_locator(plt.FixedLocator(yticks))
        ax.set_xticklabels(xlabels, **tifont)
        ax.set_yticklabels(ylabels, **tifont)
        ax.spines["bottom"].set_bounds(min(xticks), max(xticks))

        # Add grid lines
        ax.grid(
            visible=True,
            which="major",
            color="lightgrey",
            linestyle="--",
            linewidth=0.5,
        )
        ax.grid(
            visible=True, which="minor", color="lightgrey", linestyle=":", linewidth=0.5
        )

        # Set font sizes and styles
        ax.title.set_fontsize(16)
        ax.xaxis.label.set_fontsize(14)
        ax.yaxis.label.set_fontsize(14)
        ax.tick_params(axis="both", which="major", labelsize=12)

        # Tight layout
        plt.tight_layout()

    def get_fits(self, well):
        raise NotImplementedError("Subclasses should implement this method.")
