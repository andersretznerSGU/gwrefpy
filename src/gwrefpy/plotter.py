import logging

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num, num2date

from .constants import (
    DEFAULT_COLORS,
    DEFAULT_LINE_STYLES,
    DEFAULT_MARKER_STYLES,
    DEFAULT_MONOCHROME_COLORS,
    afont,
    lfont,
    tfont,
    tifont,
)
from .fitresults import FitResultData

logger = logging.getLogger(__name__)


class Plotter:
    def __init__(self):
        self.wells = None
        self.cnt_colors = 0
        self.cnt_linestyles = 0
        self.cnt_markers = 0
        self.plot_style = None
        self.color_style = None
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None

        self.fits = []

    def plot_fits(
        self,
        fits: FitResultData | list[FitResultData] = None,
        title: str = "Well Data Plot",
        xlabel: str = "Time",
        ylabel: str = "Measurement",
        mark_outliers: bool = True,
        plot_style: str = "fancy",
        color_style: str = "color",
        save_path: str | None = None,
        num: int = 6,
        **kwargs,
    ):
        """
        This method plots the time series data for all wells in the model.
        It also overlays the fitted models if available.

        Parameters
        ----------
        fits : FitResultData | list[FitResultData]
            A FitResultData instance or a list of FitResultData instances
            containing the fit results to be plotted. If None, all fits will be plotted.
        title : str
            The title of the plot.
        xlabel : str
            The label for the x-axis.
        ylabel : str
            The label for the y-axis.
        mark_outliers : bool
            If True, outliers will be marked on the plot.
        plot_style : str
            The style of the plot. Options are "fancy" or "scientific".
        color_style : str
            The color style of the plot. Options are "color" or "monochrome".
        save_path : str | None
            If provided, the plot will be saved to this path.
        num : int
            Number of ticks on the x-axis (default is 6).
        **kwargs : dict
            Additional keyword arguments for customization. See the documentation of
            Matplotlib's `plt.subplots` and `plt.savefig` for more details.
            Common kwargs include:

            - figsize (tuple): Size of the figure (width, height) in inches.
            - dpi (int): Dots per inch for the saved figure.

        Returns
        -------
        fig : matplotlib.figure.Figure
            The figure object containing the plot.
        ax : matplotlib.axes.Axes
            The axes object of the plot.
        """
        if fits is not None and not (
            isinstance(fits, FitResultData)
            or (
                isinstance(fits, list)
                and all(isinstance(f, FitResultData) for f in fits)
            )
        ):
            logger.error(
                "fits must be a FitResultData instance or a list of "
                "FitResultData instances"
            )
            raise TypeError(
                "fits must be a FitResultData instance or a list of "
                "FitResultData instances"
            )
        if fits is None:
            fits = self.fits
        elif isinstance(fits, FitResultData):
            fits = [fits]

        # Store the plot style
        if plot_style not in ["fancy", "scientific"]:
            logger.error("Invalid plot_style. Must be 'fancy' or 'scientific'.")
            raise ValueError("plot_style must be 'fancy' or 'scientific'")
        self.plot_style = plot_style

        if color_style not in ["color", "monochrome"]:
            logger.error("Invalid color_style. Must be 'color' or 'monochrome'.")
            raise ValueError("color_style must be 'color' or 'monochrome'")
        self.color_style = color_style

        # Create the plot
        figsize = kwargs.pop("figsize", (10, 6))
        fig, ax = plt.subplots(figsize=figsize, **kwargs)
        ax.set_title(title, **tfont)
        ax.set_xlabel(xlabel, **afont)
        ax.set_ylabel(ylabel, **afont)
        for fit in fits:
            logger.info(f"Plotting fit: {fit.obs_well.name} ~ {fit.ref_well.name}")
            self._set_plot_attributes(fit.obs_well)
            self._set_plot_attributes(fit.ref_well)
            self._plot_well(fit.obs_well, ax)
            self._plot_well(fit.ref_well, ax)
            if mark_outliers:
                self._mark_outliers(fit.obs_well, ax)
        self._plot_settings(ax, num, **kwargs)

        if save_path is not None:
            plt.savefig(save_path, **kwargs)
            logger.info(f"Plot saved to {save_path}")

        return fig, ax

    def _plot_well(self, well, ax):
        """Plot the time series data for a single well."""
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
        self._update_axis_limits(well)
        if self.plot_style == "fancy":
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
        """Plot the fitted model for a single well."""
        fits = self.get_fits(well)
        if isinstance(fits, list) is False:
            fits = [fits]
        for fit in fits:
            pred_const = fit.pred_const
            fit_timeseries = fit.fit_timeseries()
            x = fit_timeseries.index
            y = fit_timeseries.values
            ax.plot(x, y, linestyle="-", color=well.color, alpha=0.2, label=None)
            ax.fill_between(
                x,
                y - pred_const,
                y + pred_const,
                color=well.color,
                alpha=0.2,
                label=None,
            )
        logger.info(f"Plotting fit for well: {well.name}")

    def _mark_outliers(self, well, ax):
        """Mark outliers on the plot for a single well."""
        fit = self.get_fits(well)
        if isinstance(fit, list):
            fit = fit[0]
        outliers = fit.fit_outliers()
        well_outliers = well.timeseries[outliers]
        edgecolor = "red" if self.color_style == "color" else "black"
        if well_outliers is not None and not well_outliers.empty:
            ax.scatter(
                well_outliers.index,
                well_outliers.values,
                edgecolor=edgecolor,
                facecolors="none",
                marker="o",
                s=50,
                label=None,
                zorder=500,
            )
            logger.info(f"Marking outliers for well: {well.name}")

    def _set_plot_attributes(self, well):
        """Set default plot attributes for a well if not already set."""
        # Set default plot attributes if not already set
        if well.color is None:
            cnt = self.cnt_colors
            if self.color_style == "monochrome":
                well.color = DEFAULT_MONOCHROME_COLORS[
                    cnt % len(DEFAULT_MONOCHROME_COLORS)
                ]
            else:
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

    def _update_axis_limits(self, well):
        """Update the axis limits based on the well's time series data."""
        if self.xmin is None or well.timeseries.index.min() < self.xmin:
            self.xmin = well.timeseries.index.min()
        if self.xmax is None or well.timeseries.index.max() > self.xmax:
            self.xmax = well.timeseries.index.max()
        if self.ymin is None or well.timeseries.min() < self.ymin:
            self.ymin = well.timeseries.min()
        if self.ymax is None or well.timeseries.max() > self.ymax:
            self.ymax = well.timeseries.max()

    def _plot_settings(self, ax, num):
        """Apply final plot settings based on the selected style."""
        if self.plot_style == "fancy":
            self._plot_settings_fancy(ax)
        elif self.plot_style == "scientific":
            self._plot_settings_scientific(ax)

        # limit x axis to data range
        ax.set_xlim(left=self.xmin, right=self.xmax)

        # Set ticks font
        xticks = np.linspace(date2num(self.xmin), date2num(self.xmax), num=num)
        xlabels = [f"{num2date(tick):%Y-%m-%d}" for tick in xticks]
        yticks = ax.get_yticks()
        ylabels = [item.get_text() for item in ax.get_yticklabels()]
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
        ax.set_xticklabels(xlabels, **tifont)
        ax.set_yticklabels(ylabels, **tifont)

        # Set font sizes and styles
        ax.title.set_fontsize(16)
        ax.xaxis.label.set_fontsize(14)
        ax.yaxis.label.set_fontsize(14)
        ax.tick_params(axis="both", which="major", labelsize=12)

        # Tight layout
        plt.tight_layout()

    def _plot_settings_fancy(self, ax):
        """Apply fancy plot settings."""
        # Hide the all but the bottom spines (axis lines)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")
        ax.spines["bottom"].set_bounds(date2num(self.xmin), date2num(self.xmax))

        # Add grid lines
        ax.grid(
            visible=True,
            which="major",
            color="#E8E8E8",
            linestyle="--",
            linewidth=0.5,
        )
        ax.grid(
            visible=True, which="minor", color="#E8E8E8", linestyle=":", linewidth=0.5
        )

    def _plot_settings_scientific(self, ax):
        """Apply scientific plot settings."""
        # Add grid lines
        ax.grid(
            visible=True,
            which="major",
            color="black",
            linestyle="--",
            linewidth=0.5,
        )
        ax.grid(
            visible=True, which="minor", color="black", linestyle=":", linewidth=0.5
        )

        ax.legend(prop=lfont)

    def get_fits(self, well):
        raise NotImplementedError("Subclasses should implement this method.")
