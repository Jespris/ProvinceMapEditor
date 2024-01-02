from terraintype import TerrainType


class Province:
    def __init__(self, province_id):
        self.id: int = province_id
        self.name: str = None
        self.border: [(int, int)] = None
        self.terrain: TerrainType = None
        self.temperature: int = None

    def set_name(self, name):
        self.name = name

    def set_border(self, border):
        self.border = border

    def set_terrain(self, terrain: TerrainType):
        self.terrain = terrain

    def set_temperature(self, temperature):
        self.temperature = temperature





