from enum import Enum


class GeocodingLevel(Enum):
    ORIGINAL = 1
    MODIFIED = 2
    ESTIMATED = 3
    FACE = 4
    LOCALITY = 5
    SECTOR = 6
