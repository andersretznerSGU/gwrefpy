from src.gwrefpy.model import Model
from src.gwrefpy.well import Well


def test_datetime_to_float():
    well = Well("Test Well", model=Model("Test Model"))

    import datetime

    time = datetime.datetime(2025, 8, 27, 20, 15, 16, 626237)
    assert (
        abs(well._datetime_to_float(time) - 1756318516.626237) < 1e-6
    )  # Allow small numerical error


def test_well_name():
    model = Model("Test Model")
    well = Well("Test Well", model=model)
    assert well.name == "Test Well"

    try:
        Well("", model=model)
    except ValueError as e:
        assert str(e) == "Name cannot be an empty string."

    try:
        Well(123, model=model)
    except TypeError as e:
        assert str(e) == "Name must be a string."


def test_set_kwargs():
    model = Model("Test Model")
    well = Well("Test Well", model=model)

    well.set_kwargs(color="red", alpha=0.5, latitude=45.0, longitude=-120.0)
    assert well.color == "red"
    assert well.alpha == 0.5
    assert well.latitude == 45.0
    assert well.longitude == -120.0

    try:
        well.set_kwargs(invalid_attr=123)
    except AttributeError as e:
        assert str(e) == "WellBase has no attribute 'invalid_attr'"
