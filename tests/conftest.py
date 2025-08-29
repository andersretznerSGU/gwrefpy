from pathlib import Path

import pandas as pd
import pytest

from gwrefpy import Model, Well

THIS_DIR = Path(__file__).resolve().parent
TEST_PATH = THIS_DIR / "test_lagga2.csv"
assert TEST_PATH.exists(), f"Test file {TEST_PATH} does not exist."


@pytest.fixture()
def timeseries() -> pd.Series:
    """Fixture for loading a timeseries for testing."""
    return pd.read_csv(TEST_PATH, parse_dates=True, index_col=0).squeeze()


@pytest.fixture()
def strandangers_model() -> Model:
    """Fixture for creating Strandangers test case."""
    dates = pd.date_range("2020-01-01", periods=3, freq="D")
    values_obs = [11.4, 11.7, 11.8]
    values_ref = [8.9, 9.2, 9.4]

    obs = Well(name="obs", is_reference=False)
    obs.add_timeseries(pd.Series(values_obs, index=dates))

    ref = Well(name="ref", is_reference=True)
    ref.add_timeseries(pd.Series(values_ref, index=dates))

    model = Model(name="Strandangers")
    model.add_well(obs)
    model.add_well(ref)

    return model
