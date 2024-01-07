import random
from person import Person
from army import Army


class Nation:
    def __init__(self, name: str, capital: int):
        self.name: str = name
        self.capital: int = capital  # province id
        self.provinces: [int] = [self.capital]  # list of province IDs
        self.at_war_with: [] = []  # list of other nations
        self.alliances: [] = []  # list of other nations
        self.color = self.get_random_color()
        self.armies: [Army] = []
        self.king: Person = Person(f"King of {self.name}", random.randint(15, 60))

    def add_province(self, province_id: int):
        self.provinces.append(province_id)

    def daily_update(self):
        pass

    def monthly_update(self):
        self.king.monthly_update()
        if self.king.is_dead:
            self.king = Person(f"King of {self.name}", random.randint(0, self.king.age))

    def spawn_army(self):
        pass

    @staticmethod
    def get_random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b

    def draw_assets(self, screen):
        pass

