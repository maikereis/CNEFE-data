from dataclasses import dataclass
from enum import Enum


class GeocodingLevel(Enum):
    ORIGINAL = 1
    MODIFIED = 2
    ESTIMATED = 3
    FACE = 4
    LOCALITY = 5
    SECTOR = 6


class AddressSpecies(Enum):
    RESIDENTIAL = 1
    COLLECTIVE_DWELLING = 2
    AGRICULTURAL = 3
    EDUCATIONAL = 4
    HEALTHCARE = 5
    OTHER_ESTABLISHMENT = 6
    UNDER_CONSTRUCTION = 7
    RELIGIOUS = 8


@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float
    precision: GeocodingLevel

    def __post_init__(self):
        if not isinstance(self.latitude, float):
            raise ValueError("latitude should be of type float")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("latitude should be between -90 and 90")

        if not isinstance(self.longitude, float):
            raise ValueError("longitude should be of type float")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("longitude should be between -180 and 180")


@dataclass(frozen=True)
class PostalCode:
    code: str  # Fomat: XXXXX-XXX

    def __post_init__(self):
        if not isinstance(self.code, str):
            raise ValueError("Postal code should be of type str")
        if len(self.code) != 9 or self.code[5] != "-":
            raise ValueError("Postal code should be in the format XXXXX-XXX")
        prefix, suffix = self.code.split("-")
        if not (prefix.isdigit() and suffix.isdigit()):
            raise ValueError(
                "Postal code should contain only digits in the format XXXXX-XXX"
            )


@dataclass(frozen=True)
class TerritorialCode:
    uf: str
    municipality: str
    district: str
    subdistrict: str

    def __post_init__(self):
        if not all(
            isinstance(code, str)
            for code in [self.uf, self.municipality, self.district, self.subdistrict]
        ):
            raise ValueError("All territorial codes should be of type str")
        if len(self.uf) != 2 or not self.uf.isalpha:
            raise ValueError("UF code should be 2 alphabetic characters")


@dataclass(frozen=True)
class StreetAddress:
    street: str
    street_type: str
    number: str
    complement: str
    neighborhood: str
    postal_code: PostalCode
    territorial_code: TerritorialCode
