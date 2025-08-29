import pandas as pd


def adjust_timeseries(
    ref_timeseries: pd.Series,
    obs_timeseries: pd.Series,
    time_equivalent: pd.DateOffset | pd.Timedelta | str,
    calibration_period_start: pd.Timestamp | None = None,
    calibration_period_end: pd.Timestamp | None = None,
):
    """
    Adjusts the observation timeseries based on the time equivalent and calibration period.

    Parameters
    ----------
    ref_timeseries : pd.Series
        The reference timeseries data.
    obs_timeseries : pd.Series
        The observation timeseries data.
    time_equivalent :
        The time equivalent value for adjustment.
    calibration_period_start : pd.Timestamp | None
        The start date of the calibration period.
    calibration_period_end : pd.Timestamp | None
        The end date of the calibration period.

    Returns
    -------
    pd.Series
        The adjusted observation timeseries.
    pd.Series
        The adjusted reference timeseries.
    int
        The number of overlapping data points in the adjusted timeseries.
    """
    # Cut the timeseries to the calibration period
    if calibration_period_start is not None and calibration_period_end is not None:
        cut_ref_timeseries, cut_obs_timeseries = _cut_timeseries(
            ref_timeseries,
            obs_timeseries,
            calibration_period_start,
            calibration_period_end,
        )
    else:
        cut_ref_timeseries = ref_timeseries
        cut_obs_timeseries = obs_timeseries

    # Resample to the desired frequency
    resampled_ref_timeseries = cut_ref_timeseries.resample(time_equivalent).mean()
    resampled_obs_timeseries = cut_obs_timeseries.resample(time_equivalent).mean()

    common_times = resampled_ref_timeseries.index.intersection(
        resampled_obs_timeseries.index
    )
    aligned_ref = resampled_ref_timeseries.loc[common_times]
    aligned_obs = resampled_obs_timeseries.loc[common_times]

    return aligned_ref, aligned_obs, len(common_times)


def _cut_timeseries(
    ref_timeseries: pd.Series,
    obs_timeseries: pd.Series,
    calibration_period_start: pd.Timestamp,
    calibration_period_end: pd.Timestamp,
):
    """
    Cut the timeseries to the specified calibration period.

    Parameters
    ----------
    calibration_period_start : datetime
        The start date of the calibration period.
    calibration_period_end : datetime
        The end date of the calibration period.

    Returns
    -------
    cut_ref_timeseries : pd.Series
        The cut reference timeseries.
    cut_obs_timeseries : pd.Series
        The cut observation timeseries.
    """
    cut_ref_timeseries = ref_timeseries[calibration_period_start:calibration_period_end]
    cut_obs_timeseries = obs_timeseries[calibration_period_start:calibration_period_end]
    return cut_ref_timeseries, cut_obs_timeseries
