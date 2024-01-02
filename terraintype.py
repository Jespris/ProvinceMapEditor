from enum import Enum


class TerrainType(Enum):
    OCEAN = 0
    SEA = 1
    FLAT = 2
    HILLS = 3
    MOUNTAIN = 4

    @classmethod
    def get_terrain(cls, terrain):
        if terrain == "ocean":
            return cls.OCEAN
        if terrain == "sea":
            return cls.SEA
        if terrain == "flat":
            return cls.FLAT
        if terrain == "hills":
            return cls.HILLS
        if terrain == "mountain":
            return cls.MOUNTAIN
