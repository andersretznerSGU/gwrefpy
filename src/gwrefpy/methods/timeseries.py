import numpy as np
import pandas as pd


def groupby_time_equivalents(
    ref_timeseries: pd.Series,
    obs_timeseries: pd.Series,
    offset: pd.DateOffset | pd.Timedelta | str,
) -> tuple[pd.Series, pd.Series, int]:
    """
    Groups the reference and observation timeseries by their time equivalents.
    Currently, this function uses the mean to aggregate within each time equivalent.

    Parameters
    ----------
    ref_timeseries : pd.Series
        The reference timeseries data.
    obs_timeseries: pd.Series
        The observed timeseries data.
    offset: pd.DateOffset | pd.Timedelta | str
        Maximum date offset to allow to group pairs of data points.

    Returns
    -------
    pd.Series
        Reference time series data grouped by their time equivalents.
    pd.Series
        Observed time series data grouped by their time equivalents.
    int
        Number of grouped pairs of data points.
    """
    if not ref_timeseries.name:
        ref_timeseries.name = "ref"
    if not obs_timeseries.name:
        obs_timeseries.name = "obs"

    time_equivalents = _create_time_equivalents(
        ref_timeseries.index, obs_timeseries.index, offset
    )

    combined = pd.concat([ref_timeseries, obs_timeseries], axis="columns")
    combined_time_eqs = combined.set_index(time_equivalents, drop=True)
    time_eq_means = combined_time_eqs.groupby(combined_time_eqs.index).mean()

    time_eq_means = time_eq_means.dropna()

    return (
        time_eq_means[ref_timeseries.name],
        time_eq_means[obs_timeseries.name],
        len(time_eq_means),
    )


def _create_time_equivalents(
    ref_index: pd.DatetimeIndex,
    obs_index: pd.DatetimeIndex,
    offset: pd.DateOffset | pd.Timedelta | str,
) -> pd.Series:
    timestamps = ref_index.union(obs_index).to_series().sort_index().index
    ts_diffs = timestamps.diff()
    starts = ts_diffs > offset
    starts[0] = True

    return pd.Series(index=timestamps, data=np.cumsum(starts), name="time_equivalents")
