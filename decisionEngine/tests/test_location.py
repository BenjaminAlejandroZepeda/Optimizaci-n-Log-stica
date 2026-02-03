from decisionengine.models.location import Location


def test_location_creation():
    loc = Location(-33.44, -70.65)
    assert loc.latitude == -33.44
    assert loc.longitude == -70.65

def test_location_value_object_equality():
    a = Location(-33.44, -70.65)
    b = Location(-33.44, -70.65)
    assert a == b