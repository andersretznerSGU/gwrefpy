import datetime

import pandas as pd

from gwrefpy.utils.conversions import datetime_to_float
from gwrefpy.well import Well


def test_datetime_to_float():
    # Use timezone-aware datetime to ensure consistent behavior across environments
    time = datetime.datetime(2025, 8, 27, 20, 15, 16, 626237, tzinfo=datetime.UTC)
    expected = 1756325716.626237  # Updated to correct UTC timestamp
    actual = datetime_to_float(time)
    assert abs(actual - expected) < 1e-6  # Allow small numerical error


def test_well_name():
    well = Well("Test Well", is_reference=True)
    assert well.name == "Test Well"

    try:
        Well("", is_reference=True)
    except ValueError as e:
        assert str(e) == "Name cannot be an empty string."

    try:
        Well(123, is_reference=True)
    except TypeError as e:
        assert str(e) == "Name must be a string."


def test_set_kwargs():
    well = Well("Test Well", is_reference=True)

    well.set_kwargs(color="red", alpha=0.5, latitude=45.0, longitude=-120.0)
    assert well.color == "red"
    assert well.alpha == 0.5
    assert well.latitude == 45.0
    assert well.longitude == -120.0

    try:
        well.set_kwargs(invalid_attr=123)
    except AttributeError as e:
        assert str(e) == "Well has no attribute 'invalid_attr'"


def test_well_with_valid_timeseries(timeseries):
    well = Well("Test Well", is_reference=True, timeseries=timeseries)
    assert well is not None
    pd.testing.assert_series_equal(well.timeseries, timeseries)


def test_add_timeseries_invalid_input_types():
    """Test that add_timeseries raises TypeError for non-pandas Series inputs."""
    well = Well("Test Well", is_reference=True)

    try:
        well.add_timeseries("not a series")  # type: ignore
    except TypeError as e:
        assert str(e) == "Timeseries must be a pandas Series."


def test_add_timeseries_empty_series():
    """Test that add_timeseries raises ValueError for empty pandas Series."""
    well = Well("Test Well", is_reference=True)
    empty_series = pd.Series([], dtype=float)

    try:
        well.add_timeseries(empty_series)
    except ValueError as e:
        assert str(e) == "Timeseries cannot be empty."


def test_add_timeseries_non_datetime_index():
    """Test that add_timeseries raises TypeError for non-DatetimeIndex."""
    well = Well("Test Well", is_reference=True)

    # Test with integer index
    series_int_index = pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2])
    try:
        well.add_timeseries(series_int_index)
    except TypeError as e:
        assert "Timeseries index must be pandas.DatetimeIndex" in str(e)
        assert "got <class 'pandas.core.indexes.base.Index'>" in str(e)

    # Test with string index
    series_str_index = pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"])
    try:
        well.add_timeseries(series_str_index)
    except TypeError as e:
        assert "Timeseries index must be pandas.DatetimeIndex" in str(e)
        assert "got <class 'pandas.core.indexes.base.Index'>" in str(e)


def test_add_timeseries_non_float_values():
    """Test that add_timeseries raises TypeError for non-float values."""
    well = Well("Test Well", is_reference=True)
    date_index = pd.date_range("2023-01-01", periods=3, freq="D")

    # Test with integer values
    series_int_values = pd.Series([1, 2, 3], index=date_index)
    try:
        well.add_timeseries(series_int_values)
    except TypeError as e:
        assert "Timeseries values must be float dtype" in str(e)
        assert "got int64" in str(e)

    # Test with string values
    series_str_values = pd.Series(["1.0", "2.0", "3.0"], index=date_index)
    try:
        well.add_timeseries(series_str_values)
    except TypeError as e:
        assert "Timeseries values must be float dtype" in str(e)
        assert "got object" in str(e)

    # Test with boolean values
    series_bool_values = pd.Series([True, False, True], index=date_index)
    try:
        well.add_timeseries(series_bool_values)
    except TypeError as e:
        assert "Timeseries values must be float dtype" in str(e)
        assert "got bool" in str(e)


def test_add_timeseries_valid_data():
    """Test that add_timeseries accepts valid pandas Series with DatetimeIndex."""
    well = Well("Test Well", is_reference=True)

    # Create valid timeseries
    date_index = pd.date_range("2023-01-01", periods=5, freq="D")
    valid_series = pd.Series([1.0, 2.5, 3.7, 4.2, 5.9], index=date_index)

    # This should not raise any exception
    well.add_timeseries(valid_series)

    # Verify the timeseries was added correctly
    assert well.timeseries is not None
    pd.testing.assert_series_equal(well.timeseries, valid_series)
