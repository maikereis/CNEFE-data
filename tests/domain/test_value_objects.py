from dataclasses import FrozenInstanceError

import pytest

from addresses.domain.value_objects import (
    AddressSpecies,
    Coordinate,
    GeocodingLevel,
    PostalCode,
)


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


def test_address_species_values():
    assert AddressSpecies.RESIDENTIAL.value == 1
    assert AddressSpecies.COLLECTIVE_DWELLING.value == 2
    assert AddressSpecies.AGRICULTURAL.value == 3
    assert AddressSpecies.EDUCATIONAL.value == 4
    assert AddressSpecies.HEALTHCARE.value == 5
    assert AddressSpecies.OTHER_ESTABLISHMENT.value == 6
    assert AddressSpecies.UNDER_CONSTRUCTION.value == 7
    assert AddressSpecies.RELIGIOUS.value == 8


def test_address_species_names():
    assert AddressSpecies.RESIDENTIAL.name == "RESIDENTIAL"
    assert AddressSpecies.COLLECTIVE_DWELLING.name == "COLLECTIVE_DWELLING"
    assert AddressSpecies.AGRICULTURAL.name == "AGRICULTURAL"
    assert AddressSpecies.EDUCATIONAL.name == "EDUCATIONAL"
    assert AddressSpecies.HEALTHCARE.name == "HEALTHCARE"
    assert AddressSpecies.OTHER_ESTABLISHMENT.name == "OTHER_ESTABLISHMENT"
    assert AddressSpecies.UNDER_CONSTRUCTION.name == "UNDER_CONSTRUCTION"
    assert AddressSpecies.RELIGIOUS.name == "RELIGIOUS"


def test_invalid_address_species_enum_lookup_by_value():
    with pytest.raises(ValueError):
        AddressSpecies(99)


def test_invalid_address_species_enum_access_by_name():
    with pytest.raises(AttributeError):
        _ = AddressSpecies.NON_EXISTENT


def test_coordinate_valid():
    coord = Coordinate(latitude=45.0, longitude=90.0, precision=1)
    assert coord.latitude == 45.0
    assert coord.longitude == 90.0


def test_coordinate_invalid():
    with pytest.raises(ValueError):
        Coordinate(latitude=100.0, longitude=90.0, precision=None)
    with pytest.raises(ValueError):
        Coordinate(latitude=45.0, longitude=200.0, precision=None)
    with pytest.raises(ValueError):
        Coordinate(latitude="not_a_float", longitude=90.0, precision=None)
    with pytest.raises(ValueError):
        Coordinate(latitude=45.0, longitude="not_a_float", precision=None)


def test_coordinate_invalid_latitude():
    with pytest.raises(ValueError, match="latitude should be between -90 and 90"):
        Coordinate(latitude=95.0, longitude=45.0, precision=None)
    with pytest.raises(ValueError, match="latitude should be of type float"):
        Coordinate(latitude="invalid", longitude=45.0, precision=None)


def test_coordinate_invalid_longitude():
    with pytest.raises(ValueError, match="longitude should be between -180 and 180"):
        Coordinate(latitude=45.0, longitude=195.0, precision=None)
    with pytest.raises(ValueError, match="longitude should be of type float"):
        Coordinate(latitude=45.0, longitude="invalid", precision=None)


def test_coordinate_immutable():
    coord = Coordinate(0.0, 0.0, 1)
    with pytest.raises(FrozenInstanceError):
        coord.latitude = 10


def test_postal_code_valid():
    code = PostalCode(code="1234-567")
    assert code.code == "1234-567"


def test_postal_code_invalid():
    with pytest.raises(ValueError, match="Postal code should be of type str"):
        PostalCode(code=1234567)  # Not a string
    with pytest.raises(
        ValueError, match="Postal code should be in the format XXXX-XXX"
    ):
        PostalCode(code="1234567")  # Missing hyphen
    with pytest.raises(
        ValueError, match="Postal code should be in the format XXXX-XXX"
    ):
        PostalCode(code="12345-67")  # Incorrect format
    with pytest.raises(
        ValueError,
        match="Postal code should contain only digits in the format XXXX-XXX",
    ):
        PostalCode(code="12A4-567")  # Non-digit character
    with pytest.raises(
        ValueError,
        match="Postal code should contain only digits in the format XXXX-XXX",
    ):
        PostalCode(code="1234-56B")  # Non-digit character


def test_postal_code_immutable():
    code = PostalCode(code="1234-567")
    with pytest.raises(FrozenInstanceError):
        code.code = "7654-321"
