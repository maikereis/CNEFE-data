import pytest

from addresses.domain.value_objects import GeocodingLevel


def test_geocoding_level_values():
    assert GeocodingLevel.ORIGINAL.value == 1
    assert GeocodingLevel.MODIFIED.value == 2
    assert GeocodingLevel.ESTIMATED.value == 3
    assert GeocodingLevel.FACE.value == 4
    assert GeocodingLevel.LOCALITY.value == 5
    assert GeocodingLevel.SECTOR.value == 6


def test_geocoding_level_names():
    assert GeocodingLevel.ORIGINAL.name == "ORIGINAL"
    assert GeocodingLevel.MODIFIED.name == "MODIFIED"
    assert GeocodingLevel.ESTIMATED.name == "ESTIMATED"
    assert GeocodingLevel.FACE.name == "FACE"
    assert GeocodingLevel.LOCALITY.name == "LOCALITY"
    assert GeocodingLevel.SECTOR.name == "SECTOR"


def test_invalid_geocoding_enum_lookup_by_value():
    with pytest.raises(ValueError):
        GeocodingLevel(99)


def test_invalid_geocoding_enum_access_by_name():
    with pytest.raises(AttributeError):
        _ = GeocodingLevel.UNKNOWN
