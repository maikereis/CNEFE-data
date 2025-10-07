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
