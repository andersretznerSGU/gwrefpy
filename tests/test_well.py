from src.gwrefpy.model import Model
from src.gwrefpy.well import WellBase


def test_datetime_to_float():
    well = WellBase("Test Well", model=Model("Test Model", "1.0"))

    import datetime

    time = datetime.datetime(2025, 8, 27, 20, 15, 16, 626237)
    assert (
        abs(well._datetime_to_float(time) - 1756318516.626237) < 1e-6
    )  # Allow small numerical error


def test_well_name():
    model = Model("Test Model", "1.0")
    well = WellBase("Test Well", model=model)
    assert well.name == "Test Well"

    try:
        WellBase("", model=model)
    except ValueError as e:
        assert str(e) == "Name cannot be an empty string."

    try:
        WellBase(123, model=model)
    except TypeError as e:
        assert str(e) == "Name must be a string."
