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
def strandangers_example() -> tuple[pd.Series, pd.Series]:
    """Test fixture to create Strandangers example."""
    obs = pd.Series(
        index=[
            pd.Timestamp("2023-01-07"),
            pd.Timestamp("2023-02-01"),
            pd.Timestamp("2023-02-25"),
        ],
        data=[11.4, 11.7, 11.8],
        name="obs",
    )
    ref = pd.Series(
        index=[
            pd.Timestamp("2023-01-08"),
            pd.Timestamp("2023-02-03"),
            pd.Timestamp("2023-02-08"),
            pd.Timestamp("2023-02-25"),
            pd.Timestamp("2023-02-28"),
        ],
        data=[8.9, 9.2, 9.3, 9.3, 9.5],
        name="ref",
    )
    return obs, ref


@pytest.fixture()
def strandangers_model(strandangers_example) -> Model:
    """Fixture for creating Strandangers test case."""
    obs, ref = strandangers_example

    obs_well = Well("obs", is_reference=False)
    obs_well.add_timeseries(obs)

    ref_well = Well("ref", is_reference=True)
    ref_well.add_timeseries(ref)

    model = Model(name="Strandangers")
    model.add_well(obs_well)
    model.add_well(ref_well)

    return model
