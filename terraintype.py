from enum import Enum, auto


class TerrainType(Enum):
    OCEAN = auto()
    SEA = auto()
    FLAT = auto()
    HILLS = auto()
    MOUNTAIN = auto()

    @classmethod
    def get_terrain(cls, terrain):
        terrain_map = {
            "ocean": cls.OCEAN,
            "sea": cls.SEA,
            "flat": cls.FLAT,
            "hills": cls.HILLS,
            "mountain": cls.MOUNTAIN
        }
        return terrain_map.get(terrain.lower(), None)  # Using lower() for case-insensitivity

    def to_string(self):
        return self.name

