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

    def is_clicked(self, pos) -> bool:
        x = pos[0]
        y = pos[1]
        n = len(self.border)
        inside = False

        p1x, p1y = self.border[0]
        for i in range(n + 1):
            p2x, p2y = self.border[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_inters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= x_inters:
                                inside = not inside
            p1x, p1y = p2x, p2y

        return inside



