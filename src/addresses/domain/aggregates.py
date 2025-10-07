from dataclasses import dataclass

from addresses.domain.value_objects import (
    AddressSpecies,
    Coordinate,
    PostalCode,
    StreetAddress,
    TerritorialDivision,
)


@dataclass
class Address:
    id: str
    territorial_division: TerritorialDivision
    street_address: StreetAddress
    postal_code: PostalCode
    coordinate: Coordinate
    species: AddressSpecies

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id:
            raise ValueError("ID should be a non-empty string")
        if not isinstance(self.territorial_division, TerritorialDivision):
            raise ValueError(
                "territorial_division should be an instance of TerritorialDivision"
            )
        if not isinstance(self.street_address, StreetAddress):
            raise ValueError("street_address should be an instance of StreetAddress")
        if not isinstance(self.postal_code, PostalCode):
            raise ValueError("postal_code should be an instance of PostalCode")
        if not isinstance(self.coordinate, Coordinate):
            raise ValueError("coordinate should be an instance of Coordinate")
        if not isinstance(self.species, AddressSpecies):
            raise ValueError("species should be an instance of AddressSpecies")
