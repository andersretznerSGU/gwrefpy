from src.gwrefpy.model import Model
from src.gwrefpy.well import WellBase


def test_add_well_to_model():
    model = Model("Test Model", "1.0")
    well1 = WellBase("Well 1", model=model)
    WellBase("Well 2", model=model)

    assert len(model.wells) == 2
    assert model.wells[0].name == "Well 1"
    assert model.wells[1].name == "Well 2"

    try:
        model.add_well("Not a well")
    except TypeError as e:
        assert str(e) == "Only WellBase instances can be added to the model."

    try:
        model.add_well(well1)
    except ValueError as e:
        assert str(e) == "Well 'Well 1' is already in the model."
