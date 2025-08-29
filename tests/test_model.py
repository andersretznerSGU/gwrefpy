from src.gwrefpy.model import Model
from src.gwrefpy.well import Well


def test_add_well_to_model():
    model = Model("Test Model")
    well1 = Well("Well 1", is_reference=True, model=model)
    Well("Well 2", is_reference=True, model=model)

    assert len(model.wells) == 2
    assert model.wells[0].name == "Well 1"
    assert model.wells[1].name == "Well 2"

    try:
        model.add_well("Not a well")
    except TypeError as e:
        assert str(e) == "Only Well instances can be added to the model."

    try:
        model.add_well(well1)
    except ValueError as e:
        assert str(e) == "Well 'Well 1' is already in the model."
