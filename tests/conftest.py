import pandas as pd
from pathlib import Path
import pytest


THIS_DIR = Path(__file__).resolve().parent
TEST_PATH = THIS_DIR / "test_lagga2.csv"
assert TEST_PATH.exists(), f"Test file {TEST_PATH} does not exist."


@pytest.fixture()
def timeseries() -> pd.Series:
    """Fixture for loading a timeseries for testing."""
    return pd.read_csv(TEST_PATH, parse_dates=True, index_col=0).squeeze()
