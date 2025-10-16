import pytest

from addresses.domain.aggregates import Address
from addresses.domain.value_objects import (
    AddressSpecies,
    Coordinate,
    GeocodingLevel,
    PostalCode,
    StreetAddress,
    TerritorialDivision,
)


@pytest.fixture
def valid_objects():
    return {
        "territorial_division": TerritorialDivision(
            uf="SP", municipality="São Paulo", district="Centro", subdistrict="Sé"
        ),
        "street_address": StreetAddress(
            street="Av. Paulista",
            street_type="Av",
            number=1000,
            complement="Altos",
            neighborhood="Novo",
        ),
        "postal_code": PostalCode(code="01310-100"),
        "coordinate": Coordinate(
            latitude=-23.561684, longitude=-46.625378, precision=GeocodingLevel.ORIGINAL
        ),
        "species": AddressSpecies.RESIDENTIAL,
    }


def test_address_creation(valid_objects):
    address = Address(
        id="12345",
        territorial_division=valid_objects["territorial_division"],
        street_address=valid_objects["street_address"],
        postal_code=valid_objects["postal_code"],
        coordinate=valid_objects["coordinate"],
        species=valid_objects["species"],
    )
    assert address.id == "12345"
    assert isinstance(address.territorial_division, TerritorialDivision)
    assert isinstance(address.street_address, StreetAddress)
    assert isinstance(address.postal_code, PostalCode)
    assert isinstance(address.coordinate, Coordinate)
    assert isinstance(address.species, AddressSpecies)


def test_invalid_id(valid_objects):
    with pytest.raises(ValueError, match="ID should be a non-empty string"):
        Address(
            id="",
            territorial_division=valid_objects["territorial_division"],
            street_address=valid_objects["street_address"],
            postal_code=valid_objects["postal_code"],
            coordinate=valid_objects["coordinate"],
            species=valid_objects["species"],
        )


def test_invalid_territorial_division(valid_objects):
    with pytest.raises(
        ValueError,
        match="territorial_division should be an instance of TerritorialDivision",
    ):
        Address(
            id="12345",
            territorial_division=None,
            street_address=valid_objects["street_address"],
            postal_code=valid_objects["postal_code"],
            coordinate=valid_objects["coordinate"],
            species=valid_objects["species"],
        )


def test_invalid_street_address(valid_objects):
    with pytest.raises(
        ValueError, match="street_address should be an instance of StreetAddress"
    ):
        Address(
            id="12345",
            territorial_division=valid_objects["territorial_division"],
            street_address=None,
            postal_code=valid_objects["postal_code"],
            coordinate=valid_objects["coordinate"],
            species=valid_objects["species"],
        )


def test_invalid_postal_code(valid_objects):
    with pytest.raises(
        ValueError, match="postal_code should be an instance of PostalCode"
    ):
        Address(
            id="12345",
            territorial_division=valid_objects["territorial_division"],
            street_address=valid_objects["street_address"],
            postal_code=None,
            coordinate=valid_objects["coordinate"],
            species=valid_objects["species"],
        )


def test_invalid_coordinate(valid_objects):
    with pytest.raises(
        ValueError, match="coordinate should be an instance of Coordinate"
    ):
        Address(
            id="12345",
            territorial_division=valid_objects["territorial_division"],
            street_address=valid_objects["street_address"],
            postal_code=valid_objects["postal_code"],
            coordinate=None,
            species=valid_objects["species"],
        )


def test_invalid_species(valid_objects):
    with pytest.raises(
        ValueError, match="species should be an instance of AddressSpecies"
    ):
        Address(
            id="12345",
            territorial_division=valid_objects["territorial_division"],
            street_address=valid_objects["street_address"],
            postal_code=valid_objects["postal_code"],
            coordinate=valid_objects["coordinate"],
            species=None,
        )
