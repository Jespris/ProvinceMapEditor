from enum import Enum, auto


class TerrainType(Enum):
    OCEAN = auto()
    SEA = auto()
    FLAT = auto()
    HILLS = auto()
    MOUNTAIN = auto()
    IMPASSABLE_MOUNTAIN = auto()

    @classmethod
    def get_terrain(cls, terrain):
        terrain_map = {
            "ocean": cls.OCEAN,
            "sea": cls.SEA,
            "flat": cls.FLAT,
            "hills": cls.HILLS,
            "mountain": cls.MOUNTAIN,
            "impassable_mountain": cls.IMPASSABLE_MOUNTAIN
        }
        return terrain_map.get(terrain.lower(), None)  # Using lower() for case-insensitivity

    def to_string(self):
        return self.name

    def get_movement_speed(self):
        if self == self.SEA:
            return 2.0
        elif self == self.OCEAN:
            return 1.8
        elif self == self.FLAT:
            return 1.0
        elif self == self.HILLS:
            return 0.7
        elif self == self.MOUNTAIN:
            return 0.3
        elif self == self.IMPASSABLE_MOUNTAIN:
            return -1.0

    def is_water(self):
        if self == self.SEA or self == self.OCEAN:
            return True
        return False


