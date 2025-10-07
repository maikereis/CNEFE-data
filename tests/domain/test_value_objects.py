import pytest

from addresses.domain.value_objects import AddressSpecies, GeocodingLevel


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
