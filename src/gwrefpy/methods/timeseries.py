
from collections.abc import Sequence
from typing import Literal
import numpy as np
import pandas as pd
from ..well import Well

def groupby_time_equivalents(
    obs_timeseries: pd.Series,
    ref_timeseries: pd.Series,
    offset: pd.DateOffset | pd.Timedelta | str,
    aggregation: Literal["mean", "median", "min", "max"] = "mean",
) -> tuple[pd.Series, pd.Series, int]:
    """
    Groups the reference and observation timeseries by their time equivalents.
    For each observation time point, finds all reference time points within the offset
    and aggregates the reference values. Creates one group per observation time point.
    Parameters
    ----------
    obs_timeseries: pd.Series
        The observed timeseries data.
    ref_timeseries : pd.Series
        The reference timeseries data.
    offset: pd.DateOffset | pd.Timedelta | str
        Maximum date offset to allow for matching reference points to each observation point.
    aggregation: Literal["mean", "median", "min", "max"], optional
        The aggregation method to use when multiple reference points match an observation point.
        Default is "mean".
    Returns
    -------
    pd.Series
        Reference time series data grouped by their time equivalents (aggregated per obs time).
    pd.Series
        Observed time series data (one per obs time).
    int
        Number of grouped pairs of data points (number of obs times with at least one ref match).
    """
    if not obs_timeseries.name or obs_timeseries.name != "obs":
        obs_timeseries.name = "obs"
    if not ref_timeseries.name or ref_timeseries.name != "ref":
        ref_timeseries.name = "ref"
    # Convert offset to Timedelta for easier comparison
    if isinstance(offset, str):
        offset_td = pd.Timedelta(offset)
    elif isinstance(offset, pd.DateOffset):
        # Approximate DateOffset to Timedelta (this is a simplification)
        offset_td = pd.Timedelta(days=offset.days if hasattr(offset, 'days') else 1)
    else:
        offset_td = offset
    ref_agg = []
    obs_agg = []
    for obs_time, obs_val in obs_timeseries.items():
        # Find ref times within offset
        ref_mask = (ref_timeseries.index >= obs_time - offset_td) & (ref_timeseries.index <= obs_time + offset_td)
        matching_refs = ref_timeseries[ref_mask]
        if not matching_refs.empty:
            # Aggregate ref values
            agg_ref_val = getattr(matching_refs, aggregation)()
            ref_agg.append((obs_time, agg_ref_val))
            obs_agg.append((obs_time, obs_val))
    if ref_agg:
        ref_series = pd.Series([v for _, v in ref_agg], index=[t for t, _ in ref_agg], name="ref")
        obs_series = pd.Series([v for _, v in obs_agg], index=[t for t, _ in obs_agg], name="obs")
        n = len(ref_series)
    else:
        ref_series = pd.Series([], dtype=float, name="ref")
        obs_series = pd.Series([], dtype=float, name="obs")
        n = 0
    return ref_series, obs_series, n

def analyze_offsets(
    ref: pd.Series | Well,
    obs: pd.Series | Well,
    offsets: Sequence[pd.DateOffset | pd.Timedelta | str],
) -> pd.Series:
    """
    Tests the grouping of time series data by different offsets. This can be helpful
    when choosing an offset.
    Parameters
    ----------
    ref: pd.Series | Well
        The reference time series data.
    obs: pd.Series | Well
        The observed time series data.
    offsets: list[pd.DateOffset | pd.Timedelta | str]
        The list of offsets to test.
    Returns
    -------
    pd.Series
        The number of observation points with at least one matching reference point within each offset.
    """
    if isinstance(ref, Well):
        ref = ref.timeseries
    if isinstance(obs, Well):
        obs = obs.timeseries
    data = []
    idx = []
    for offset in offsets:
        _, _, n_pairs = groupby_time_equivalents(ref, obs, offset)
        data.append(n_pairs)
        if isinstance(offset, (pd.DateOffset, pd.Timedelta)):
            idx.append(str(offset))
        else:
            idx.append(offset)
    return pd.Series(index=idx, data=data, name="n_pairs")
