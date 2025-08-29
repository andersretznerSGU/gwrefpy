import pytest
import pandas as pd
from gwrefpy.methods.timeseries import adjust_timeseries


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
    )
    ref = pd.Series(
        index=[
            pd.Timestamp("2023-01-08"),
            pd.Timestamp("2023-02-03"),
            pd.Timestamp("2023-02-08"),
            pd.Timestamp("2023-02-25"),
            pd.Timestamp("2023-05-28"),
        ],
        data=[8.9, 9.2, 9.3, 9.3, 9.5],
    )
    return obs, ref


def test_strandangers_example(strandangers_example) -> None:
    obs, ref = strandangers_example

    ref_adj, obs_adj, n = adjust_timeseries(ref, obs, time_equivalent="7D")
    assert n == 3
